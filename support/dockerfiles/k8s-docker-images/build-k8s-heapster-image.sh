#!/bin/bash

set -e

DIST_TAG=$1
DIST_VER=$2
STAGE_DIR=$3
PH_BUILDER_TAG=$4
ARCH=x86_64

source common.sh

# Docker images for heapster - kubernetes cluster monitoring tool.
fn=$(get_spec_path "*/heapster/heapster.spec" "${@:5}")

K8S_HEAPSTER_VER=$(get_spec_ver "${fn}")
K8S_HEAPSTER_VER_REL=${K8S_HEAPSTER_VER}-$(get_spec_rel "${fn}")
K8S_HEAPSTER_RPM=heapster-${K8S_HEAPSTER_VER_REL}${DIST_TAG}.${ARCH}.rpm
K8S_HEAPSTER_RPM_FILE=${STAGE_DIR}/RPMS/${ARCH}/${K8S_HEAPSTER_RPM}

if [ ! -f ${K8S_HEAPSTER_RPM_FILE} ]; then
  echo "Kubernetes HEAPSTER RPM ${K8S_HEAPSTER_RPM_FILE} not found. Exiting.."
  exit 1
fi

IMG_NAME=vmware/photon-${DIST_VER}-k8s-heapster-amd64:${K8S_HEAPSTER_VER}
IMG_ID=$(docker images -q ${IMG_NAME} 2> /dev/null)
if [[ ! -z "${IMG_ID}" ]]; then
  echo "Removing image ${IMG_NAME}"
  docker rmi -f ${IMG_NAME}
fi

mkdir -p tmp/k8heapster
cp ${K8S_HEAPSTER_RPM_FILE} tmp/k8heapster/
pushd ./tmp/k8heapster
cmd="cd '${PWD}' && rpm2cpio '${K8S_HEAPSTER_RPM}' | cpio -vid"
run_cmd "${cmd}" "${PH_BUILDER_TAG}"
popd

start_repo_server

K8S_TAR_NAME=k8s-heapster-${K8S_HEAPSTER_VER_REL}.${ARCH}.tar
create_container_img_archive "${IMG_NAME}" "./Dockerfile.heapster" "." \
                             "${K8S_TAR_NAME}" "${STAGE_DIR}/docker_images/"

rm -rf ./tmp
