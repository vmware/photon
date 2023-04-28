#!/bin/bash

source /etc/os-release
PROG="$(basename $0)"
FROM_VERSION="$VERSION_ID"
TO_VERSION=''       # non-blank value indicates an os-upgrade, otherwise, update
ASSUME_YES_OPT=''   # value '-y' denotes non-interactive invocation
REPOS_OPT=''        # --disablerepo=* --enablerepo=repo, repo is given in --repo
UPDATE_PKGS=y       # If 'y', update packages before upgrade. Appliances may not
                    # provide repos to update packages in currently installed OS
                    # need this skipping for appliances
RM_PKGS_PRE=''      # Comma separated list of packages to remove before upgrade
RM_PKGS_POST=''     # Comma separated list of packages to remove afer upgrade
INSTALL_ALL=''      # non-empty value signifies that all packages from provided
                    # repos mentioned in --repos option needs to be installed

deprecated_packages='
    asciidoc autoconf213 ca-certificates-nxtgn-openssl-pki compat-gdbm
    debugmode elasticsearch fipsify haproxy-dataplaneapi hawkey iptraf
    js kibana kube-controllers libgsystem linux-aws-hmacgen
    linux-esx-hmacgen linux-hmacgen linux-secure-hmacgen linux-secure-lkcm liota
    logstash mozjs60 nxtgn-openssl openjdk10 openjre10 photon-checksum-generator
    ovn-central ovn-common ovn-controller-vtep ovn-doc ovn-docker ovn-host
    python2 pygobject-devel python3-cgroup-utils python3-future python3-gcovr
    python3-google-compute-engine python3-lvm2-libs python3-macholib
    python-certifi python-lockfile python-vcversioner rubygem-connection_pool
    rubygem-net-http-persistent yarn
'

declare -A replaced_pkgs_map=(      # This hashtable maps package name changes
  [python3-pycrypto]=python3-pycryptodome
)

enabled_services=''     # list of enabled services
disabled_services=''    # list of disabled serfices

pkgs_to_remove=''

TDNF=/usr/bin/tdnf
RPM=/usr/bin/rpm
SYSTEMCTL=/usr/bin/systemctl
TR=/usr/bin/tr
AWK=/usr/bin/awk
SED=/usr/bin/sed
CP=/usr/bin/cp

RPM_DB_LOC=/var/lib/rpm
TMP_BACKUP_LOC=''                   # temp location for 'rpm -qa' & rpm db copy

function show_help() {
  local rc

  if [ -z "$1" ]; then
    rc=0
  else
    rc=$1
  fi

  echo -n "
Usage: $PROG [--repos=r1,...] [--upgrade-os] [--assume-yes] [--skip-update] [--install-all] [--rm-pkgs-pre=p1,p2,...] [--rm-pkgs-post=p1,p2,...]

This script upgrades or updates Photon OS based upon the options provided.

--help         : Shows this help text
--repos        : Script will use only the specified repos which must exist
                 e.g. --repos=appliance,appliance-photon
--upgrade-os   : When option is given, Photon OS is upgraded to next release,
                else, all packages are updated to latest available versions
--assume-yes   : Runs the script non-interactively and assumes yes for responses
--skip-update  : Skip updating tdnf & packages before upgrading (for appliances)
--install-all  : Install all packages from provided repos from --repos option,
                --repos must be specified for --install-all
--rm-pkgs-pre  : Comma separated list of packages to remove before upgrade
--rm-pkgs-post : Comma separated list of packages to remove afer upgrade
"
  exit $rc
}

function echoerr() {
  echo -ne "$*" 1>&2
}

# To be called on irrecoverable error. It provides a user with actionable items
# to help debugging
function abort() {
  local rc=$1
  shift

  echoerr "$*\nOriginal list of RPMs and RPM DB are stored in $TMP_BACKUP_LOC,"\
          " please provide contents of that folder along with system journal "\
          " logs for analysis; these logs can be captured using command-\n"\
          "# /usr/bin/journalctl -xa > $TMP_BACKUP_LOC/journal.log\n" \
          "Cannot continue. Aborting.\n"
  exit $rc
}

