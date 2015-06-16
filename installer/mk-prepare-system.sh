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

if [ $# -lt 1 ]; then
   echo "Usage: $PRGNAME <tools path>"
   exit 1
fi

TOOLS_PATH=$1

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

#
# Setup tools if tools.tar.gz already exists
#
[ -b $TOOLS_PATH/tools.tar.gz ] || {
	run_command " Uncompressing tools" "tar -C ${BUILDROOT} -xzvf $TOOLS_PATH/tools.tar.gz" "${LOGFILE}"
		
	rm -rf /tools || true
	if [ ! -e /tools ]; then 
		ln -s ${BUILDROOT}/tools /tools || true
    fi
    PATH=$PATH:/tools/bin
    }
cd ${BUILDROOT} || fail "${PRGNAME}: Change directory: ${BUILDROOT}: FAILURE"
#
#	Setup the filesystem for chapter 06
#
mkdir -p LOGS
RPMPKG="$(find RPMS -name 'filesystem-[0-9]*.rpm' -print)"
[ -z ${RPMPKG} ] && fail "	Filesystem rpm package missing: Can not continue"
run_command "	Installing filesystem" "rpm -Uvh --nodeps --root ${BUILDROOT} ${RPMPKG}" "LOGS/filesystem.completed"
run_command "	Creating symlinks: /tools/bin/{bash,cat,echo,pwd,stty}" "ln -fsv /tools/bin/{bash,cat,echo,pwd,stty} ${BUILDROOT}/bin"   "LOGS/filesystem.completed"
run_command "	Creating symlinks: /tools/bin/perl /usr/bin" "ln -fsv /tools/bin/perl ${BUILDROOT}/usr/bin" "LOGS/filesystem.completed"
run_command "	Creating symlinks: /tools/lib/libgcc_s.so{,.1}" "ln -fsv /tools/lib/libgcc_s.so{,.1} ${BUILDROOT}/usr/lib" "LOGS/filesystem.completed"
run_command "	Creating symlinks: /tools/lib/libstdc++.so{,.6} /usr/lib" "ln -fsv /tools/lib/libstdc++.so{,.6} ${BUILDROOT}/usr/lib"	 "LOGS/filesystem.completed"
#run_command "	Sed: /usr/lib/libstdc++.la" "sed 's/tools/usr/' ${BUILDROOT}/tools/lib/libstdc++.la > ${BUILDROOT}/usr/lib/libstdc++.la" "LOGS/filesystem.completed"
run_command "	Creating symlinks: bash /bin/sh" "ln -fsv bash ${BUILDROOT}/bin/sh" "LOGS/filesystem.completed"

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
