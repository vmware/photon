#!/bin/bash

PROG="$(basename $0)"

PHOTON_UPGRADE_UTILS_DIR="/usr/lib/photon-upgrade"

source ${PHOTON_UPGRADE_UTILS_DIR}/utils.sh
source ${PHOTON_UPGRADE_UTILS_DIR}/common.sh

FROM_VERSION="$(/usr/bin/lsb_release -s -r)"
TO_VERSION=''       # non-blank value indicates an os-upgrade, otherwise, update
ASSUME_YES_OPT=''   # value '-y' denotes non-interactive invocation
REPOS_OPT=''        # --disablerepo=* --enablerepo=repo, repo is given in --repos
UPDATE_PKGS=y       # If 'y', update packages before upgrade. Appliances may not
                    # provide repos to update packages in currently installed OS
                    # thus, need this skipping for appliances
INSTALL_ALL=''      # non-empty value signifies that all packages from provided
                    # repos mentioned in --repos option needs to be installed

# temp location for 'rpm -qa' & rpm db copy
TMP_BACKUP_LOC=''

function show_help() {
  local rc=0

  if [ -n "$1" ]; then
    rc=$1
  fi

  echo -n "
Usage: $PROG [--help | -h] [--repos=r1,...] [--upgrade-os] [--assume-yes] [--skip-update] [--install-all]

This script upgrades or updates Photon OS based upon the options provided.

--help        : Shows this help text
--repos       : Script will use only the specified repos which must exist
                e.g. --repos=appliance,appliance-photon
--upgrade-os  : When option is given, Photon OS is upgraded to next release,
                else, all packages are updated to latest available versions
--assume-yes  : Runs the script non-interactively and assumes yes for responses
--skip-update : Skip updating tdnf & packages before upgrading (for appliances)
--install-all : Install all packages from provided repos from --repos option,
                --repos must be specified for --install-all
"
  exit $rc
}

# Remember what services are enabled or disabled before upgrade
function record_enabled_disabled_services() {
  enabled_services_arr+=( $(get_services_by_state enabled) )
  disabled_services_arr+=( $(get_services_by_state disabled) )
}

# Reset states of services where they were before upgrade
function reset_enabled_disabled_services() {
  local s=''

  for s in ${enabled_services_arr[@]}; do
    ${SYSTEMCTL} enable ${s}
  done

  for s in ${disabled_services_arr[@]}; do
    ${SYSTEMCTL} disable ${s}
  done
}

# Remove all debuginfo packages as they may hamper during upgrade
function remove_debuginfo_packages() {
  local installed_debuginfo_pkgs="$(${RPM} -qa | grep -- -debuginfo-)"
  local rc=0
  [ -z "$installed_debuginfo_pkgs" ] && return 0
  echo "Following debuginfo packages will be removed - $installed_debuginfo_pkgs"
  if ! ${TDNF} -q '--disablerepo=*' $ASSUME_YES_OPT \
         erase $installed_debuginfo_pkgs; then
    rc=$?
    abort $ERETRY_EAGAIN "Error removing debuginfo packages"
  fi
  echo "All debuginfo packages were successfully removed."
}

# The packages replacing any of the existing already installed packages will
# be installed with the call to this method
function install_replacement_packages() {
  local pkgs="${!replaced_pkgs_map[@]}"
  local replacement_pkgs=''
  local p=''
  local rc=0

  for p in $pkgs; do
    ${RPM} -q --quiet $p && replacement_pkgs="$replacement_pkgs ${replaced_pkgs_map[$p]}"
  done

  if [ -n "$replacement_pkgs" ]; then
    echo -ne "Installing following packages which are replacing existing" \
             "packages -\n$replacement_pkgs\n"
    if ! ${TDNF} $REPOS_OPT $ASSUME_YES_OPT install $replacement_pkgs; then
      rc=$?
      abort $rc "Error installing replacement packages '$replacement_pkgs' (tdnf error code: $rc)."
    fi
    echo "Replacement packages '$replacement_pkgs' are successfully installed"
  fi
}

