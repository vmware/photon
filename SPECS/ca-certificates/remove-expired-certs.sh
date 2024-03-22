#!/bin/bash

# Begin /bin/remove-expired-certs.sh
# Version 20120211
# Make sure the date is parsed correctly on all systems

function mydate() {
  local y=$( echo $1 | cut -d" " -f4 )
  local M=$( echo $1 | cut -d" " -f1 )
  local d=$( echo $1 | cut -d" " -f2 )
  local m
  if [ ${d} -lt 10 ]; then d="0${d}"; fi
  case $M in
    Jan) m="01";;
    Feb) m="02";;
    Mar) m="03";;
    Apr) m="04";;
    May) m="05";;
    Jun) m="06";;
    Jul) m="07";;
    Aug) m="08";;
    Sep) m="09";;
    Oct) m="10";;
    Nov) m="11";;
    Dec) m="12";;
  esac
  certdate="${y}${m}${d}"
}

OPENSSL=/usr/bin/openssl
DIR=/etc/ssl/certs
if [ $# -gt 0 ]; then
  DIR="$1"
fi

certs=$( find ${DIR} -type f -name "*.pem" -o -name "*.crt" )
today=$( date +%Y%m%d )
for cert in $certs; do
  notafter=$( $OPENSSL x509 -enddate -in "${cert}" -noout )
  date=$( echo ${notafter} |  sed 's/^notAfter=//' )
  mydate "$date"
  if [ ${certdate} -lt ${today} ]; then
    echo "${cert} expired on ${certdate}! Removing..."
    rm -f "${cert}"
  fi
done

find -L ${DIR} -type l -delete
