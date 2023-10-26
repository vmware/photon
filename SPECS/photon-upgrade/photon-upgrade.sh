#!/bin/bash

PROG="$(basename $0)"

PHOTON_UPGRADE_UTILS_DIR="/usr/lib/photon-upgrade"

source ${PHOTON_UPGRADE_UTILS_DIR}/utils.sh
source ${PHOTON_UPGRADE_UTILS_DIR}/common.sh

FROM_VERSION="$(/usr/bin/lsb_release -s -r)"
TO_VERSION=''       # non-blank value indicates an os-upgrade, otherwise, update
ASSUME_YES_OPT=''   # value '-y' denotes non-interactive invocation
REPOS_OPT=''        # --disablerepo=* --enablerepo=repo, repo is given in --repo
UPDATE_PKGS=y       # If 'y', update packages. Appliances may not provide repos
                    # to update packages in currently installed OS and may need
                    # this skipping capability for appliances
RM_PKGS_PRE=''      # Comma separated list of packages to remove before upgrade
RM_PKGS_POST=''     # Comma separated list of packages to remove afer upgrade
INSTALL_ALL=''      # non-empty value signifies that all packages from provided
                    # repos mentioned in --repos option needs to be installed
UPGRADE_OS='n'      # y denotes OS upgrade operation, otherwise package update

declare -a enabled_services_arr=()     # list of enabled services
declare -a disabled_services_arr=()    # list of disabled serfices
declare -a depreated_pkgs_to_remove_arr=()  # tracks installed deprecated pkgs
declare -A installed_pkgs_map=()       # installed and replacement pkgs map

TMP_BACKUP_LOC=''                   # temp location for 'rpm -qa' & rpm db copy

function show_help() {
  local rc=0

  if [ -n "$1" ]; then
    rc=$1
  fi

  builtin echo -n "
Usage: $PROG [--repos=r1,...] [--upgrade-os] [--to-ver={4.0|5.0}] [--assume-yes] [--skip-update] [--install-all] [--rm-pkgs-pre=p1,p2,...] [--rm-pkgs-post=p1,p2,...]

This script upgrades or updates Photon OS based upon the options provided.

--help         : Shows this help text
--repos        : Script will use only the specified repos which must exist
                 e.g. --repos=appliance,appliance-photon
--upgrade-os   : When option is given, Photon OS is upgraded to next release,
                 else, all packages are updated to latest available versions
--to-ver       : The Photon OS version to upgrade to, can be 4.0 or 5.0, where
                 default value of --to-ver is 4.0
--assume-yes   : Runs the script non-interactively and assumes yes for responses
--skip-update  : Skip updating tdnf & packages before upgrading (for appliances)
--install-all  : Install all packages from provided repos from --repos option,
                 --repos must be specified for --install-all. This option works
                 from Photon OS 4.0 and later)
--rm-pkgs-pre  : Comma separated list of packages to remove before upgrade
--rm-pkgs-post : Comma separated list of packages to remove afer upgrade
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
  local installed_debuginfo_pkgs="$(${RPM} -qa | ${GREP} -- -debuginfo-)"
  local rc=0
  [ -z "$installed_debuginfo_pkgs" ] && return 0
  echo "Following debuginfo packages will be removed - $installed_debuginfo_pkgs"

  ${TDNF} -q --disablerepo=* $ASSUME_YES_OPT erase $installed_debuginfo_pkgs
  rc=$?
  if [ $rc -ne 0 ]; then
    abort $ERETRY_EAGAIN "Error removing debuginfo packages (tdnf error: $rc)"
  fi
  echo "All debuginfo packages were successfully removed."
}

