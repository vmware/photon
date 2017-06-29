#/bin/bash

PHOTON_VERSION=`( cat /etc/photon-release | grep -i "vmware photon" ) | cut -d- -f1 | grep -o -E '[0-9]+.[0-9]+'`
LATEST_VERSION='2.0'


deprecated_pkgs=('fleet' 'rocket' 'NetworkManager' 'NetworkManager-devel')

#some packages like fleet, rocket etc are removed from 2.0
#lets remove those before moving to 2.0
function remove_unsupported_pkgs() {
  for pkg in ${deprecated_pkgs[@]}; do
    rpm -q $pkg
    if [ $? -eq 0 ]; then
      tdnf erase $pkg -y
      if [ $? -eq 0 ]; then
        echo "Could not erase $pkg. Cannot continue."
        exit
      fi
    fi
  done
}

#move mesos-devel along
function fix_mesos_devel_symlink() {
  has_mesos_devel=`rpm -q mesos-devel`
  if [ $? -eq 0 ]; then
    if [ -d '/usr/include/mesos/slave' ] && [ ! -L '/usr/include/mesos/slave' ] && [ ! -d '/usr/include/mesos/agent' ]; then
      mv /usr/include/mesos/slave /usr/include/mesos/agent
      ln -s /usr/include/mesos/agent /usr/include/mesos/slave
    fi
  fi
}

#there are certain packages that cause upgrade issues.
#upgrade those to latest within the current version
#so that they dont cause a problem in distro-sync
function fix_packages_with_upgrade_issues() {
  pkgs=('httpd:2.4.25-3.ph1'
        'lldb:3.9.1-3.ph1'
        'netcat:0.7.1-3.ph1'
        'nfs-utils:1.3.3-5.ph1'
        'nginx:1.11.13-3.ph1'
        'pciutils:3.3.1-3.ph1'
        'userspace-rcu:0.9.1-3.ph1'
        'texinfo:6.1-3.ph1')
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
  fix_mesos_devel_symlink
}

function upgrade_tdnf() {
   tdnf -y update tdnf
}

#because there are no 2.0 repos yet, fit to what we have.
#remove when 2.0 repos are published.
function upgrade_photon_release_dev() {
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

function upgrade_photon_release() {
   tdnf -y update photon-release --releasever=$LATEST_VERSION
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
  for pkg in ${deprecated_pkgs[@]}; do
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

function check_and_upgrade() {
  if [ $PHOTON_VERSION == $LATEST_VERSION ]; then
    echo "Your current version $PHOTON_VERSION is the latest version. Nothing to do."
    exit
  fi
  check_deprecated
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
      make_var_run_a_symlink
      upgrade_photon_release_dev
      #upgrade_photon_release
      distro_upgrade
      rebuilddb
      ;;
    *) exit;;
  esac
}

check_and_upgrade
