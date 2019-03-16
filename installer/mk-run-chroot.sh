#!/bin/bash
#################################################
#       Title:  mk-run-chroot                   #
#        Date:  2014-11-26                      #
#     Version:  1.0                             #
#      Author:  mbassiouny@vmware.com           #
#     Options:                                  #
#################################################
#   Overview
#       Run the passed command into the chroot
#   End
#
set -o errexit      # exit if error...insurance ;
set -o nounset      # exit if variable not initalized
set +h          # disable hashall
SCRIPT_PATH=$(dirname $(realpath -s $0))
source $SCRIPT_PATH/config.inc
PRGNAME=${0##*/}    # script name minus the path
LOGFILE=/var/log/"${PRGNAME}-${LOGFILE}"    #   set log file name
#LOGFILE=/dev/null      #   uncomment to disable log file
[ ${EUID} -eq 0 ]   || fail "${PRGNAME}: Need to be root user: FAILURE"
[ -z ${BUILDROOT} ] && fail "${PRGNAME}: Build root not set: FAILURE"

# Remove the name of this script from our argument list
#shift

#
#   Goto chroot and run the command specified as parameter.
#
chroot "${BUILDROOT}" \
    /usr/bin/env -i \
    HOME=/root \
    TERM="$TERM" \
    PS1='\u:\w\$ ' \
    PATH=/bin:/usr/bin:/sbin:/usr/sbin \
    /usr/bin/bash --login +h -c "cd installer;$*"

exit 0
