#!/bin/bash

set -ex

echoerr()
{
  echo -e "$*" 1>&2
}

echo PHOTON_RELEASE_VERSION=$PHOTON_RELEASE_VERSION
arch="$(uname -m)"
SYSROOT=/sysroot
ROOTFS_TAR_FILENAME="$(pwd)/stage/photon-rootfs-$PHOTON_RELEASE_VERSION-$PHOTON_BUILD_NUMBER.${arch}.tar.gz"

mkdir -p $SYSROOT
rm -rf /etc/yum.repos.d/*

cat > /etc/yum.repos.d/photon-local.repo <<- EOF
[photon-local]
name=VMware Photon Linux ${PHOTON_RELEASE_VERSION}($arch)
baseurl=file://$(pwd)/stage/RPMS
gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY
gpgcheck=0
enabled=1
skip_if_unavailable=True
EOF

tdnf install -y rpm tar gzip grep coreutils

rpm --root $SYSROOT/ --initdb

tdnf --releasever ${PHOTON_RELEASE_VERSION} \
     --installroot $SYSROOT/ \
     --rpmverbosity error \
     install -y \
     filesystem bash toybox tdnf photon-release photon-repos curl

actual_pkg_list=($(tdnf --installroot $SYSROOT/ \
                        --disablerepo=* -q \
                        list installed 2>/dev/null | cut -d'.' -f1))

expected_pkg_list=(
  bash bzip2-libs ca-certificates ca-certificates-pki curl curl-libs
  e2fsprogs-libs elfutils-libelf expat-libs filesystem glibc glibc-libs
  krb5 libcap libgcc libsolv libssh2 lua-libs ncurses-libs nspr nss-libs
  openssl-libs photon-release photon-repos popt readline rpm-libs
  sqlite-libs tdnf tdnf-cli-libs toybox xz-libs zlib zstd-libs
)

actual_pkg_count=${#actual_pkg_list[@]}
expected_pkg_count=${#expected_pkg_list[@]}

pkg_diff="$(echo ${expected_pkg_list[@]} ${actual_pkg_list[@]} | \
            tr ' ' '\n' | sort | uniq -u)"

if [ $expected_pkg_count -ne $actual_pkg_count ] || [ -n "${pkg_diff}" ]; then
  echoerr "Following package difference found in docker image:\n${pkg_diff}"
  echoerr "Expected package count: $expected_pkg_count"
  echoerr "Actual package count: $actual_pkg_count"
  exit 1
fi

rpm --root $SYSROOT/ --import $SYSROOT/etc/pki/rpm-gpg/*

# cleanup anything not needed inside rootfs
pushd $SYSROOT
rm -rf usr/src/ home/* var/log/* var/cache/tdnf/
# set TERM to linux due to stripped terminfo
echo "export TERM=linux" >> etc/bash.bashrc

popd

tar -I 'gzip -9' -C $SYSROOT -cpf $ROOTFS_TAR_FILENAME .

# expected size plus 2% wiggle room
max_size=17313736

actual_size=$(wc -c $ROOTFS_TAR_FILENAME | cut -d' ' -f1)
if (( $actual_size > $max_size )); then
  echoerr "ERROR: docker image tarball size is bigger than expected"
  echoerr "Expected size(in bytes): $max_size"
  echoerr "Actual size(in bytes): $actual_size"
  rm -f $ROOTFS_TAR_FILENAME
  exit 1
fi