# The replacing packages correspoinding to any of the installed packages will
# be installed with the call to this method
function install_replacement_packages() {
  local rc=0

  if [ ${#installed_pkgs_map[@]} -gt 0 ]; then
    echo "Installing following packages which are replacing removed" \
             "packages -\n${installed_pkgs_map[@]}"
    ${TDNF} $REPOS_OPT -y install ${installed_pkgs_map[@]}
    rc=$?
    if [ $rc -ne 0 ]; then
      abort $rc "Error installing replacement packages '${installed_pkgs_map[@]}'."
    fi
    echo "Replacement packages '${installed_pkgs_map[@]}' are successfully installed"
    restore_configs $TMP_BACKUP_LOC ${installed_pkgs_map[@]} apache-tomcat9
  fi
}

# Installed packges which were replaced by other packages or installed packages
# which were renamed will be removed by this method. The replacing package gets
# installed in install_replacement_packages()
function remove_replaced_packages() {
  local pkgs="${!replaced_pkgs_map[@]}"
  local p=''
  local rc=0

  for p in $pkgs; do
    ${RPM} -q --quiet $p && installed_pkgs_map+=([$p]=${replaced_pkgs_map[$p]})
  done

  if [ ${#installed_pkgs_map[@]} -gt 0 ]; then
    backup_configs $TMP_BACKUP_LOC ${!installed_pkgs_map[@]}
    echo "Removing following packages which will be replaced by other "\
             "packages -\n${!installed_pkgs_map[@]}"
    ${TDNF} $REPOS_OPT -y erase ${!installed_pkgs_map[@]}
    rc=$?
    if [ $rc -ne 0 ]; then
      abort $rc "Error removing replaced packages '${!installed_pkgs_map[@]}'."
    fi
    echo "Removal of replaced packages '${!installed_pkgs_map[@]}' succeeded."
  fi
}

#Some packages are deprecaed in 4.0 or 5.0, lets remove them before upgrading
function remove_unsupported_packages() {
  local rc=0

  if [ ${#deprecated_pkgs_to_remove_arr[@]} -gt 0 ]; then
    ${TDNF} $REPOS_OPT $ASSUME_YES_OPT erase ${deprecated_pkgs_to_remove_arr[@]}
    rc=$?
    if [ $rc -ne 0 ]; then
      abort $ERETRY_EAGAIN "Could not erase all unsupported packages (tdnf error code: $rc)."
    else
      echo "All unsupported packages are removed successfully."
    fi
  fi
}

function tdnf_makecache() {
  echo "Generating tdnf cache on Photon OS $(/usr/bin/lsb_release -s -r)"
  ${TDNF} $REPOS_OPT makecache
}

function distro_upgrade() {
  local ver="$1"
  local rc=0

  if [ "$ver" = "$FROM_VERSION" ]; then
    echo "Upgrading all installed Photon OS $FROM_VERSION packages to latest" \
         "available versions."
  else
    echo "Upgrading Photon OS to $TO_VERSION from $FROM_VERSION"
  fi

  if ${TDNF} $REPOS_OPT $ASSUME_YES_OPT distro-sync --releasever=$ver --refresh; then
      echo "All packages were upgraded to latest versions successfully."
      if [ "$ver" = "$TO_VERSION" ]; then
        ${TDNF} $REPOS_OPT $ASSUME_YES_OPT reinstall photon-release --releasever=$ver --refresh
        tdnf_makecache
        ${TDNF} $REPOS_OPT $ASSUME_YES_OPT install systemd-udev
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
      if ! ${TDNF} -q --disablerepo=* -y erase $p; then
        rc=$?
        err_rm_pkg_list="$err_rm_pkg_list $p"
        echo "Warning: Could not remove package '$p' post upgrade, error code: $rc."
      fi
    fi
  done
  if [ -n "$err_rm_pkg_list" ]; then
    echo "Warning: following packages were not removed post upgrade -" \
             "$err_rm_pkg_list"
  fi
}

# If user specifies --install-all and --repos then install all packages
# from the provided repos which are not installed
function install_all_from_repo()
{
  local available_pkgs_for_install="$(
      ${RPM} -q $(${TDNF} $REPOS_OPT repoquery --available) 2>&1 | \
        ${SED} -nE 's#^package ([^ ]+\.ph[0-9]+\.[^ ]+) is not installed#\1#p'
  )"
  local rc=0
  echo '--install-all option was passed.'
  if [ -n "$available_pkgs_for_install" ]; then
    echo "installing following packages from provided repos:" \
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
function pre_upgrade_rm_pkgs()
{
  local pkglist=''
  local p

  [ -z "$RM_PKGS_PRE" ] && return 0

  echo "Removing following user specified packages before upgrade - $RM_PKGS_PRE"

  for p in $(builtin echo "$RM_PKGS_PRE" | ${TR} , ' '); do
    if ${RPM} -q --quiet $p; then
      if ${TDNF} $REPOS_OPT $ASSUME_YES_OPT erase $p; then
        echo "Successfully removed user named pacakge $p."
      else
        pkglist="$pkglist $p"
      fi
    fi
  done
  if [ -n "$pkglist" ]; then
     abort $ERETRY_EAGAIN \
       "Error removing following user specified packages before upgrade: $pkglist" \
       "\nPlease remove those packages and retry the photon-upgrade.sh."
  fi
}

# Removes those packages named in --rm-pkgs-post after upgrade
function post_upgrade_rm_pkgs()
{
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
  TMP_BACKUP_LOC="$($MKTEMP -p /tmp -d photon-upgrade-XXX)"
  local rpmqa_file="$TMP_BACKUP_LOC/rpm-qa.txt"

  echo "Recording list of all installed RPMs on this machine to $rpmqa_file."
  ${RPM} -qa > $rpmqa_file
  echo "Creating backup of RPM DB."
  ${CP} -a $rpm_db_loc $TMP_BACKUP_LOC
}

# This will cleanup the backup created by backup_rpms_list_n_db()
function cleanup_and_exit() {
  if [ -n "$TMP_BACKUP_LOC" ] && [ -e "$TMP_BACKUP_LOC" ]; then
    rm -rf "$TMP_BACKUP_LOC"
  fi
  exit $1
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

#if the current install has packages deprecated in the target version,
#there is no clean upgrade path. confirm if it is okay to remove.
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

# Checks whether tdnf repo configurations are as expected or not.  The method
# aborts photon-upgrade if it finds photon-release package from other
# OS releases than the one being updated or upgraded to.
function is_repo_config_valid_for_release() {
  local r=$1   # release number 3.0, 4.0 etc.
  local -A tag_to_rel_map=(
    [ph3]=3.0
    [ph4]=4.0
    [ph5]=5.0
  )
  local t
  local phrel_pkgs_tags="$(
           ${TDNF} $REPOS_OPT --releasever=$r --refresh list available photon-release | \
           ${SED} -nE 's/^\S+\s+[^\-]+-[0-9]+\.(\S+)\s+.*$/\1/p' | ${SORT} | ${UNIQ}
        )"
  [ -z "$phrel_pkgs_tags" ] && \
    abort $ERETRY_EINVAL "No photon-release package from $r release was found." \
                         "Is photon-upgrade invoked properly? " \
                         "Please recheck the tdnf repo configurations and rerun."
  for t in $phrel_pkgs_tags; do
    if [ "$r" != "${tag_to_rel_map[$t]}" ]; then
      abort $ERETRY_EINVAL "Found unexpected photon-release package from ${tag_to_rel_map[$t]} release." \
                           "Is photon-upgrade invoked properly? " \
                           "Please recheck the tdnf repo configurations and rerun."
    fi
  done
}

function verify_version_and_upgrade() {
  local yn=''

  if [ $FROM_VERSION = $TO_VERSION ]; then
    echo "Your current version $FROM_VERSION is the latest version. Nothing to do."
    exit 0
  fi
  if [ -z "$ASSUME_YES_OPT" ]; then
    # This is interactive invocation of the script
    echo "You are about to upgrade PhotonOS from $FROM_VERSION to $TO_VERSION."
    echo "Please backup your data before proceeding. Continue (y/n)?"
    read yn
  else
    # -y or --assume-yes was given on command line; non-interactive invocation
    echo "Upgrading Photon OS from $FROM_VERSION to $TO_VERSION." \
         "Assuming that data backup has already been done."
    yn=y    # script is run non-interactively to do upgrade
  fi

  builtin echo ''
  case "$yn" in
    [Yy]*)
      is_repo_config_valid_for_release $TO_VERSION
      find_wrongly_enabled_services # Terminates upgrade on finding any regular
                                    # file in multi-user.target.wants under /etc
      backup_rpms_list_n_db $RPM_DB_LOC
      tdnf_makecache
      if [ "$UPDATE_PKGS" = 'y' ]; then
        # Vanilla Photon OS would want to update package manager and other
        # packages. Appliances may not need this.
        update_solv_to_support_complex_deps
        prepare_for_upgrade
        distro_upgrade $FROM_VERSION
      fi
      find_installed_deprecated_packages
      remove_unsupported_packages
      pre_upgrade_rm_pkgs
      rebuilddb
      record_enabled_disabled_services
      remove_replaced_packages
      fix_pre_upgrade_config
      distro_upgrade $TO_VERSION
      if [ "$TO_VERSION" = "5.0" ]; then
        relocate_rpmdb
      else
        rebuilddb
      fi
      fix_post_upgrade_config
      install_replacement_packages
      rebuilddb
      remove_residual_pkgs
      reset_enabled_disabled_services
      if [ -n "$INSTALL_ALL" ]; then
        install_all_from_repo
      fi
      post_upgrade_rm_pkgs
      rebuilddb
      ask_for_reboot
      ;;
    *) cleanup_and_exit 0;;
  esac
}

CMD_ARGS=$(
  getopt --long \
  'assume-yes,help,install-all,repos:,rm-pkgs-pre:,rm-pkgs-post:,to-ver:,skip-update,upgrade-os' \
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
      TO_VERSION=4.0   # default Photon OS version to upgrade to, --to-ver
                       # must be used to upgrade to Photon OS 5.0
      UPGRADE_OS='y'   # mark for OS upgrade
      ;;
    -- )
      break
      ;;
  esac
  shift
done

if [ "$UPGRADE_OS" = "n" ] && [ -n "$TO_VERSION" ]; then
  echoerr "--to-ver was specified without specifying --upgrade-os"
  show_help $ERETRY_EINVAL
fi

if [ -n "$TO_VERSION" ]; then
  case "$TO_VERSION" in
    4.0 )
      source ${PHOTON_UPGRADE_UTILS_DIR}/ph3-to-ph4-upgrade.sh
      ;;
    5.0 )
      source ${PHOTON_UPGRADE_UTILS_DIR}/ph3-to-ph5-upgrade.sh
      ;;
    * )
      echoerr "Valid values for --to-ver can only be 4.0 or 5.0"
      show_help $ERETRY_EINVAL
      ;;
  esac
elif [ -n "$INSTALL_ALL" ]; then
  echoerr "--install-all option is not supported for Photon OS 3.0"
  show_help $ERETRY_EINVAL
fi

# If repos are provided with --repos or --repos= option, only those repos will
# be used during both, upgrading OS or updatig installed RPMs to latest version

if [ -n "$INSTALL_ALL" ] && [ -z "$REPOS_OPT" ]; then
  # --install-all is given but --repos was not specified - invalid invocation
  show_help $ERETRY_EINVAL
fi

remove_debuginfo_packages
if [ "$UPGRADE_OS" = "y" ]; then
  # The script is run with --upgrade-os option, upgrading Photon OS
  verify_version_and_upgrade
elif [ "$UPDATE_PKGS" = 'y' ]; then
  # The script is run without --upgrade-os option.
  # Upgrading all installed RPMs to latest versions.
  backup_rpms_list_n_db $RPM_DB_LOC
  pre_upgrade_rm_pkgs
  tdnf_makecache
  distro_upgrade $FROM_VERSION
  rebuilddb
  post_upgrade_rm_pkgs
fi
cleanup_and_exit 0
