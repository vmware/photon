declare -a deprecated_packages_arr=(
  c-rest-engine c-rest-engine-devel cgroup-utils dcerpc dcerpc-devel
  fcgi fcgi-devel glib-doc glib-networking-lang gmock-static gtest-static
  json_spirit json_spirit-devel libnss-ato lightstep-tracer-cpp lightwave
  lightwave-client lightwave-client-libs lightwave-devel lightwave-post
  lightwave-samples lightwave-server likewise-open likewise-open-devel linux-aws
  linux-aws-devel linux-aws-docs linux-aws-drivers-gpu linux-aws-oprofile
  linux-aws-sound linux-drivers-intel-sgx linux-oprofile ndsend netmgmt
  netmgmt-cli-devel netmgmt-devel openjdk8 openjdk8-doc openjdk8-sample
  openjdk8-src openjre8 openjre8 pmd pmd-cli pmd-devel pmd-gssapi-unix pmd-libs
  pmd-python3 python3-backports_abc python3-PyPAM- sqlite2 sqlite2-devel
  sshfs tiptop ulogd ulogd-mysql ulogd-pcap ulogd-sqlite
)

# This hashtable maps package name changes
declare -A replaced_pkgs_map=(
  [postgresql10]=postgresql15
  [postgresql10-libs]=postgresql15-libs
  [postgresql10-devel]=postgresql15-devel
)

# list of enabled services
declare -a enabled_services_arr=()

# list of disabled serfices
declare -a disabled_services_arr=()

declare -a deprecated_pkgs_to_remove_arr=()

function relocate_rpmdb() {
  local nold=$(${RPM} -qa | ${WC} -l)
  local nnew=0
  local rc=0

  mkdir -p $NEW_RPMDB_PATH
  if [ -d "$NEW_RPMDB_PATH/rpm" ]; then
    ${RM} -rf "$NEW_RPMDB_PATH/rpm"
  fi

  if ! ${CP} -pr "$OLD_RPM_DB_PATH" "$NEW_RPMDB_PATH"; then
    rc=$?
    abort $rc "Error copying rpmdb to new location."
  fi

  rebuilddb
  nnew=$(${RPM} -qa | ${WC} -l)
  if [ $nnew -ge $nold ]; then
    # RPMDB relocated successfully thus cleanup the old location
    ${RM}-rf "$OLD_RPM_DB_PATH"
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
