#!/bin/bash

#################################################
#	Title:	cloud-image-build.sh		#
#        Date:	2015-07-22   	 		#
#     Version:	1.0				#
#      Author:	anishs@vmware.com		#
#################################################
#	Overview
#		Create cloud images
#	End
#

set -x
PHOTON_ISO_PATH=$1
BUILD_SCRIPTS_FOLDER=$2
IMG_NAME=$3
SRC_ROOT=$4
GENERATED_DATA_PATH=$5
PHOTON_STAGE_PATH="${PHOTON_ISO_PATH%/*}"
INSTALLER_PATH=$PHOTON_STAGE_PATH/$IMG_NAME

PHOTON_IMG_OUTPUT_PATH=$PHOTON_STAGE_PATH/$IMG_NAME

VMDK_CONFIG_FILE=${BUILD_SCRIPTS_FOLDER}/$IMG_NAME/vmdk_$IMG_NAME.json
VMDK_CONFIG_SAFE_FILE=${BUILD_SCRIPTS_FOLDER}/$IMG_NAME/vmdk_safe_$IMG_NAME.json
ISO_MOUNT_FOLDER=$PHOTON_STAGE_PATH/iso_mount

mkdir -p $ISO_MOUNT_FOLDER
mkdir -p $INSTALLER_PATH/installer
cp -R $SRC_ROOT/installer $INSTALLER_PATH/

cd $INSTALLER_PATH/installer
cp $VMDK_CONFIG_FILE $VMDK_CONFIG_SAFE_FILE
cp ${BUILD_SCRIPTS_FOLDER}/mk-setup-vmdk.sh .
cp ${BUILD_SCRIPTS_FOLDER}/mk-clean-vmdk.sh .

if [ $IMG_NAME != "ova" ]
  then
    cp ${BUILD_SCRIPTS_FOLDER}/mk-setup-grub.sh .
fi

if [ -e ${BUILD_SCRIPTS_FOLDER}/${IMG_NAME}/mk-setup-grub.sh ]
  then
    cp ${BUILD_SCRIPTS_FOLDER}/${IMG_NAME}/mk-setup-grub.sh .
fi

if [ -e ${BUILD_SCRIPTS_FOLDER}/${IMG_NAME}/mk-setup-vmdk.sh ]
  then
    cp ${BUILD_SCRIPTS_FOLDER}/${IMG_NAME}/mk-setup-vmdk.sh .
fi

if [ -e ${BUILD_SCRIPTS_FOLDER}/${IMG_NAME}/mk-clean-vmdk.sh ]
  then
    cp ${BUILD_SCRIPTS_FOLDER}/${IMG_NAME}/mk-clean-vmdk.sh .
fi

PASSWORD=`date | md5sum | cut -f 1 -d ' '`
sed -i "s/PASSWORD/$PASSWORD/" $VMDK_CONFIG_SAFE_FILE
cat $VMDK_CONFIG_SAFE_FILE
./photonInstaller.py -p $GENERATED_DATA_PATH/build_install_options_$IMG_NAME.json -r $PHOTON_STAGE_PATH/RPMS -v $INSTALLER_PATH/photon-${IMG_NAME} -o $GENERATED_DATA_PATH -f $VMDK_CONFIG_SAFE_FILE
rm $VMDK_CONFIG_SAFE_FILE


cd $BUILD_SCRIPTS_FOLDER



DISK_DEVICE=`losetup --show -f ${PHOTON_IMG_OUTPUT_PATH}/photon-${IMG_NAME}.raw`

echo "Mapping device partition to loop device"
kpartx -av $DISK_DEVICE

DEVICE_NAME=`echo $DISK_DEVICE|cut -c6- `

echo "DISK_DEVICE=$DISK_DEVICE"
echo "ROOT_PARTITION=/dev/mapper/${DEVICE_NAME}p2"

rm -rf $PHOTON_IMG_OUTPUT_PATH/photon-${IMG_NAME}
mkdir $PHOTON_IMG_OUTPUT_PATH/photon-${IMG_NAME}

