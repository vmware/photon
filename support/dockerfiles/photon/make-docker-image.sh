#!/bin/bash

if [ "$#" -lt 1 ]; then
	echo "Script to create new photon base docker image."
	echo "Usage: $0 <path to workspace>"
	exit -1
fi

set -e
set -x

PROGRAM=$0
MAIN_PACKAGE=$1


TEMP_CHROOT=$(pwd)/temp_chroot
ROOTFS_TAR_FILENAME=photon-rootfs-$PHOTON_RELEASE_VERSION-$PHOTON_BUILD_NUMBER.tar.bz2
STAGE_DIR=$(pwd)/stage

rm -rf /etc/yum.repos.d/*

cat > /etc/yum.repos.d/photon-local.repo <<- EOF

[photon-local]
name=VMware Photon Linux 1.0(x86_64)
baseurl=file://$(pwd)/stage/RPMS
gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY
gpgcheck=0
enabled=1
skip_if_unavailable=True

EOF

rm -rf $TEMP_CHROOT 
mkdir $TEMP_CHROOT

rpm --root $TEMP_CHROOT/ --initdb
tdnf upgrade -y tdnf 
tdnf --installroot $TEMP_CHROOT/ install -y bash coreutils filesystem findutils glibc grep photon-release photon-repos tdnf util-linux vim which

rpm --root $TEMP_CHROOT/ --import $TEMP_CHROOT/etc/pki/rpm-gpg/*

cd $TEMP_CHROOT
#create /var/run symlink
ln -sf ../run var/run
# cleanup anything not needed inside rootfs
rm -rf usr/src/
rm -rf home/*
# rm -rf var/lib/yum/*
rm -rf var/log/*

#find var/cache/tdnf/photon/rpms -type f -name "*.rpm" -exec rm {} \;
tdnf install -y tar
tar cpjf ../$ROOTFS_TAR_FILENAME .
mkdir -p $STAGE_DIR
mv ../$ROOTFS_TAR_FILENAME $STAGE_DIR/
cd ..

# cleanup
rm -rf $TEMP_CHROOT

