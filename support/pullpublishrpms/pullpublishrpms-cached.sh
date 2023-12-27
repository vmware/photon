#!/bin/bash

PRGNAME=${0##*/}

if [ $# -ne 3 ]; then
  echo -e "\nERROR: '${PRGNAME}' Invalid input args.
Usage: ${PRGNAME} <rpms-path> <rpms-url> <input-file>\n" 1>&2
  exit 1
fi

ARCH="$(uname -m)"

RPMSPATHDIR="$1"
PUBLISHCACHE="$2"
INPUTFILE="$3-${ARCH}"

mkdir -p ${RPMSPATHDIR}/{${ARCH},noarch}

sed -e "s|^|${PUBLISHCACHE}/|g" ${INPUTFILE} | xargs -n 1 -P 10 cp -t ${RPMSPATHDIR}
if [ $? -ne 0 ]; then
  echo -e "\nERROR: '${PRGNAME}' failed to copy one or more rpms.
Thoroughly check entries in ${INPUTFILE} and ensure that file(s) are present in server\n" 1>&2
  exit 1
fi

if ls ${RPMSPATHDIR}/*.${ARCH}.rpm &> /dev/null; then
  mv ${RPMSPATHDIR}/*.${ARCH}.rpm ${RPMSPATHDIR}/${ARCH}
fi

if ls ${RPMSPATHDIR}/*.noarch.rpm &> /dev/null; then
  mv ${RPMSPATHDIR}/*.noarch.rpm ${RPMSPATHDIR}/noarch
fi