# discover any regular file in /etc/systemd/system/multi-user.target.wants,
# whcih is meant for enabled services. If found, terminate the upgrade process
function find_wrongly_enabled_services()
{
  local f
  local p=/etc/systemd/system/multi-user.target.wants
  local wes=''  # holds space separated Wrongly Enabled Services list

  pushd $p
  for f in *; do
    if [ ! -L $f ]; then
      wes="${wes}${p}/${f} "
    fi
  done
  popd
  if [ -n "$wes" ]; then
    echoerr "Incorrect service configuratiion of following regular file(s) was found - " \
        "'$wes'.\nThese files must be removed for the upgrade to continue.\n" \
        "Those files may be removed and corresponding 'systemctl enable' command " \
        "may be, subsequently, used for enabling those systemd units.\n"
    exit 22 # EINVAL
  fi
}


# displays the space separated list of systemd managed services which have
# provided state
# e.g. get_services_by_state(enabled) - will return space separated list of
# enabled services
function get_services_by_state(){
  local state=$1

  ${SYSTEMCTL} list-unit-files |\
    ${AWK} "/[[:space:]]$state[[:space:]]*\$/{print \$1}"
  return $?
}

# Remember what services are enabled or disabled before upgrade
function record_enabled_disabled_services() {
  enabled_services="$(get_services_by_state enabled)"
  disabled_services="$(get_services_by_state disabled)"
}

# Reset states of services where they were before upgrade
function reset_enabled_disabled_services() {
  local svc

  for svc in $disabled_services; do
    ${SYSTEMCTL} disable $svc
  done
  for svc in $enabled_services; do
    ${SYSTEMCTL} enable $svc
  done
}

