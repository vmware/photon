#!/bin/bash

SCRIPT_DIR="$(dirname "$(realpath $0)")"
TARGET="${SCRIPT_DIR}/../../bin/vixdiskutil"

if [ "$1" = "clean" ]; then
  echo "Cleaning $(basename ${TARGET}) ..."
  rm -f ${TARGET}
  exit 0
fi

[ -f ${TARGET} ] && exit 0

LIBDIR="/usr/lib/vmware"
LDFLAGS="-ldl -lvixDiskLib -lvixMntapi -lpthread -lssl -lfuse"
CFLAGS="-Wall -Wextra -Werror"

# libvixDiskLibVim.so can come from any of the below sources
# search them one by one
if ldconfig -v 2>/dev/null | grep -qw libvixDiskLibVim.so; then
  LDFLAGS+=" -lvixDiskLibVim"
elif [ -f "${LIBDIR}/libvixDiskLibVim.so" ]; then
  LDFLAGS+=" -lvixDiskLibVim"
elif [ -n "${LD_LIBRARY_PATH}" ]; then
  for entry in ${LD_LIBRARY_PATH//:/ }; do
    if [ -f "${entry}/libvixDiskLibVim.so" ]; then
      LDFLAGS+=" -lvixDiskLibVim"
      break
    fi
  done
fi

echo "Building $(basename ${TARGET}) ..."

[ ! -d "$(dirname ${TARGET})" ] && mkdir -p "$(dirname ${TARGET})"

(
set -x
if ! g++ -o ${TARGET} ${SCRIPT_DIR}/vixDiskUtil.cpp ${CFLAGS} -L${LIBDIR} ${LDFLAGS}; then
  echo "ERROR: failed to build $(basename ${TARGET})"
  exit 1
fi
)

exit $?
