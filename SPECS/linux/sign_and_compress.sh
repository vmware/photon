#!/bin/bash

# Extra modules that we are building won't get signed by 'make modules_sign'
# This script is for signing and compressing everything.

MODULES_DIR="$1"
if [ ! -d "${MODULES_DIR}" ]; then
  echo "ERROR: MODULES_DIR('${MODULES_DIR}') does not exist ..." 1>&2
  exit 1
fi

KERNEL_BUILD_DIR="$2"
if [ ! -d "${KERNEL_BUILD_DIR}" ]; then
  echo "ERROR: KERNEL_BUILD_DIR('${KERNEL_BUILD_DIR}') does not exist ..." 1>&2
  exit 1
fi

NCPUS="$((($(nproc) + 1) / 2))"
BATCH_SIZE="1"
ERROR_FN="${KERNEL_BUILD_DIR}/signerr.log"
SIGN_ALGO="sha512"
STRIP="$(command -v strip)"
STRIP_OPTS="--strip-debug"

# retain .BTF section in linux-generic
if [ "${RPM_PACKAGE_NAME}" = "linux" ]; then
  STRIP_OPTS+=" --keep-section '.BTF'"
fi

echo -n "Signing program args:
NCPUS:      ${NCPUS}
BATCH_SIZE: ${BATCH_SIZE}
ERROR_FN:   ${ERROR_FN}
SIGN_ALGO:  ${SIGN_ALGO}
STRIP:      ${STRIP}
STRIP_OPTS: '${STRIP_OPTS}'
"

test -f ${ERROR_FN} && rm ${ERROR_FN}

echoerr() {
  echo -ne "$*" >&2
}

abort() {
  local rc=$1
  shift
  echoerr "$*"
  exit $rc
}

sign_and_compress() {
  local SIGN_FILE_BIN="${KERNEL_BUILD_DIR}/scripts/sign-file"
  local SIGN_PEM_FN="${KERNEL_BUILD_DIR}/certs/signing_key.pem"
  local SIGN_X509_FN="${KERNEL_BUILD_DIR}/certs/signing_key.x509"
  local file="$0"

  # strip debug symbols out before signing
  if ! ${STRIP} ${STRIP_OPTS} ${file}; then
    abort "\nERROR: while stripping (${file}) ..." |& tee ${ERROR_FN}
  fi

  chmod a-x ${file}

  echo "Signing - '${file}' ..."
  ${SIGN_FILE_BIN} \
    ${SIGN_ALGO} \
    ${SIGN_PEM_FN} \
    ${SIGN_X509_FN} \
    ${file}

  if [ $? -ne 0 ]; then
    abort "\nERROR: while signing (${file}) ..." |& tee ${ERROR_FN}
  fi

  # Compress the signed files
  if ! xz -T ${NCPUS} "${file}"; then
    abort "\nERROR: while compressing (${file}) ..." |& tee ${ERROR_FN}
  fi
}

export -f sign_and_compress
export NCPUS KERNEL_BUILD_DIR ERROR_FN SIGN_ALGO STRIP STRIP_OPTS

echo -e "\nStarting sign and compress of all modules ...\n"
# Find all files and process them in batches
pushd "${MODULES_DIR}" >/dev/null || exit 1
find . -name *.ko -type f -print0 | \
  xargs -0 -r -n ${BATCH_SIZE} -P ${NCPUS} bash -c 'sign_and_compress "$@"'
popd >/dev/null

if [ -f "${ERROR_FN}" ]; then
  abort "\nERROR: during signing or compressing ...\n"
fi

echo -en "\nSign and compress done ...
\nVerifying that all modules are signed and compressed ...\n"

if ! test -z "$(find ${MODULES_DIR} -type f -name '*.ko')"; then
  abort "\nERROR: atleast one module with .ko is left behind ...\n"
fi

ret=0
for module in $(find ${MODULES_DIR} -type f -name '*.ko.xz'); do
  if ! modinfo ${module} | grep -iq "^sig_hashalgo:[[:space:]]\+${SIGN_ALGO}$"; then
    echoerr "\nERROR: ${module} is not properly signed ...\n"
    [ ${ret} -eq 0 ] && ret=1
  fi
done

if [ ${ret} -eq 0 ]; then
  echo -e "\nVerification done, all modules are signed and compressed properly ...\n"
fi

exit ${ret}
