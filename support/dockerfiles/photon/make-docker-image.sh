#!/bin/bash

set -ex

echoerr() {
  echo -e "$*" >&2
}

PH_REL_VER="${PHOTON_RELEASE_VERSION}"
echo "PHOTON_RELEASE_VERSION=${PH_REL_VER}"

# TODO: this should be set from env or while invoking this script from build.py
# Since we are still at development phase for 9.2, keeping the logic fragmented
# Once all package splits are done, builder should be patched as needed
PH_SUBRELASE_VER=""

arch="$(uname -m)"
SYSROOT=/sysroot
ROOTFS_TAR_FILENAME="/photon/stage/photon-rootfs-$PH_REL_VER-$PHOTON_BUILD_NUMBER.${arch}.tar.gz"
STAGE_DIR="/photon/stage"

mkdir -p $SYSROOT
rm -rf /etc/yum.repos.d/*

cat > /etc/yum.repos.d/photon-local.repo <<- EOF
[photon-local]
name=VMware Photon Linux ${PH_REL_VER}($arch)
baseurl=file://${STAGE_DIR}/RPMS
gpgcheck=0
enabled=1
EOF

tdnf install -y --setopt=tsflags=nodocs rpm tar gzip grep coreutils bc

rpm --root $SYSROOT/ --initdb

tdnf --releasever ${PH_REL_VER} \
     --installroot ${SYSROOT}/ \
     --rpmverbosity error \
     --setopt=tsflags=nodocs \
     install -y \
     filesystem bash toybox tdnf photon-release photon-repos curl

actual_pkg_list=($(tdnf --installroot $SYSROOT/ \
                        --disablerepo=* -q \
                        list installed 2>/dev/null | cut -d'.' -f1))

isRpmV6=0
rpmVer=$(rpm --root "${SYSROOT}" -q --qf '%{version}\n' rpm-libs)
if [ "${rpmVer%%.*}" -eq 6 ]; then
  echo "rpm-libs is 6.x"
  isRpmV6=1
fi

expected_pkg_list=(
  bash bzip2-libs ca-certificates ca-certificates-pki curl curl-libs
  e2fsprogs-libs elfutils-libelf expat-libs filesystem glibc glibc-libs
  krb5 libgcc libsolv libssh2 libxcrypt lua-libs ncurses-libs nspr
  nss-libs openssl-libs photon-release photon-repos popt readline rpm-libs
  sqlite-libs tdnf tdnf-cli-libs toybox xz-libs zlib zstd-libs
)

if [ ${isRpmV6} -ne 0 ]; then
  expected_pkg_list+=(libstdc++ rpm-sequoia)
fi

if rpm --root "${SYSROOT}" -q libcap-libs; then
  expected_pkg_list+=(libcap-libs)
else
  expected_pkg_list+=(libcap)
fi

actual_pkg_count=${#actual_pkg_list[@]}
expected_pkg_count=${#expected_pkg_list[@]}

pkg_diff="$(echo ${expected_pkg_list[@]} ${actual_pkg_list[@]} | \
            tr ' ' '\n' | sort | uniq -u)"

if [ ${expected_pkg_count} -ne ${actual_pkg_count} ] || [ -n "${pkg_diff}" ]; then
  echoerr "Following package difference found in docker image:\n${pkg_diff}"
  echoerr "Expected package count: $expected_pkg_count"
  echoerr "Actual package count: $actual_pkg_count"
  exit 1
fi

rpm --root $SYSROOT/ --import $SYSROOT/etc/pki/rpm-gpg/*

# cleanup anything not needed inside rootfs
pushd $SYSROOT
rm -rf usr/src/ home/* var/log/* var/cache/tdnf/
# set TERM to linux due to stripped terminfo
echo "export TERM=linux" >> etc/bash.bashrc

popd

tar -I 'gzip -9' -C $SYSROOT -cpf $ROOTFS_TAR_FILENAME .

# expected size plus 2% wiggle room
if [ ${isRpmV6} -ne 0 ]; then
  size="18.5"
else
  size="16.6"
fi
max_size=$(printf "%.0f\n" "$(echo "${size} * 1024 * 1024" | bc -l)")

actual_size=$(wc -c ${ROOTFS_TAR_FILENAME} | cut -d' ' -f1)
if (( ${actual_size} > ${max_size} )); then
  echoerr "ERROR: docker image tarball size is bigger than expected"
  echoerr "Expected size(in bytes): $max_size"
  echoerr "Actual size(in bytes): $actual_size"
  rm -f $ROOTFS_TAR_FILENAME
  exit 1
fi
