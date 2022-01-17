#!/bin/bash

FROM_VERSION="$(grep '^VMware Photon' /etc/photon-release | cut -d ' ' -f 4)"
TO_VERSION='4.0'

deprecated_packages='
    asciidoc autoconf213 ca-certificates-nxtgn-openssl-pki compat-gdbm
    debugmode elasticsearch fipsify haproxy-dataplaneapi hawkey iptraf
    js kibana kube-controllers libgsystem linux-aws-hmacgen
    linux-esx-hmacgen linux-hmacgen linux-secure-hmacgen linux-secure-lkcm liota
    logstash mozjs60 nxtgn-openssl openjdk10 openjre10 photon-checksum-generator
    ovn-central ovn-common ovn-controller-vtep ovn-doc ovn-docker ovn-host
    python2 pygobject-devel python3-cgroup-utils python3-future python3-gcovr
    python3-google-compute-engine python3-lvm2-libs python3-macholib
    python-certifi python-lockfile python3-pycrypto python-vcversioner
    rubygem-connection_pool rubygem-net-http-persistent yarn
'
pkgs_to_remove=''

function echoerr() {
  echo -ne "$*" 1>&2
}

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
      echoerr "Could not erase all unsupported packages. Failed to continue, aborting.\n"
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
    echoerr "Could not upgrade photon-release package. Cannot continue the upgrade, aborting.\n"
    exit $rc
  fi
}

function distro_upgrade() {
  local ver="$1"
  local rc=0

  if [ "$ver" == "$FROM_VERSION" ]; then
    echo "Upgrading all installed packages to latest versions."
  else
    echo "Upgrading all packages to Photon $TO_VERSION"
  fi

  if tdnf distro-sync --refresh; then
      echo "The packages were upgraded successfully."
  else
    rc=$?
    if [ "$ver" == "$FROM_VERSION" ]; then
      echoerr "Failed in upgrading all Photon $FROM_VERSION packages to latest versions."
    else
      echoerr "Failed in upgrading all packages to Photon $TO_VERSION."
    fi
    echoerr " Cannot continue the upgrade, aborting.\n"
    exit $rc
  fi
}

function rebuilddb() {
  local rc=0
  if ! rpm --rebuilddb; then
    rc=$?
    echoerr "Failed rebuilding installed package database. Cannot continue the upgrade, aborting.\n"
    exit $rc
  fi
}

function post_upgrade_remove_pkgs() {
  local pkgs='libmetalink'
  local found_pkgs=''
  local rc=0
  local p=''

  for p in $pkgs; do
    if rpm -q --quiet $p; then
      found_pkgs="$found_pkgs $p"
      if ! tdnf -q -y remove $p; then
        rc=$?
        echo -e "Warning: Could not remove deprecated package '$p' post upgrade, error code: $rc."
      fi
    fi
  done
  if [ -n "$found_pkgs" ]; then
    echo -e "Successfully removed all unsupported packages post upgrade."
  fi
}

#must reboot after an upgrade
function ask_for_reboot() {
  local yn=''
  read -p "Reboot is recommended after an upgrade. Reboot now(y/n)?" yn
  case $yn in
    [Yy]* ) reboot;;
    [Nn]* ) exit;;
  esac
}

#if the current install has packages deprecated in the target version,
#there is no clean upgrade path. confirm if it is okay to remove.
function find_installed_deprecated_packages() {
  local pkg=''
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
    echoerr "Could not update package management software and libraries." \
        "Cannot continue the upgrade.\n"
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
      distro_upgrade $FROM_VERSION
      remove_unsupported_packages
      rebuilddb
      upgrade_photon_release
      distro_upgrade $TO_VERSION
      rebuilddb
      post_upgrade_remove_pkgs
      apply_systemd_presets
      ask_for_reboot
      ;;
    *) exit;;
  esac
}

verify_version_and_upgrade
