#!/bin/bash
#################################################
#       Title:  mk-finalize-system              #
#        Date:  2014-11-26                      #
#     Version:  1.0                             #
#      Author:  mbassiouny@vmware.com           #
#     Options:                                  #
#################################################
#	Overview
#		Finalize the system after the installation
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

/sbin/ldconfig
/usr/sbin/pwconv
/usr/sbin/grpconv
/bin/systemd-machine-id-setup
#/sbin/locale-gen.sh
exit 0
