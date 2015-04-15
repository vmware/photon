#!/bin/bash

if [ "$#" -lt 2 ]; then
	echo "Script to create new Photon Docker image."
	echo "Usage: $0 <path to workspace> <installation type>"
	exit -1
fi

set -e
set -x

PROGRAM=$0
ROOT=$1
TYPE=$2
IN_CONTAINER=$3

ROOTFS_TAR_FILENAME=rootfs.tar.bz2
INSTALLER_DIR=/workspace/photon/installer
PACKAGE_BUILDER_DIR=/workspace/photon/support/package-builder
DOCKERFILES_DIR=/workspace/photon/support/dockerfiles/photon/

if [ -z "$IN_CONTAINER" ]
then
	rm -f $ROOTFS_TAR_FILENAME
	docker run -it --privileged --rm -v $ROOT:/workspace toliaqat/ubuntu-dev bash /workspace/photon/support/dockerfiles/photon/${PROGRAM} $ROOT $TYPE "In Container" && \
	[ -e "$ROOTFS_TAR_FILENAME" ] && docker build -t photon:$TYPE .
else
	
	cd $INSTALLER_DIR && \
	cp sample_config.json docker_image_config.json && \
	sed -i -e "s/minimal/$TYPE/" docker_image_config.json && \
 	./photonInstaller.py -f -w /mnt/photon-root docker_image_config.json && \
 	rm docker_image_config.json
	cd $PACKAGE_BUILDER_DIR && \
	./umount-build-root.sh /mnt/photon-root && \
	cd /mnt/photon-root && \
	rm -rf tools/
	rm -rf usr/src/
	rm -rf boot/
	rm -rf lib/modules/
	tar cpjf /$ROOTFS_TAR_FILENAME . && \
	cp /$ROOTFS_TAR_FILENAME $DOCKERFILES_DIR
fi

