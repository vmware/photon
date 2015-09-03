#!/bin/bash

PHOTON_IMG_OUTPUT_PATH=$1
tar -Szcf $PHOTON_IMG_OUTPUT_PATH/photon-ami.tar.gz $PHOTON_IMG_OUTPUT_PATH/photon-ami.raw

rm -f $PHOTON_IMG_OUTPUT_PATH/photon-ami.raw
