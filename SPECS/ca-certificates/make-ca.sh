#!/bin/bash

# Begin make-ca.sh
# Script to populate OpenSSL's CApath from a bundle of PEM formatted CAs
# The file certdata.txt must exist in the local directory
# Version number is obtained from the version of the data.
# Authors: DJ Lucas
#          Bruce Dubbs
# Version 20120211

certdata="certdata.txt"
if [ ! -r $certdata ]; then
  echo "ERROR: ${certdata} must be in the local directory" >&2
  exit 1
fi

REVISION=$(grep CVS_ID $certdata | cut -f4 -d'$')
if [ -z "${REVISION}" ]; then
  echo "ERROR: ${certdata} has no 'Revision' in CVS_ID" >&2
  exit 1
fi

SCRIPT_DIR="$(dirname ${BASH_SOURCE[0]})"

VERSION=$(echo $REVISION | cut -f2 -d" ")
TEMPDIR=$(mktemp -d)
TRUSTATTRIBUTES="CKA_TRUST_SERVER_AUTH"
BUNDLE="BLFS-ca-bundle-${VERSION}.crt"
CONVERTSCRIPT="${SCRIPT_DIR}/make-cert.pl"
SSLDIR="/etc/ssl"

mkdir -p "${TEMPDIR}/certs"
# Get a list of staring lines for each cert
CERTBEGINLIST=$(grep -n "^# Certificate" "${certdata}" | cut -d":" -f1)
# Get a list of ending lines for each cert
CERTENDLIST=$(grep -n "^CKA_TRUST_STEP_UP_APPROVED" "${certdata}" | cut -d ":" -f 1)
# Start a loop
for certbegin in ${CERTBEGINLIST}; do
  for certend in ${CERTENDLIST}; do
    if test "${certend}" -gt "${certbegin}"; then
      break
    fi
  done
  # Dump to a temp file with the name of the file as the beginning line number
  sed -n "${certbegin},${certend}p" "${certdata}" > "${TEMPDIR}/certs/${certbegin}.tmp"
done

unset CERTBEGINLIST CERTDATA CERTENDLIST certebegin certend

mkdir -p certs
# Make sure the directory is clean
rm -rf certs/*

for tempfile in ${TEMPDIR}/certs/*.tmp; do
  # Make sure that the cert is trusted...
  grep "${TRUSTATTRIBUTES}" "${tempfile}" | \
    egrep "TRUST_UNKNOWN|NOT_TRUSTED" > /dev/null
  if test "${?}" = "0"; then
    # Throw a meaningful error and remove the file
    cp "${tempfile}" tempfile.cer
    perl ${CONVERTSCRIPT} > tempfile.crt
    keyhash=$(openssl x509 -noout -in tempfile.crt -hash)
    echo "Certificate ${keyhash} is not trusted!  Removing..."
    rm -f tempfile.cer tempfile.crt "${tempfile}"
    continue
  fi
  # If execution made it to here in the loop, the temp cert is trusted
  # Find the cert data and generate a cert file for it
  cp "${tempfile}" tempfile.cer
  perl ${CONVERTSCRIPT} > tempfile.crt
  keyhash=$(openssl x509 -noout -in tempfile.crt -hash)
  mv tempfile.crt "certs/${keyhash}.pem"
  rm -f tempfile.cer "${tempfile}"
  echo "Created ${keyhash}.pem"
done

# Remove denylisted files
# MD5 Collision Proof of Concept CA
if test -f certs/8f111d69.pem; then
  echo "Certificate 8f111d69 is not trusted!  Removing..."
  rm -f certs/8f111d69.pem
fi

# Finally, generate the bundle and clean up.
cat certs/*.pem > ${BUNDLE}
rm -r "${TEMPDIR}"
