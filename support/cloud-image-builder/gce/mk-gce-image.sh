#!/bin/bash

PHOTON_IMG_OUTPUT_PATH=$1
RAWFILE="photon-gce.raw"
TARFILE="photon-gce.tar.gz"

echo "Creating ${TARFILE} file from ${RAWFILE}.raw."
tar -Szcf $PHOTON_IMG_OUTPUT_PATH/${TARFILE} $PHOTON_IMG_OUTPUT_PATH/${RAWFILE}
