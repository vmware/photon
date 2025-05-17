#!/bin/bash

set -o pipefail

trap '' SIGINT SIGQUIT
PROG="$(basename $0)"
CMDLINE="$0 $@ # PID: $$"

PHOTON_UPGRADE_UTILS_DIR="/usr/lib/photon-upgrade"

TIMESTAMP=$(date +%Y-%m-%d-%H-%M-%S)
LOG_FN="/var/log/${PROG}-${TIMESTAMP}.log"

# sourcing these files should not have any errors
set -e
source ${PHOTON_UPGRADE_UTILS_DIR}/utils.sh
source ${PHOTON_UPGRADE_UTILS_DIR}/common.sh
set +e

FROM_VERSION="$(/usr/bin/lsb_release -s -r)"
TO_VERSION=''       # non-blank value indicates an os-upgrade, otherwise, update
ASSUME_YES_OPT=''   # value '-y' denotes non-interactive invocation
REPOS_OPT=''        # --disablerepo=* --enablerepo=repo, repo is given in --repos
UPDATE_PKGS=y       # If 'y', update packages. Appliances may not provide repos
                    # to update packages in currently installed OS and may need
                    # this skipping capability for appliances
RM_PKGS_PRE=''      # Comma separated list of packages to remove before upgrade
RM_PKGS_POST=''     # Comma separated list of packages to remove afer upgrade
INSTALL_ALL=''      # non-empty value signifies that all packages from provided
                    # repos mentioned in --repos option needs to be installed
UPGRADE_OS='n'      # y denotes OS upgrade operation, otherwise package update
PRECHECK_ONLY='n'   # When set to y, indicates that pre upgrade checks to
                    # find anomalies need to be be performed. Those anomalies
                    # will impact the upgrade. Exits after performing checks.

# Temp location for 'rpm -qa' & rpm db copy
TMP_BACKUP_LOC=''

# List of enabled services
declare -a enabled_services_arr=()

# List of disabled serfices
declare -a disabled_services_arr=()

# Tracks installed deprecated pkgs
declare -a deprecated_pkgs_to_remove_arr=()

# extra packages which got removed while removing deprecated and replaed pkgs
declare -a extra_erased_pkgs_arr=()

KERNEL_COREDUMP_PATTERN_ORIGINAL="$(get_kernel_coredump_pattern)"

function show_help() {
  local rc=0

  if [ -n "$1" ]; then
    rc=$1
  fi

  builtin echo -n "
Usage: $PROG [--repos=r1,...] [--upgrade-os] [--to-ver=5.0] [--assume-yes] [--skip-update] [--install-all] [--rm-pkgs-pre=p1,p2,...] [--rm-pkgs-post=p1,p2,...]
This script upgrades or updates Photon OS based upon the options provided.
--help         : Shows this help text
--repos        : Script will use only the specified repos which must exist
                 e.g. --repos=appliance,appliance-photon
--upgrade-os   : When option is given, Photon OS is upgraded to next release,
                 else, all packages are updated to latest available versions
--to-ver       : The Photon OS version to upgrade to, default value of this
                 option is 5.0 when not provided.
--assume-yes   : Runs the script non-interactively and assumes yes for responses
--skip-update  : Skip updating tdnf and installed packages in existing system
                 before proceeding with upgrading the Photon OS (for appliances)
--install-all  : Install all packages from provided repos from --repos option,
                 --repos must be specified for --install-all. This option works
                 from Photon OS 4.0 and later)
--rm-pkgs-pre  : Comma separated list of packages to remove before upgrade
--rm-pkgs-post : Comma separated list of packages to remove afer upgrade
--precheck-only: Performs checks for anomalies that will impact the OS upgrade
                 and warns the user about found anomalies and exits
"
  exit $rc
}

# Remember what services are enabled or disabled before upgrade
function record_enabled_disabled_services() {
  echo "Determining enabled systemd units to be enabled post upgrade of OS..."
  enabled_services_arr+=( $(get_services_by_state enabled) )
  echo "Enabled systemd utils are: ( ${enabled_services_arr[@]} )"

  echo "Determining disabled systemd units to be disabled post upgrade of OS..."
  disabled_services_arr+=( $(get_services_by_state disabled) )
  echo "Disabled systemd utils are: ( ${disabled_services_arr[@]} )"
}

# Reset states of services where they were before upgrade
function reset_enabled_disabled_services() {
  local s=''

  echo "Resetting systemd units' enabled/disabled configuration."
  # The disabled services are reset first and then enabled services
  for s in ${disabled_services_arr[@]}; do
    echo "Disabling systemd unit $s."
    ${SYSTEMCTL} disable ${s}
  done

  for s in ${enabled_services_arr[@]}; do
    echo "Enabling systemd unit $s."
    ${SYSTEMCTL} enable ${s}
  done
}

