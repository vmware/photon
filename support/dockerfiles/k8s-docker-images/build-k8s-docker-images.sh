#!/bin/bash -xe

DIST_TAG=$1
DIST_VER=$2
SPEC_DIR=$3
STAGE_DIR=$4
PH_BUILDER_TAG=$5
ARCH=x86_64

source common.sh

start_repo_server

# Docker images for kubernetes artifacts
fn="$(find -L "$SPEC_DIR" -type f -path "*/kubernetes/kubernetes.spec" )"
K8S_VER=$(get_spec_ver "${fn}")
K8S_VER_REL=${K8S_VER}-$(get_spec_rel "${fn}")
K8S_RPM=kubernetes-${K8S_VER_REL}${DIST_TAG}.${ARCH}.rpm
K8S_RPM_FILE=${STAGE_DIR}/RPMS/$ARCH/${K8S_RPM}
K8S_PAUSE_RPM=kubernetes-pause-${K8S_VER_REL}${DIST_TAG}.${ARCH}.rpm
K8S_PAUSE_RPM_FILE=${STAGE_DIR}/RPMS/$ARCH/${K8S_PAUSE_RPM}

if [ ! -f ${K8S_RPM_FILE} ]; then
  echo "Kubernetes RPM ${K8S_RPM_FILE} not found. Exiting.."
  exit 1
fi

K8S_BINS=(kube-apiserver kube-controller-manager kube-proxy kube-scheduler)
for K8S_BIN in ${K8S_BINS[*]}; do
  IMG_NAME=vmware/photon-${DIST_VER}-${K8S_BIN}-amd64:v${K8S_VER}
  IMG_ID=$(docker images -q ${IMG_NAME} 2> /dev/null)
  if [[ ! -z "${IMG_ID}" ]]; then
    echo "Removing image ${IMG_NAME}"
    docker rmi -f ${IMG_NAME}
  fi
done

mkdir -p tmp/k8s

cp ${K8S_RPM_FILE} \
    ${K8S_PAUSE_RPM_FILE} \
    tmp/k8s/

pushd ./tmp/k8s
cmd="cd '${PWD}' && rpm2cpio '${K8S_RPM}' | cpio -vid && rpm2cpio '${K8S_PAUSE_RPM}' | cpio -vid"
run_cmd "${cmd}" "${PH_BUILDER_TAG}"
popd

for K8S_BIN in ${K8S_BINS[*]}; do
  IMG_NAME=vmware/photon-${DIST_VER}-${K8S_BIN}-amd64:v${K8S_VER}
  K8S_TAR_NAME=${K8S_BIN}-v${K8S_VER_REL}.${ARCH}.tar
  create_container_img_archive "${IMG_NAME}" "./Dockerfile.${K8S_BIN}" "." \
                                "${K8S_TAR_NAME}" "${STAGE_DIR}/docker_images/"
done

# K8S Pause container
PAUSE_IMG_NAME=vmware/photon-${DIST_VER}-pause-amd64:v${K8S_VER}
PAUSE_TAR_NAME=k8s-pause-v${K8S_VER_REL}.${ARCH}.tar

PAUSE_IMG_ID=$(docker images -q ${PAUSE_IMG_NAME} 2> /dev/null)
if [[ ! -z "${PAUSE_IMG_ID}" ]]; then
  echo "Removing image ${PAUSE_IMG_NAME}"
  docker rmi -f ${PAUSE_IMG_NAME}
fi

create_container_img_archive "${PAUSE_IMG_NAME}" "./Dockerfile.pause" "." \
                              "${PAUSE_TAR_NAME}" "${STAGE_DIR}/docker_images/"

rm -rf ./tmp
