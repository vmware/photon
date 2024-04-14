read -d "\n" -a deprecated_packages_arr < "$1/ph4-to-ph5-deprecated-pkgs.txt"

# This hashtable maps package name changes between source and target Photon OS
# Examples:
#   [p1]=p2
#   [p3]="p4 p5"     where p3 is replaced by either p4 or p5
# we do not expect any core packages here
declare -A replaced_pkgs_map=(
  [apache-tomcat]="apache-tomcat10 apache-tomcat9"
  [apache-tomcat-webapps]="apache-tomcat10-webapps apache-tomcat9-webapps"
  [apache-tomcat9]="apache-tomcat9 apache-tomcat10"
  [apache-tomcat9-webapps]="apache-tomcat9-webapps apache-tomcat10-webapps"
  [netmgmt]=network-config-manager
  [openjdk8]="openjdk17 openjdk11"
  [openjdk8-doc]="openjdk17-doc openjdk11-doc"
  [openjdk8-src]="openjdk17-src openjdk11-src"
  [openjdk11]=" openjdk11 openjdk17"
  [openjdk11-doc]="openjdk11-doc openjdk17-doc"
  [openjdk11-src]="openjdk11-src openjdk17-src"
  [openjre8]="openjdk17-jre openjdk11-jre openjdk17 openjdk11"
  [openjdk11-jre]="openjdk17-jre openjdk11-jre openjdk17 openjdk11"
  [pgaudit13]="pgaudit13 pgaudit15 pgaudit14"
  [pgaudit14]="pgaudit14 pgaudit15"
  [pmd]=pmd-ng
  [postgresql10]="postgresql15 postgresql14 postgresql13"
  [postgresql10-libs]="postgresql15-libs postgresql14-libs postgresql13-libs"
  [postgresql10-devel]="postgresql15-devel postgresql14-devel postgresql13-devel"
  [postgresql13]="postgresql13 postgresql15 postgresql14"
  [postgresql13-libs]="postgresql13-libs postgresql15-libs postgresql14-libs"
  [postgresql13-devel]="postgresql13-devel postgresql15-devel postgresql14-devel"
  [postgresql14]="postgresql14 postgresql15"
  [postgresql14-libs]="postgresql14-libs postgresql15-libs"
  [postgresql14-devel]="postgresql14-devel postgresql15-devel"
  [repmgr]="repmgr15 repmgr14 repmgr13"
  [repmgr10]="repmgr15 repmgr14 repmgr13"
  [repmgr13]="repmgr13 repmgr15 repmgr14"
  [repmgr14]="repmgr14 repmgr15"
)

# Hash keys are paths in source OS mapping to paths as values in target OS
declare -A conf_path_map=(
  # config of apache-tomcat in 4.0 will be restored for apache-tomcat-9 in 5.0
  [/var/opt/apache-tomcat/conf]=/var/opt/apache-tomcat9/conf
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
  $SED -i -E 's/^(\S+\s+\S+\s+ext4\s+.*?),noacl,(.*)$/\1,\2/' $FSTAB
  $SED -i -E 's/^(\S+\s+\S+\s+ext4\s+)noacl,(.*)$/\1\2/' $FSTAB
  $SED -i -E 's/^(\S+\s+\S+\s+ext4\s+\S+),noacl(\s+.*)$/\1\2/' $FSTAB
  return
}
