#!/bin/bash
#################################################
#	Title:	mk-clean-vmdk			#
#        Date:	2015-02-10   	 		#
#     Version:	1.0				#
#      Author:	mbassiouny@vmware.com		#
#     Options:					#
#################################################
#	Overview
#		Cleaning up vmdk creation process
#	End
#
set -o errexit		# exit if error...insurance ;)
set -o nounset		# exit if variable not initalized
set +h			# disable hashall
PRGNAME=${0##*/}	# script name minus the path
SCRIPT_PATH=$(dirname $(realpath -s $0))
INSTALLER_PATH=$SCRIPT_PATH/../../installer
source ${INSTALLER_PATH}/config.inc		#	configuration parameters
LOGFILE="/var/log/${PRGNAME}-${LOGFILE}"	#	set log file name
LFS_DISK="/mnt/photon-disk"
[ ${EUID} -eq 0 ]	|| { echo "${PRGNAME}: Need to be root user: FAILURE"; exit 1; }
> ${LOGFILE}		#	clear/initialize logfile

# Check if passing DISK-DEVICE
[ $# -eq 1 ] || { echo "Invalid arguments, you should pass disk device"; exit 1; }
DISK_DEVICE=$1

echo "Deleting device map parition"
kpartx -d $DISK_DEVICE >> $LOGFILE

echo "Detaching loop device from vmdk"
losetup -d $DISK_DEVICE

