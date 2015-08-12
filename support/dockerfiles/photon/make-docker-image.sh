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
ROOTFS_TAR_FILENAME=photon-rootfs.tar.bz2
STAGE_DIR=$(pwd)/stage

sudo createrepo $STAGE_DIR/RPMS

cat > yum.conf <<- EOF

[main]
cachedir=$(pwd)/temp_chroot/var/cache/yum
keepcache=1
debuglevel=2
logfile=$(pwd)/temp_chroot/var/log/yum.log
exactarch=1
obsoletes=1

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

# use host's yum to install in chroot
mkdir -p $TEMP_CHROOT/var/lib/rpm
rpm --root $TEMP_CHROOT/ --initdb
yum -c yum.conf --disablerepo=* --enablerepo=photon-local --installroot=$TEMP_CHROOT install -y filesystem glibc
yum -c yum.conf --disablerepo=* --enablerepo=photon-local --installroot=$TEMP_CHROOT install -y yum bash coreutils photon-release $MAIN_PACKAGE
yum -c yum.conf --disablerepo=* --enablerepo=photon-local --installroot=$TEMP_CHROOT clean all

cp /etc/resolv.conf $TEMP_CHROOT/etc/

# # reinstalling inside to make sure rpmdb is created for tdnf.
# # TODO find better solution.
# chroot $TEMP_CHROOT bash -c \
#    "tdnf install -y filesystem; \
#     tdnf install -y glibc ; \
#     tdnf install -y bash ; \
#     tdnf install -y coreutils ; \
#     tdnf install -y rpm-ostree ; \
#     tdnf install -y photon-release; \
#     rpm -e --nodeps perl; \
#     rpm -e --nodeps perl-DBD-SQLite; \
#     rpm -e --nodeps perl-Module-ScanDeps; \
#     rpm -e --nodeps perl-DBIx-Simple; \
#     rpm -e --nodeps perl-DBI; \
#     rpm -e --nodeps perl-WWW-Curl;"

cd $TEMP_CHROOT
# cleanup anything not needed inside rootfs
rm -rf usr/src/
rm -rf home/*
# rm -rf var/lib/yum/*
rm -rf var/log/*

#find var/cache/tdnf/photon/rpms -type f -name "*.rpm" -exec rm {} \;

tar cpjf ../$ROOTFS_TAR_FILENAME .
mkdir -p $STAGE_DIR
mv ../$ROOTFS_TAR_FILENAME $STAGE_DIR/

cd ..

# cleanup
rm -rf $TEMP_CHROOT
rm yum.conf

