#!/bin/bash
set -x
PHOTON_IMG_OUTPUT_PATH=$1
SRC_ROOT=$2

rm -f $PHOTON_IMG_OUTPUT_PATH/*.vmdk
rm -f $PHOTON_IMG_OUTPUT_PATH/*.ova
sed "s|VMDK_IMAGE|$PHOTON_IMG_OUTPUT_PATH/photon-ova-uefi.vmdk|" vmx-uefi-template > /tmp/vmx-temp-uefi.vmx

cd $PHOTON_IMG_OUTPUT_PATH

DISK_DEVICE=`losetup --show -f ${PHOTON_IMG_OUTPUT_PATH}/photon-ova_uefi.raw`

echo "Mapping device partition to loop device"
kpartx -av $DISK_DEVICE

DEVICE_NAME=`echo $DISK_DEVICE|cut -c6- `

echo "DISK_DEVICE=$DISK_DEVICE"
echo "ROOT_PARTITION=/dev/mapper/${DEVICE_NAME}p2"

rm -rf $PHOTON_IMG_OUTPUT_PATH/photon-ova_uefi
mkdir $PHOTON_IMG_OUTPUT_PATH/photon-ova_uefi

mount -v -t ext4 /dev/mapper/${DEVICE_NAME}p2 $PHOTON_IMG_OUTPUT_PATH/photon-ova_uefi

rm -f $PHOTON_IMG_OUTPUT_PATH/photon-ova_uefi/etc/systemd/system/multi-user.target.wants/cloud-*

umount $PHOTON_IMG_OUTPUT_PATH/photon-ova_uefi

echo "Deleting device map partition"
kpartx -d $DISK_DEVICE

rm -rf $PHOTON_IMG_OUTPUT_PATH/photon-ova_uefi

echo "Detaching loop device from raw disk"
losetup -d $DISK_DEVICE

$SRC_ROOT/tools/bin/vixdiskutil -convert $PHOTON_IMG_OUTPUT_PATH/photon-ova_uefi.raw -cap 16000 $PHOTON_IMG_OUTPUT_PATH/photon-ova-uefi.vmdk
$SRC_ROOT/tools/bin/vixdiskutil -wmeta toolsVersion 2147483647 $PHOTON_IMG_OUTPUT_PATH/photon-ova-uefi.vmdk

mkdir -p $PHOTON_IMG_OUTPUT_PATH/temp
ovftool /tmp/vmx-temp-uefi.vmx $PHOTON_IMG_OUTPUT_PATH/temp/photon-ova-uefi.ovf
cd $PHOTON_IMG_OUTPUT_PATH/temp

sed -i "s/otherGuest/other3xLinux64Guest/g" $PHOTON_IMG_OUTPUT_PATH/temp/photon-ova-uefi.ovf
#disable pcibridge and add uefi metadata
sed -i '/vmw:value="efi"\/>/a \ \t<vmw:ExtraConfig ovf:required="false" vmw:key="uefi.secureBoot.enabled" vmw:value="TRUE"/>\n \ \t<vmw:ExtraConfig ovf:required="false" vmw:key="pciBridge5.present" vmw:value="false"/>\n \ \t<vmw:ExtraConfig ovf:required="false" vmw:key="pciBridge6.present" vmw:value="false"/>\n \ \t<vmw:ExtraConfig ovf:required="false" vmw:key="pciBridge7.present" vmw:value="false"/> ' $PHOTON_IMG_OUTPUT_PATH/temp/photon-ova-uefi.ovf
#Add product info
sed -i '/\/VirtualSystem>/i \ \t<ProductSection> \n \t\t<Info>Information about the installed software</Info> \n \t\t<Product>Photon</Product> \n \t\t<Vendor>VMware Inc.</Vendor> \n \t\t<Version>1.0.0</Version> \n \t\t<FullVersion>1.0.0-TP2</FullVersion> \n \t</ProductSection> ' $PHOTON_IMG_OUTPUT_PATH/temp/photon-ova-uefi.ovf

openssl sha1 *.vmdk photon-ova-uefi.ovf > photon-ova-uefi.mf
tar cf photon-ova-uefi-$PHOTON_RELEASE_VER-$PHOTON_BUILD_NUM.ova photon-ova-uefi.ovf photon-ova-uefi.mf photon-ova-uefi-disk1.vmdk
mv $PHOTON_IMG_OUTPUT_PATH/temp/photon-ova-uefi-$PHOTON_RELEASE_VER-$PHOTON_BUILD_NUM.ova $PHOTON_IMG_OUTPUT_PATH/

rm -rf $PHOTON_IMG_OUTPUT_PATH/temp/

rm -f $PHOTON_IMG_OUTPUT_PATH/photon-ova_uefi.raw

