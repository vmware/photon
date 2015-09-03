#!/bin/bash
set -x
PHOTON_IMG_OUTPUT_PATH=$1
SRC_ROOT=$2

rm -f $PHOTON_IMG_OUTPUT_PATH/*.vmdk
rm -f $PHOTON_IMG_OUTPUT_PATH/*.ova
sed "s|VMDK_IMAGE|$PHOTON_IMG_OUTPUT_PATH/photon-ova-uefi.vmdk|" vmx-uefi-template > /tmp/vmx-temp-uefi.vmx

cd $SRC_ROOT/tools/src/vixDiskUtil
mkdir -p $SRC_ROOT/tools/bin
make clean
make

cd $PHOTON_IMG_OUTPUT_PATH

$SRC_ROOT/tools/bin/vixdiskutil -convert $PHOTON_IMG_OUTPUT_PATH/photon-ova_uefi.raw -cap 16000 $PHOTON_IMG_OUTPUT_PATH/photon-ova-uefi.vmdk
$SRC_ROOT/tools/bin/vixdiskutil -wmeta toolsVersion 2147483647 $PHOTON_IMG_OUTPUT_PATH/photon-ova-uefi.vmdk

mkdir -p $PHOTON_IMG_OUTPUT_PATH/temp
ovftool /tmp/vmx-temp-uefi.vmx $PHOTON_IMG_OUTPUT_PATH/temp/photon-ova-uefi.ovf
cd $PHOTON_IMG_OUTPUT_PATH/temp

sed -i "s/otherGuest/other3xLinux64Guest/g" $PHOTON_IMG_OUTPUT_PATH/temp/photon-ova-uefi.ovf
#Add uefi metadata
sed -i '/vmw:value="efi"\/>/a \ \t<vmw:Config ovf:required="false" vmw:key="uefi.secureBoot.enabled" vmw:value="TRUE"/>\n \ \t<vmw:Config ovf:required="false" vmw:key="isolation.monitor.control.disable" vmw:value="FALSE"/> ' $PHOTON_IMG_OUTPUT_PATH/temp/photon-ova-uefi.ovf
#Add product info
sed -i '/\/VirtualHardwareSection>/i \ \t<ProductSection> \n \t\t<Info>Information about the installed software</Info> \n \t\t<Product>Photon</Product> \n \t\t<Vendor>VMware Inc.</Vendor> \n \t\t<Version>1.0.0</Version> \n \t\t<FullVersion>1.0.0-TP2</FullVersion> \n \t</ProductSection> ' $PHOTON_IMG_OUTPUT_PATH/temp/photon-ova-uefi.ovf

openssl sha1 *.vmdk photon-ova-uefi.ovf > photon-ova-uefi.mf
tar cf photon-ova-uefi.ova photon-ova-uefi.ovf photon-ova-uefi.mf photon-ova-uefi-disk1.vmdk

cp $PHOTON_IMG_OUTPUT_PATH/temp/photon-ova-uefi.ova $PHOTON_IMG_OUTPUT_PATH/
rm -rf $PHOTON_IMG_OUTPUT_PATH/temp/

rm -f $PHOTON_IMG_OUTPUT_PATH/photon-ova_uefi.raw

