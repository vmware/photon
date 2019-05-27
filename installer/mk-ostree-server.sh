#!/bin/bash
#################################################
#       Title:  mk-ostree-server                #
#        Date:  2015-07-15                      #
#     Version:  1.0                             #
#      Author:  tliaqat@vmware.com              #
#     Options:                                  #
#################################################
#   Overview
#       Install OSTree Server
#   End
#

set -o errexit          # exit if error...insurance ;)
set -o nounset          # exit if variable not initalized
set +h                  # disable hashall
PRGNAME=${0##*/}        # script name minus the path
source config.inc       #   configuration parameters
source function.inc     #   commonn functions
LOGFILE=/var/log/"${PRGNAME}-${LOGFILE}"    #   set log file name

ROOT=$1

mkdir -p ${ROOT}/srv/rpm-ostree
ostree --repo=${ROOT}/srv/rpm-ostree/repo init --mode=archive-z2  2>&1 | tee "${LOGFILE}"
rpm-ostree compose tree --repo=${ROOT}/srv/rpm-ostree/repo photon-base.json  2>&1 |  tee "${LOGFILE}"
