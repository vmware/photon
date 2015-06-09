#!/bin/bash
#################################################
#	Title:	pullpublishrpms.sh	   	#
#        Date:	2015-06-06          		#
#     Version:	1.0				#
#      Author:	dthaluru@vmware.com             #
#################################################

PRGNAME=${0##*/}

if [ $# -lt 1 ]; then
    echo "${PRGNAME}: No publish rpms path and log path are specified. Usage : ${PRGNAME} <publish-rpms-path>"
    exit 1
fi

PUBLISHRPMSPATHDIR=$1

if [ ${EUID} -ne 0 ]; then
    echo "${PRGNAME}: Need to be root user: FAILURE"
    exit 1
fi

wget -c -nv  -r -nH --cut-dirs=4 -B https://bintray.com/artifact/download/vmware/photon_release_1.0_TP1_x86_64/ -i rpmfilelist -P ${PUBLISHRPMSPATHDIR}
