#!/bin/bash
#################################################
#       Title:  mk-mount-disk                   #
#        Date:  2014-11-26                      #
#     Version:  1.0                             #
#      Author:  mbassiouny@vmware.com           #
#     Options:                                  #
#################################################
#	Overview
#		This mount a partition passed in arguments or a in the config.inc in root photon mount directory
#	End
#
set -o errexit		# exit if error...insurance ;
set -o nounset		# exit if variable not initalized
set +h			# disable hashall
PRGNAME=${0##*/}	# script name minus the path
SCRIPT_PATH=$(dirname $(realpath -s $0))
source $SCRIPT_PATH/config.inc		#	configuration parameters
source $SCRIPT_PATH/function.inc
LOGFILE=/var/log/"${PRGNAME}-${LOGFILE}"	#	set log file name
#LOGFILE=/dev/null		#	uncomment to disable log file
[ ${EUID} -eq 0 ]	|| fail "${PRGNAME}: Need to be root user: FAILURE"
> ${LOGFILE}		#	clear/initialize logfile

while [[ $# > 0 ]]
do
    key="$1"
    shift
 
    case $key in
        -p|--partitionmountpoint)
        PARTITION="$1"
        MOUNTPOINT="$2"
        shift 2

        # make sure the directory exists
        run_command "Making Directory" "mkdir -p ${BUILDROOT}${MOUNTPOINT}" "${LOGFILE}"
        run_command "Mounting Partition" "mount -v ${PARTITION} ${BUILDROOT}${MOUNTPOINT}" "${LOGFILE}"
    ;;
    *)
        # unknown option
    ;;
    esac
done

