#!/bin/bash

if [ "$#" -lt 1 ]; then
	echo "Script to create new photon base docker image."
	echo "Usage: $0 <path to workspace>"
	exit -1
fi

set -e
set -x

PROGRAM=$0
WORKSPACE_DIR=$1
RPMS_DIR=$WORKSPACE_DIR/stage/RPMS
TEMP_CHROOT=$(pwd)/temp_chroot

ROOTFS_TAR_FILENAME=photon-rootfs.tar.bz2
STAGE_DIR=$WORKSPACE_DIR/stage


sudo createrepo $RPMS_DIR

cat > yum.conf <<- "EOF"

[main]
cachedir=$(pwd)/temp_chroot/var/cache/yum
keepcache=1
debuglevel=2
logfile=$(pwd)/temp_chroot/var/log/yum.log
exactarch=1
obsoletes=1

[photon]
name=VMware Photon Linux 1.0(x86_64)
baseurl=https://dl.bintray.com/vmware/photon_release_1.0_x86_64
gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY
gpgcheck=0
enabled=1
skip_if_unavailable=True

EOF

rm -rf $TEMP_CHROOT 
mkdir $TEMP_CHROOT

# use host's yum to install in chroot
yum -c yum.conf --installroot=$TEMP_CHROOT install -y filesystem glibc
yum -c yum.conf --installroot=$TEMP_CHROOT install -y bash tdnf coreutils photon-release
yum -c yum.conf clean all
cp /etc/resolv.conf $TEMP_CHROOT/etc/

# reinstalling inside to make sure rpmdb is created for tdnf.
# TODO find better solution.
chroot $TEMP_CHROOT bash -c \
   "tdnf install -y filesystem; \
    tdnf install -y glibc ; \
    tdnf install -y bash ; \
    tdnf install -y coreutils ; \
    tdnf install -y tdnf ; \
    tdnf install -y photon-release; \
    rpm -e --nodeps perl"

cd $TEMP_CHROOT
# cleanup anything not needed inside rootfs
rm -rf usr/src/
rm -rf home/*
rm -rf var/lib/yum/*
rm -rf /var/log/*
tar cpjf ../$ROOTFS_TAR_FILENAME .
mv ../$ROOTFS_TAR_FILENAME $STAGE_DIR
cd ..

# cleanup
rm -rf $TEMP_CHROOT
rm yum.conf

