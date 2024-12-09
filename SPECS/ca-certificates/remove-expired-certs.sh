#!/bin/bash

OPENSSL=/usr/bin/openssl
if ! test -x ${OPENSSL}; then
  echo "ERROR: ${OPENSSL} not present, quit ..." 1>&2
  exit 1
fi

DIR=/etc/ssl/certs
if [ $# -gt 0 ]; then
  DIR="$1"
fi

certs=($(find ${DIR} -type f -name "*.pem" -o -name "*.crt"))
for cert in ${certs[@]}; do
  cert_expiry_date="$(${OPENSSL} x509 -dateopt iso_8601 -enddate -in ${cert} -noout | cut -d '=' -f 2)"
  cert_expiry_epoch=$(date -u -d "${cert_expiry_date}" '+%s')
  cur_time_in_epoch="$(date -u '+%s')"
  if [ ${cert_expiry_epoch} -lt ${cur_time_in_epoch} ]; then
    echo "${cert} expired on ${cert_expiry_date}! Removing..."
    rm -f "${cert}"
  fi
done

# remove all dangling symlinks at once
find -L ${DIR} -type l -delete
