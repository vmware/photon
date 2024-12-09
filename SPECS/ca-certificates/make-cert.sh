#!/bin/bash

# Input file containing octal-encoded certificate data
CERTDATA="$1"

if [ ! -f "${CERTDATA}" ]; then
  echo "ERROR: file '${CERTDATA}' not found!" >&2
  exit 1
fi

OPENSSL=/usr/bin/openssl
if ! test -x ${OPENSSL}; then
  echo "ERROR: ${OPENSSL} not present, quit ..." 1>&2
  exit 1
fi

IN_CERT=0
TmpFile=""

while IFS= read -r line; do
  # Start of a certificate block
  if [[ "$line" =~ ^CKA_VALUE\ MULTILINE_OCTAL ]]; then
    IN_CERT=1
    TmpFile="$(mktemp)"
  elif [[ "$line" =~ ^END$ && ${IN_CERT} -eq 1 ]]; then
    # End of the certificate block
    IN_CERT=0
    # Convert DER to PEM and append to the output file
    ${OPENSSL} x509 -inform DER -text -in "${TmpFile}" -fingerprint
    echo -e "\n"
    rm -f "${TmpFile}"
  elif [ ${IN_CERT} -eq 1 ]; then
    echo "$line" | sed -E 's/\\([0-7]{1,3})/\\\\\1/g' | xargs -I{} printf "{}" >> "${TmpFile}"
  fi
done < "${CERTDATA}"