# Remove all debuginfo packages as they may hamper during upgrade
function remove_debuginfo_packages() {
  local installed_debuginfo_pkgs="$(${RPM} -qa | grep -- '-debuginfo$')"
  local rc=0
  [ -z "$installed_debuginfo_pkgs" ] && return 0
  echo "Following debuginfo packages will be removed - $installed_debuginfo_pkgs"
  erase_pkgs $installed_debuginfo_pkgs
  rc=$?
  if [ ${rc} -ne 0 ]; then
    abort $ERETRY_EAGAIN "Error removing debuginfo packages"
  fi
  echo "All debuginfo packages were successfully removed."
}

# Usage: is_precheck_running
# Checks if we are just running the prechecks
function is_precheck_running() {
  [ $PRECHECK_ONLY = 'y' ]
  return $?
}

# Usage: is_package_removed_before_upgrade pkg
# Checks if the package is marked for removal before upgrade when pkg is
# specified in --rm-pkgs-pre
# Returns: 0, when package is removed before upgrade, otherwise, 1
function is_package_removed_before_upgrade() {
  local p

  for p in $(builtin echo "$RM_PKGS_PRE" | ${TR} , ' ') ${residual_pkgs_arr[@]}; do
    if [ "$p" = "$1" ]; then
      return 0
    fi
  done
  return 1
}

