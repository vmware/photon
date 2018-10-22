#!/bin/bash

FROM_VERSION="$(awk '/VMware Photon OS /{print $4}' /etc/photon-release)"
TO_VERSION='3.0'

# The package list of deprecated packages from 2.0 to 3.0
depPkgsFrom2To3='urlgrabber librepo ceph-deploy conntrack-tools libhif yum createrepo ceph ostree micro-config-drive gmock deltarpm rpm-ostree kibana docker-volume-vsphere yarn mesos yum-metadata-parser'

#Some packages are deprecaed from 3.0, lets remove them before moving to 3.0
function remove_unsupported_pkgs() {
  local rc
  for pkg in $depPkgsFrom2To3; do
    if rpm -q $pkg; then
      tdnf erase $pkg -y
      rc=$?
      if [ $rc -ne 0 ]; then
        echo "Could not erase $pkg. Cannot continue."
        exit $rc
      fi
    fi
  done
}

function upgrade_photon_release() {
   tdnf -y update photon-release --releasever=$TO_VERSION --refresh
}

function distro_upgrade() {
   tdnf distro-sync --refresh
}

function rebuilddb() {
   rpm --rebuilddb
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
function check_deprecated() {
  pkgs_to_remove=''
  for pkg in ${depPkgsFrom2To3}; do
    installed=`rpm -q $pkg`
    if [ $? -eq 0 ]; then
      pkgs_to_remove="${pkgs_to_remove}${pkg}\n"
    fi
  done
  if [ "$pkgs_to_remove" != "" ];then
    echo "The following packages are deprecated and must be removed before upgrade."
    echo -e $pkgs_to_remove
    read -p "Proceed(y/n)?" yn
    case $yn in
      [Nn]* ) exit;;
    esac
  fi
}

#there is a chance that /var/run is a directory
#in this case, move its contents to /run and make it a symlink
function make_var_run_a_symlink() {
  if [ -d '/var/run' ] && [ ! -L '/var/run' ] ; then
    mv /var/run/* /run
    rm -rf /var/run
    ln -sf /run /var/run
  fi
}

#next version of photon uses specs with dependencies
#of the form x or y. update tdnf, libsolv and rpm to support it.
function update_solv_to_support_complex_deps() {
   tdnf -y update libsolv rpm tdnf --refresh
   rebuilddb
}

function check_and_upgrade() {
  if [ $FROM_VERSION == $TO_VERSION ]; then
    echo "Your current version $FROM_VERSION is the latest version. Nothing to do."
    exit
  fi
  check_deprecated
  echo "You are about to upgrade PhotonOS from $FROM_VERSION to $TO_VERSION."
  echo -n "Please backup your data before proceeding. Continue (y/n)?"
  read
  echo

  case $REPLY in
    [Yy]*)
      update_solv_to_support_complex_deps
      remove_unsupported_pkgs
      rebuilddb
      make_var_run_a_symlink
      upgrade_photon_release
      distro_upgrade
      rebuilddb
      ask_for_reboot
      ;;
    *) exit;;
  esac
}

check_and_upgrade
