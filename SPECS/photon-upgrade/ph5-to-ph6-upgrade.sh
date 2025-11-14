read -d "\n" -a deprecated_packages_arr < "$1/ph5-to-ph6-deprecated-pkgs.txt"

# This hashtable maps package name changes between source and target Photon OS
# Examples:
#   [p1]=p2
#   [p3]="p4 p5"     where p3 is replaced by either p4 or p5
# we do not expect any core packages here
declare -A replaced_pkgs_map=(
  # Replaced and Replacing Package names map will be populated on next
  # Photon OS release
  [apache-tomcat]="apache-tomcat10 apache-tomcat9"
  [apache-tomcat-webapps]="apache-tomcat10-webapps apache-tomcat9-webapps"
  [fakeroot-ng]="fakeroot"
  [gcovr]="gcovr python3-gcovr"
  [openjdk11]="openjdk11 openjdk21 openjdk17"
  [openjdk11-doc]="openjdk11-doc openjdk21-doc openjdk17-doc"
  [openjdk11-jre]="openjdk11-jre openjdk21-jre openjdk17-jre"
  [openjdk11-src]="openjdk11-src openjdk21-src openjdk17-src"
  [openjdk17]="openjdk17 openjdk21"
  [openjdk17-doc]="openjdk17-doc openjdk21-doc"
  [openjdk17-jre]="openjdk17-jre openjdk21-jre"
  [openjdk17-src]="openjdk17-src openjdk21-src"
  [pgaudit13]="pgaudit13 pgaudit17 pgaudit16 pgaudit15 pgaudit14"
  [pgaudit14]="pgaudit14 pgaudit17 pgaudit16 pgaudit15"
  [pgaudit15]="pgaudit15 pgaudit17 pgaudit16"
  [pgaudit16]="pgaudit16 pgaudit17"
  [postgresql10]="postgresql17 postgresql16 postgresql15 postgresql14 postgresql13"
  [postgresql10-devel]="postgresql17-devel postgresql16-devel postgresql15-devel postgresql14-devel postgresql13-devel"
  [postgresql10-libs]="postgresql17-libs postgresql16-libs postgresql15-libs postgresql14-libs postgresql13-libs"
  [postgresql13]="postgresql13 postgresql17 postgresql16 postgresql15 postgresql14"
  [postgresql13-client]="postgresql13-client postgresql17-client postgresql16-client postgresql15-client postgresql14-client"
  [postgresql13-devel]="postgresql13-devel postgresql17-devel postgresql16-devel postgresql15-devel postgresql14-devel"
  [postgresql13-libs]="postgresql13-libs postgresql17-libs postgresql16-libs postgresql15-libs postgresql14-libs"
  [postgresql13-server]="postgresql13-server postgresql17-server postgresql16-server postgresql15-server postgresql14-server"
  [postgresql14]="postgresql14 postgresql17 postgresql16 postgresql15"
  [postgresql14-client]="postgresql14-client postgresql17-client postgresql16-client postgresql15-client"
  [postgresql14-devel]="postgresql14-devel postgresql17-devel postgresql16-devel postgresql15-devel"
  [postgresql14-libs]="postgresql14-libs postgresql17-libs postgresql16-libs postgresql15-libs"
  [postgresql14-server]="postgresql14-server postgresql17-server postgresql16-server postgresql15-server"
  [postgresql15]="postgresql15 postgresql17 postgresql16"
  [postgresql15-client]="postgresql15-client postgresql17-client postgresql16-client"
  [postgresql15-devel]="postgresql15-devel postgresql17-devel postgresql16-devel"
  [postgresql15-libs]="postgresql15-libs postgresql17-libs postgresql16-libs"
  [postgresql15-server]="postgresql15-server postgresql17-server postgresql16-server"
  [postgresql16]="postgresql16 postgresql17"
  [postgresql16-client]="postgresql16-client postgresql17-client"
  [postgresql16-devel]="postgresql16-devel postgresql17-devel"
  [postgresql16-libs]="postgresql16-libs postgresql17-libs"
  [postgresql16-server]="postgresql16-server postgresql17-server"
  [repmgr]="repmgr17 repmgr16 repmgr15 repmgr14 repmgr13"
  [repmgr10]="repmgr17 repmgr16 repmgr15 repmgr14 repmgr13"
  [repmgr13]="repmgr13 repmgr17 repmgr16 repmgr15 repmgr14"
  [repmgr14]="repmgr14 repmgr17 repmgr16 repmgr15"
  [repmgr15]="repmgr15 repmgr17 repmgr16"
  [repmgr16]="repmgr16 repmgr17"
)

# Hash keys are paths in source OS mapping to paths as values in target OS
declare -A conf_path_map=(
   [/var/opt/apache-tomcat/conf]="/var/opt/apache-tomcat10/conf /var/opt/apache-tomcat9/conf"
)

# Residual pkgs to remove post upgrade
declare -a residual_pkgs_arr=(
)

# Take care of pre upgrade config changes
function fix_pre_upgrade_config() {
  return 0
}

# Take care of post upgrade config changes
function fix_post_upgrade_config() {
  return 0
}
