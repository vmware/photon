read -d "\n" -a deprecated_packages_arr < "$1/ph5-to-ph6-deprecated-pkgs.txt"

# This hashtable maps package name changes between source and target Photon OS
# Examples:
#   [p1]=p2
#   [p3]="p4 p5"     where p3 is replaced by either p4 or p5
# we do not expect any core packages here
declare -A replaced_pkgs_map=(
  # Replaced and Replacing Package names map will be populated on next
  # Photon OS release
  [fakeroot-ng]="fakeroot"
  [gcovr]="gcovr python3-gcovr"
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
