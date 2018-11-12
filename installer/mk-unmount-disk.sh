#!/bin/bash
#################################################
#       Title:  mk-unmount-disk                 #
#        Date:  2014-11-26                      #
#     Version:  1.0                             #
#      Author:  mbassiouny@vmware.com           #
#     Options:                                  #
#################################################
#   Overview
#       This unmount the mounted directories after installing photon
#   End
#
set -o errexit      # exit if error...insurance ;
set -o nounset      # exit if variable not initalized
set +h          # disable hashall
SCRIPT_PATH=$(dirname $(realpath -s $0))
source $SCRIPT_PATH/config.inc
PRGNAME=${0##*/}    # script name minus the path
LOGFILE=/var/log/"${PRGNAME}-${LOGFILE}"    #   set log file name
#LOGFILE=/dev/null      #   uncomment to disable log file
[ ${EUID} -eq 0 ]   || fail "${PRGNAME}: Need to be root user: FAILURE"
[ -z ${BUILDROOT} ]     && fail "${PRGNAME}: BUILDROOT not set: FAILURE"

if mountpoint ${BUILDROOT}/run >/dev/null 2>&1; then umount -l ${BUILDROOT}/run; fi
if mountpoint ${BUILDROOT}/sys >/dev/null 2>&1; then umount -l ${BUILDROOT}/sys; fi
if mountpoint ${BUILDROOT}/proc    >/dev/null 2>&1; then umount -l ${BUILDROOT}/proc; fi
if mountpoint ${BUILDROOT}/dev >/dev/null 2>&1; then umount -l -R ${BUILDROOT}/dev; fi
sync
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
        if mountpoint ${BUILDROOT}${MOUNTPOINT} >/dev/null 2>&1; then umount -l ${BUILDROOT}${MOUNTPOINT}; fi
        sync
    ;;
    *)
        # unknown option
    ;;
    esac
done
exit 0
