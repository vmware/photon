#!/bin/bash

set -e

DIST_TAG=$1
DIST_VER=$2
SPEC_DIR=$3
STAGE_DIR=$4
PH_BUILDER_TAG=$5
ARCH=x86_64

source common.sh

# Docker images for kubernetes-dashboard
fn="${SPEC_DIR}/kubernetes-dashboard/kubernetes-dashboard.spec"
K8S_DASH_VER=$(get_spec_ver "${fn}")
K8S_DASH_VER_REL=${K8S_DASH_VER}-$(get_spec_rel "${fn}")
K8S_DASH_RPM=kubernetes-dashboard-${K8S_DASH_VER_REL}${DIST_TAG}.${ARCH}.rpm
K8S_DASH_RPM_FILE=${STAGE_DIR}/RPMS/$ARCH/${K8S_DASH_RPM}
K8S_DASH_TAR=kubernetes-dashboard-v${K8S_DASH_VER_REL}.${ARCH}.tar

if [ ! -f ${K8S_DASH_RPM_FILE} ]; then
  echo "Kubernetes Dashboard RPM ${K8S_DASH_RPM_FILE} not found. Exiting.."
  exit 1
fi

IMG_NAME=vmware/photon-${DIST_VER}-kubernetes-dashboard-amd64:v${K8S_DASH_VER}

IMG_ID="$(docker images -q ${IMG_NAME} 2> /dev/null)"
if [[ ! -z "${IMG_ID}" ]]; then
  echo "Removing image ${IMG_NAME}"
  docker rmi -f ${IMG_NAME}
fi

mkdir -p tmp/k8dash
cp ${K8S_DASH_RPM_FILE} tmp/k8dash/
cp ./Dockerfile.kubernetes-dashboard tmp/k8dash

pushd ./tmp/k8dash
cmd="cd '${PWD}' && rpm2cpio '${K8S_DASH_RPM}' | cpio -vid"
run_cmd "${cmd}" "${PH_BUILDER_TAG}"

mkdir -p img

cp -pr usr/bin/dashboard \
       opt/k8dashboard/* \
       img/
cp ./Dockerfile.kubernetes-dashboard img/Dockerfile

pushd img
cat Dockerfile
create_container_img_archive "${IMG_NAME}" "Dockerfile" "." \
                             "${K8S_DASH_TAR}" "${STAGE_DIR}/docker_images/"
popd # img
popd # tmp/k8dash

rm -rf ./tmp
