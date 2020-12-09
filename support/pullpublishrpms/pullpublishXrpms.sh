#!/bin/bash
#################################################
#	Title:	pullpublishxrpms.sh	   	#
#        Date:	04-10-2017          		#
#     Version:	1.0				#
#      Author:	hudaiyakumar@vmware.com         #
#################################################

PRGNAME=${0##*/}

if [ $# -lt 1 ]; then
    echo "${PRGNAME}: No publish rpms path and log path are specified. Usage : ${PRGNAME} <publish-rpms-path>"
    exit 1
fi

PUBLISHRPMSPATHDIR=$1

if [ $# -eq 2 ]; then
   PUBLISHCACHE=$2
   while read FILE; do cp -r $PUBLISHCACHE/$FILE $PUBLISHRPMSPATHDIR/$FILE; done < xrpmfilelist
else
   cat xrpmfilelist | awk '{print "https://packages.vmware.com/photon/photon_publish_x_rpms/"$1}' | xargs -n 1 -P 10 wget --user-agent Mozilla/4.0 -c -nv -nc -r -nH --cut-dirs=2 -P ${PUBLISHRPMSPATHDIR}
fi

ls ${PUBLISHRPMSPATHDIR}/*.rpm
if [ $? -eq 0 ];then
   mkdir -p ${PUBLISHRPMSPATHDIR}/noarch
   mv ${PUBLISHRPMSPATHDIR}/*noarch*.rpm ${PUBLISHRPMSPATHDIR}/noarch/
   mkdir -p ${PUBLISHRPMSPATHDIR}/$(uname -m)
   mv ${PUBLISHRPMSPATHDIR}/*.rpm ${PUBLISHRPMSPATHDIR}/$(uname -m)/
fi
