#/bin/bash

PHOTON_VERSION=`( cat /etc/photon-release | grep -i "vmware photon" ) | cut -d- -f1 | grep -o -E '[0-9]+.[0-9]+'`
TARGET_VERSION=$1
LATEST_VERSION='2.0'

function fix_packages_with_upgrade_issues() {
}

function upgrade_tdnf() {
   tdnf -y update tdnf
}

function upgrade_photon_release() {
   tdnf -y update photon-release --releasever=$TARGET_VERSION
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

function check_and_upgrade() {
  if [ $PHOTON_VERSION == $LATEST_VERSION ]; then
    echo "Your current version $PHOTON_VERSION is the latest version. Nothing to do."
    exit
  fi
  echo "You are about to upgrade PhotonOS from $PHOTON_VERSION to $LATEST_VERSION."
  echo -n "Please backup your data before proceeding. Continue (y/n)?"
  read
  echo

  case $REPLY in
    [Yy]*)
      update_packages_with_upgrade_issues 
      upgrade_tdnf
      upgrade_photon_release
      distro_upgrade
      rebuilddb
      ;;
    *) exit;;
  esac
}

check_and_upgrade
