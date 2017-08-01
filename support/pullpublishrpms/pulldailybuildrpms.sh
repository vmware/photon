#!/bin/bash
#################################################
#	Title:	pulldailybuildrpms.sh	   	            #
#        Date:	2017-07-31          		        #
#     Version:	1.0				                      #
#      Author:	ruig@vmware.com                 #
#################################################

PRGNAME=${0##*/}

if [ $# -lt 1 ]; then
    echo "${PRGNAME}: No daily build rpms path and log path are specified. Usage : ${PRGNAME} <daily-build-rpms-path>"
    exit 1
fi

PUBLISHRPMSPATHDIR=$1

# Grab the latest daily build's timestamp from photon-filer
DATE_TAG=`wget -qO- http://photon-filer.eng.vmware.com/builds/dev | grep -o -P "(\ *href=\"[0-9]*-[0-9]*-[0-9]*-[0-9]*)" | grep -o -P "(\ *[0-9]*-[0-9]*-[0-9]*-[0-9]*)" | tail -1`

wget --accept rpm -r --no-parent -nv -nc -nH --cut-dirs=5 http://photon-filer.eng.vmware.com/builds/dev/$DATE_TAG/stage/RPMS/ -P ${PUBLISHRPMSPATHDIR}
