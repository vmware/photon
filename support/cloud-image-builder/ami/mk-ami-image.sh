#!/bin/bash

PHOTON_IMG_OUTPUT_PATH=$1
tar -Szcf $PHOTON_IMG_OUTPUT_PATH/photon-ami-$PHOTON_RELEASE_VER-$PHOTON_BUILD_NUM.tar.gz $PHOTON_IMG_OUTPUT_PATH/photon-ami.raw
cd $PHOTON_IMG_OUTPUT_PATH && ln -s photon-ami-$PHOTON_RELEASE_VER-$PHOTON_BUILD_NUM.tar.gz photon-ami.tar.gz

rm -f $PHOTON_IMG_OUTPUT_PATH/photon-ami.raw
