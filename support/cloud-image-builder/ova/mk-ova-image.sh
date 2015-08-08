#!/bin/bash
set -x
PHOTON_IMG_OUTPUT_PATH=$1
SRC_ROOT=$2
sed "s|VMDK_IMAGE|$PHOTON_IMG_OUTPUT_PATH/photon-ova.vmdk|" vmx-template > /tmp/vmx-temp.vmx

qemu-img convert -f raw -O vmdk -o adapter_type=lsilogic $PHOTON_IMG_OUTPUT_PATH/photon-ova.raw $PHOTON_IMG_OUTPUT_PATH/photon-ova-flat.vmdk 
cd $SRC_ROOT/tools/src/vixDiskUtil
mkdir -p $SRC_ROOT/tools/bin
make clean
make
$SRC_ROOT/tools/bin/vixdiskutil -clone $PHOTON_IMG_OUTPUT_PATH/photon-ova-flat.vmdk $PHOTON_IMG_OUTPUT_PATH/photon-ova.vmdk
$SRC_ROOT/tools/bin/vixdiskutil -wmeta toolsVersion 2147483647 $PHOTON_IMG_OUTPUT_PATH/photon-ova.vmdk

cd $PHOTON_IMG_OUTPUT_PATH

ovftool /tmp/vmx-temp.vmx $PHOTON_IMG_OUTPUT_PATH/photon-stream-ova.ova

