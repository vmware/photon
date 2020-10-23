#!/bin/bash

FROM_VERSION="$(grep '^VMware Photon' /etc/photon-release | cut -d ' ' -f 4)"
TO_VERSION='4.0'

deprecated_packages='
    bzr nxtgn-openssl ca-certificates-nxtgn-openssl-pki compat-gdbm
    debugmode distrib-compat haproxy-dataplaneapi ipcalc python2
    python3-cgroup-utils python3-gcovr python3-google-compute-engine
    python3-lvm2-libs python3-pam yarn
'
pkgs_to_remove=''

# Before going for post upgrade reboot, reneable all required services
function apply_systemd_presets() {
  /usr/bin/systemctl preset-all
}

#Some packages are deprecaed in 4.0, lets remove them before upgrading
function remove_unsupported_packages() {
  local rc=0
  if [ -n "$pkgs_to_remove" ]; then
    tdnf -y erase $(echo -e $pkgs_to_remove)
    rc=$?
    if [ $rc -ne 0 ]; then
      echo "Could not erase all unsupported packages. Failed to continue, aborting."
      exit $rc
    else
      echo "All unsupported packages are removed successfully."
    fi
  fi
}

function upgrade_photon_release() {
  local rc=0
  echo "Upgrading the photon-release package"
  if tdnf -y update photon-release --releasever=$TO_VERSION --refresh; then
    echo "The photon-release package upgrade successfully."
  else
    rc=$?
    echo -e "Could not upgrade photon-release package. Cannot continue the upgrade, aborting."
    exit $rc
  fi
}

function distro_upgrade() {
  local rc=0
  echo "Upgrading all packages to Photon $TO_VERSION" 
  if tdnf distro-sync --refresh; then
    echo "The packages were upgraded successfully."
  else
    rc=$?
    echo -e "Failed in upgrading all packages to Phton $TO_VERSION. Cannot continue the upgrade, aborting."
    exit $rc
  fi
}

function rebuilddb() {
  local rc=0
  if ! rpm --rebuilddb; then
    rc=$?
    echo -e "Failed rebuilding installed package database. Cannot continue the upgrade, aborting."
    exit $rc
  fi
}

#must reboot after an upgrade
function ask_for_reboot() {
  read -p "Reboot is recommended after an upgrade. Reboot now(y/n)?" yn
  case $yn in
    [Yy]* ) reboot;;
    [Nn]* ) exit;;
  esac
}

#if the current install has packages deprecated in the target version,
#there is no clean upgrade path. confirm if it is okay to remove.
function find_installed_deprecated_packages() {
  for pkg in ${deprecated_packages}; do
    if rpm --quiet -q $pkg; then
      pkgs_to_remove="${pkgs_to_remove}${pkg}\n"
    fi
  done
  if [ -n "$pkgs_to_remove" ]; then
    echo "The following packages are deprecated and must be removed before upgrade."
    echo -e "$pkgs_to_remove"
    read -p "Proceed(y/n)?" yn
    case $yn in
      [Nn]* ) exit;;
    esac
  fi
}

#next version of photon uses specs with dependencies
#of the form x or y. update tdnf, libsolv and rpm to support it.
function update_solv_to_support_complex_deps() {
  local rc=0
  echo "Updating package management software and libraries."
  if tdnf -y update libsolv rpm tdnf --refresh; then
    echo "Upgrade of package management software and libraries succeeded."
    rebuilddb
  else
    rc=$?
    echo "Could not update package management software and libraries." \
        "Cannot continue the upgrade."
    exit $rc
  fi
}

function verify_version_and_upgrade() {
  if [ $FROM_VERSION == $TO_VERSION ]; then
    echo "Your current version $FROM_VERSION is the latest version. Nothing to do."
    exit 0
  fi
  find_installed_deprecated_packages
  echo "You are about to upgrade PhotonOS from $FROM_VERSION to $TO_VERSION."
  echo -n "Please backup your data before proceeding. Continue (y/n)?"
  read
  echo

  case $REPLY in
    [Yy]*)
      update_solv_to_support_complex_deps
      remove_unsupported_packages
      rebuilddb
      upgrade_photon_release
      distro_upgrade
      rebuilddb
      apply_systemd_presets
      ask_for_reboot
      ;;
    *) exit;;
  esac
}

verify_version_and_upgrade
