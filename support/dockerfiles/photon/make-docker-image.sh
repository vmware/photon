#!/bin/bash

set -ex

echoerr()
{
	echo -e "$*" 1>&2
}

arch="$(uname -m)"
TEMP_CHROOT=$(pwd)/temp_chroot
ROOTFS_TAR_FILENAME=photon-rootfs-$PHOTON_RELEASE_VERSION-$PHOTON_BUILD_NUMBER.tar.bz2
STAGE_DIR=$(pwd)/stage

rm -rf /etc/yum.repos.d/*

cat > /etc/yum.repos.d/photon-local.repo <<- EOF

[photon-local]
name=VMware Photon Linux 1.0($arch)
baseurl=file://$(pwd)/stage/RPMS
gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY
gpgcheck=0
enabled=1
skip_if_unavailable=True

EOF

rm -rf $TEMP_CHROOT
mkdir $TEMP_CHROOT

tdnf upgrade -y tdnf
tdnf install -y tar grep coreutils

rpm --root $TEMP_CHROOT/ --initdb

# install coreutils first, it will reduce ln warnings
tdnf --installroot $TEMP_CHROOT/ install -y coreutils

tdnf --installroot $TEMP_CHROOT/ \
     install -y \
     util-linux bash filesystem findutils glibc \
     grep photon-release photon-repos tdnf vim which

actual_pkg_list=($(tdnf --installroot $TEMP_CHROOT/ \
                        --disablerepo=* -q \
                        list installed 2>/dev/null | cut -d' ' -f1))

expected_pkg_list=(
  attr.$arch bash.$arch bzip2.$arch ca-certificates.$arch
  coreutils.$arch curl.$arch elfutils-libelf.$arch expat.$arch
  file.$arch filesystem.$arch findutils.$arch glib.$arch glibc.$arch
  gmp.$arch gpgme.$arch grep.$arch hawkey.$arch libassuan.$arch
  libcap.$arch libdb.$arch libffi.$arch libgcc.$arch libgpg-error.$arch
  librepo.$arch libsolv.$arch libssh2.$arch libstdc++.$arch lua.$arch
  ncurses.$arch nspr.$arch nss.$arch openssl.$arch pcre.$arch
  photon-release.noarch photon-repos.noarch pkg-config.$arch popt.$arch
  readline.$arch rpm.$arch sqlite-autoconf.$arch tcsh.$arch tdnf.$arch
  util-linux.$arch vim.$arch which.$arch xz.$arch zlib.$arch
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

pushd $TEMP_CHROOT
#create /var/run symlink
ln -sf ../run var/run
# cleanup anything not needed inside rootfs
rm -rf usr/src/
rm -rf home/*
# rm -rf var/lib/yum/*
rm -rf var/log/*

#find var/cache/tdnf/photon/rpms -type f -name "*.rpm" -exec rm {} \;
tar cpjf ../$ROOTFS_TAR_FILENAME .
popd

max_size=$(( 44 * 1024 * 1024 ))
actual_size=$(wc -c $ROOTFS_TAR_FILENAME | cut -d' ' -f1)
if (( $actual_size > $max_size )); then
  echoerr "ERROR: docker image tarball size is bigger than expected"
	echoerr "Expected size(in bytes): $max_size"
	echoerr "Actual size(in bytes): $actual_size"
  rm -rf $TEMP_CHROOT $ROOTFS_TAR_FILENAME
  exit 1
fi

mv $ROOTFS_TAR_FILENAME $STAGE_DIR

# cleanup
rm -rf $TEMP_CHROOT
