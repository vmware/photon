#!/bin/bash
#################################################
#       Title:  mk-mount-disk                   #
#        Date:  2014-11-26                      #
#     Version:  1.0                             #
#      Author:  mbassiouny@vmware.com           #
#     Options:                                  #
#################################################
#	Overview
#		This mount a partition passed in arguments or a in the config.inc in root photon mount directory
#	End
#
set -o errexit		# exit if error...insurance ;
set -o nounset		# exit if variable not initalized
set +h			# disable hashall
PRGNAME=${0##*/}	# script name minus the path
source config.inc		#	configuration parameters
source function.inc
LOGFILE=/var/log/"${PRGNAME}-${LOGFILE}"	#	set log file name
#LOGFILE=/dev/null		#	uncomment to disable log file
[ ${EUID} -eq 0 ]	|| fail "${PRGNAME}: Need to be root user: FAILURE"
> ${LOGFILE}		#	clear/initialize logfile

# Check if passing a partition
if [ $# -eq 1 ] 
	then
		PARTITION=$1
fi

run_command "Mounting HD" "mount -v -t ext4 ${PARTITION} ${BUILDROOT}" "${LOGFILE}"

