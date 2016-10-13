#!/bin/bash
set -x
PHOTON_IMG_OUTPUT_PATH=$1
SRC_ROOT=$2

rm -f $PHOTON_IMG_OUTPUT_PATH/*.vmdk
rm -f $PHOTON_IMG_OUTPUT_PATH/*.ova
sed "s|VMDK_IMAGE|$PHOTON_IMG_OUTPUT_PATH/photon-ova-ovs.vmdk|" vmx-ovs-template > /tmp/vmx-temp-ovs.vmx

cp ../update_custom_password.py $PHOTON_IMG_OUTPUT_PATH/

cd $PHOTON_IMG_OUTPUT_PATH

DISK_DEVICE=`losetup --show -f ${PHOTON_IMG_OUTPUT_PATH}/photon-ova_ovs.raw`
echo "Mapping device partition to loop device"
kpartx -av $DISK_DEVICE
DEVICE_NAME=`echo $DISK_DEVICE|cut -c6- `
echo "DISK_DEVICE=$DISK_DEVICE"
echo "ROOT_PARTITION=/dev/mapper/${DEVICE_NAME}p2"

rm -rf $PHOTON_IMG_OUTPUT_PATH/photon-ova_ovs
mkdir $PHOTON_IMG_OUTPUT_PATH/photon-ova_ovs

mount -v -t ext4 /dev/mapper/${DEVICE_NAME}p2 $PHOTON_IMG_OUTPUT_PATH/photon-ova_ovs
rm -f $PHOTON_IMG_OUTPUT_PATH/photon-ova_ovs/etc/systemd/system/multi-user.target.wants/cloud-*
cp $PHOTON_IMG_OUTPUT_PATH/photon-ova_ovs/etc/shadow $PHOTON_IMG_OUTPUT_PATH/photon-ova_ovs/etc/shadow.bak
sed -e "s/^\(root:\)[^:]*:/\1x:/" $PHOTON_IMG_OUTPUT_PATH/photon-ova_ovs/etc/shadow.bak > $PHOTON_IMG_OUTPUT_PATH/photon-ova_ovs/etc/shadow
./update_custom_password.py ovs $PHOTON_IMG_OUTPUT_PATH/photon-ova_ovs
rm -f $PHOTON_IMG_OUTPUT_PATH/photon-ova_ovs/etc/shadow-
rm -f $PHOTON_IMG_OUTPUT_PATH/photon-ova_ovs/etc/shadow.bak
umount $PHOTON_IMG_OUTPUT_PATH/photon-ova_ovs

echo "Deleting device map partition"
kpartx -d $DISK_DEVICE
rm -rf $PHOTON_IMG_OUTPUT_PATH/photon-ova_ovs
echo "Detaching loop device from raw disk"
losetup -d $DISK_DEVICE


$SRC_ROOT/tools/bin/vixdiskutil -convert $PHOTON_IMG_OUTPUT_PATH/photon-ova_ovs.raw -cap 16000 $PHOTON_IMG_OUTPUT_PATH/photon-ova-ovs.vmdk
$SRC_ROOT/tools/bin/vixdiskutil -wmeta toolsVersion 2147483647 $PHOTON_IMG_OUTPUT_PATH/photon-ova-ovs.vmdk

mkdir -p $PHOTON_IMG_OUTPUT_PATH/temp
ovftool /tmp/vmx-temp-ovs.vmx $PHOTON_IMG_OUTPUT_PATH/temp/photon-ova-ovs.ovf
cd $PHOTON_IMG_OUTPUT_PATH/temp

sed -i "s/otherGuest/other3xLinux64Guest/g" $PHOTON_IMG_OUTPUT_PATH/temp/photon-ova-ovs.ovf
#disable pcibridge and add uefi metadata
#sed -i '/vmw:value="efi"\/>/a \ \t<vmw:ExtraConfig ovf:required="false" vmw:key="uefi.secureBoot.enabled" vmw:value="TRUE"/>\n \ \t<vmw:ExtraConfig ovf:required="false" vmw:key="pciBridge5.present" vmw:value="false"/>\n \ \t<vmw:ExtraConfig ovf:required="false" vmw:key="pciBridge6.present" vmw:value="false"/>\n \ \t<vmw:ExtraConfig ovf:required="false" vmw:key="pciBridge7.present" vmw:value="false"/> ' $PHOTON_IMG_OUTPUT_PATH/temp/photon-ova-ovs.ovf
#Add product info
sed -i '/\/VirtualSystem>/i \ \t<ProductSection> \n \t\t<Info>Information about the installed software</Info> \n \t\t<Product>Photon</Product> \n \t\t<Vendor>VMware Inc.</Vendor> \n \t\t<Version>1.0.0</Version> \n \t\t<FullVersion>1.0.0-TP3</FullVersion> \n \t</ProductSection> ' $PHOTON_IMG_OUTPUT_PATH/temp/photon-ova-ovs.ovf

openssl sha1 *.vmdk photon-ova-ovs.ovf > photon-ova-ovs.mf
tar cf photon-ova-ovs-$PHOTON_RELEASE_VER-$PHOTON_BUILD_NUM.ova photon-ova-ovs.ovf photon-ova-ovs.mf photon-ova-ovs-disk1.vmdk
mv $PHOTON_IMG_OUTPUT_PATH/temp/photon-ova-ovs-$PHOTON_RELEASE_VER-$PHOTON_BUILD_NUM.ova $PHOTON_IMG_OUTPUT_PATH/

rm -rf $PHOTON_IMG_OUTPUT_PATH/temp/

rm -f $PHOTON_IMG_OUTPUT_PATH/photon-ova_ovs.raw

