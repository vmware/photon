#!/bin/bash
#################################################
#	Title:	run-in-chroot.sh    				#
#        Date:	2015-02-26          			#
#     Version:	1.0				                #
#      Author:	sharathg@vmware.com             #
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

BUILDROOT=$1
shift 

# Remove the name of this script from our argument list
#shift

PHOTON_ENV_CMD=/usr/bin/env
PHOTON_BASH_CMD=/bin/bash

test -x ${BUILDROOT}/tools/bin/env && PHOTON_ENV_CMD=/tools/bin/env
test -x ${BUILDROOT}/tools/bin/bash && PHOTON_BASH_CMD=/tools/bin/bash

#
#	Goto chroot and run the command specified as parameter.
#
chroot "${BUILDROOT}" \
	$PHOTON_ENV_CMD -i \
	HOME=/root \
	TERM="$TERM" \
	PS1='\u:\w\$ ' \
	PATH=/bin:/usr/bin:/sbin:/usr/sbin:/tools/bin \
	SHELL=/bin/bash \
	$PHOTON_BASH_CMD --login +h -c "$*"

exit 0
