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

if [ $# -lt 1 ]; then
    fail "${PRGNAME}: No build root specified. Usage : ${PRGNAME} <build-root>"
fi

#Clean up our build root first
BUILDROOT=$1
PARENT=/usr/src/photon

if mountpoint ${BUILDROOT}/run	>/dev/null 2>&1; then umount ${BUILDROOT}/run; fi
if mountpoint ${BUILDROOT}/sys	>/dev/null 2>&1; then umount ${BUILDROOT}/sys; fi
if mountpoint ${BUILDROOT}/proc	>/dev/null 2>&1; then umount ${BUILDROOT}/proc; fi
if mountpoint ${BUILDROOT}/dev	>/dev/null 2>&1; then umount -R ${BUILDROOT}/dev; fi

cp /etc/resolv.conf ${BUILDROOT}/etc/

if [ ${EUID} -eq 0 ] ; then
# 	Ommited in the filesystem.spec file - not needed for booting
    [ -e ${BUILDROOT}/dev/console ]	|| mknod -m 600 ${BUILDROOT}/dev/console c 5 1
    [ -e ${BUILDROOT}/dev/null ]	|| mknod -m 666 ${BUILDROOT}/dev/null c 1 3
    [ -e ${BUILDROOT}/dev/random ]	|| mknod -m 444 ${BUILDROOT}/dev/random c 1 8
    [ -e ${BUILDROOT}/dev/urandom ]	|| mknod -m 444 ${BUILDROOT}/dev/urandom c 1 9

    chown -R 0:0 ${BUILDROOT}/*	|| fail "${PRGNAME}: Changing ownership: ${BUILDROOT}: FAILURE"

#
#	Mount kernel filesystem
#
    if ! mountpoint ${BUILDROOT}/dev	>/dev/null 2>&1; then mount --rbind /dev ${BUILDROOT}/dev; mount --make-rslave ${BUILDROOT}/dev; fi
    if ! mountpoint ${BUILDROOT}/proc	>/dev/null 2>&1; then mount -t proc proc ${BUILDROOT}/proc; fi
    if ! mountpoint ${BUILDROOT}/sys 	>/dev/null 2>&1; then mount -t sysfs sysfs ${BUILDROOT}/sys; fi
    if ! mountpoint ${BUILDROOT}/run	>/dev/null 2>&1; then mount -t tmpfs tmpfs ${BUILDROOT}/run; fi
    if [ -h ${BUILDROOT}/dev/shm ];			 then mkdir -pv ${BUILDROOT}/$(readlink ${BUILDROOT}/dev/shm); fi
fi

exit 0
