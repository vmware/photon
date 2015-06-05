#!/bin/bash
#################################################
#	Title:	prepare-build-root.sh   			#
#        Date:	2014-12-12          			#
#     Version:	1.0				                #
#      Author:	sharathg@vmware.com             #
#################################################
set -o errexit
set -o nounset
set +h
source common.inc

PRGNAME=${0##*/}

if [ $# -lt 4 ]; then
    fail "${PRGNAME}: No build root specified. Usage : ${PRGNAME} <build-root> <spec-path> <rpm-path> <log-path>"
fi

#Clean up our build root first
BUILDROOT=$1
SPEC_PATH=$2
RPM_PATH=$3
LOG_PATH=$4
PARENT=/usr/src/photon

LOGFILE="$(date +%Y-%m-%d).log"
LOGFILE=$LOG_PATH/"${PRGNAME}-${LOGFILE}"

if mountpoint ${BUILDROOT}/run	>/dev/null 2>&1; then umount ${BUILDROOT}/run; fi
if mountpoint ${BUILDROOT}/sys	>/dev/null 2>&1; then umount ${BUILDROOT}/sys; fi
if mountpoint ${BUILDROOT}/proc	>/dev/null 2>&1; then umount ${BUILDROOT}/proc; fi
if mountpoint ${BUILDROOT}/dev/pts	>/dev/null 2>&1; then umount ${BUILDROOT}/dev/pts; fi
if mountpoint ${BUILDROOT}/dev	>/dev/null 2>&1; then umount ${BUILDROOT}/dev; fi

mkdir -p ${BUILDROOT}/tmp
mkdir -p ${BUILDROOT}${PARENT}
mkdir -p ${BUILDROOT}${PARENT}/RPMS/x86_64
mkdir -p ${BUILDROOT}${PARENT}/BUILD
mkdir -p ${BUILDROOT}${PARENT}/BUILDROOT
mkdir -p ${BUILDROOT}${PARENT}/LOGS
mkdir -p ${BUILDROOT}${PARENT}/SOURCES
mkdir -p ${BUILDROOT}${PARENT}/SPECS

#copy localegen files.
cp ./locale* ${BUILDROOT}${PARENT}/
#copy kernel config files
cp ./config* ${BUILDROOT}${PARENT}/

#copy our macros and set the processor count
#NUMPROCS=`nproc`
#let NUMPROCS=$NUMPROCS+1
#echo "%_smp_mflags -j${NUMPROCS}" >> ${BUILDROOT}/tools/etc/rpm/macros

#	Setup the filesystem for chapter 06
RPMPKG="$(find $RPM_PATH -name 'filesystem*.rpm' -print)"
if [ -z ${RPMPKG} ] ; then
run_command "	Extracting filesystem spec" "cp ${SPEC_PATH}/filesystem/filesystem.spec ${BUILDROOT}/${PARENT}/SPECS" "$LOG_PATH/filesystem.log"
run_command "	Building filesystem rpm " "rpmbuild -ba --nocheck --root ${BUILDROOT} --define \\\"_topdir ${PARENT}\\\" ${PARENT}/SPECS/filesystem.spec" "$LOG_PATH/filesystem.log"
run_command "	Extracting filesystem rpm" "cp ${BUILDROOT}/${PARENT}/RPMS/x86_64/filesystem*.rpm ${RPM_PATH}/x86_64/" "$LOG_PATH/filesystem.log"
fi
RPMPKGFILE="$(find ${RPM_PATH} -name 'filesystem*.rpm' -printf %f)"
[ -z ${RPMPKGFILE} ] && fail "	Filesystem rpm package missing: Can not continue"
run_command "	Installing filesystem " "rpm -Uvh --nodeps --root ${BUILDROOT} ${RPM_PATH}/x86_64/${RPMPKGFILE}" "$LOG_PATH/filesystem.completed"


# 	Ommited in the filesystem.spec file - not needed for booting
[ -e ${BUILDROOT}/dev/console ]	|| mknod -m 600 ${BUILDROOT}/dev/console c 5 1
[ -e ${BUILDROOT}/dev/null ]		|| mknod -m 666 ${BUILDROOT}/dev/null c 1 3
[ -e ${BUILDROOT}/dev/random ]    || mknod -m 444 ${BUILDROOT}/dev/random c 1 8
[ -e ${BUILDROOT}/dev/urandom ]    || mknod -m 444 ${BUILDROOT}/dev/urandom c 1 9

chown -R 0:0 ${BUILDROOT}/*	|| fail "${PRGNAME}: Changing ownership: ${BUILDROOT}: FAILURE"

#
#	Mount kernel filesystem
#
if ! mountpoint ${BUILDROOT}/dev	>/dev/null 2>&1; then mount --bind /dev ${BUILDROOT}/dev; fi
if ! mountpoint ${BUILDROOT}/dev/pts	>/dev/null 2>&1; then mount -t devpts devpts ${BUILDROOT}/dev/pts -o gid=5,mode=620; fi
if ! mountpoint ${BUILDROOT}/proc	>/dev/null 2>&1; then mount -t proc proc ${BUILDROOT}/proc; fi
if ! mountpoint ${BUILDROOT}/sys 	>/dev/null 2>&1; then mount -t sysfs sysfs ${BUILDROOT}/sys; fi
if ! mountpoint ${BUILDROOT}/run	>/dev/null 2>&1; then mount -t tmpfs tmpfs ${BUILDROOT}/run; fi
if [ -h ${BUILDROOT}/dev/shm ];			 then mkdir -pv ${BUILDROOT}/$(readlink ${BUILDROOT}/dev/shm); fi
exit 0
