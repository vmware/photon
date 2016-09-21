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
BUILD_SCRIPTS_PATH=$1
IMG_NAME=$2
SRC_ROOT=$3
GENERATED_DATA_PATH=$4
PHOTON_ISO_PATH=$5
PHOTON_STAGE_PATH=${PHOTON_ISO_PATH%/*}
ADDITIONAL_RPMS_PATH=$6
INSTALLER_PATH=$PHOTON_STAGE_PATH/$IMG_NAME
ISO_MOUNT_FOLDER=$PHOTON_STAGE_PATH/iso_mount

PHOTON_IMG_OUTPUT_PATH=$PHOTON_STAGE_PATH/$IMG_NAME
VMDK_CONFIG_FILE=${BUILD_SCRIPTS_PATH}/$IMG_NAME/vmdk_$IMG_NAME.json
VMDK_CONFIG_SAFE_FILE=${BUILD_SCRIPTS_PATH}/$IMG_NAME/vmdk_safe_$IMG_NAME.json

mkdir -p $INSTALLER_PATH/installer
cp -R $SRC_ROOT/installer $INSTALLER_PATH/

cd $INSTALLER_PATH/installer
cp $VMDK_CONFIG_FILE $VMDK_CONFIG_SAFE_FILE
cp ${BUILD_SCRIPTS_PATH}/mk-setup-vmdk.sh .
cp ${BUILD_SCRIPTS_PATH}/mk-clean-vmdk.sh .


if [[ $IMG_NAME != ova* ]]
  then
    cp ${BUILD_SCRIPTS_PATH}/mk-setup-grub.sh .
fi

if [ -e ${BUILD_SCRIPTS_PATH}/${IMG_NAME}/mk-setup-grub.sh ]
  then
    cp ${BUILD_SCRIPTS_PATH}/${IMG_NAME}/mk-setup-grub.sh .
fi

PASSWORD=`date | md5sum | cut -f 1 -d ' '`
sed -i "s/PASSWORD/$PASSWORD/" $VMDK_CONFIG_SAFE_FILE

if [ -n "$ADDITIONAL_RPMS_PATH" ]
  then
    mkdir $PHOTON_STAGE_PATH/RPMS/additonal
    cp -f $ADDITIONAL_RPMS_PATH/* $PHOTON_STAGE_PATH/RPMS/additonal/
fi

./photonInstaller.py -p $GENERATED_DATA_PATH/build_install_options_$IMG_NAME.json -r $PHOTON_STAGE_PATH/RPMS -v $INSTALLER_PATH/photon-${IMG_NAME} -o $GENERATED_DATA_PATH -f $VMDK_CONFIG_SAFE_FILE
cat $VMDK_CONFIG_SAFE_FILE
rm $VMDK_CONFIG_SAFE_FILE

cd $BUILD_SCRIPTS_PATH

DISK_DEVICE=`losetup --show -f ${PHOTON_IMG_OUTPUT_PATH}/photon-${IMG_NAME}.raw`

echo "Mapping device partition to loop device"
kpartx -av $DISK_DEVICE

DEVICE_NAME=`echo $DISK_DEVICE|cut -c6- `

echo "DISK_DEVICE=$DISK_DEVICE"
echo "ROOT_PARTITION=/dev/mapper/${DEVICE_NAME}p2"

rm -rf $PHOTON_IMG_OUTPUT_PATH/photon-${IMG_NAME}
mkdir $PHOTON_IMG_OUTPUT_PATH/photon-${IMG_NAME}

UUID_VALUE=$(blkid -s UUID -o value /dev/mapper/${DEVICE_NAME}p2)

mkdir -p $ISO_MOUNT_FOLDER
mount -o loop $PHOTON_ISO_PATH $ISO_MOUNT_FOLDER
mount -v -t ext4 /dev/mapper/${DEVICE_NAME}p2 $PHOTON_IMG_OUTPUT_PATH/photon-${IMG_NAME}
rm -rf $PHOTON_IMG_OUTPUT_PATH/photon-${IMG_NAME}/installer
rm -rf $PHOTON_IMG_OUTPUT_PATH/photon-${IMG_NAME}/LOGS
cp $PHOTON_IMG_OUTPUT_PATH/photon-${IMG_NAME}/etc/shadow $PHOTON_IMG_OUTPUT_PATH/photon-${IMG_NAME}/etc/shadow.bak
sed -e "s/^\(root:\)[^:]*:/\1*:/" $PHOTON_IMG_OUTPUT_PATH/photon-${IMG_NAME}/etc/shadow.bak > $PHOTON_IMG_OUTPUT_PATH/photon-${IMG_NAME}/etc/shadow
rm -f $PHOTON_IMG_OUTPUT_PATH/photon-${IMG_NAME}/etc/shadow.bak
rm -f $PHOTON_IMG_OUTPUT_PATH/photon-${IMG_NAME}/etc/shadow-
rm -f $PHOTON_IMG_OUTPUT_PATH/photon-${IMG_NAME}/etc/machine-id
touch $PHOTON_IMG_OUTPUT_PATH/photon-${IMG_NAME}/etc/machine-id
rm -f $PHOTON_IMG_OUTPUT_PATH/photon-${IMG_NAME}/etc/fstab
echo "UUID=$UUID_VALUE    /    ext4    defaults 1 1" >> $PHOTON_IMG_OUTPUT_PATH/photon-${IMG_NAME}/etc/fstab

mkdir -p $PHOTON_IMG_OUTPUT_PATH/photon-${IMG_NAME}/var/lib/cloud/seed/nocloud
cat << EOF >> $PHOTON_IMG_OUTPUT_PATH/photon-${IMG_NAME}/var/lib/cloud/seed/nocloud/meta-data
instance-id: iid-local01
local-hostname: photon-machine
EOF
cat << EOF >> $PHOTON_IMG_OUTPUT_PATH/photon-${IMG_NAME}/var/lib/cloud/seed/nocloud/user-data
#cloud-config

runcmd:
  - (echo -ne 'photon-';cat /dev/urandom | tr -dc 'a-zA-Z0-9' | head -c 9)|xargs hostnamectl set-hostname
  - hostname | xargs -I '{}' sed -i 's/photon-.*$/{}/g' /etc/hosts
  - systemctl status systemd-resolved >/dev/null || systemctl restart systemd-resolved
EOF

mount -o bind /proc $PHOTON_IMG_OUTPUT_PATH/photon-${IMG_NAME}/proc
mount -o bind /dev $PHOTON_IMG_OUTPUT_PATH/photon-${IMG_NAME}/dev
mount -o bind /dev/pts $PHOTON_IMG_OUTPUT_PATH/photon-${IMG_NAME}/dev/pts
mount -o bind /sys $PHOTON_IMG_OUTPUT_PATH/photon-${IMG_NAME}/sys
if [ -n "$ADDITIONAL_RPMS_PATH" ]
  then
    mkdir $PHOTON_IMG_OUTPUT_PATH/photon-${IMG_NAME}/additional_rpms
    mkdir $PHOTON_IMG_OUTPUT_PATH/photon-${IMG_NAME}/var/run
    cp -f $PHOTON_STAGE_PATH/RPMS/additonal/* $PHOTON_IMG_OUTPUT_PATH/photon-${IMG_NAME}/additional_rpms/
    chroot $PHOTON_IMG_OUTPUT_PATH/photon-${IMG_NAME} /bin/bash -c "rpm -i /additional_rpms/*"
    rm -rf $PHOTON_IMG_OUTPUT_PATH/photon-${IMG_NAME}/additional_rpms/
fi

if [ $IMG_NAME != "ova" ] && [ $IMG_NAME != "ova_uefi" ] && [ $IMG_NAME != "ova_ovs" ]
  then
    cd $BUILD_SCRIPTS_PATH
    if [ $IMG_NAME = "gce" ]
      then
        cp ntpd.service $PHOTON_IMG_OUTPUT_PATH/photon-${IMG_NAME}/lib/systemd/system/
        cp eth0.service $PHOTON_IMG_OUTPUT_PATH/photon-${IMG_NAME}/lib/systemd/system/
    fi
    if [ $IMG_NAME != "ova_generic" ]
      then
        if [ -e $IMG_NAME/cloud-photon.cfg ]
          then
            cp -f $IMG_NAME/cloud-photon.cfg $PHOTON_IMG_OUTPUT_PATH/photon-${IMG_NAME}/etc/cloud/cloud.cfg
        fi
        cp $IMG_NAME/$IMG_NAME-patch.sh $PHOTON_IMG_OUTPUT_PATH/photon-${IMG_NAME}/
        cp /etc/resolv.conf $PHOTON_IMG_OUTPUT_PATH/photon-${IMG_NAME}/etc/
        echo "chrooting and running patch inside the chroot"
        chroot $PHOTON_IMG_OUTPUT_PATH/photon-${IMG_NAME} /bin/bash -c "/$IMG_NAME-patch.sh"
        rm -f $PHOTON_IMG_OUTPUT_PATH/photon-${IMG_NAME}/$IMG_NAME-patch.sh
        # Change the max password days to 99999
        chroot $PHOTON_IMG_OUTPUT_PATH/photon-${IMG_NAME} /bin/bash -c "cat /etc/shadow | cut -d: -f1 | xargs -I {} chage -I -1 -m 0 -M 99999 -E -1 -W 7 {}"
        sed -i 's/^PASS_MAX_DAYS.*/PASS_MAX_DAYS   99999/' $PHOTON_IMG_OUTPUT_PATH/photon-${IMG_NAME}/etc/login.defs
    fi
fi
umount $PHOTON_IMG_OUTPUT_PATH/photon-${IMG_NAME}/sys
umount $PHOTON_IMG_OUTPUT_PATH/photon-${IMG_NAME}/dev/pts
umount $PHOTON_IMG_OUTPUT_PATH/photon-${IMG_NAME}/dev
umount $PHOTON_IMG_OUTPUT_PATH/photon-${IMG_NAME}/proc
umount $PHOTON_IMG_OUTPUT_PATH/photon-${IMG_NAME}
umount $ISO_MOUNT_FOLDER
rm -rf $ISO_MOUNT_FOLDER

echo "Deleting device map partition"
kpartx -d $DISK_DEVICE

rm -rf photon-${IMG_NAME}

echo "Detaching loop device from raw disk"
losetup -d $DISK_DEVICE


cd $IMG_NAME
./mk-$IMG_NAME-image.sh $PHOTON_STAGE_PATH/$IMG_NAME $SRC_ROOT

exit 0
