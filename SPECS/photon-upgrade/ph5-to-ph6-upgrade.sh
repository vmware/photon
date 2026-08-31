read -d "\n" -a deprecated_packages_arr < "$1/ph5-deprecated-pkgs.txt"

# This hashtable maps package name changes between source and target Photon OS
# Examples:
#   [p1]=p2
#   [p3]="p4 p5"     where p3 is replaced by either p4 or p5
# we do not expect any core packages here
declare -A replaced_pkgs_map=(
  # Replaced and Replacing Package names map will be populated on next
  [apache-tomcat9]="apache-tomcat9 apache-tomcat11 apache-tomcat10"
  [apache-tomcat9-webapps]="apache-tomcat9-webapps apache-tomcat11-webapps apache-tomcat10-webapps"

  [apache-tomcat10]="apache-tomcat10 apache-tomcat11"
  [apache-tomcat10-webapps]="apache-tomcat10-webapps apache-tomcat11-webapps"

  [dhcp]="dhcpcd"
  [dhcp-libs]="dhcpcd"
  [dhcp-client]="dhcpcd"
  [dhcp-server]="kea"

  [fakeroot-ng]="fakeroot"

  [openjdk11]="openjdk11 openjdk25 openjdk21 openjdk17"
  [openjdk11-doc]="openjdk11-doc openjdk25-doc openjdk21-doc openjdk17-doc"
  [openjdk11-jre]="openjdk11-jre openjdk25-jre openjdk21-jre openjdk17-jre"
  [openjdk11-src]="openjdk11-src openjdk25-src openjdk21-src openjdk17-src"

  [openjdk17]="openjdk17 openjdk25 openjdk21"
  [openjdk17-doc]="openjdk17-doc openjdk25-doc openjdk21-doc"
  [openjdk17-jre]="openjdk17-jre openjdk25-jre openjdk21-jre"
  [openjdk17-src]="openjdk17-src openjdk25-src openjdk21-src"

  [openjdk21]="openjdk21 openjdk25"
  [openjdk21-doc]="openjdk21-doc openjdk25-doc"
  [openjdk21-jre]="openjdk21-jre openjdk25-jre"
  [openjdk21-src]="openjdk21-src openjdk25-src"

  [pgaudit13]="pgaudit18 pgaudit17 pgaudit16 pgaudit15"
  [pgaudit14]="pgaudit18 pgaudit17 pgaudit16 pgaudit15"
  [pgaudit15]="pgaudit15 pgaudit18 pgaudit17 pgaudit16"
  [pgaudit16]="pgaudit16 pgaudit18 pgaudit17"
  [pgaudit17]="pgaudit17 pgaudit18"

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

  [postgresql16]="postgresql16 postgresql18 postgresql17"
  [postgresql16-client]="postgresql16-client postgresql18-client postgresql17-client"
  [postgresql16-devel]="postgresql16-devel postgresql18-devel postgresql17-devel"
  [postgresql16-libs]="postgresql16-libs postgresql18-libs postgresql17-libs"
  [postgresql16-server]="postgresql16-server postgresql18-server postgresql17-server"

  [postgresql17]="postgresql17 postgresql18"
  [postgresql17-client]="postgresql17-client postgresql18-client"
  [postgresql17-devel]="postgresql17-devel postgresql18-devel"
  [postgresql17-libs]="postgresql17-libs postgresql18-libs"
  [postgresql17-server]="postgresql17-server postgresql18-server"

  [procmail]="dovecot"

  [repmgr]="repmgr18 repmgr17 repmgr16 repmgr15"
  [repmgr10]="repmgr18 repmgr17 repmgr16 repmgr15"
  [repmgr13]="repmgr18 repmgr17 repmgr16 repmgr15"
  [repmgr14]="repmgr18 repmgr17 repmgr16 repmgr15"
  [repmgr15]="repmgr15 repmgr18 repmgr17 repmgr16"
  [repmgr16]="repmgr16 repmgr18 repmgr17"
  [repmgr17]="repmgr17 repmgr18"
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
