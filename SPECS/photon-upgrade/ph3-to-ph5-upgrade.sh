# set for Photon OS 5.0 upgrade
TO_VERSION='5.0'

read -d "\n" -a deprecated_packages_arr < "$PHOTON_UPGRADE_UTILS_DIR/ph3-to-ph5-deprecated-pkgs.txt"

# This hashtable maps package name changes between source and target Photon OS
# Examples:
#   [p1]=p2
#   [p3]="p4 p5"     where p3 is replaced by either p4 or p5
# we do not expect any core packages here
declare -A replaced_pkgs_map=(
  [apache-tomcat]="apache-tomcat10 apache-tomcat9"
  [autoconf213]=autoconf
  [gcc-10]=gcc
  [iptraf]=iptraf-ng
  [mozjs60]=mozjs
  [mozjs60-devel]=mozjs-devel
  [netmgmt]=network-config-manager
  [nxtgn-openssl]=openssl
  [nxtgn-openssl-c_rehash]=openssl-c_rehash
  [nxtgn-openssl-devel]=openssl-devel
  [nxtgn-openssl-perl]=openssl-perl
  [openjdk8]="openjdk17 openjdk11"
  [openjdk8-doc]="openjdk17-doc openjdk11-doc"
  [openjdk8-src]="openjdk17-src openjdk11-src"
  [openjre8]="openjdk17 openjdk11"
  [openjdk10]="openjdk17 openjdk11"
  [openjdk10-doc]="openjdk17-doc openjdk11-doc"
  [openjdk10-src]="openjdk17-src openjdk11-src"
  [openjre10]="openjdk17 openjdk11"
  [pmd]=pmd-ng
  [postgresql]="postgresql15 postgresql14 postgresql13"
  [postgresql-libs]="postgresql15-libs postgresql14-libs postgresql13-libs"
  [postgresql-devel]="postgresql15-devel postgresql14-devel postgresql13-devel"
  [postgresql13]="postgresql15 postgresql14 postgresql13"
  [postgresql13-libs]="postgresql15-libs postgresql14-libs postgresql13-libs"
  [postgresql13-devel]="postgresql15-devel postgresql14-devel postgresql13-devel"
  [pgaudit13]="pgaudit15 pgaudit14 pgaudit13"
  [python3-pycrypto]=python3-pycryptodome
  [repmgr]="repmgr15 repmgr14 repmgr13"
  [repmgr13]="repmgr15 repmgr14 repmgr13"
)

# Residual pkgs to remove post upgrade
declare -a residual_pkgs_arr=(
  libmetalink libdb
)

# Hash keys are paths in source OS mapping to paths (as values) in target OS
declare -A conf_path_map=(
  # config of apache-tomcat in 3.0 will be restored for apache-tomcat-9 in 5.0
  [/var/opt/apache-tomcat/conf]=/var/opt/apache-tomcat9/conf
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
