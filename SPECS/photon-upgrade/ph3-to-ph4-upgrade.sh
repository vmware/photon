# set for Photon OS 4.0 upgrade
TO_VERSION='4.0'

read -d "\n" -a deprecated_packages_arr < "$PHOTON_UPGRADE_UTILS_DIR/ph3-to-ph4-deprecated-pkgs.txt"

# This hashtable maps package name changes
# we do not expect any core packages here
declare -A replaced_pkgs_map=(
  [autoconf213]=autoconf
  [gcc-10]=gcc
  [iptraf]=iptraf-ng
  [mozjs60]=mozjs
  [mozjs60-devel]=mozjs-devel
  [nxtgn-openssl]=openssl
  [nxtgn-openssl-c_rehash]=openssl-c_rehash
  [nxtgn-openssl-devel]=openssl-devel
  [nxtgn-openssl-perl]=openssl-perl
  [openjdk8]="openjdk17 openjdk11 openjdk8"
  [openjdk8-doc]="openjdk17-doc openjdk11-doc openjdk8-doc"
  [openjdk8-src]="openjdk17-src openjdk11-src openjdk8-src"
  [openjdk10]="openjdk17 openjdk11"
  [openjdk10-doc]="openjdk17-doc openjdk11-doc"
  [openjdk10-src]="openjdk17-src openjdk11-src"
  [openjdk11]="openjdk17 openjdk11"
  [openjdk11-doc]="openjdk17-doc openjdk11-doc"
  [openjdk11-src]="openjdk17-src openjdk11-src"
  [openjre8]="openjdk17-jre openjdk11-jre openjre8"
  [openjre10]="openjdk17-jre openjdk11-jre"
  [postgresql]="postgresql14 postgresql13 postgresql10"
  [postgresql-libs]="postgresql14-libs postgresql13-libs postgresql10-libs"
  [postgresql-devel]="postgresql14-devel postgresql13-devel postgresql10-devel"
  [postgresql13]="postgresql14 postgresql13 postgresql10"
  [postgresql13-libs]="postgresql14-libs postgresql13-libs postgresql10-libs"
  [postgresql13-devel]="postgresql14-devel postgresql13-devel postgresql10-devel"
  [pgaudit13]="pgaudit14 pgaudit13"
  [repmgr]="repmgr14 repmgr13 repmgr10"
  [repmgr13]="repmgr14 repmgr13 repmgr10"
)

# Residual pkgs to remove post upgrade
declare -a residual_pkgs_arr=(
  libmetalink libdb
)

# Hash keys are paths in source OS mapping to paths (as values) in target OS
declare -A conf_path_map=()

# Take care of post upgrade config changes
function fix_post_upgrade_config() {
  local python_link=/usr/bin/python

  # fix pam
  echo "Fixing PAM config post upgrade for pam_faillock.so and pam_pwquality.so."
  ${SED} -i -E 's/^(\s*\w+\s+\w+\s+)pam_tally2?\.so.*$/\1pam_faillock.so/' /etc/pam.d/*
  ${SED} -i -E 's/pam_cracklib.so/pam_pwquality.so/' /etc/pam.d/*
  echo "Setting $python_link."
  test -e $python_link || $LN -s python3 $python_link
}
