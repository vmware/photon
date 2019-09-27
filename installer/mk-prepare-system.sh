#!/bin/bash
#################################################
#       Title:  mk-prepare-system               #
#        Date:  2014-11-26                      #
#     Version:  1.0                             #
#      Author:  mbassiouny@vmware.com           #
#     Options:                                  #
#################################################
#   Overview
#       Preparing the system to install photon
#   End
#
set -o errexit      # exit if error...insurance ;
set -o nounset      # exit if variable not initalized
set +h          # disable hashall
set -x
SCRIPT_PATH=$(dirname $(realpath -s $0))
source $SCRIPT_PATH/config.inc
source $SCRIPT_PATH/function.inc
PRGNAME=${0##*/}    # script name minus the path

LOGFILE=/var/log/"${PRGNAME}-${LOGFILE}"    #   set log file name
#LOGFILE=/dev/null      #   uncomment to disable log file

[ ${EUID} -eq 0 ]   || fail "${PRGNAME}: Need to be root user: FAILURE"
[ -z ${BUILDROOT} ] && fail "${PRGNAME}: Build root not set: FAILURE"

WORKINGDIR=$1
RPMS_PATH=$2

if mountpoint ${BUILDROOT}/run  >/dev/null 2>&1; then umount ${BUILDROOT}/run; fi
if mountpoint ${BUILDROOT}/sys  >/dev/null 2>&1; then umount ${BUILDROOT}/sys; fi
if mountpoint ${BUILDROOT}/proc >/dev/null 2>&1; then umount ${BUILDROOT}/proc; fi
if mountpoint ${BUILDROOT}/dev/pts  >/dev/null 2>&1; then umount ${BUILDROOT}/dev/pts; fi
if mountpoint ${BUILDROOT}/dev  >/dev/null 2>&1; then umount ${BUILDROOT}/dev; fi
sync
[ ${EUID} -eq 0 ]   || fail "${PRGNAME}: Need to be root user: FAILURE"

mkdir -p ${BUILDROOT}/var/lib/rpm
mkdir -p ${BUILDROOT}/cache/tdnf
rpm   --root ${BUILDROOT} --initdb
# tdnf conf is created in working directory which is parent of buildroot
tdnf install filesystem --installroot ${BUILDROOT} --assumeyes -c ${WORKINGDIR}/tdnf.conf || \
    docker run -v $RPMS_PATH:$RPMS_PATH -v $WORKINGDIR:$WORKINGDIR photon:3.0 \
	tdnf install filesystem --installroot ${BUILDROOT} --assumeyes -c ${WORKINGDIR}/tdnf.conf
 
#   Ommited in the filesystem.spec file - not needed for booting
[ -e ${BUILDROOT}/dev/console ] || mknod -m 600 ${BUILDROOT}/dev/console c 5 1
[ -e ${BUILDROOT}/dev/null ]    || mknod -m 666 ${BUILDROOT}/dev/null c 1 3
[ -e ${BUILDROOT}/dev/random ]  || mknod -m 444 ${BUILDROOT}/dev/random c 1 8
[ -e ${BUILDROOT}/dev/urandom ] || mknod -m 444 ${BUILDROOT}/dev/urandom c 1 9

if [[   $# -eq 0 ]] || [[ $1 != 'install' ]]; then
    chown -R 0:0 ${BUILDROOT}/* || :
fi

#   Mount kernel filesystem
#
if ! mountpoint ${BUILDROOT}/dev    >/dev/null 2>&1; then mount --bind /dev ${BUILDROOT}/dev; fi
if ! mountpoint ${BUILDROOT}/dev/pts    >/dev/null 2>&1; then mount -t devpts devpts ${BUILDROOT}/dev/pts -o gid=5,mode=620; fi
if ! mountpoint ${BUILDROOT}/proc   >/dev/null 2>&1; then mount -t proc proc ${BUILDROOT}/proc; fi
if ! mountpoint ${BUILDROOT}/sys    >/dev/null 2>&1; then mount -t sysfs sysfs ${BUILDROOT}/sys; fi
if ! mountpoint ${BUILDROOT}/run    >/dev/null 2>&1; then mount -t tmpfs tmpfs ${BUILDROOT}/run; fi
if [ -h ${BUILDROOT}/dev/shm ];          then mkdir -pv ${BUILDROOT}/$(readlink ${BUILDROOT}/dev/shm); fi
exit 0
