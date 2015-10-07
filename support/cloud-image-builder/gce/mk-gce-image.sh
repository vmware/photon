#!/bin/bash

PHOTON_IMG_OUTPUT_PATH=$1
RAWFILE="photon-gce.raw"
TARFILE="photon-gce-$PHOTON_RELEASE_VER-$PHOTON_BUILD_NUM.tar.gz"

echo "Creating ${TARFILE} file from ${RAWFILE}."
cd $PHOTON_IMG_OUTPUT_PATH
mv ${RAWFILE} disk.raw
tar -Szcf $PHOTON_IMG_OUTPUT_PATH/${TARFILE} disk.raw
cd $PHOTON_IMG_OUTPUT_PATH && ln -s ${TARFILE} photon-gce.tar.gz

rm -f disk.raw
