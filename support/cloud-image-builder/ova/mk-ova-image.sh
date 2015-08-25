#!/bin/bash
set -x
PHOTON_IMG_OUTPUT_PATH=$1
SRC_ROOT=$2

#Generate two ova images one with a random password and the other with a defined password

sed "s|VMDK_IMAGE|$PHOTON_IMG_OUTPUT_PATH/photon-ova.vmdk|" vmx-template > /tmp/vmx-temp.vmx
sed "s|VMDK_IMAGE|$PHOTON_IMG_OUTPUT_PATH/photon-custom.vmdk|" vmx-template > /tmp/vmx-temp-custom.vmx

cp update_custom_password.py $PHOTON_IMG_OUTPUT_PATH/

cd $SRC_ROOT/tools/src/vixDiskUtil
mkdir -p $SRC_ROOT/tools/bin
make clean
make
$SRC_ROOT/tools/bin/vixdiskutil -convert $PHOTON_IMG_OUTPUT_PATH/photon-ova.raw -cap 16000 $PHOTON_IMG_OUTPUT_PATH/photon-ova.vmdk
$SRC_ROOT/tools/bin/vixdiskutil -wmeta toolsVersion 2147483647 $PHOTON_IMG_OUTPUT_PATH/photon-ova.vmdk

cd $PHOTON_IMG_OUTPUT_PATH

mkdir -p $PHOTON_IMG_OUTPUT_PATH/temp
ovftool /tmp/vmx-temp.vmx $PHOTON_IMG_OUTPUT_PATH/temp/photon-ova.ovf
cd $PHOTON_IMG_OUTPUT_PATH/temp

sed -i "s/otherGuest/other3xLinux64Guest/g" $PHOTON_IMG_OUTPUT_PATH/temp/photon-ova.ovf
rm -f $PHOTON_IMG_OUTPUT_PATH/temp/photon-ova.mf
openssl sha1 *.vmdk photon-ova.ovf > photon-ova.mf
tar cf photon-ova.ova photon-ova.ovf photon-ova.mf photon-ova-disk1.vmdk

cp $PHOTON_IMG_OUTPUT_PATH/temp/photon-ova.ova $PHOTON_IMG_OUTPUT_PATH/
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
rm -f $PHOTON_IMG_OUTPUT_PATH/temp1/photon-custom.mf
openssl sha1 *.vmdk photon-custom.ovf > photon-custom.mf
tar cf photon-custom.ova photon-custom.ovf photon-custom.mf photon-custom-disk1.vmdk
cp $PHOTON_IMG_OUTPUT_PATH/temp1/photon-custom.ova $PHOTON_IMG_OUTPUT_PATH/
cd $PHOTON_IMG_OUTPUT_PATH
rm -rf $PHOTON_IMG_OUTPUT_PATH/temp/
rm -rf $PHOTON_IMG_OUTPUT_PATH/temp1/
