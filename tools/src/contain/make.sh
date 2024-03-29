#!/bin/bash

if [ "$EUID" -ne 0 ]; then
  echo "You must be root to run this script."
  exit 1
fi

SCRIPT_DIR="$(dirname "$(realpath $0)")"
TARGET="${SCRIPT_DIR}/../../bin/contain_unpriv"

if [ "$1" = "clean" ]; then
  echo "Cleaning $(basename ${TARGET}) ..."
  rm -f ${TARGET}
  exit 0
fi

[ -f ${TARGET} ] && exit 0

CFLAGS="-Wall -Wextra -Werror -O2"

echo "Building $(basename ${TARGET}) ..."

[ ! -d "$(dirname ${TARGET})" ] && mkdir -p "$(dirname ${TARGET})"

(
set -x
if ! gcc -o ${TARGET} ${SCRIPT_DIR}/*.c ${CFLAGS}; then
  echo "ERROR: failed to build $(basename ${TARGET})"
  exit 1
fi
)
ret=$?

if [ $ret -eq 0 ]; then
  install -o root -g root -m 4755 ${TARGET} "$(dirname ${TARGET})"/contain
  ret=$?
fi

exit $ret
