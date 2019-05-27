#!/bin/bash

set -x

if [ "$#" -lt 0 ]; then
	echo "Script to create new Photon OSTree repo inside a docker container."
	echo "Usage: $0 "
	exit -1
fi

PROGRAM=$0
SRCROOT=$1

createrepo stage/RPMS

cp ${SRCROOT}/installer/photon-ostree.repo ${SRCROOT}/installer/photon-ostree.repo.bak
echo "baseurl=file:///RPMS" >> ${SRCROOT}/installer/photon-ostree.repo

rm -rf stage/ostree-repo
mkdir -p stage/ostree-repo

sudo docker run -it --privileged -v ${SRCROOT}:/photon -v $(pwd)/stage/RPMS:/RPMS -v $(pwd)/stage/ostree-repo:/srv/rpm-ostree -w="/photon/installer"  ankitaj/photon-build:rpm-ostree-3.0 ./mk-ostree-server.sh /

(cd stage/ostree-repo/repo/; tar -zcf ../../ostree-repo.tar.gz .; )

# Restore file
mv -f ${SRCROOT}/installer/photon-ostree.repo.bak ${SRCROOT}/installer/photon-ostree.repo
sudo rm -rf ${SRCROOT}/stage/ostree-repo
