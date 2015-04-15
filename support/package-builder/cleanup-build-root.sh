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

if [ $# -lt 1 ]; then
    fail "${PRGNAME}: No build root specified. Usage : ${PRGNAME} <build-root>"
fi

#Clean up our build root first
BUILDROOT=$1

./umount-build-root.sh $1

rm -rf ${BUILDROOT}/*

exit 0
