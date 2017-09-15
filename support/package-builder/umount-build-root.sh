#!/bin/bash
#################################################
#	Title:	cleanup-build-root.sh				#
#        Date:	2015-02-26          			#
#     Version:	1.0				                #
#      Author:	sharathg@vmware.com             #
#     Options:					                #
#################################################
set -o errexit
set -o nounset
set +h

source common.inc

LOGFILE="$(date +%Y-%m-%d).log"
PRGNAME=${0##*/}
LOGFILE=/var/log/"${PRGNAME}-${LOGFILE}"
if [ $# -lt 1 ]; then
    fail "${PRGNAME}: No build root specified. Usage : ${PRGNAME} <build-root>"
fi

#Clean up our build root first
BUILDROOT=$1

[ -z ${BUILDROOT} ]		&& fail "${PRGNAME}: BUILDROOT not set: FAILURE"
if [ ${EUID} -eq 0 ] ; then
    if mountpoint ${BUILDROOT}/run	>/dev/null 2>&1; then umount ${BUILDROOT}/run; fi
    if mountpoint ${BUILDROOT}/sys	>/dev/null 2>&1; then umount ${BUILDROOT}/sys; fi
    if mountpoint ${BUILDROOT}/proc	>/dev/null 2>&1; then umount ${BUILDROOT}/proc; fi
    if mountpoint ${BUILDROOT}/dev	>/dev/null 2>&1; then umount -R ${BUILDROOT}/dev; fi
fi

exit 0
