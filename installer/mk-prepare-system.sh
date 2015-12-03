#!/bin/bash
#################################################
#       Title:  mk-prepare-system               #
#        Date:  2014-11-26                      #
#     Version:  1.0                             #
#      Author:  mbassiouny@vmware.com           #
#     Options:                                  #
#################################################
#	Overview
#		Preparing the system to install photon
#	End
#
set -o errexit		# exit if error...insurance ;
set -o nounset		# exit if variable not initalized
set +h			# disable hashall
source config.inc
source function.inc
PRGNAME=${0##*/}	# script name minus the path

LOGFILE=/var/log/"${PRGNAME}-${LOGFILE}"	#	set log file name
#LOGFILE=/dev/null		#	uncomment to disable log file

[ ${EUID} -eq 0 ] 	|| fail "${PRGNAME}: Need to be root user: FAILURE"
[ -z ${BUILDROOT} ]	&& fail "${PRGNAME}: Build root not set: FAILURE"

if mountpoint ${BUILDROOT}/run	>/dev/null 2>&1; then umount ${BUILDROOT}/run; fi
if mountpoint ${BUILDROOT}/sys	>/dev/null 2>&1; then umount ${BUILDROOT}/sys; fi
if mountpoint ${BUILDROOT}/proc	>/dev/null 2>&1; then umount ${BUILDROOT}/proc; fi
if mountpoint ${BUILDROOT}/dev/pts	>/dev/null 2>&1; then umount ${BUILDROOT}/dev/pts; fi
if mountpoint ${BUILDROOT}/dev	>/dev/null 2>&1; then umount ${BUILDROOT}/dev; fi
[ ${EUID} -eq 0 ]	|| fail "${PRGNAME}: Need to be root user: FAILURE"

cd ${BUILDROOT} || fail "${PRGNAME}: Change directory: ${BUILDROOT}: FAILURE"

#
#	Setup the filesystem for chapter 06
#
if [[	$# -gt 0 ]] && [[ $1 == 'install' ]]; then
	mkdir -p ${BUILDROOT}/var/lib/rpm
	rpm   --root ${BUILDROOT} --initdb
    tdnf install filesystem --installroot ${BUILDROOT} --nogpgcheck --assumeyes
else
	RPMPKG="$(find RPMS -name 'filesystem-[0-9]*.rpm' -print)"
	[ -z ${RPMPKG} ] && fail "	Filesystem rpm package missing: Can not continue"
	run_command "	Installing filesystem" "rpm -Uvh --nodeps --root ${BUILDROOT} --dbpath /var/lib/rpm ${RPMPKG}" "${LOGFILE}"
fi
 
# 	Ommited in the filesystem.spec file - not needed for booting
[ -e ${BUILDROOT}/dev/console ]	|| mknod -m 600 ${BUILDROOT}/dev/console c 5 1
[ -e ${BUILDROOT}/dev/null ]    || mknod -m 666 ${BUILDROOT}/dev/null c 1 3
[ -e ${BUILDROOT}/dev/random ]  || mknod -m 444 ${BUILDROOT}/dev/random c 1 8
[ -e ${BUILDROOT}/dev/urandom ] || mknod -m 444 ${BUILDROOT}/dev/urandom c 1 9

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
