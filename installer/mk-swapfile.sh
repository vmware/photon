#!/bin/bash
#################################################
#       Title:  mk-swapfile                     #
#        Date:  2016-02-17                      #
#     Version:  1.0                             #
#      Author:  xiaolinl@vmware.com             #
#     Options:                                  #
#################################################
#	Overview
#		Create swap file after the installation
#	End
#
set -o errexit		# exit if error...insurance ;
set -o nounset		# exit if variable not initalized
set +h			# disable hashall
source config.inc
source function.inc
PRGNAME=${0##*/}	# script name minus the path
LOGFILE=/var/log/"${PRGNAME}-${LOGFILE}"	#	set log file name
#LOGFILE=/dev/null		#	uncomment to disable log file
[ ${EUID} -eq 0 ] 	|| fail "${PRGNAME}: Need to be root user: FAILURE"

/bin/dd if=/dev/zero of=/swapfile bs=1M count=512
/bin/chmod 600 /swapfile
/sbin/mkswap /swapfile
/sbin/swapon /swapfile
exit 0
