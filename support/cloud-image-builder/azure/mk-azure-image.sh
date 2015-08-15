#!/bin/bash

PHOTON_IMG_OUTPUT_PATH=$1
qemu-img create -f vpc -o subformat=fixed $PHOTON_IMG_OUTPUT_PATH/photon-azure.vhd 2G
qemu-img convert -f raw -O vpc $PHOTON_IMG_OUTPUT_PATH/photon-azure.raw $PHOTON_IMG_OUTPUT_PATH/photon-azure.vhd
