#!/bin/bash

PRGNAME=${0##*/}

if [ $# -ne 3 ]; then
  echo "${PRGNAME}: Invalid input args." 1>&2
  echo "Usage: ${PRGNAME} <rpms-path> <rpms-url> <input-file>" 1>&2
  exit 1
fi

ARCH="$(uname -m)"

RPMSPATHDIR="$1"
RPMS_URL="$2"
INPUTFILE="$3-${ARCH}"

mkdir -p ${RPMSPATHDIR}/{${ARCH},noarch}

c=$(($(echo "$RPMS_URL" | tr -cd '/' | wc -c) - 2))

sed "s|^|${RPMS_URL}/|g" ${INPUTFILE} | \
  xargs -n 1 -P 10 wget --user-agent Mozilla/4.0 -c -nv -nc -r -nH --quiet --cut-dirs=$c -P ${RPMSPATHDIR}

if ls ${RPMSPATHDIR}/*.${ARCH}.rpm &> /dev/null; then
  mv ${RPMSPATHDIR}/*.${ARCH}.rpm ${RPMSPATHDIR}/${ARCH}
fi

if ls ${RPMSPATHDIR}/*.noarch.rpm &> /dev/null; then
  mv ${RPMSPATHDIR}/*.noarch.rpm ${RPMSPATHDIR}/noarch
fi
