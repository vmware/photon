#!/bin/bash
#################################################
#	Title:	mk-setup-vmdk			#
#        Date:	2014-11-14   	 		#
#     Version:	1.0				#
#      Author:	dthaluru@vmware.com		#
#     Options:					#
#################################################
#	Overview
#		Creating hard disk with photon on it
#	End
#
set -o errexit		# exit if error...insurance ;)
set -o nounset		# exit if variable not initalized
set +h			# disable hashall
PRGNAME=${0##*/}	# script name minus the path
SCRIPT_PATH=$(dirname $(realpath -s $0))
INSTALLER_PATH=$SCRIPT_PATH/../../../installer
source ${INSTALLER_PATH}/config.inc		#	configuration parameters
source ${INSTALLER_PATH}/function.inc		#	commonn functions
LOGFILE="/var/log/${PRGNAME}-${LOGFILE}"	#	set log file name
LFS_DISK="/mnt/photon-disk"
[ ${EUID} -eq 0 ]	|| die "${PRGNAME}: Need to be root user: FAILURE"
> ${LOGFILE}		#	clear/initialize logfile

echo -e "Setting up the disk...\n"
set -x
LFS_OPTION=""
VMDK_IMAGE_NAME=mydisk.vmdk
ROOT_PARTITION_SIZE=1
SWAP_PARTITION_SIZE=0
BOOT_FIRM_WARE="bios"

while [[ $# > 0 ]]
do
	key="$1"
	shift
 
	case $key in
		-rp|--ROOT_PARTITION_SIZE)
		ROOT_PARTITION_SIZE="$1"
		shift
	;;
		-sp|--SWAP_PARTITION_SIZE)
		SWAP_PARTITION_SIZE="$1"
		shift
	;;
		-fm|--firmware)
		BOOT_FIRM_WARE="$1"
		shift

	;;
		-a|--all)
		LFS_OPTION="all"
	;;
		-m|--minimal)
		LFS_OPTION=""
	;;
		-n|--IMG_NAME)
		VMDK_IMAGE_NAME="$1".raw
		shift
	;;
		-h|--help)
		echo 'Usage:'
		echo '-rp|--ROOT_PARTITION_SIZE :sets root partition size'
		echo '-sp|--SWAP_PARTITION_SIZE :sets swap partition size'
		echo '-a|--all                  :installs all available packages'
		echo '-n|--IMG_NAME             :sets name of the vmdk image'
		echo '-m|--minimal              :installs basic packages'
		echo '-fm|--firmware            :firmware'
		exit 0
	;;
	*)
		# unknown option
	;;
	esac
done

mkdir -p $LFS_DISK

TOTAL_SIZE=` echo $ROOT_PARTITION_SIZE + $SWAP_PARTITION_SIZE | bc`

echo "Creating raw disk file " $VMDK_IMAGE_NAME " of size " $TOTAL_SIZE
# hack to create 512MB image instead of 1GB - use 512 instead of 1024
dd if=/dev/zero of=$VMDK_IMAGE_NAME bs=1024 count=$(($TOTAL_SIZE * 1024 * 2048))
chmod 755 $VMDK_IMAGE_NAME

parted -s $VMDK_IMAGE_NAME 'mklabel msdos mkpart primary fat32 1M 89MB mkpart primary ext4 89MB 1112MB mkpart primary ext4 1112MB 100%'

echo "Associating loopdevice to raw disk"
DISK_DEVICE=`losetup --show -f -P $VMDK_IMAGE_NAME`

#echo "Creating partition on raw disk"
#if [ $SWAP_PARTITION_SIZE -gt 0 ] 
#then
#      sgdisk -n 1::+8M -n 2::+${ROOT_PARTITION_SIZE}G -n 3: -p $DISK_DEVICE >> $LOGFILE
#else
#      sgdisk -n 1::+8M -n 2: -p $DISK_DEVICE >> $LOGFILE
#fi

#if [ $BOOT_FIRM_WARE = "efi" ]
#then
#    echo "EFI boot partition"
#    sgdisk -t1:ef00 $DISK_DEVICE >> $LOGFILE
#else
#    echo "BIOS boot partition"
#    sgdisk -t1:ef02 $DISK_DEVICE >> $LOGFILE
#fi

echo "Mapping device partition to loop device"
kpartx -avs $DISK_DEVICE >> $LOGFILE

DEVICE_NAME=`echo $DISK_DEVICE|cut -c6- `

echo "Formatting partitions"
mkfs.ext4 -F -v -O ^huge_file -b 4096 -L rootfs /dev/mapper/${DEVICE_NAME}p3
mkfs.ext4 -F -v -b 4096 -L boot /dev/mapper/${DEVICE_NAME}p2
mkfs.fat -n EFI /dev/mapper/${DEVICE_NAME}p1

echo "DISK_DEVICE=$DISK_DEVICE"
echo "ROOT_PARTITION=/dev/mapper/${DEVICE_NAME}p3"
echo "BOOT_PARTITION=/dev/mapper/${DEVICE_NAME}p2"
echo "ESP_PARTITION=/dev/mapper/${DEVICE_NAME}p1"


