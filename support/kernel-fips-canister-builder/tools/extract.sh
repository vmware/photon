#! /bin/sh
#
# Helper script to extract caniter object file from rpm
#
# Copyright (C) 2020, 2021, VMware, Inc.
# Author: Alexey Makhalov <amakhalov@vmware.com>
#

set -xe

test "$#" -ne 1 && echo "Usage: $0 Linux flavour (e.g: linux / linux-secure)" && exit 1

FLAVOR=$1
RPM=$(ls -1 -tu build/stage/RPMS/x86_64/${FLAVOR}-fips* | head -n1)
TARBALL=$(rpm -qpl ${RPM})

rpm2cpio ${RPM} | cpio -iv --to-stdout .${TARBALL} | tar xjv -O $(basename ${TARBALL} .tar.bz2)/fips_canister.o > fips_canister-${FLAVOR}.o
#strip --strip-debug fips_canister-${FLAVOR}.o
