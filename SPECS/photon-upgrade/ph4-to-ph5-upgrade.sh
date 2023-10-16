read -d "\n" -a deprecated_packages_arr < "$1/ph4-to-ph5-deprecated-pkgs.txt"

# This hashtable maps package name changes
declare -A replaced_pkgs_map=(
  [ansible]=ansible               # This & next 4 lines handle ansible removal
  [ansible-community-general]=ansible-community-general
  [ansible-devel]=ansible-devel
  [ansible-posix]=ansible-posix
  [stig-hardening]=stig-hardening
  [postgresql]=postgresql14
  [postgresql-libs]=postgresql14-libs
  [postgresql-devel]=postgresql14-devel
  [postgresql10]=postgresql15
  [postgresql10-libs]=postgresql15-libs
  [postgresql10-devel]=postgresql15-devel
  [repmgr]=repmgr14
  [repmgr10]=repmgr15
  [apache-tomcat]=apache-tomcat10
)

# Hash keys are paths in source OS mapping to paths as values in target OS
declare -A conf_path_map=(
  # config of apache-tomcat in 4.0 will be restored for apache-tomcat-9 in 5.0
  [/var/opt/apache-tomcat/conf]=/var/opt/apache-tomcat9/conf
)

# Residual pkgs to remove post upgrade
declare -a residual_pkgs_arr=(
  libdb libmetalink nasm-rdoff zsh-html
)

function relocate_rpmdb() {
  local nold=$(${RPM} -qa | ${WC} -l)
  local nnew=0
  local rc=0

  mkdir -p $NEW_RPMDB_PATH
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