# Installed packges which were replaced by other packages or installed packages
# which were renamed get removed by this method. The replacing package gets
# installed in install_replacement_packages()
function remove_replaced_packages() {
  local pkgs="${!replaced_pkgs_map[@]}"
  local installed_pkgs=''
  local p=''
  local rc=0

  for p in $pkgs; do
    ${RPM} -q --quiet $p && installed_pkgs="$installed_pkgs $p"
  done

  if [ -n "$installed_pkgs" ]; then
    echo -ne "Removing following packages which were replaced by other "\
             "packages -\n$installed_pkgs\n"
    if ! ${TDNF} $REPOS_OPT $ASSUME_YES_OPT erase $installed_pkgs; then
      rc=$?
      abort $rc "Error removing replaced packages $installed_pkgs (tdnf error code: $rc)."
    fi
    echo "Removal of replaced packages '$installed_pkgs' succeeded."
  fi
}

#Some packages are deprecaed in 5.0, lets remove them before upgrading
function remove_unsupported_packages() {
  local rc=0

  if [ ${#deprecated_pkgs_to_remove_arr[@]} -gt 0 ]; then
    ${TDNF} $ASSUME_YES_OPT erase ${deprecated_pkgs_to_remove_arr[@]}
    rc=$?
    if [ $rc -ne 0 ]; then
      abort $ERETRY_EAGAIN "Could not erase all unsupported packages (tdnf error code: $rc)."
    else
      echo "All unsupported packages are removed successfully."
    fi
  fi
}

function upgrade_photon_release() {
  local rc=0

  echo "Upgrading the photon-release package"
  if ${TDNF} $REPOS_OPT $ASSUME_YES_OPT update photon-release \
    --releasever=$TO_VERSION --refresh; then
    echo "The photon-release package upgrade successfully."
  else
    rc=$?
    abort $ERETRY_EAGAIN "Could not upgrade photon-release package (tdnf error code: $rc)."
  fi
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

  if ${TDNF} $REPOS_OPT $ASSUME_YES_OPT distro-sync --refresh; then
      echo "All packages were upgraded to latest versions successfully."
  else
    rc=$?
    if [ "$ver" = "$FROM_VERSION" ]; then
      abort $ERETRY_EAGAIN "Error in upgrading all packages to latest versions (tdnf error code: $rc)."
    else
      abort $rc "Error in upgrading to Photon OS $TO_VERSION from $FROM_VERSION."
    fi
  fi
}

function post_upgrade_remove_pkgs() {
  local pkgs="$*"
  local err_rm_pkg_list=''
  local rc=0
  local p=''

  for p in $pkgs; do
    if $RPM -q --quiet $p; then
      if ! ${TDNF} -q '--disablerepo=*' -y remove $p; then
        rc=$?
        err_rm_pkg_list="$err_rm_pkg_list $p"
        echo -e "Warning: Could not remove deprecated package '$p' post upgrade, error code: $rc."
      fi
    fi
  done
  if [ -n "$err_rm_pkg_list" ]; then
    echo -ne "Warning: following packages were not removed post upgrade-" \
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
  echo -n '--install-all option was passed, '
  if [ -n "$available_pkgs_for_install" ]; then
    echo "installing following packages from provided repos:" \
      "$(echo $available_pkgs_for_install | ${SED} -E 's/ /, /g')"
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

# Backup 'rpm -qa' and RPM DB before changing RPM DB in anyway, this will help
# in debugging any failures and will be used to provide actionable item to the
# end-user
function backup_rpms_list_n_db() {
  TMP_BACKUP_LOC="$(mktemp -p /tmp -d photon-upgrade-XXX)"
  local rpmqa_file="$TMP_BACKUP_LOC/rpm-qa.txt"

  echo "Recording list of all installed RPMs on this machine to $rpmqa_file."
  ${RPM} -qa > $rpmqa_file
  echo "Creating back of RPM DB."
  ${CP} -a $OLD_RPM_DB_PATH $TMP_BACKUP_LOC
}

# This will cleanup the backup created by backup_rpms_list_n_db()
function cleanup_and_exit() {
  if [ -n "$TMP_BACKUP_LOC" -a -e "$TMP_BACKUP_LOC" ]; then
    ${RM} -rf "$TMP_BACKUP_LOC"
  fi
  exit $1
}

#must reboot after an upgrade
function ask_for_reboot() {
  local yn=''

  echo -n "Reboot is recommended after an upgrade. "
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

function verify_version_and_upgrade() {
  local yn=''

  if [ $FROM_VERSION = $TO_VERSION ]; then
    echo "Your current version $FROM_VERSION is the latest version. Nothing to do."
    exit 0
  fi
  backup_rpms_list_n_db
  find_installed_deprecated_packages
  if [ -z "$ASSUME_YES_OPT" ]; then
    # This is interactive invocation of the script
    echo "You are about to upgrade PhotonOS from $FROM_VERSION to $TO_VERSION."
    echo -n "Please backup your data before proceeding. Continue (y/n)?"
    read yn
  else
    # -y or --assme-yes was given on command line; non-interactive invocation
    echo "Upgrading Photon OS from $FROM_VERSION to $TO_VERSION." \
         "Assuming that data backup has already been done."
    yn=y    # script is run non-interactively to do upgrade
  fi

  echo
  case "$yn" in
    [Yy]*)
      if [ "$UPDATE_PKGS" = 'y' ]; then
        # Vanilla Photon OS would want to update package manager and other
        # packages. Appliances control builds so do not need this.
        update_solv_to_support_complex_deps
        prepare_for_upgrade
        distro_upgrade $FROM_VERSION
      fi
      remove_unsupported_packages
      rebuilddb
      record_enabled_disabled_services
      remove_replaced_packages
      upgrade_photon_release
      update_core_packages
      relocate_rpmdb
      install_replacement_packages
      distro_upgrade $TO_VERSION
      rebuilddb
      post_upgrade_remove_pkgs
      reset_enabled_disabled_services
      fix_post_upgrade_config
      if [ -n "$INSTALL_ALL" ]; then
        install_all_from_repo
      fi
      rebuilddb
      ask_for_reboot
      ;;
    *) cleanup_and_exit 0;;
  esac
}

while [ $# -gt 0 ]; do
  case "$1" in
    --help | -h )
      show_help 0
      ;;
    --upgrade-os )
      TO_VERSION=5.0
      source ${PHOTON_UPGRADE_UTILS_DIR}/ph4-to-ph5-upgrade.sh
      ;;
    --assume-yes )
      ASSUME_YES_OPT='-y'
      ;;
    --skip-update )
      UPDATE_PKGS='n'  # Any value other than 'y' would not update packages
      ;;
    --install-all)
      ;;
    --repos=* | --repos )
      if echo "$1" | grep -q -- '^--repos='; then
        repos_csv="$(echo "$1" | cut -d = -f 2)"
      else
        repos_csv="$2"
        shift
      fi
      if [ -n "$REPOS_OPT" ]; then
        echoerr "--repos was specified more than once"
        show_help $ERETRY_EINVAL
      fi

      for r in $(echo "$repos_csv" | ${TR} , ' '); do
        REPOS_OPT="$REPOS_OPT --enablerepo=$r"
      done

      if [ -n "$repos_csv" ]; then
        REPOS_OPT="--disablerepo=* $REPOS_OPT"
      fi
      ;;
    * )
      echoerr "Invalid option '$1' speciied"
      show_help $ERETRY_EINVAL
      ;;
  esac
  shift
done

# If repos are provided with --repos or --repos= option, only those repos will
# be used during both, upgrading OS or updatig installed RPMs to latest version

if [ -n "$INSTALL_ALL" -a -z "$REPOS_OPT" ]; then
  # --install-all is given but --repos was not specified - invalid invocation
  show_help $ERETRY_EINVAL
fi

remove_debuginfo_packages
if [ -n "$TO_VERSION" ]; then
  # The script is run with --upgrade-os option, upgrading Photon OS
  verify_version_and_upgrade
else
  # The script is run withour or --upgrade-os option.
  # Upgrading all installed RPMs to latest versions.
  backup_rpms_list_n_db
  distro_upgrade $FROM_VERSION
  rebuilddb
  if [ -n "$INSTALL_ALL" ]; then
    install_all_from_repo
  fi
fi

cleanup_and_exit 0
