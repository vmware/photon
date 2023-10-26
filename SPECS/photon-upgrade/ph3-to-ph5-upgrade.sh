# set for Photon OS 5.0 upgrade
TO_VERSION='5.0'

declare -a deprecated_packages_arr=(
  asciidoc bzr c-rest-engine c-rest-engine-devel
  ca-certificates-nxtgn-openssl ca-certificates-nxtgn-openssl-pki
  cgroup-utils compat-gdbm debugmode dejavu-fonts ebtables-nft elasticsearch fcgi
  fcgi-devel fipsify glog-docs gmock-static gtest-static hawkey js json_spirit
  json_spirit-devel kaigen-gothic-cjk kibana kube-controllers libdb-docs libgsystem libnss-ato
  lightstep-tracer-cpp lightwave lightwave-client lightwave-client-libs
  lightwave-devel lightwave-post lightwave-samples lightwave-server
  likewise-open likewise-open-devel linux-aws linux-aws-docs
  linux-drivers-intel-sgx linux-esx-hmacgen linux-hmacgen linux-oprofile
  linux-rt-drivers-intel-i40e-2.15.9 linux-rt-drivers-intel-i40e-2.16.11
  linux-rt-drivers-intel-i40e-2.22.18 linux-rt-drivers-intel-iavf-4.2.7
  linux-rt-drivers-intel-iavf-4.4.2 linux-rt-drivers-intel-iavf-4.5.3
  linux-rt-drivers-intel-iavf-4.8.2 linux-rt-drivers-intel-ice-1.11.14
  linux-rt-drivers-intel-ice-1.6.4 linux-rt-drivers-intel-ice-1.8.3
  linux-rt-drivers-intel-ice-1.9.11 linux-secure-hmacgen linux-secure-lkcm
  liota logstash mozjs60 ndsend netmgmt nxtgn-openssl openjdk8
  openjre8 ovn-central ovn-common ovn-controller-vtep ovn-doc ovn-docker
  ovn-host photon-checksum-generator pmd pmd-cli pmd-devel pmd-libs
  pmd-python3 pygobject-devel python-certifi python-lockfile
  python-vcversioner python2 python2-libs python3-backports_abc python3-cgroup-utils
  python3-future python3-lvm2-libs python3-macholib python3-PyPAM
  python3-setproctitle  python3-stevedore python3-terminaltables
  rubygem-connection_pool rubygem-net-http-persistent rubygem-zeitwerk salt3
  sqlite2 sshfs tiptop ulogd uriparser urw-fonts xtrans-devel
  yarn zsh-html
  # recently deprecated packages
  libcalico libsoup-doc python3-m2r
)

# This hashtable maps package name changes
# we do not expect any core packages here
declare -A replaced_pkgs_map=(
  [ansible]=ansible   # Added for workaround pertaining to python3-pycrypto
  [ansible-posix]=ansible-posix   # This & next 2 lines handle ansible removal
  [ansible-community-general]=ansible-community-general  # handle ansible removal
  [stig-hardening]=stig-hardening                        # handle ansible removal
  [apache-tomcat]=apache-tomcat10
  [gcc-10]=gcc
  [iptraf]=iptraf-ng
  [openjdk8]=openjdk11
  [openjdk8-doc]=openjdk11-doc
  [openjdk8-src]=openjdk11-src
  [openjre8]=openjdk11
  [openjdk10]=openjdk11
  [openjdk10-doc]=openjdk11-doc
  [openjdk10-src]=openjdk11-src
  [openjre10]=openjdk11
  [postgresql]=postgresql15
  [postgresql-libs]=postgresql15-libs
  [postgresql-devel]=postgresql15-devel
  [python3-gcovr]=gcovr
  [python3-google-compute-engine]=google-compute-engine
  [python3-pycrypto]=python3-pycryptodome
  [repmgr]=repmgr15
)

# Residual pkgs to remove post upgrade
declare -a residual_pkgs_arr=(
  libmetalink libdb libdb-docs
)

# Take care of post upgrade config changes
function fix_post_upgrade_config() {
  local python_link=/usr/bin/python
  local FSTAB=/etc/fstab

  # fix pam
  echo "Fixing PAM config post upgrade for pam_faillock.so and pam_pwquality.so."
  ${SED} -i -E 's/^(\s*\w+\s+\w+\s+)pam_tally2?\.so.*$/\1pam_faillock.so/' /etc/pam.d/*
  ${SED} -i -E 's/pam_cracklib.so/pam_pwquality.so/' /etc/pam.d/*
  # noacl option is no longer supported for ext4, hence remove them from fstab
  $SED -i -E 's/^(\S+\s+\S+\s+ext4\s+.*?),noacl,(.*)$/\1,\2/' $FSTAB
  $SED -i -E 's/^(\S+\s+\S+\s+ext4\s+)noacl,(.*)$/\1\2/' $FSTAB
  $SED -i -E 's/^(\S+\s+\S+\s+ext4\s+\S+),noacl(\s+.*)$/\1\2/' $FSTAB
  echo "Setting $python_link."
  test -e $python_link || $LN -s python3 $python_link
}

# rpm in Photon OS 5.0 uses different location for rpmdb by default
# hence, relocate rpmdb before upgrading rpm package
function relocate_rpmdb() {
  local nold=$(${RPM} -qa | ${WC} -l)
  local nnew=0
  local rc=0

  mkdir -p $NEW_RPMDB_LOC
  if [ -d "$NEW_RPMDB_LOC/rpm" ]; then
    ${RM} -rf "$NEW_RPMDB_LOC/rpm"
  fi

  if ! ${CP} -pr "$RPM_DB_LOC" "$NEW_RPMDB_LOC"; then
    rc=$?
    abort $rc "Error copying rpmdb to new location."
  fi

  rebuilddb
  nnew=$(${RPM} -qa | ${WC} -l)
  if [ $nnew -ge $nold ]; then
    # RPMDB relocated successfully thus cleanup the old location
    ${RM} -rf "$RPM_DB_LOC"
    echo "rpmdb relocation succeeded."
  else
    rc=$?
    abort $rc "Error: Relocated rpmdb is corrupt ($nnew RPMs found < expected $nold RPMs)"
  fi
}

# Usage: backup_configs backup_root_path pkg1 pkg2 ...
# backs up the config of apache-tomcat, if it is being upgraded to apache-tomcat9
# Post upgrade this configuration will be restored in restore_configs()
function backup_configs() {
  local backup_root_path=$1
  shift
  local srcpath='/var/opt/apache-tomcat/conf'
  local target_path="$backup_root_path/$srcpath"
  local pkg
  for pkg in $*; do
    if [ "$pkg" = "apache-tomcat" ]; then
      if [ -e "$srcpath" ]; then
        echo "Backing up $pkg config to be restored after upgrade."
        mkdir -p "$target_path"
        ${CP} -ra $srcpath/* $target_path
      fi
    fi
  done
}

# Usage: restore_configs backup_root_path pkg1 pkg2 ...
# Restores the config of apache-tomcat to apache-tomcat9 in 5.0
function restore_configs() {
  local backup_root_path=$1
  shift
  local srcpath="$backup_root_path/var/opt/apache-tomcat/conf"
  local target_path="/var/opt/apache-tomcat9/conf"
  local pkg
  for pkg in $*; do
    if [ "$pkg" = "apache-tomcat9" ]; then
      if [ -e "$srcpath" ]; then
        echo "Restoring config for $pkg."
        ${RPM} -q --quiet $pkg && ${CP} -ra $srcpath/* $target_path
      fi
    fi
  done
}
