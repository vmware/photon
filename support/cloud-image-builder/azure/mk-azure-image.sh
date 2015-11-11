#!/bin/bash

PHOTON_IMG_OUTPUT_PATH=$1
SRC_ROOT=$2
cd $SRC_ROOT/tools/src/imgconverter
mkdir -p $SRC_ROOT/tools/bin
make clean
make
$SRC_ROOT/tools/bin/imgconverter -i $PHOTON_IMG_OUTPUT_PATH/photon-azure.raw -v vhd -o $PHOTON_IMG_OUTPUT_PATH/photon-azure-$PHOTON_RELEASE_VER-$PHOTON_BUILD_NUM.vhd

rm -f $PHOTON_IMG_OUTPUT_PATH/photon-azure.raw

