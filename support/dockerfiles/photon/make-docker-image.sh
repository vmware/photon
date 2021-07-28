#!/bin/bash

set -ex

echoerr()
{
  echo -e "$*" 1>&2
}

echo PHOTON_RELEASE_VERSION=$PHOTON_RELEASE_VERSION
arch="$(uname -m)"
TEMP_CHROOT=$(pwd)/temp_chroot
ROOTFS_TAR_FILENAME=photon-rootfs-$PHOTON_RELEASE_VERSION-$PHOTON_BUILD_NUMBER.tar.gz
STAGE_DIR=$(pwd)/stage

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

rm -rf $TEMP_CHROOT
mkdir $TEMP_CHROOT

tdnf install -y rpm tar gzip grep coreutils

rpm --root $TEMP_CHROOT/ --initdb

tdnf --releasever ${PHOTON_RELEASE_VERSION} \
     --installroot $TEMP_CHROOT/ \
     --rpmverbosity error \
     install -y \
     filesystem bash toybox tdnf photon-release photon-repos curl

actual_pkg_list=($(tdnf --installroot $TEMP_CHROOT/ \
                        --disablerepo=* -q \
                        list installed 2>/dev/null | cut -d' ' -f1))

expected_pkg_list=(
  bash.$arch bzip2-libs.$arch ca-certificates.$arch
  ca-certificates-pki.$arch curl.$arch curl-libs.$arch
  e2fsprogs-libs.$arch elfutils-libelf.$arch expat.$arch
  expat-libs.$arch filesystem.$arch glibc.$arch krb5.$arch
  libcap.$arch libdb.$arch libgcc.$arch libgcrypt.$arch
  libgpg-error.$arch libmetalink.$arch libsolv.$arch libssh2.$arch
  lua.$arch ncurses-libs.$arch nspr.$arch nss-libs.$arch
  openssl.$arch photon-release.noarch photon-repos.noarch popt.$arch
  readline.$arch rpm-libs.$arch sqlite-libs.$arch tdnf.$arch
  tdnf-cli-libs.$arch toybox.$arch xz-libs.$arch zlib.$arch
  zstd-libs.$arch
)

actual_pkg_count=${#actual_pkg_list[@]}
expected_pkg_count=${#expected_pkg_list[@]}

pkg_diff="$(echo ${expected_pkg_list[@]} ${actual_pkg_list[@]} | \
            tr ' ' '\n' | sort | uniq -u)"

if [ $expected_pkg_count -ne $actual_pkg_count ] || [ -n "${pkg_diff}" ]; then
  echoerr "Following package difference found in docker image:\n${pkg_diff}"
  echoerr "Expected package count: $expected_pkg_count"
  echoerr "Actual package count: $actual_pkg_count"
  rm -rf $TEMP_CHROOT
  exit 1
fi

rpm --root $TEMP_CHROOT/ --import $TEMP_CHROOT/etc/pki/rpm-gpg/*

# cleanup anything not needed inside rootfs
pushd $TEMP_CHROOT
rm -rf usr/src/
rm -rf home/*
# rm -rf var/lib/yum/*
rm -rf var/log/*
# set TERM to linux due to stripped terminfo
echo "export TERM=linux" >> etc/bash.bashrc

#find var/cache/tdnf/photon/rpms -type f -name "*.rpm" -exec rm {} \;
tar cpzf ../$ROOTFS_TAR_FILENAME .
popd

max_size=$(( 16 * 1024 * 1024 ))
actual_size=$(wc -c $ROOTFS_TAR_FILENAME | cut -d' ' -f1)
if (( $actual_size > $max_size )); then
  echoerr "ERROR: docker image tarball size is bigger than expected"
  echoerr "Expected size(in bytes): $max_size"
  echoerr "Actual size(in bytes): $actual_size"
  rm -rf $TEMP_CHROOT $ROOTFS_TAR_FILENAME
  exit 1
fi

mv $ROOTFS_TAR_FILENAME $STAGE_DIR/

# cleanup
rm -rf $TEMP_CHROOT
