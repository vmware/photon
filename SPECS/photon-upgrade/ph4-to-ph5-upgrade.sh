read -d "\n" -a deprecated_packages_arr < "$1/ph4-to-ph5-deprecated-pkgs.txt"

# This hashtable maps package name changes between source and target Photon OS
# Examples:
#   [p1]=p2
#   [p3]="p4 p5"     where p3 is replaced by either p4 or p5
# we do not expect any core packages here
declare -A replaced_pkgs_map=(
  [apache-tomcat]="apache-tomcat11 apache-tomcat10 apache-tomcat9"
  [apache-tomcat-webapps]="apache-tomcat11-webapps apache-tomcat10-webapps apache-tomcat9-webapps"

  [apache-tomcat9]="apache-tomcat9 apache-tomcat11 apache-tomcat10"
  [apache-tomcat9-webapps]="apache-tomcat9-webapps apache-tomcat11-webapps apache-tomcat10-webapps"

  [calico-confd]="calico-confd confd"

  [chkconfig]="alternatives"

  [dstat]="dstat dool"

  [fakeroot-ng]="fakeroot"

  [gcc-12]="gcc"

  [gcovr]="gcovr python3-gcovr"

  [google-compute-engine]="google-compute-engine google-guest-configs"
  [google-compute-engine-services]="google-compute-engine-services google-guest-configs"

  [netmgmt]=network-config-manager
  [netmgmt-devel]="network-config-manager-devel"

  [openjdk8]="openjdk25 openjdk21 openjdk17 openjdk11"
  [openjre8]="openjdk25-jre openjdk21-jre openjdk17-jre openjdk11-jre"
  [openjdk8-doc]="openjdk25-doc openjdk21-doc openjdk17-doc openjdk11-doc"
  [openjdk8-src]="openjdk25-src openjdk21-src openjdk17-src openjdk11-src"

  [pmd]=pmd-ng
  [pmd-cli]="pmd-ng"
  [pmd-libs]=pmd-ng
  [pmd-gssapi-unix]="pmd-ng"

  [procmail]="dovecot"

  [pgaudit13]="pgaudit18 pgaudit17 pgaudit16 pgaudit15"
  [pgaudit14]="pgaudit18 pgaudit17 pgaudit16 pgaudit15"
  [pgaudit15]="pgaudit15 pgaudit18 pgaudit17 pgaudit16"

  [postgresql10]="postgresql18 postgresql17 postgresql16 postgresql15"
  [postgresql10-devel]="postgresql18-devel postgresql17-devel postgresql16-devel postgresql15-devel"
  [postgresql10-libs]="postgresql18-libs postgresql17-libs postgresql16-libs postgresql15-libs"

  [postgresql13]="postgresql18 postgresql17 postgresql16 postgresql15"
  [postgresql13-client]="postgresql18-client postgresql17-client postgresql16-client postgresql15-client"
  [postgresql13-devel]="postgresql18-devel postgresql17-devel postgresql16-devel postgresql15-devel"
  [postgresql13-libs]="postgresql18-libs postgresql17-libs postgresql16-libs postgresql15-libs"
  [postgresql13-server]="postgresql18-server postgresql17-server postgresql16-server postgresql15-server"

  [postgresql14]="postgresql18 postgresql17 postgresql16 postgresql15"
  [postgresql14-client]="postgresql18-client postgresql17-client postgresql16-client postgresql15-client"
  [postgresql14-devel]="postgresql18-devel postgresql17-devel postgresql16-devel postgresql15-devel"
  [postgresql14-libs]="postgresql18-libs postgresql17-libs postgresql16-libs postgresql15-libs"
  [postgresql14-server]="postgresql18-server postgresql17-server postgresql16-server postgresql15-server"

  [postgresql15]="postgresql15 postgresql18 postgresql17 postgresql16"
  [postgresql15-client]="postgresql15-client postgresql18-client postgresql17-client postgresql16-client"
  [postgresql15-devel]="postgresql15-devel postgresql18-devel postgresql17-devel postgresql16-devel"
  [postgresql15-libs]="postgresql15-libs postgresql18-libs postgresql17-libs postgresql16-libs"
  [postgresql15-server]="postgresql15-server postgresql18-server postgresql17-server postgresql16-server"

  [python3-gcovr]="gcovr python3-gcovr"

  [repmgr]="repmgr18 repmgr17 repmgr16 repmgr15"
  [repmgr10]="repmgr18 repmgr17 repmgr16 repmgr15"
  [repmgr13]="repmgr18 repmgr17 repmgr16 repmgr15"
  [repmgr14]="repmgr18 repmgr17 repmgr16 repmgr15"
  [repmgr15]="repmgr15 repmgr18 repmgr17 repmgr16"

  [rubygem-mini_portile]="rubygem-mini_portile2"
)

# Hash keys are paths in source OS mapping to paths as values in target OS
declare -A conf_path_map=(
  # config of apache-tomcat in 4.0 will be restored for apache-tomcat-9 in 5.0
  [/var/opt/apache-tomcat/conf]="/var/opt/apache-tomcat10/conf /var/opt/apache-tomcat9/conf"
  [/var/opt/apache-tomcat9/conf]="/var/opt/apache-tomcat9/conf /var/opt/apache-tomcat10/conf"
)

# Residual pkgs to remove post upgrade
declare -a residual_pkgs_arr=(
  libdb libmetalink
)

function relocate_rpmdb() {
  local nold=$(${RPM} -qa | ${WC} -l)
  local nnew=0
  local rc=0

  ${MKDIR} -p $NEW_RPMDB_PATH
  if [ -d "$NEW_RPMDB_PATH/rpm" ]; then
    ${RM} -rf "$NEW_RPMDB_PATH/rpm"
  fi

  if ! ${CP} -pr "$OLD_RPMDB_PATH" "$NEW_RPMDB_PATH"; then
    rc=$?
    abort $rc "Error copying rpmdb to new location."
  fi

  rebuilddb
  nnew=$(${RPM} -qa | ${WC} -l)
  if [ $nnew -ge $nold ]; then
    # RPMDB relocated successfully thus cleanup the old location
    ${RM} -rf "$OLD_RPMDB_PATH"
    echo "rpmdb relocation succeeded."
  else
    rc=$?
    abort $rc "Error: Relocated rpmdb is corrupt ($nnew RPMs found < expected $nold RPMs)"
  fi
}

# Take care of post upgrade config changes
function fix_post_upgrade_config() {
  local FSTAB=/etc/fstab
  # noacl option is no longer supported for ext4, hence remove them from fstab
  $SED -i -E 's/^(\S+\s+\S+\s+ext[2-4]\s+.*?),noacl,(.*)$/\1,\2/' $FSTAB
  $SED -i -E 's/^(\S+\s+\S+\s+ext[2-4]\s+)noacl,(.*)$/\1\2/' $FSTAB
  $SED -i -E 's/^(\S+\s+\S+\s+ext[2-4]\s+\S+),noacl(\s+.*)$/\1\2/' $FSTAB
  return
}
