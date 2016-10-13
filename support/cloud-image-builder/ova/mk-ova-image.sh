#!/bin/bash
set -x
PHOTON_IMG_OUTPUT_PATH=$1
SRC_ROOT=$2

rm -f $PHOTON_IMG_OUTPUT_PATH/*.vmdk
rm -f $PHOTON_IMG_OUTPUT_PATH/*.ova

#Generate two ova images one with a random password and the other with a defined password

sed "s|VMDK_IMAGE|$PHOTON_IMG_OUTPUT_PATH/photon-ova.vmdk|" vmx-template > /tmp/vmx-temp.vmx
sed "s|VMDK_IMAGE|$PHOTON_IMG_OUTPUT_PATH/photon-custom.vmdk|" vmx-template > /tmp/vmx-temp-custom.vmx

cp ../update_custom_password.py $PHOTON_IMG_OUTPUT_PATH/

$SRC_ROOT/tools/bin/vixdiskutil -convert $PHOTON_IMG_OUTPUT_PATH/photon-ova.raw -cap 16000 $PHOTON_IMG_OUTPUT_PATH/photon-ova.vmdk
$SRC_ROOT/tools/bin/vixdiskutil -wmeta toolsVersion 2147483647 $PHOTON_IMG_OUTPUT_PATH/photon-ova.vmdk

cd $PHOTON_IMG_OUTPUT_PATH

mkdir -p $PHOTON_IMG_OUTPUT_PATH/temp
ovftool /tmp/vmx-temp.vmx $PHOTON_IMG_OUTPUT_PATH/temp/photon-ova.ovf
cd $PHOTON_IMG_OUTPUT_PATH/temp

sed -i "s/otherGuest/other3xLinux64Guest/g" $PHOTON_IMG_OUTPUT_PATH/temp/photon-ova.ovf
#Add product info
sed -i '/\/VirtualSystem>/i \ \t<ProductSection> \n \t\t<Info>Information about the installed software</Info> \n \t\t<Product>Photon</Product> \n \t\t<Vendor>VMware Inc.</Vendor> \n \t\t<Version>1.0</Version> \n \t\t<FullVersion>1.0</FullVersion> \n \t</ProductSection> ' $PHOTON_IMG_OUTPUT_PATH/temp/photon-ova.ovf
rm -f $PHOTON_IMG_OUTPUT_PATH/temp/photon-ova.mf
openssl sha1 *.vmdk photon-ova.ovf > photon-ova.mf
tar cf photon-ova-$PHOTON_RELEASE_VER-$PHOTON_BUILD_NUM.ova photon-ova.ovf photon-ova.mf photon-ova-disk1.vmdk
mv $PHOTON_IMG_OUTPUT_PATH/temp/photon-ova-$PHOTON_RELEASE_VER-$PHOTON_BUILD_NUM.ova $PHOTON_IMG_OUTPUT_PATH/

#generate a second ova with lower hardware version
cp photon-ova.ovf photon-ova-hw10.ovf
sed -i 's/vmx-11/vmx-10/g' photon-ova-hw10.ovf
rm -f $PHOTON_IMG_OUTPUT_PATH/temp/photon-ova.mf
openssl sha1 *.vmdk photon-ova-hw10.ovf > photon-ova-hw10.mf
tar cf photon-ova-hw10-$PHOTON_RELEASE_VER-$PHOTON_BUILD_NUM.ova photon-ova-hw10.ovf photon-ova-hw10.mf photon-ova-disk1.vmdk
mv $PHOTON_IMG_OUTPUT_PATH/temp/photon-ova-hw10-$PHOTON_RELEASE_VER-$PHOTON_BUILD_NUM.ova $PHOTON_IMG_OUTPUT_PATH/

cd $PHOTON_IMG_OUTPUT_PATH
rm -rf photon-custom
DISK_DEVICE=`losetup --show -f ${PHOTON_IMG_OUTPUT_PATH}/photon-ova.raw`
kpartx -av $DISK_DEVICE

DEVICE_NAME=`echo $DISK_DEVICE|cut -c6- `

rm -rf $PHOTON_IMG_OUTPUT_PATH/photon-custom
mkdir $PHOTON_IMG_OUTPUT_PATH/photon-custom

mount -v -t ext4 /dev/mapper/${DEVICE_NAME}p2 $PHOTON_IMG_OUTPUT_PATH/photon-custom
#The defined password is 'changeme'
cp $PHOTON_IMG_OUTPUT_PATH/photon-custom/etc/shadow $PHOTON_IMG_OUTPUT_PATH/photon-custom/etc/shadow.bak
sed -e "s/^\(root:\)[^:]*:/\1x:/" $PHOTON_IMG_OUTPUT_PATH/photon-custom/etc/shadow.bak > $PHOTON_IMG_OUTPUT_PATH/photon-custom/etc/shadow
./update_custom_password.py changeme $PHOTON_IMG_OUTPUT_PATH/photon-custom
rm -f $PHOTON_IMG_OUTPUT_PATH/photon-custom/etc/shadow-
rm -f $PHOTON_IMG_OUTPUT_PATH/photon-custom/etc/shadow.bak
# Force immediate password expiry
chroot $PHOTON_IMG_OUTPUT_PATH/photon-custom /bin/bash -c "chage -d 0 root"
umount $PHOTON_IMG_OUTPUT_PATH/photon-custom
kpartx -d $DISK_DEVICE

rm -rf photon-custom

echo "Detaching loop device from raw disk"
losetup -d $DISK_DEVICE

$SRC_ROOT/tools/bin/vixdiskutil -convert $PHOTON_IMG_OUTPUT_PATH/photon-ova.raw -cap 16000 $PHOTON_IMG_OUTPUT_PATH/photon-custom.vmdk

$SRC_ROOT/tools/bin/vixdiskutil -wmeta toolsVersion 2147483647 $PHOTON_IMG_OUTPUT_PATH/photon-custom.vmdk

mkdir -p $PHOTON_IMG_OUTPUT_PATH/temp1
ovftool /tmp/vmx-temp-custom.vmx $PHOTON_IMG_OUTPUT_PATH/temp1/photon-custom.ovf
cd $PHOTON_IMG_OUTPUT_PATH/temp1
sed -i "s/otherGuest/other3xLinux64Guest/g" $PHOTON_IMG_OUTPUT_PATH/temp1/photon-custom.ovf
#Add product info
sed -i '/\/VirtualSystem>/i \ \t<ProductSection> \n \t\t<Info>Information about the installed software</Info> \n \t\t<Product>Photon</Product> \n \t\t<Vendor>VMware Inc.</Vendor> \n \t\t<Version>1.0</Version> \n \t\t<FullVersion>1.0</FullVersion> \n \t</ProductSection> ' $PHOTON_IMG_OUTPUT_PATH/temp1/photon-custom.ovf
rm -f $PHOTON_IMG_OUTPUT_PATH/temp1/photon-custom.mf
openssl sha1 *.vmdk photon-custom.ovf > photon-custom.mf
tar cf photon-custom-$PHOTON_RELEASE_VER-$PHOTON_BUILD_NUM.ova photon-custom.ovf photon-custom.mf photon-custom-disk1.vmdk
mv $PHOTON_IMG_OUTPUT_PATH/temp1/photon-custom-$PHOTON_RELEASE_VER-$PHOTON_BUILD_NUM.ova $PHOTON_IMG_OUTPUT_PATH/

#generate a second custom ova with lower hardware version
cp photon-custom.ovf photon-custom-hw10.ovf
sed -i 's/vmx-11/vmx-10/g' photon-custom-hw10.ovf
rm -f $PHOTON_IMG_OUTPUT_PATH/temp/photon-custom.mf
openssl sha1 *.vmdk photon-custom-hw10.ovf > photon-custom-hw10.mf
tar cf photon-custom-hw10-$PHOTON_RELEASE_VER-$PHOTON_BUILD_NUM.ova photon-custom-hw10.ovf photon-custom-hw10.mf photon-custom-disk1.vmdk
mv $PHOTON_IMG_OUTPUT_PATH/temp1/photon-custom-hw10-$PHOTON_RELEASE_VER-$PHOTON_BUILD_NUM.ova $PHOTON_IMG_OUTPUT_PATH/

cd $PHOTON_IMG_OUTPUT_PATH
rm -rf $PHOTON_IMG_OUTPUT_PATH/temp/
rm -rf $PHOTON_IMG_OUTPUT_PATH/temp1/
rm -f $PHOTON_IMG_OUTPUT_PATH/photon-ova.raw
