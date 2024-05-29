#!/bin/bash

set -e

DIST_TAG=$1
DIST_VER=$2
SPEC_DIR=$3
STAGE_DIR=$4
PH_BUILDER_TAG=$5
ARCH=noarch

source common.sh

# Docker image for wavefront-proxy
fn="$(find -L "$SPEC_DIR" -type f -path "*/wavefront-proxy/wavefront-proxy.spec" )"
WAVEFRONT_PROXY_VER=$(get_spec_ver "${fn}")
WAVEFRONT_PROXY_VER_REL=${WAVEFRONT_PROXY_VER}-$(get_spec_rel "${fn}")
WAVEFRONT_PROXY_RPM=wavefront-proxy-${WAVEFRONT_PROXY_VER_REL}${DIST_TAG}.${ARCH}.rpm
WAVEFRONT_PROXY_RPM_FILE=${STAGE_DIR}/RPMS/${ARCH}/${WAVEFRONT_PROXY_RPM}
WAVEFRONT_PROXY_TAR=wavefront-proxy-v${WAVEFRONT_PROXY_VER_REL}.tar

if [ ! -f ${WAVEFRONT_PROXY_RPM_FILE} ]; then
  echo "wavefront-proxy RPM ${WAVEFRONT_PROXY_RPM_FILE} not found. Exiting.."
  exit 1
fi

IMG_NAME=vmware/photon-${DIST_VER}-wavefront-proxy:v${WAVEFRONT_PROXY_VER}

IMG_ID=$(docker images -q ${IMG_NAME} 2> /dev/null)
if [[ ! -z "${IMG_ID}" ]]; then
  echo "Removing image ${IMG_NAME}"
  docker rmi -f ${IMG_NAME}
fi

mkdir -p tmp/wavefront-proxy
cp ${WAVEFRONT_PROXY_RPM_FILE} tmp/wavefront-proxy/
pushd ./tmp/wavefront-proxy
cmd="cd '${PWD}' && rpm2cpio '${WAVEFRONT_PROXY_RPM}' | cpio -vid"
run_cmd "${cmd}" "${PH_BUILDER_TAG}"
popd

start_repo_server

create_container_img_archive "${IMG_NAME}" "Dockerfile.wavefront-proxy" "." \
                             "${WAVEFRONT_PROXY_TAR}" "${STAGE_DIR}/docker_images/"

rm -rf ./tmp
