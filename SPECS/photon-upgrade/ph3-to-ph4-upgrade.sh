# set for Photon OS 4.0 upgrade
TO_VERSION='4.0'

declare -a deprecated_packages_arr=(
    apache-tomcat-webapps asciidoc
    #autoconf213
    bzr ca-certificates-nxtgn-openssl ca-certificates-nxtgn-openssl-pki
    compat-gdbm debugmode dejavu-fonts elasticsearch ebtables-nft fipsify
    glog-docs haproxy-dataplaneapi hawkey
    js kaigen-gothic-cjk kibana kube-controllers libgsystem linux-aws-hmacgen
    linux-esx-hmacgen linux-hmacgen linux-rt-drivers-intel-i40e-2.15.9
    linux-rt-drivers-intel-i40e-2.16.11 linux-rt-drivers-intel-i40e-2.22.18
    linux-rt-drivers-intel-iavf-4.2.7 linux-rt-drivers-intel-iavf-4.4.2
    linux-rt-drivers-intel-iavf-4.5.3 linux-rt-drivers-intel-iavf-4.8.2
    linux-rt-drivers-intel-ice-1.11.14 linux-rt-drivers-intel-ice-1.6.4
    linux-rt-drivers-intel-ice-1.8.3 linux-rt-drivers-intel-ice-1.9.11
    linux-secure-hmacgen linux-secure-lkcm liota
    logstash mozjs60 ntpsec nxtgn-openssl openjdk10 openjre10 photon-checksum-generator
    ovn-central ovn-common ovn-controller-vtep ovn-doc ovn-docker ovn-host
    python2 python2-libs pygobject-devel python3-cgroup-utils python3-future python3-gcovr
    python3-google-compute-engine python3-lvm2-libs python3-macholib python3-ntp
    python3-pefile python3-setproctitle python3-stevedore python3-terminaltables
    python-certifi python-lockfile python-vcversioner rubygem-connection_pool
    rubygem-net-http-persistent rubygem-zeitwerk xtrans-devel yarn zsh-html
)

# This hashtable maps package name changes
# we do not expect any core packages here
declare -A replaced_pkgs_map=(
  [ansible]=ansible   # Added for workaround pertaining to python3-pycrypto
  [ansible-posix]=ansible-posix   # This & next 2 lines handle ansible removal
  [ansible-community-general]=ansible-community-general  # handle ansible removal
  [stig-hardening]=stig-hardening                        # handle ansible removal
  [gcc-10]=gcc
  [iptraf]=iptraf-ng
  [python3-gcovr]=gcovr
  [python3-pycrypto]=python3-pycryptodome
  [openjdk10]=openjdk11
  [openjdk10-doc]=openjdk11-doc
  [openjdk10-src]=openjdk11-src
  [openjre10]=openjdk11
)

# Residual pkgs to remove post upgrade
declare -a residual_pkgs_arr=(
  libmetalink libdb libdb-docs
)

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

# backup_configs() is No-op function in 3.0 to 4.0 upgrade
function backup_configs() { :; }

# restore_configs() is No-op function in 3.0 to 4.0 upgrade
function restore_configs() { :; }
