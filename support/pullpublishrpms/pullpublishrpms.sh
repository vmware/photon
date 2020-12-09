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

if [ $# -eq 2 ]; then
   PUBLISHCACHE=$2
   while read FILE; do cp -r $PUBLISHCACHE/$FILE $PUBLISHRPMSPATHDIR/$FILE; done < rpmfilelist
else
   cat rpmfilelist | awk '{print "https://packages.vmware.com/photon/photon_publish_rpms/"$1}' | xargs -n 1 -P 10 wget --user-agent Mozilla/4.0 -c -nv -nc -r -nH --cut-dirs=2 -P ${PUBLISHRPMSPATHDIR}
fi

ls ${PUBLISHRPMSPATHDIR}/*.rpm
if [ $? -eq 0 ];then
   mkdir -p ${PUBLISHRPMSPATHDIR}/noarch
   mv ${PUBLISHRPMSPATHDIR}/*noarch*.rpm ${PUBLISHRPMSPATHDIR}/noarch/
   mkdir -p ${PUBLISHRPMSPATHDIR}/$(uname -m)
   mv ${PUBLISHRPMSPATHDIR}/*.rpm ${PUBLISHRPMSPATHDIR}/$(uname -m)/
fi