# Usage: check_installed_packages_in_target_repo p1 p2 p3
# Finds out if the packages stated in arguments are available in the target
# repo used for upgrade
function check_installed_packages_in_target_repo() {
  local -a rpms_arr=(
    $(
        $PRINTF "%s\n" \
          $(
            ${RPM} -q --queryformat "%{NAME}\n" \
            $(
              ${RPM} -qa | ${GREP} "\\.$PH4RPMTAG\\."
            )
        ) ${deprecated_pkgs_to_remove_arr[@]} ${!replaced_pkgs_map[@]} | \
        $SORT | $UNIQ -u
    )
  )
  local -a missings_arr=()
  local i
  local n

  echo "Finding packages in the target repo. This may take a while ..."
  missings_arr+=($(check_packages_in_target_repo ${rpms_arr[@]}))
  n=${#missings_arr[@]}
  for ((i=0; i<$n; i++)); do
    is_package_removed_before_upgrade "${missings_arr[$i]}" && \
      unset missings_arr[$i]
  done
  if [ ${#missings_arr[@]} -gt 0 ]; then
    abort $ERETRY_EINVAL "Error: Packages - ${missings_arr[@]} - are not" \
          "available in the target repo for OS upgrade. Please provide" \
          "the correct repo having the required packages."
  else
    echo "All installed packages are validated in the target repo."
    return 0
  fi
}

# Usage: check_packages_in_target_repo p1 p2 p3 ...
# Checks that provided packages as arguments are all available in $TO_VERSION
# repo and returns 0 when it finds all, returns count of packages which it
# could not find (error) and also prints the names of packages that it could
# not find in the target repo
function check_packages_in_target_repo() {
  local -a missing_pkgs_arr=()
  local ptgt=''
  local -A providing_pkgs_map=(
    [coreutils]="coreutils-selinux coreutils"
  )

  local list_available_fn="${TMP_BACKUP_LOC}/list_available.txt"

  if ! test -s "${list_available_fn}"; then
    ${TDNF} $REPOS_OPT "--releasever=$TO_VERSION" list available | \
      $AWK '{print $1}' | ${UNIQ} | ${SORT} > "${list_available_fn}"
    if [ $? -ne 0 ]; then
      ${RM} -f "${list_available_fn}"
      abort 1 "ERROR($FUNCNAME): tdnf list available failed ..."
    fi
    ${SED} -i -e "s/^\(.*\).$(uname -m).*$/\1/" "${list_available_fn}"
    ${SED} -i -e "s/^\(.*\).noarch.*$/\1/" "${list_available_fn}"
  fi

  for ptgt in $*; do
    [ ${#ptgt} -gt 10 -a "${ptgt: -10}" = '-debuginfo' ] && continue

    $GREP -qw "^${ptgt}$" "${list_available_fn}" &> /dev/null && \
      continue

    # fallback method, some packages might be available through Provides
    ${TDNF} $REPOS_OPT "--releasever=$TO_VERSION" list available \
       ${providing_pkgs_map[$ptgt]:-$ptgt} &> /dev/null && continue

    missing_pkgs_arr+=($ptgt)
  done

  builtin echo ${missing_pkgs_arr[@]}
  return ${#missing_pkgs_arr[@]}
}

# Usage: find_installed_replaced_packages
# First determines which of the replaced or renamed packages are installed
# and then resets the replaced_pkgs_map[package_name] to the first available
# package in the statically stated list of packages
function find_installed_replaced_packages() {
  local psrc=''
  local ptgt=''
  local errstr=''
  local replacing_pkgs=''
  local i=0
  local n=0
  local found_in_target=n
  local -a missing_exp_pkgs_arr=()

  for psrc in ${!replaced_pkgs_map[@]}; do
    if ${RPM} -q --quiet $psrc; then
      found_in_target=n
      replacing_pkgs="${replaced_pkgs_map[$psrc]}"
      # set replaced_pkgs_map[$psrc] to the first package available in the
      # stated list of packages in the below for loop
      for ptgt in $replacing_pkgs; do
        if check_packages_in_target_repo $ptgt 1>/dev/null 2>/dev/null; then
          if [ "$psrc" = "$ptgt" ]; then
            # The replacing pkg $ptgt is the same as the installed pkg $psrc
            # This can happen for some packages, openjre8, for example
            # Where multiple pkgs can replace the installed pkg in target os
            # here we found the same package in the target OS, so del entry
            unset replaced_pkgs_map[$psrc]
          else
            replaced_pkgs_map[$psrc]=$ptgt
          fi
          found_in_target=y
          break
        fi
      done
      if [ "$found_in_target" = 'n' ]; then
        # The replacing packages were not found in the target repo.
        missing_exp_pkgs_arr+=($psrc)
      fi
    else
      unset replaced_pkgs_map[$psrc]
    fi
  done

  n=${#missing_exp_pkgs_arr[@]}
  for ((i=0; i<$n; i++)); do
    # Check if those packages which were not found in the target repo were
    # marked for removal before upgrade, if not, the upgrade will fail due to
    # those missing packages in the target repo
    is_package_removed_before_upgrade "${missing_exp_pkgs_arr[$i]}" && \
      unset missing_exp_pkgs_arr[$i]
  done

  if [ ${#missing_exp_pkgs_arr[@]} -gt 0 ]; then
    errstr="ERROR: Following installed packages do not have their corresponding replacing packages available in the target repo.\n"
    for p in ${missing_exp_pkgs_arr[@]}; do
      errstr="${errstr}   - $p needs any of following packages in target repo - ${replaced_pkgs_map[$p]}\n"
    done
    abort $ERETRY_EINVAL $errstr
  else
    return 0
  fi
}

# Usage: install_other_packages
# Install all the other packages - install replacement packages corresponnding
# to any of the earlier removed packagers and also install those earlier erased
# packages which got removed due removal of some other packages
function install_other_packages() {
  local rc=0

  if [ ${#replaced_pkgs_map[@]} -gt 0 -o ${#extra_erased_pkgs_arr[@]} -gt 0 ]; then
    [ ${#replaced_pkgs_map[@]} -gt 0 ] && \
      echo "Installing following packages which are replacing removed"\
           "packages -\n    - ${replaced_pkgs_map[@]}"
    [ ${#extra_erased_pkgs_arr[@]} -gt 0 ] && \
      echo "Installing following other packages which were originally"\
           "installed -\n    - ${extra_erased_pkgs_arr[@]}"
    install_pkgs ${replaced_pkgs_map[@]} ${extra_erased_pkgs_arr[@]}
    rc=$?
    if [ $rc -ne 0 ]; then
      abort $rc "Error installing replacement and earlier removed packages."
    fi
    echo "All the following packages were installed successfully -\n"\
         "    - ${replaced_pkgs_map[@]} ${extra_erased_pkgs_arr[@]}"
  fi
}

# Installed packges which were replaced by other packages or installed packages
# which were renamed get removed by this method. The replacing package gets
# installed in install_replacement_packages()
function remove_replaced_packages() {
  local rc=0

  if [ ${#replaced_pkgs_map[@]} -gt 0 ]; then
    backup_configs
    echo "Removing following packages which were replaced by other "\
             "packages -\n${!replaced_pkgs_map[@]}\n"
    erase_pkgs ${!replaced_pkgs_map[@]}
    rc=$?
    if [ $rc -ne 0 ]; then
      abort $rc "Error removing replaced packages - ${!replaced_pkgs_map[@]} - (tdnf error code: $rc)."
    fi
    echo "Removal of replaced packages '${!replaced_pkgs_map[@]}' succeeded."
  fi
}

# Usage: find_extra_erased_pkgs p1 p2 p3 ...
# Finds packages which will also be removed as side effect of removing
# the packages provided in the argument because these identified packges
# depend on one or more of the packges from the argument list
# Returns:
#   0 - success, when the erased packages are only of Photon OS (*.ph4.*rpm)
#   $ERETRY_EAGAIN - fail, when the erased package(s) include those packages
#                    which are not provided by Photon OS
function find_extra_erased_pkgs() {
  local -a expected_pkgs_arr=()
  local -a unexpected_pkgs_arr=()
  local pname=''
  local arch=''
  local version=''
  local repo=''
  local szhuman=''
  local szbytes=''
  local f="$TMP_BACKUP_LOC/find_extra_erased_pkgs.txt"
  local rc=0

  [ $# -eq 0 ] && builtin echo '' && return 0
  $STDBUF -o L $TDNF --assumeno '--disablerepo=*' erase $* > $f 2>&1
  rc=$?
  [ $rc -ne $EC_TDNF_ASSUMENO ] && echo "Unexpected return code $rc from tdnf, expected code was $EC_TDNF_ASSUMENO" && return $rc
  while read pname arch version repo szhuman szbytes; do
    if [ "$pname" = "Removing:" ]; then
      while read pname arch version repo szhuman szbytes; do
        if [ -z "$pname" ]; then
          break
        fi
        if [ "${version: -4}" != ".$PH4RPMTAG" ]; then
          unexpected_pkgs_arr+=($pname)
        elif ! is_package_removed_before_upgrade $pname; then
          expected_pkgs_arr+=($pname)
        fi
      done
      break
    fi
  done < $f
  $RM -f $f
  if [ ${#unexpected_pkgs_arr[@]} -gt 0 ]; then
    echoerr "Following packages will get removed which were not installed by Photon OS -\n"\
            "    ---- ${unexpected_pkgs_arr[@]} ----\nAbove listed non-Photon OS packages will"\
            "also get removed while removing below list of Photon OS packages during the"\
            "process of OS upgrade -\n    ---- ${expected_pkgs_arr[@]} ----"
  fi
  printf '%s\n' ${expected_pkgs_arr[@]} $* | $SORT | $UNIQ -u
  return ${#unexpected_pkgs_arr[@]}
}

#Some packages are deprecaed in 5.0, lets remove them before upgrading
function remove_unsupported_packages() {
  local rc=0

  if [ ${#deprecated_pkgs_to_remove_arr[@]} -gt 0 ]; then
    erase_pkgs ${deprecated_pkgs_to_remove_arr[@]}
    rc=$?
    if [ $rc -ne 0 ]; then
      abort $ERETRY_EAGAIN "Could not erase all unsupported packages (tdnf error code: $rc)."
    else
      echo "All unsupported packages are removed successfully."
    fi
  fi
}

# Usage1: tdnf_makecache
# Usage2; tdnf_makecache releasever
# Generates repository cache for all selected/enabled repositories
function tdnf_makecache() {
  local v="${1:-$(/usr/bin/lsb_release -s -r)}"
  echo "Generating tdnf cache on Photon OS $v"
  ${TDNF} $REPOS_OPT --releasever=$v --refresh makecache
}

function distro_upgrade() {
  local ver="$1"
  local rc=0
  local p

  if [ "$ver" = "$FROM_VERSION" ]; then
    echo "Upgrading all installed Photon OS $FROM_VERSION packages to latest" \
         "available versions."
  else
    echo "Upgrading Photon OS to $TO_VERSION from $FROM_VERSION"
  fi

  if ${TDNF} $REPOS_OPT $ASSUME_YES_OPT distro-sync --releasever=$ver --refresh; then
      echo "All packages were upgraded to latest versions successfully."
      if [ "$ver" = "$TO_VERSION" ]; then
        echo "The OS has been upgraded to $TO_VERSION."
        relocate_rpmdb
        rebuilddb
        ${TDNF} $REPOS_OPT $ASSUME_YES_OPT reinstall photon-release "--releasever=$ver" --refresh
        tdnf_makecache $TO_VERSION
        install_pkgs systemd-udev
      fi
  else
    rc=$?
    if [ "$ver" = "$FROM_VERSION" ]; then
      abort $ERETRY_EAGAIN "Error in upgrading all packages to latest versions (tdnf error code: $rc)."
    else
      abort $ERETRY_EAGAIN "Error in upgrading to Photon OS $TO_VERSION from $FROM_VERSION ((tdnf error code: $rc)."
    fi
  fi
}

# Removes any residual packages which weren't removed during distro_upgrade()
function remove_residual_pkgs() {
  local err_rm_pkg_list=''
  local rc=0
  local p=''

  for p in ${residual_pkgs_arr[@]}; do
    if $RPM -q --quiet $p; then
      erase_pkgs $p
      rc=$?
      if [ $rc -ne 0 ]; then
        err_rm_pkg_list="$err_rm_pkg_list $p"
        echo "Warning: Could not remove package '$p' post upgrade (tdnf error code: $rc)."
      fi
    fi
  done
  if [ -n "$err_rm_pkg_list" ]; then
    echo "Warning: following packages were not removed post upgrade-" \
             "$err_rm_pkg_list"
  fi
}

# If user specifies --install-all and --repos then install all packages
# from the provided repos which are not installed
function install_all_from_repo() {
  local available_pkgs_for_install="$(
      ${RPM} -q $(${TDNF} $REPOS_OPT repoquery --available) 2>&1 | \
        ${SED} -nE 's#^package ([^ ]+\.ph[0-9]+\.[^ ]+) is not installed#\1#p'
  )"
  local rc=0
  echo '--install-all option was passed.'
  if [ -n "$available_pkgs_for_install" ]; then
    echo "Installing following packages from provided repos:" \
      "$(builtin echo $available_pkgs_for_install | ${SED} -E 's/ /, /g')"
    if ${TDNF} $REPOS_OPT $ASSUME_YES_OPT install $available_pkgs_for_install
    then
       echo "Found packages were installed successfully."
    else
       rc=$?
       echoerr "Error ($rc) installing following found packages:" \
               "$available_pkgs_for_install."
    fi
  else
    echo "all packages from provided repos are already installed."
  fi
  return $rc
}

# Removes those packages named in --rm-pkgs-pre option before upgrading
function pre_upgrade_rm_pkgs() {
  local pkglist=''
  local p

  [ -z "$RM_PKGS_PRE" ] && return 0

  echo "Removing following user specified packages before upgrade - $RM_PKGS_PRE"

  for p in $(builtin echo "$RM_PKGS_PRE" | ${TR} , ' '); do
    if ${RPM} -q --quiet $p; then
      if erase_pkgs $p; then
        echo "Successfully removed user named pacakge $p."
      else
        pkglist="$pkglist $p"
      fi
    fi
  done
  if [ -n "$pkglist" ]; then
     abort $ERETRY_EAGAIN \
       "Error removing following user named packages before upgrade: $pkglist" \
       "\nPlease remove those packages and retry the photon-upgrade.sh."
  fi
}

# Removes those packages named in --rm-pkgs-post after upgrade
function post_upgrade_rm_pkgs() {
  local pkglist=''
  local p

  [ -z "$RM_PKGS_POST" ] && return 0

  echo "Removing following user specified packages after upgrade - $RM_PKGS_POST"

  for p in $(builtin echo "$RM_PKGS_POST" | ${TR} , ' '); do
    if ${RPM} -q --quiet $p; then
      if ${TDNF} $REPOS_OPT $ASSUME_YES_OPT erase $p; then
        echo "Successfully removed user named pacakge $p."
      else
        pkglist="$pkglist $p"
      fi
    fi
  done
  if [ -n "$pkglist" ]; then
     echoerr "Warning: following user specified packages could not be removed post upgrade: " \
             "$pkglist"
  fi
}

# Backup 'rpm -qa' and RPM DB before changing RPM DB in anyway, this will help
# in debugging any failures and will be used to provide actionable item to the
# end-user
function backup_rpms_list_n_db() {
  local rpm_db_loc=$1
  TMP_BACKUP_LOC="/tmp/${PROG}-${TIMESTAMP}"
  ${MKDIR} -p ${TMP_BACKUP_LOC} || exit 1
  local rpmqa_file="$TMP_BACKUP_LOC/rpm-qa.txt"

  echo "Recording list of all installed RPMs on this machine to $rpmqa_file."
  ${RPM} -qa > $rpmqa_file
  echo "Creating backup of RPM DB."
  ${CP} -a $rpm_db_loc $TMP_BACKUP_LOC
}

# This will cleanup the backup created by backup_rpms_list_n_db()
function cleanup_and_exit() {
  if [ "$1" = "0" ] && ! is_precheck_running; then
    if [ -n "$TMP_BACKUP_LOC" ] && [ -e "$TMP_BACKUP_LOC" ]; then
      rm -rf "$TMP_BACKUP_LOC"
    fi
    write_to_syslog "photon-upgrade completed successfully."
  else
    is_precheck_running || \
      write_to_syslog "photon-upgrade terminated with exit code $rc."
  fi
  exit ${1:-0}
}

#must reboot after an upgrade
function ask_for_reboot() {
  local yn=''

  echo "Reboot is recommended after an upgrade. "
  if [ -n "$ASSUME_YES_OPT" ]; then
    # This is non-interactive invocation of the script
    echo "Please reboot the system."
  else
    read -p "Reboot now(y/n)?" yn
    case $yn in
      [Yy]* ) reboot;;
      [Nn]* ) cleanup_and_exit 0;;
    esac
  fi
}

# if the current installed OS has packages deprecated in the target version,
# so there is no clean upgrade path for those packages. They get removed.
function find_installed_deprecated_packages() {
  local pkg=''
  local yn=''

  deprecated_pkgs_to_remove_arr+=(
    $(find_installed_packages ${deprecated_packages_arr[@]})
  )

  if [ ${#deprecated_pkgs_to_remove_arr[@]} -gt 0 ]; then
    echo "The following deprecated packages will be removed before upgrade -"
    $PRINTF "    %s\n" ${deprecated_pkgs_to_remove_arr[@]}
    if [ -z "$ASSUME_YES_OPT" ]; then
      # This is interactive invocation of the script
      read -p "Proceed(y/n)?" yn
      case $yn in
        [Nn]* ) cleanup_and_exit 0 ;;
      esac
    fi
  fi
}

# Update package managers
function update_solv_to_support_complex_deps() {
  local rc=0

  echo "Updating package management software and libraries."
  if ${TDNF} $REPOS_OPT -y update libsolv rpm tdnf --refresh; then
    echo "Upgrade of package management software and libraries succeeded."
    rebuilddb
  else
    rc=$?
    abort $ERETRY_EAGAIN "Could not update package management software and libraries (tdnf error code: $rc)."
  fi
}

# Updates all installed Photon OS packages to latest versions
function do_ph4_to_ph4_update() {
  # old_new_pkg_map hash captures those packages which have another version
  # available in 4.0 with a different name. For example, apache-tomcat and
  # apache-tomcat9 both are avaialble in 4.0. The update repo must provide only
  # the newer rpm to upgrade to it from installed version.
  local -A old_new_pkg_map=(
    [apache-tomcat]="apache-tomcat apache-tomcat9"
  )
  # Hash keys map paths in older version of package to those in newer versions.
  # The conf_path_map hash is only used in restore_configs() and nowhere else.
  # Each update/upgrade path may bring it's own map.
  declare -A conf_path_map=(
    # config of apache-tomcat in 4.0 to be restored for apache-tomcat9
    [/var/opt/apache-tomcat/conf]=/var/opt/apache-tomcat9/conf
  )
  # The cleanup_residual_files_map hash has command that help cleanup any
  # residual files that the uninstalled package leaves behind. This elimnates
  # any errors that are shown during updates of packages from old_new_pkg_map
  declare -A cleanup_residual_files_map=(
    [apache-tomcat]="${RM} -rf /var/opt/apache-tomcat /usr/share/java/tomcat"
  )
  local i=''    # Iterator for keys of old_new_pkg_map to detect installed pkgs
  local f=''    # Loop variable for detecting pkgs in repo corresponding to $i
  local -a removed_pkgs_list=()
  local found=no
  # set of installed packages from the keys of old_new_pkg_map hash
  local -a inst_pkgs_arr=(
    $(find_installed_packages ${!old_new_pkg_map[@]})
  )
  # set of packages which are not installed from the keys of old_new_pkg_map
  local -a notinst_pkgs_arr=(
    $(
      $PRINTF '%s\n' ${!old_new_pkg_map[@]} ${inst_pkgs_arr[@]} | $SORT | \
        $UNIQ -u
    )
  )

  trap exit_cleanup EXIT
  disable_all_coredumps || abort $ERETRY_EAGAIN "Could not disable coredumps."
  write_to_syslog "Starting update of packages with command line: $CMDLINE"
  backup_rpms_list_n_db $OLD_RPMDB_PATH
  remove_debuginfo_packages
  pre_upgrade_rm_pkgs
  tdnf_makecache
  rebuilddb

  # cleanup old_new_pkg_map hash and cleanup_residual_files_map hash for those
  # packages which are not installed
  for i in ${notinst_pkgs_arr[@]}; do
    unset old_new_pkg_map[$i]
    unset cleanup_residual_files_map[$i]
  done

  for i in ${inst_pkgs_arr[@]}; do
    found=no
    for f in ${old_new_pkg_map[$i]}; do
      if ${TDNF} $REPOS_OPT list available $f > /dev/null 2>&1; then
        found=yes
        if [ "$f" = "$i" ]; then
          # Found the same package name in the repo as the one installed.
          # Only that found package will be used  for update.
          unset old_new_pkg_map[$i]
          unset cleanup_residual_files_map[$i]
        else
          # The installed package is not found but the other replacing package
          # is found in the repo. The old package and it's dependent packagtes
          # will be removed before updating all packages to newer version and
          # the other replacing package and all removed packages will be
          # reinstalled post update and their configurations will be restored.
          old_new_pkg_map[$i]=$f
        fi
        break
      fi
    done
    if [ "$found" = "no" ]; then
      unset old_new_pkg_map[$i]
      unset cleanup_residual_files_map[$i]
    fi
  done

  if [ ${#old_new_pkg_map[@]} -gt 0 ]; then
    for i in ${!old_new_pkg_map[@]}; do
      echo "Note: The installed $i will be upgraded to ${old_new_pkg_map[$i]}"
    done
  fi

  # At this point old_new_pkg_map keys are the packages which are installed and
  # will be replaced by those packages which are named in corresponding values
  removed_pkgs_list+=( $(find_extra_erased_pkgs ${!old_new_pkg_map[@]}) )
  backup_configs $TMP_BACKUP_LOC ${removed_pkgs_list[@]} ${!old_new_pkg_map[@]}
  erase_pkgs ${!old_new_pkg_map[@]}
  if [ ${#cleanup_residual_files_map[@]} -gt 0 ]; then
    for i in ${!cleanup_residual_files_map[@]}; do
      echo "Executing '${cleanup_residual_files_map[$i]}' for cleanup."
      eval "${cleanup_residual_files_map[$i]}"
    done
  fi
  # Upgrading all installed RPMs to lastest available versions in the repo.
  distro_upgrade $FROM_VERSION
  rebuilddb
  install_pkgs ${removed_pkgs_list[@]} ${old_new_pkg_map[@]}
  if [ -n "$INSTALL_ALL" ]; then
    install_all_from_repo
  fi
  post_upgrade_rm_pkgs
  restore_configs $TMP_BACKUP_LOC
}


# Checks whether tdnf repo configurations are as expected or not.  The method
# aborts photon-upgrade if it finds photon-release package from other
# OS releases than the one being updated or upgraded to.
function is_repo_config_valid_for_release() {
  local r=$1   # release number 3.0, 4.0 etc.
  local -A tag_to_rel_map=(
    [$PH3RPMTAG]=3.0
    [$PH4RPMTAG]=4.0
    [$PH5RPMTAG]=5.0
  )
  local t
  local phrel_pkgs_tags="$(
           ${TDNF} $REPOS_OPT --releasever=$r --refresh list available photon-release | \
           ${SED} -nE 's/^\S+\s+[^\-]+-[0-9]+\.(\S+)\s+.*$/\1/p' | ${SORT} | ${UNIQ}
        )"
  if [ -z "$phrel_pkgs_tags" ]; then
    abort $ERETRY_EINVAL "No photon-release package from $r release was found." \
                         "Is photon-upgrade invoked properly? " \
                         "Please recheck the tdnf repo configurations and rerun."
    return $ERETRY_EINVAL
  fi
  for t in $phrel_pkgs_tags; do
    if [ "$r" != "${tag_to_rel_map[$t]}" ]; then
      abort $ERETRY_EINVAL "Found unexpected photon-release package from ${tag_to_rel_map[$t]} release." \
                           "Is photon-upgrade invoked properly? " \
                           "Please recheck the tdnf repo configurations and rerun."
      return $ERETRY_EINVAL
    fi
  done
  return 0
}

function verify_version_and_upgrade() {
  local yn=''
  local rc=0

  if [ $FROM_VERSION = $TO_VERSION ]; then
    echo "Your current version $FROM_VERSION is the latest version. Nothing to do."
    exit 0
  fi
  if [ -z "$ASSUME_YES_OPT" ]; then
    # This is interactive invocation of the script
    echo "You are about to upgrade PhotonOS from $FROM_VERSION to $TO_VERSION."
    echo "Please backup your data before proceeding."
    echo "Continue (y/n)?"
    read yn
  elif ! is_precheck_running; then
    # -y or --assume-yes was given on command line; non-interactive invocation
    echo "Upgrading Photon OS from $FROM_VERSION to $TO_VERSION." \
         "Assuming that data backup has already been done."
    yn=y    # script is run non-interactively to do upgrade
  else
    yn=y
  fi

  echo ''
  case "$yn" in
    [Yy]*)
      is_precheck_running || \
        write_to_syslog "Starting OS upgrade with command line: $CMDLINE"
      is_repo_config_valid_for_release $TO_VERSION
      rc=$?
      find_incorrect_units
      ((rc+=$?))
      is_precheck_running || backup_rpms_list_n_db $OLD_RPMDB_PATH
      find_files_for_review
      tdnf_makecache $FROM_VERSION
      if [ "$UPDATE_PKGS" = 'y' ] && ! is_precheck_running; then
        # Vanilla Photon OS would want to update package manager and other
        # packages. Appliances control builds so do not need this.
        update_solv_to_support_complex_deps
        prepare_for_upgrade
        distro_upgrade $FROM_VERSION
      fi
      find_installed_deprecated_packages
      tdnf_makecache $TO_VERSION
      find_installed_replaced_packages
      check_installed_packages_in_target_repo
      ((rc+=$?))
      tdnf_makecache $FROM_VERSION
      extra_erased_pkgs_arr+=(
        $(
          find_extra_erased_pkgs ${deprecated_pkgs_to_remove_arr[@]} \
                                 ${!replaced_pkgs_map[@]}
        )
      )
      if is_precheck_running; then
        if [ $rc -eq 0 ]; then
          echo "Prechecks: PASS, exiting with status($rc)."
        else
          echoerr "Prechecks: FAIL, exiting with status($rc)."
        fi
        exit $rc
      fi
      trap exit_cleanup EXIT
      disable_all_coredumps || abort $ERETRY_EAGAIN "Could not disable coredumps."
      remove_debuginfo_packages
      backup_configs $TMP_BACKUP_LOC \
                     ${!replaced_pkgs_map[@]} \
                     ${extra_erased_pkgs_arr[@]}
      record_enabled_disabled_services
      remove_unsupported_packages
      pre_upgrade_rm_pkgs
      rebuilddb
      remove_replaced_packages
      distro_upgrade $TO_VERSION
      install_other_packages
      rebuilddb
      fix_post_upgrade_config
      remove_residual_pkgs
      if [ -n "$INSTALL_ALL" ]; then
        install_all_from_repo
      fi
      restore_configs $TMP_BACKUP_LOC
      reset_enabled_disabled_services
      post_upgrade_rm_pkgs
      rebuilddb
      ask_for_reboot
      ;;
    *) cleanup_and_exit 0;;
  esac
}

CMD_ARGS=$(
  getopt --long \
  'assume-yes,help,install-all,precheck-only,repos:,rm-pkgs-pre:,rm-pkgs-post:,to-ver:,skip-update,upgrade-os' \
  -- -- "$@"
)
if [ $? -ne 0 ]; then
  show_help $ERETRY_EINVAL
fi
eval set -- $CMD_ARGS
while [ $# -gt 0 ]; do
  case "$1" in
    --assume-yes )
      ASSUME_YES_OPT='-y'
      ;;
    --help )
      show_help 0
      ;;
    --install-all)
      INSTALL_ALL='y' # install all packages from provided repos by --repos
      ;;
    --precheck-only )
      PRECHECK_ONLY='y'
      ASSUME_YES_OPT='-y'
      # Below 2 values are set just to let prechecks run with minimum set of args
      TO_VERSION=${TO_VERSION:-5.0}
      UPGRADE_OS='y'
      ;;
    --repos )
      repos_csv="$2"
      if [ -n "$REPOS_OPT" ]; then
        echoerr "--repos was specified more than once"
        show_help $ERETRY_EINVAL
      fi
      for r in $(builtin echo "$repos_csv" | ${TR} , ' '); do
        REPOS_OPT="$REPOS_OPT --enablerepo=$r"
      done
      if [ -n "$repos_csv" ]; then
        REPOS_OPT="--disablerepo=* $REPOS_OPT"
      fi
      shift
      ;;
    --rm-pkgs-pre )
      [ -n "$RM_PKGS_PRE" ] && \
        echoerr "--rm-pkgs-pre was specified more than once" && \
          show_help $ERETRY_EINVAL
      RM_PKGS_PRE="$2"
      shift
      ;;
    --rm-pkgs-post )
      [ -n "$RM_PKGS_POST" ] && \
        echoerr "--rm-pkgs-post was specified more than once" && \
          show_help $ERETRY_EINVAL
      RM_PKGS_POST="$2"
      shift
      ;;
    --skip-update )
      UPDATE_PKGS='n'  # Any value other than 'y' would not update packages
      ;;
    --to-ver )
      TO_VERSION="$2"
      shift
      ;;
    --upgrade-os )
      TO_VERSION=${TO_VERSION:-5.0}
      UPGRADE_OS='y'
      ;;
    -- )
      break
      ;;
  esac
  shift
done

if [ "$UPGRADE_OS" = "n" ]; then
  if [ -n "$TO_VERSION" ]; then
    echoerr "--to-ver was specified without specifying --upgrade-os"
    show_help $ERETRY_EINVAL
  fi
elif [ -z "$TO_VERSION" ]; then
  TO_VERSION=5.0
fi

case "$TO_VERSION" in
  '' )
    ;;
  5.0 )
    source "${PHOTON_UPGRADE_UTILS_DIR}/ph4-to-ph5-upgrade.sh" "${PHOTON_UPGRADE_UTILS_DIR}"
    ;;
  * )
    echoerr "Valid values for --to-ver can only be 5.0"
    show_help $ERETRY_EINVAL
    ;;
esac

# If repos are provided with --repos or --repos= option, only those repos will
# be used during both, upgrading OS or updatig installed RPMs to latest version

if [ -n "$INSTALL_ALL" -a -z "$REPOS_OPT" ]; then
  # --install-all is given but --repos was not specified - invalid invocation
  show_help $ERETRY_EINVAL
fi

if [ "$UPGRADE_OS" = "y" ]; then
  # The script is run with --upgrade-os option, upgrading Photon OS
  is_precheck_running && echo "Prechecks for OS upgrade will be performed."
  verify_version_and_upgrade
elif [ "$UPDATE_PKGS" = 'y' ]; then
  # The script is run without --upgrade-os option.
  # Upgrading all installed RPMs to latest versions.
  do_ph4_to_ph4_update
fi
cleanup_and_exit 0
