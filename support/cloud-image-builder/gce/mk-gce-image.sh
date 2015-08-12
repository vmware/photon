#!/bin/bash

PHOTON_IMG_OUTPUT_PATH=$1
RAWFILE="photon-gce.raw"
TARFILE="photon-gce.tar.gz"

echo "Creating ${TARFILE} file from ${RAWFILE}."
cd $PHOTON_IMG_OUTPUT_PATH
mv ${RAWFILE} disk.raw
tar -Szcf $PHOTON_IMG_OUTPUT_PATH/${TARFILE} disk.raw
