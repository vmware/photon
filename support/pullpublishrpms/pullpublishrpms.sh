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
INPUTFILE=rpmfilelist-$(uname -m)

if [ $# -eq 2 ]; then
   PUBLISHCACHE=$2
   while read FILE; do cp -r $PUBLISHCACHE/$FILE $PUBLISHRPMSPATHDIR/$FILE; done < $INPUTFILE
else
   cat $INPUTFILE | awk '{print "https://bintray.com/artifact/download/vmware/photon_publish_rpms/"$1}' | xargs -n 1 -P 10 wget --user-agent Mozilla/4.0 -c -nv -nc -r -nH --quiet --cut-dirs=4 -P ${PUBLISHRPMSPATHDIR}
fi
