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

mkdir -p $PHOTON_IMG_OUTPUT_PATH/temp
ovftool /tmp/vmx-temp.vmx $PHOTON_IMG_OUTPUT_PATH/temp/photon-stream-ova.ovf
cd $PHOTON_IMG_OUTPUT_PATH/temp

sed -i "s/otherGuest/other3xLinux64Guest/g" $PHOTON_IMG_OUTPUT_PATH/temp/photon-stream-ova.ovf
rm -f $PHOTON_IMG_OUTPUT_PATH/temp/photon-stream-ova.mf
openssl sha1 *.vmdk *.ovf > photon-stream-ova.mf
tar cf photon-stream-ova.ova photon-stream-ova.ovf photon-stream-ova.mf photon-stream-ova-disk1.vmdk

cp $PHOTON_IMG_OUTPUT_PATH/temp/photon-stream-ova.ova $PHOTON_IMG_OUTPUT_PATH/
cd $PHOTON_IMG_OUTPUT_PATH
rm -rf $PHOTON_IMG_OUTPUT_PATH/temp/