mount -v -t ext4 /dev/mapper/${DEVICE_NAME}p2 $PHOTON_IMG_OUTPUT_PATH/photon-${IMG_NAME}
rm -rf $PHOTON_IMG_OUTPUT_PATH/photon-${IMG_NAME}/installer
rm -rf $PHOTON_IMG_OUTPUT_PATH/photon-${IMG_NAME}/LOGS
cp $PHOTON_IMG_OUTPUT_PATH/photon-${IMG_NAME}/etc/shadow $PHOTON_IMG_OUTPUT_PATH/photon-${IMG_NAME}/etc/shadow.bak
sed -e "s/^\(root:\)[^:]*:/\1*:/" $PHOTON_IMG_OUTPUT_PATH/photon-${IMG_NAME}/etc/shadow.bak > $PHOTON_IMG_OUTPUT_PATH/photon-${IMG_NAME}/etc/shadow
rm -f $PHOTON_IMG_OUTPUT_PATH/photon-${IMG_NAME}/etc/shadow.bak
rm -f $PHOTON_IMG_OUTPUT_PATH/photon-${IMG_NAME}/etc/shadow-

if [ $IMG_NAME != "ova" ]
  then
    mount -o bind /proc $PHOTON_IMG_OUTPUT_PATH/photon-${IMG_NAME}/proc
    mount -o bind /dev $PHOTON_IMG_OUTPUT_PATH/photon-${IMG_NAME}/dev
    mount -o bind /dev/pts $PHOTON_IMG_OUTPUT_PATH/photon-${IMG_NAME}/dev/pts
    mount -o bind /sys $PHOTON_IMG_OUTPUT_PATH/photon-${IMG_NAME}/sys
    if [ $IMG_NAME = "gce" ]
      then
        cp ntpd.service $PHOTON_IMG_OUTPUT_PATH/photon-${IMG_NAME}/lib/systemd/system/
    fi
    cp ntpd.service $PHOTON_IMG_OUTPUT_PATH/photon-${IMG_NAME}/lib/systemd/system/
    cp eth0.service $PHOTON_IMG_OUTPUT_PATH/photon-${IMG_NAME}/lib/systemd/system/
    cp -f docker.service $PHOTON_IMG_OUTPUT_PATH/photon-${IMG_NAME}/lib/systemd/system/
    cp -f docker.socket $PHOTON_IMG_OUTPUT_PATH/photon-${IMG_NAME}/lib/systemd/system/
    if [ -e $IMG_NAME/cloud-photon.cfg ]
    then
        cp -f $IMG_NAME/cloud-photon.cfg $PHOTON_IMG_OUTPUT_PATH/photon-${IMG_NAME}/etc/cloud/cloud.cfg
    fi
    
    cp $IMG_NAME/$IMG_NAME-patch.sh $PHOTON_IMG_OUTPUT_PATH/photon-${IMG_NAME}/


    cp /etc/resolv.conf $PHOTON_IMG_OUTPUT_PATH/photon-${IMG_NAME}/etc/
    echo "chrooting and running patch inside the chroot"
    chroot $PHOTON_IMG_OUTPUT_PATH/photon-${IMG_NAME} /bin/bash -c "/$IMG_NAME-patch.sh"
    rm -f $PHOTON_IMG_OUTPUT_PATH/photon-${IMG_NAME}/$IMG_NAME-patch.sh

    umount $PHOTON_IMG_OUTPUT_PATH/photon-${IMG_NAME}/sys
    umount $PHOTON_IMG_OUTPUT_PATH/photon-${IMG_NAME}/dev/pts
    umount $PHOTON_IMG_OUTPUT_PATH/photon-${IMG_NAME}/dev
    umount $PHOTON_IMG_OUTPUT_PATH/photon-${IMG_NAME}/proc
fi
umount $PHOTON_IMG_OUTPUT_PATH/photon-${IMG_NAME}

echo "Deleting device map partition"
kpartx -d $DISK_DEVICE

rm -rf photon-${IMG_NAME}

echo "Detaching loop device from raw disk"
losetup -d $DISK_DEVICE


cd $IMG_NAME
./mk-$IMG_NAME-image.sh $PHOTON_STAGE_PATH/$IMG_NAME $SRC_ROOT

exit 0
