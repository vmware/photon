#!/bin/bash
set -x
PHOTON_IMG_OUTPUT_PATH=$1
SRC_ROOT=$2

rm -f $PHOTON_IMG_OUTPUT_PATH/*.vmdk
rm -f $PHOTON_IMG_OUTPUT_PATH/*.ova

#Generate two ova images one with a random password and the other with a defined password

sed "s|VMDK_IMAGE|$PHOTON_IMG_OUTPUT_PATH/photon-generic-ova.vmdk|" vmx-generic-template > /tmp/vmx-generic-temp.vmx
sed "s|VMDK_IMAGE|$PHOTON_IMG_OUTPUT_PATH/photon-generic-custom.vmdk|" vmx-generic-template > /tmp/vmx-generic-temp-custom.vmx

cp ../update_custom_password.py $PHOTON_IMG_OUTPUT_PATH/

$SRC_ROOT/tools/bin/vixdiskutil -convert $PHOTON_IMG_OUTPUT_PATH/photon-ova_generic.raw -cap 16000 $PHOTON_IMG_OUTPUT_PATH/photon-generic-ova.vmdk
$SRC_ROOT/tools/bin/vixdiskutil -wmeta toolsVersion 2147483647 $PHOTON_IMG_OUTPUT_PATH/photon-generic-ova.vmdk

cd $PHOTON_IMG_OUTPUT_PATH

mkdir -p $PHOTON_IMG_OUTPUT_PATH/temp
ovftool /tmp/vmx-generic-temp.vmx $PHOTON_IMG_OUTPUT_PATH/temp/photon-generic-ova.ovf
cd $PHOTON_IMG_OUTPUT_PATH/temp

sed -i "s/otherGuest/other3xLinux64Guest/g" $PHOTON_IMG_OUTPUT_PATH/temp/photon-generic-ova.ovf
#Add product info
sed -i '/\/VirtualSystem>/i \ \t<ProductSection> \n \t\t<Info>Information about the installed software</Info> \n \t\t<Product>Photon</Product> \n \t\t<Vendor>VMware Inc.</Vendor> \n \t\t<Version>1.0.0</Version> \n \t\t<FullVersion>1.0.0-TP2</FullVersion> \n \t</ProductSection> ' $PHOTON_IMG_OUTPUT_PATH/temp/photon-generic-ova.ovf
rm -f $PHOTON_IMG_OUTPUT_PATH/temp/photon-generic-ova.mf
openssl sha1 *.vmdk photon-generic-ova.ovf > photon-generic-ova.mf
tar cf photon-generic-ova-$PHOTON_RELEASE_VER-$PHOTON_BUILD_NUM.ova photon-generic-ova.ovf photon-generic-ova.mf photon-generic-ova-disk1.vmdk
mv $PHOTON_IMG_OUTPUT_PATH/temp/photon-generic-ova-$PHOTON_RELEASE_VER-$PHOTON_BUILD_NUM.ova $PHOTON_IMG_OUTPUT_PATH/
cd $PHOTON_IMG_OUTPUT_PATH
rm -rf photon-generic-custom
DISK_DEVICE=`losetup --show -f ${PHOTON_IMG_OUTPUT_PATH}/photon-ova_generic.raw`
kpartx -av $DISK_DEVICE

DEVICE_NAME=`echo $DISK_DEVICE|cut -c6- `

rm -rf $PHOTON_IMG_OUTPUT_PATH/photon-generic-custom
mkdir $PHOTON_IMG_OUTPUT_PATH/photon-generic-custom

mount -v -t ext4 /dev/mapper/${DEVICE_NAME}p2 $PHOTON_IMG_OUTPUT_PATH/photon-generic-custom
#The defined password is 'changeme'
cp $PHOTON_IMG_OUTPUT_PATH/photon-generic-custom/etc/shadow $PHOTON_IMG_OUTPUT_PATH/photon-generic-custom/etc/shadow.bak
sed -e "s/^\(root:\)[^:]*:/\1x:/" $PHOTON_IMG_OUTPUT_PATH/photon-generic-custom/etc/shadow.bak > $PHOTON_IMG_OUTPUT_PATH/photon-generic-custom/etc/shadow
./update_custom_password.py changeme $PHOTON_IMG_OUTPUT_PATH/photon-generic-custom
rm -f $PHOTON_IMG_OUTPUT_PATH/photon-generic-custom/etc/shadow-
rm -f $PHOTON_IMG_OUTPUT_PATH/photon-generic-custom/etc/shadow.bak
# Force immediate password expiry
chroot $PHOTON_IMG_OUTPUT_PATH/photon-generic-custom /bin/bash -c "chage -d 0 root"
umount $PHOTON_IMG_OUTPUT_PATH/photon-generic-custom
kpartx -d $DISK_DEVICE

rm -rf photon-generic-custom

echo "Detaching loop device from raw disk"
losetup -d $DISK_DEVICE

$SRC_ROOT/tools/bin/vixdiskutil -convert $PHOTON_IMG_OUTPUT_PATH/photon-ova_generic.raw -cap 16000 $PHOTON_IMG_OUTPUT_PATH/photon-generic-custom.vmdk

$SRC_ROOT/tools/bin/vixdiskutil -wmeta toolsVersion 2147483647 $PHOTON_IMG_OUTPUT_PATH/photon-generic-custom.vmdk

mkdir -p $PHOTON_IMG_OUTPUT_PATH/temp1
ovftool /tmp/vmx-generic-temp-custom.vmx $PHOTON_IMG_OUTPUT_PATH/temp1/photon-generic-custom.ovf
cd $PHOTON_IMG_OUTPUT_PATH/temp1
sed -i "s/otherGuest/other3xLinux64Guest/g" $PHOTON_IMG_OUTPUT_PATH/temp1/photon-generic-custom.ovf
#Add product info
sed -i '/\/VirtualSystem>/i \ \t<ProductSection> \n \t\t<Info>Information about the installed software</Info> \n \t\t<Product>Photon</Product> \n \t\t<Vendor>VMware Inc.</Vendor> \n \t\t<Version>1.0.0</Version> \n \t\t<FullVersion>1.0.0-TP2</FullVersion> \n \t</ProductSection> ' $PHOTON_IMG_OUTPUT_PATH/temp1/photon-generic-custom.ovf
rm -f $PHOTON_IMG_OUTPUT_PATH/temp1/photon-generic-custom.mf
openssl sha1 *.vmdk photon-generic-custom.ovf > photon-generic-custom.mf
tar cf photon-generic-custom-$PHOTON_RELEASE_VER-$PHOTON_BUILD_NUM.ova photon-generic-custom.ovf photon-generic-custom.mf photon-generic-custom-disk1.vmdk
mv $PHOTON_IMG_OUTPUT_PATH/temp1/photon-generic-custom-$PHOTON_RELEASE_VER-$PHOTON_BUILD_NUM.ova $PHOTON_IMG_OUTPUT_PATH/
cd $PHOTON_IMG_OUTPUT_PATH
rm -rf $PHOTON_IMG_OUTPUT_PATH/temp/
rm -rf $PHOTON_IMG_OUTPUT_PATH/temp1/
rm -f $PHOTON_IMG_OUTPUT_PATH/photon-ova_generic.raw
