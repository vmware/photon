#!/bin/bash

set -x

if [ "$#" -lt 0 ]; then
	echo "Script to create new Photon OSTree repo inside a docker container."
	echo "Usage: $0 "
	exit -1
fi

PROGRAM=$0

createrepo stage/RPMS

cp installer/photon-ostree.repo installer/photon-ostree.repo.bak
echo "baseurl=file:///photon/stage/RPMS" >> installer/photon-ostree.repo

rm -rf stage/ostree-repo
mkdir -p stage/ostree-repo

sudo docker run -it --privileged -v $(pwd):/photon -v $(pwd)/stage/ostree-repo:/srv/rpm-ostree -w="/photon/installer"  toliaqat/photon:rpm-ostree ./mk-ostree-server.sh /

tar -zcf stage/ostree-repo.tar.gz stage/ostree-repo/repo/

# Restore file
mv -f installer/photon-ostree.repo.bak installer/photon-ostree.repo
rm -rf stage/ostree-repo
