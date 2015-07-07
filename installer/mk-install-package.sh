#!/bin/bash
#################################################
#       Title:  mk-install-package              #
#        Date:  2014-11-26                      #
#     Version:  1.0                             #
#      Author:  mbassiouny@vmware.com           #
#     Options:                                  #
#################################################
#	Overview
#		install a passed package into a photon system
#	End
#
set -o errexit		# exit if error...insurance ;
set -o nounset		# exit if variable not initalized
set +h			# disable hashall
source config.inc
source function.inc
PRGNAME=${0##*/}	# script name minus the path
RPM_PARAMS="-Uvh"
LOGFILE=/var/log/"${PRGNAME}-${LOGFILE}"

if [ $# -ge 2 ]
then
    RPM_PARAMS="-Uvh $2"
fi

[ ${EUID} -eq 0 ] 	|| fail "${PRGNAME}: Need to be root user: FAILURE"

RPMPKG=""
RPMPKG=$(find ${RPMROOT} -name "$1" -print)
# TODO: sometimes we catch several items into RPMPKG.
# In case we have several releases in rpm cache. Need to handle that.
[ -z $RPMPKG ] && fail "installation error: rpm package not found\n"

run_command "Installing: $1" "rpm --nodeps ${RPM_PARAMS} ${RPMPKG}" "${LOGFILE}"

exit 0
