#/bin/bash

PHOTON_VERSION=`( cat /etc/photon-release | grep -i "vmware photon" ) | cut -d- -f1 | grep -o -E '[0-9]+.[0-9]+'`
TARGET_VERSION=$1
LATEST_VERSION='2.0'

#some packages like fleet, rocket etc are removed from 2.0
#lets remove those before moving to 2.0
function remove_unsupported_pkgs() {
  pkgs=('fleet' 'rocket')
  for pkg in ${pkgs[@]}; do
    rpm -q $pkg
    if [ $? -eq 0 ]; then
      tdnf erase $pkg -qy
      if [ $? -eq 0 ]; then
        echo "Could not erase $pkg. Cannot continue."
        exit
      fi
    fi
  done
}

#there are certain packages that cause upgrade issues.
#upgrade those to latest within the current version
#so that they dont cause a problem in distro-sync
function fix_packages_with_upgrade_issues() {
  pkgs=('python-six:1.10.0-4.ph1')
  for pkg in ${pkgs[@]}; do
    name=${pkg%%:*}
    version=${pkg#*:}
    current_version=`rpm -q --queryformat %{version}-%{release} $name`
    if [ $? -eq 0 ]; then
      if [[ "$version" > "$current_version" ]]; then
        echo "updating $name"
        tdnf update -qy "$name"
        if [ $? -ne 0 ]; then
          echo "Could not update $1 to version $2 or higher. Cannot continue"
          exit
        fi
        current_version=`rpm -q --queryformat %{version}-%{release} $name`
        if [[ "$version" > "$current_version" ]]; then
          echo "Could not update $name to version $version or higher. Cannot continue"
          exit
        fi
      fi
    fi
  done
}

function upgrade_tdnf() {
   tdnf -qy update tdnf
}

function upgrade_photon_release() {
   #when we are in beta with 2.0, we should only need the following line
   #tdnf -y update photon-release --releasever=$TARGET_VERSION

   #because there are no 2.0 repos yet, fit to what we have.
   #remove when 2.0 repos are published.
   sed -i 's/enabled=1/enabled=0/' /etc/yum.repos.d/photon.repo
   sed -i 's/enabled=1/enabled=0/' /etc/yum.repos.d/photon-updates.repo
   cat >> /etc/yum.repos.d/_photon_upgrade_dev_.repo <<-EOF
[_dev_]
name=dev
baseurl=https://dl.bintray.com/vmware/photon_dev_x86_64
gpgkey=file:///etc/pki/rpm-gpg/VMWARE-RPM-GPG-KEY
gpgcheck=1
enabled=1
skip_if_unavailable=True
EOF
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
      upgrade_tdnf
      remove_unsupported_pkgs
      fix_packages_with_upgrade_issues
      rebuilddb
      upgrade_photon_release
      distro_upgrade
      rebuilddb
      ;;
    *) exit;;
  esac
}

check_and_upgrade
