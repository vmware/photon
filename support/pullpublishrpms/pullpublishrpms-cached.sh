#!/bin/bash

PRGNAME=${0##*/}

if [ $# -ne 3 ]; then
  echo "${PRGNAME}: Invalid input args." 1>&2
  echo "Usage: ${PRGNAME} <rpms-path> <publish-cache> <input-file>" 1>&2
  exit 1
fi

ARCH="$(uname -m)"

RPMSPATHDIR="$1"
PUBLISHCACHE="$2"
INPUTFILE="$3-${ARCH}"

mkdir -p ${RPMSPATHDIR}/{${ARCH},noarch}

sed -e "s|^|${PUBLISHCACHE}/|g" ${INPUTFILE} | xargs -n 1 -P 10 cp -t ${RPMSPATHDIR}

if ls ${RPMSPATHDIR}/*.${ARCH}.rpm &> /dev/null; then
  mv ${RPMSPATHDIR}/*.${ARCH}.rpm ${RPMSPATHDIR}/${ARCH}
fi

if ls ${RPMSPATHDIR}/*.noarch.rpm &> /dev/null; then
  mv ${RPMSPATHDIR}/*.noarch.rpm ${RPMSPATHDIR}/noarch
fi
