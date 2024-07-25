#!/bin/bash

set -e

CERTIFICATES_PATH="/etc/ssl/certs/"
CONCATENATED_CERT_FILE="/etc/pki/tls/certs/ca-bundle.crt"

if ! openssl rehash $CERTIFICATES_PATH; then
   echo "Error while c_rehashing"
fi

cat $CERTIFICATES_PATH*.pem > $CONCATENATED_CERT_FILE
