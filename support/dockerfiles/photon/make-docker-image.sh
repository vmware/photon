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

DOCK_ARCH=`uname -m`

TEMP_CHROOT=$(pwd)/temp_chroot
ROOTFS_TAR_FILENAME=photon-rootfs-$PHOTON_RELEASE_VERSION-$PHOTON_BUILD_NUMBER.tar.gz
STAGE_DIR=$(pwd)/stage

rm -rf /etc/yum.repos.d/*

cat > /etc/yum.repos.d/photon-local.repo <<- EOF

[photon-local]
name=VMware Photon Linux 3.0($DOCK_ARCH)
baseurl=file://$(pwd)/stage/RPMS
gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY
gpgcheck=0
enabled=1
skip_if_unavailable=True

EOF

rm -rf $TEMP_CHROOT
mkdir $TEMP_CHROOT

tdnf install -y rpm

rpm --root $TEMP_CHROOT/ --initdb

tdnf --installroot $TEMP_CHROOT/ --rpmverbosity 10 install -y filesystem bash toybox tdnf photon-release photon-repos

rpm --root $TEMP_CHROOT/ --import $TEMP_CHROOT/etc/pki/rpm-gpg/*

cd $TEMP_CHROOT
# cleanup anything not needed inside rootfs
rm -rf usr/src/
rm -rf home/*
# rm -rf var/lib/yum/*
rm -rf var/log/*
# set TERM to linux due to stripped terminfo
echo "export TERM=linux" >> etc/bash.bashrc

#find var/cache/tdnf/photon/rpms -type f -name "*.rpm" -exec rm {} \;
tdnf install -y tar
tdnf install -y gzip
tar cpzf ../$ROOTFS_TAR_FILENAME .
mkdir -p $STAGE_DIR
mv ../$ROOTFS_TAR_FILENAME $STAGE_DIR/
cd ..

# cleanup
rm -rf $TEMP_CHROOT

