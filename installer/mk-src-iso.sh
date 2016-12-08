#!/bin/bash
#################################################
#       Title:  mk-src-iso                      #
#        Date:  2016-02-19                      #
#     Version:  1.0                             #
#      Author:  dthaluru@vmware.com             #
#     Options:                                  #
#################################################
#	Overview
#		Generates a photon source iso
#	End
#

set +x                 # disable hashall
PRGNAME=${0##*/}	    # script name minus the path
source config.inc		#	configuration parameters
source function.inc		#	commonn functions
LOGFILE=/var/log/"${PRGNAME}-${LOGFILE}"	#	set log file name


# Grab the name of the iso file 
if [ $# -lt 2 ]
then
    echo "Usage : " $0 " <output-iso-with-path>  <srpms-path> <pkg-list-path>"
    exit 1
fi
ISO_OUTPUT_NAME=$1
SRPMS_PATH=$2
SRPM_LIST=$3

WORKINGDIR=${BUILDROOT}
rm -r ${WORKINGDIR}/*
(
cd ${SRPMS_PATH}
mkdir ${WORKINGDIR}/SRPMS
for srpm_name in $SRPM_LIST; do
    FILENAME="`find . -name ${srpm_name} -type f`"
    if [ -n "$FILENAME" ]; then
        cp --parent $FILENAME ${WORKINGDIR}/SRPMS/;
    fi
done
)

mkisofs -r -o $ISO_OUTPUT_NAME $WORKINGDIR/