# Take care of pre upgrade config changes
function fix_pre_upgrade_config() {
  local python_link=/usr/bin/python

  # fix pam
  echo "Fixing PAM config to avoid authentication failures after upgrading."
  ${SED} -i -E 's/^(\s*\w+\s+\w+\s+pam_tally2?\.so).*$/\1/' /etc/pam.d/*
  echo "Fixing unsupported FipsMode config in ssh*_config for avoiding post upgrade ssh issues."
  ${SED} -i -E 's/^(\s*FipsMode\s+yes\s*)$/#\1/' /etc/ssh/sshd_config /etc/ssh/ssh_config
  if ${SYSTEMCTL} status sshd | grep -q 'Active: active (running)'; then
    ${SYSTEMCTL} restart sshd
  fi
}

# The packages replacing any of the existing already installed packages will
# be installed with the call to this method
function install_replacement_packages() {
  local pkgs="${!replaced_pkgs_map[@]}"
  local replacement_pkgs=''
  local p=''
  local rc=0

  for p in $pkgs; do
    ${RPM} -q $p && replacement_pkgs="$replacement_pkgs ${replaced_pkgs_map[$p]}"
  done

  if [ -n "$replacement_pkgs" ]; then
    echo -ne "Installing following packages which are replacing existing" \
             "packages -\n$replacement_pkgs\n"
    if ! ${TDNF} $REPOS_OPT -y install $replacement_pkgs; then
      rc=$?
      abort $rc "Error installing replacement packages '$replacement_pkgs'."
    fi
    echo "Replacement packages '$replacement_pkgs' are successfully installed"
  fi
}

# Installed packges which were replaced by other packages or installed packages
# which were renamed were removed by this method. The replacing package gets
# installed in install_replacement_packages()
function remove_replaced_packages() {
  local pkgs="${!replaced_pkgs_map[@]}"
  local installed_pkgs=''
  local p=''
  local rc=0

  for p in $pkgs; do
    ${RPM} -q $p && installed_pkgs="$installed_pkgs $p"
  done

  if [ -n "$installed_pkgs" ]; then
    echo -ne "Removing following packages which were replaced by other "\
             "packages -\n$installed_pkgs\n"
    if ! ${TDNF} $REPOS_OPT -y erase $installed_pkgs; then
      rc=$?
      abort $rc "Error removing replaced packages '$installed_pkgs'."
    fi
    echo "Removal of replaced packages '$installed_pkgs' succeeded."
  fi
}

#Some packages are deprecaed in 4.0, lets remove them before upgrading
function remove_unsupported_packages() {
  local rc=0

  if [ -n "$pkgs_to_remove" ]; then
    ${TDNF} -y erase $(echo -e $pkgs_to_remove)
    rc=$?
    if [ $rc -ne 0 ]; then
      abort 11 "Could not erase all unsupported packages (tdnf error code: $rc)."
    else
      echo "All unsupported packages are removed successfully."
    fi
  fi
}

function upgrade_photon_release() {
  local rc=0

  echo "Upgrading the photon-release package"
  if ${TDNF} $REPOS_OPT -y update photon-release --releasever=$TO_VERSION --refresh; then
    echo "The photon-release package upgrade successfully."
  else
    rc=$?
    abort 11 "Could not upgrade photon-release package (tdnf error code: $rc)."
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
      abort 11 "Error in upgrading all packages to latest versions (tdnf error code: $rc)."
    else
      abort $rc "Error in upgrading to Photon OS $TO_VERSION from $FROM_VERSION."
    fi
  fi
}

function rebuilddb() {
  local rc=0

  if ! rpm --rebuilddb; then
    rc=$?
    abort $rc "Failed rebuilding installed package database."
  fi
}

function post_upgrade_remove_pkgs() {
  local pkgs='libmetalink libdb'
  local err_rm_pkg_list=''
  local rc=0
  local p=''

  for p in $pkgs; do
    if rpm -q --quiet $p; then
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

# Take care of post upgrade config changes
function fix_post_upgrade_config() {
  local python_link=/usr/bin/python

  # fix pam
  echo "Fixing PAM config post upgrade for pam_faillock.so and pam_pwquality.so."
  ${SED} -i -E 's/^(\s*\w+\s+\w+\s+)pam_tally2?\.so.*$/\1pam_faillock.so/' /etc/pam.d/*
  ${SED} -i -E 's/pam_cracklib.so/pam_pwquality.so/' /etc/pam.d/*
  echo "Setting $python_link."
  test -e $python_link || ln -s python3 $python_link
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

# Removes those packages named in --rm-pkgs-pre option before upgrading
function pre_upgrade_rm_pkgs()
{
  local pkglist=''
  local p

  for p in $(echo "$RM_PKGS_PRE" | ${TR} , ' '); do
    if ${RPM} -q --quiet $p; then
      if ! ${TDNF} $REPOS_OPT $ASSUME_YES_OPT remove $p; then
        pkglist="$pkglist $p"
      fi
    fi
  done
  if [ -n "$pkglist" ]; then
     echoerr "Error removing following user named packages before upgrade:" \
             "$pkglist"
  fi
}

# Removes those packages named in --rm-pkgs-post after upgrade
function post_upgrade_rm_pkgs()
{
  local pkglist=''
  local p

  for p in $(echo "$RM_PKGS_POST" | ${TR} , ' '); do
    if ${RPM} -q --quiet $p; then
      if ! ${TDNF} $REPOS_OPT $ASSUME_YES_OPT remove $p; then
        pkglist="$pkglist $p"
      fi
    fi
  done
  if [ -n "$pkglist" ]; then
     echoerr "Error removing following user named packages post upgrade:" \
             "$pkglist"
  fi
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
  ${CP} -a $RPM_DB_LOC $TMP_BACKUP_LOC
}

# This will cleanup the backup created by backup_rpms_list_n_db()
function cleanup_and_exit() {
  if [ -n "$TMP_BACKUP_LOC" -a -e "$TMP_BACKUP_LOC" ]; then
    rm -rf "$TMP_BACKUP_LOC"
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

  for pkg in ${deprecated_packages}; do
    if rpm -q $pkg; then
      pkgs_to_remove="${pkgs_to_remove}${pkg}\n"
    fi
  done
  if [ -n "$pkgs_to_remove" ]; then
    if [ -z "$ASSUME_YES_OPT" ]; then
      # This is interactive invocation of the script
      echo "The following packages are deprecated and must be removed before upgrade."
      echo -e "$pkgs_to_remove"
      read -p "Proceed(y/n)?" yn
      case $yn in
        [Nn]* ) cleanup_and_exit 0 ;;
      esac
    else
      echo -ne "Removing following deprecated packages - \n$pkgs_to_remove\n"
    fi
  fi
}

#next version of photon uses specs with dependencies
#of the form x or y. update tdnf, libsolv and rpm to support it.
function update_solv_to_support_complex_deps() {
  local rc=0

  echo "Updating package management software and libraries."
  if ${TDNF} $REPOS_OPT -y update libsolv rpm tdnf --refresh; then
    echo "Upgrade of package management software and libraries succeeded."
    rebuilddb
  else
    rc=$?
    abort 11 "Could not update package management software and libraries (tdnf error code: $rc)."
  fi
}

function verify_version_and_upgrade() {
  local yn=''

  if [ $FROM_VERSION = $TO_VERSION ]; then
    echo "Your current version $FROM_VERSION is the latest version. Nothing to do."
    exit 0
  fi
  find_wrongly_enabled_services # Terminates upgrade on finding any regular file in
                                # /etc/systemd/system/multi-user.target.wants/
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
        distro_upgrade $FROM_VERSION
      fi
      remove_unsupported_packages
      pre_upgrade_rm_pkgs
      rebuilddb
      record_enabled_disabled_services
      upgrade_photon_release
      fix_pre_upgrade_config
      install_replacement_packages
      remove_replaced_packages
      distro_upgrade $TO_VERSION
      rebuilddb
      post_upgrade_remove_pkgs
      reset_enabled_disabled_services
      fix_post_upgrade_config
      if [ -n "$INSTALL_ALL" ]; then
        install_all_from_repo
      fi
      post_upgrade_rm_pkgs
      ask_for_reboot
      ;;
    *) cleanup_and_exit 0;;
  esac
}

while [ $# -gt 0 ]; do
  case "$1" in
    --help )
      show_help 0
      ;;
    --upgrade-os )
      TO_VERSION=4.0
      ;;
    --assume-yes )
      ASSUME_YES_OPT='-y'
      ;;
    --skip-update )
      UPDATE_PKGS='n'  # Any value other than 'y' would not update packages
      ;;
    --install-all)
      INSTALL_ALL='y' # install all packages from provided repos by --repos
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
        show_help 22
      fi


      for r in $(echo "$repos_csv" | ${TR} , ' '); do
        REPOS_OPT="$REPOS_OPT --enablerepo=$r"
      done

      if [ -n "$repos_csv" ]; then
        REPOS_OPT="--disablerepo=* $REPOS_OPT"
      fi
      ;;
    --rm-pkgs-pre=* )
      RM_PKGS_PRE="$(echo "$1" | cut -d = -f 2)"
      [ -z "$RM_PKGS_PRE" ] && \
        echoerr "--rm-pkgs-pre was specified without providing any package names" && \
          show_help 22
      ;;
    --rm-pkgs-pre )
      RM_PKGS_PRE="$2"
      [ -z "$RM_PKGS_PRE" ] && \
        echoerr "--rm-pkgs-pre was specified without providing any package names" && \
          show_help 22
      shift
      ;;
    --rm-pkgs-post=* )
      RM_PKGS_POST="$(echo "$1" | cut -d = -f 2)"
      [ -z "$RM_PKGS_POST" ] && \
        echoerr "--rm-pkgs-post was specified without providing any package names" && \
          show_help 22
      ;;
    --rm-pkgs-post )
      RM_PKGS_POST="$2"
      [ -z "$RM_PKGS_POST" ] && \
        echoerr "--rm-pkgs-post was specified without providing any package names" && \
          show_help 22
      shift
      ;;
    * )
      echoerr "Invalid option '$1' speciied"
      show_help 22
      ;;
  esac
  shift
done

# If repos are provided with --repos or --repos= option, only those repos will
# be used during both, upgrading OS or updatig installed RPMs to latest version

if [ -n "$INSTALL_ALL" -a -z "$REPOS_OPT" ]; then
  # --install-all is given but --repos was not specified - invalid invocation
  show_help 22
fi

if [ -n "$TO_VERSION" ]; then
  # The script is run with --upgrade-os option, upgrading Photon OS
  verify_version_and_upgrade
else
  # The script is run withour or --upgrade-os option.
  # Upgrading all installed RPMs to latest versions.
  backup_rpms_list_n_db
  pre_upgrade_rm_pkgs
  distro_upgrade $FROM_VERSION
  rebuilddb
  if [ -n "$INSTALL_ALL" ]; then
    install_all_from_repo
  fi
  post_upgrade_rm_pkgs
fi
cleanup_and_exit 0
