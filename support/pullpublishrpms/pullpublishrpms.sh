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

mkdir -p ${PUBLISHRPMSPATHDIR}/x86_64
mkdir -p ${PUBLISHRPMSPATHDIR}/noarch

for line in $(cat rpmfilelist) 
do 
    echo $line
    subRPMpath="x86_64"
    if [ `echo $line | grep -c "noarch" ` -gt 0 ]; then
        subRPMpath="noarch"
    fi
    cmd= wget https://bintray.com/artifact/download/vmware/photon_release_1.0_TP1_x86_64/$line -P ${PUBLISHRPMSPATHDIR}/${subRPMpath}
    echo $cmd
done 
