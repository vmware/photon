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
RPMPKG=$(find ../RPMS -name "$1-[0-9]*.rpm" -print)
[ -z $RPMPKG ] && fail "installation error: rpm package not found\n"
case $1 in
	linux-dev | linux-docs | glibc | gmp | gcc | bzip2 | ncurses | util-linux | e2fsprogs | shadow | bison | perl | texinfo | vim | linux | udev | rpm | dbus)
		run_command "Installing: $1" "rpm --nodeps ${RPM_PARAMS} ${RPMPKG}" "${LOGFILE}" ;;
	*)	run_command "Installing: $1" "rpm --nodeps ${RPM_PARAMS} ${RPMPKG}" "${LOGFILE}" ;;
esac
exit 0
