#!/bin/bash
#################################################
#       Title:  mk-finalize-system              #
#        Date:  2014-11-26                      #
#     Version:  1.0                             #
#      Author:  mbassiouny@vmware.com           #
#     Options:                                  #
#################################################
#   Overview
#       Finalize the system after the installation
#   End
#
set -o errexit      # exit if error...insurance ;
set -o nounset      # exit if variable not initalized
set +h          # disable hashall
set -x
SCRIPT_PATH=$(dirname $(realpath -s $0))
source $SCRIPT_PATH/config.inc
PRGNAME=${0##*/}    # script name minus the path
[ ${EUID} -eq 0 ]   || fail "${PRGNAME}: Need to be root user: FAILURE"

/sbin/ldconfig
/usr/sbin/pwconv
/usr/sbin/grpconv
/bin/systemd-machine-id-setup
/usr/bin/touch /etc/locale.conf
/bin/echo "LANG=en_US.UTF-8" > /etc/locale.conf

# Importing the pubkey
rpm --import /etc/pki/rpm-gpg/*

#locale-gen.sh needs /usr/share/locale/locale.alias which is shipped with
#  glibc-lang rpm, in some photon installations glibc-lang rpm is not installed
#  by default. Call localedef directly here to define locale environment.
/usr/bin/localedef -c -i en_US -f UTF-8 en_US.UTF-8
#/sbin/locale-gen.sh

exit 0
