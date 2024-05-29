#!/bin/bash

set -e

DIST_TAG=$1
DIST_VER=$2
SPEC_DIR=$3
STAGE_DIR=$4
PH_BUILDER_TAG=$5
ARCH=x86_64

source common.sh

# Docker images for coredns
fn="$(find -L "$SPEC_DIR" -type f -path "*/coredns/coredns.spec" )"
K8S_COREDNS_VER=$(get_spec_ver "${fn}")
K8S_COREDNS_VER_REL=${K8S_COREDNS_VER}-$(get_spec_rel "${fn}")
K8S_COREDNS_RPM=coredns-${K8S_COREDNS_VER_REL}${DIST_TAG}.${ARCH}.rpm
K8S_COREDNS_RPM_FILE=${STAGE_DIR}/RPMS/$ARCH/${K8S_COREDNS_RPM}
K8S_COREDNS_TAR=coredns-v${K8S_COREDNS_VER_REL}.${ARCH}.tar

if [ ! -f ${K8S_COREDNS_RPM_FILE} ]; then
  echo "Core DNS RPM ${K8S_COREDNS_RPM_FILE} not found. Exiting.."
  exit 1
fi

IMG_NAME=vmware/photon-${DIST_VER}-coredns-amd64:v${K8S_COREDNS_VER}

IMG_ID=$(docker images -q ${IMG_NAME} 2> /dev/null)
if [[ ! -z "${IMG_ID}" ]]; then
  echo "Removing image ${IMG_NAME}"
  docker rmi -f ${IMG_NAME}
fi

mkdir -p tmp
cp ${K8S_COREDNS_RPM_FILE} tmp
pushd ./tmp
cmd="cd '${PWD}' && rpm2cpio '${K8S_COREDNS_RPM}' | cpio -vid"
run_cmd "${cmd}" "${PH_BUILDER_TAG}"
popd

start_repo_server

create_container_img_archive "${IMG_NAME}" "./Dockerfile.coredns" "." \
                             "${K8S_COREDNS_TAR}" "${STAGE_DIR}/docker_images/"

rm -rf ./tmp
