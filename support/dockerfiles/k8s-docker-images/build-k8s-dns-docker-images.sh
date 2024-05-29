#!/bin/bash

set -e

DIST_TAG=$1
DIST_VER=$2
SPEC_DIR=$3
STAGE_DIR=$4
PH_BUILDER_TAG=$5
ARCH=x86_64

source common.sh

# Docker images for kubernetes-dns artifacts
fn="$(find -L "$SPEC_DIR" -type f -path "*/kubernetes-dns/kubernetes-dns.spec" )"
K8S_DNS_VER=$(get_spec_ver "${fn}")
K8S_DNS_VER_REL=${K8S_DNS_VER}-$(get_spec_rel "${fn}")
K8S_DNS_RPM=kubernetes-dns-${K8S_DNS_VER_REL}${DIST_TAG}.${ARCH}.rpm
K8S_DNS_RPM_FILE=${STAGE_DIR}/RPMS/$ARCH/${K8S_DNS_RPM}
K8S_DNS_BINS=(dnsmasq-nanny kube-dns sidecar)

if [ ! -f ${K8S_DNS_RPM_FILE} ]; then
  echo "Kubernetes DNS RPM ${K8S_DNS_RPM_FILE} not found. Exiting.."
  exit 1
fi

for K8S_BIN in ${K8S_DNS_BINS[*]}; do
  IMG_NAME=vmware/photon-${DIST_VER}-k8s-dns-${K8S_BIN}-amd64:${K8S_DNS_VER}
  IMG_ID=$(docker images -q ${IMG_NAME} 2> /dev/null)
  if [[ ! -z "${IMG_ID}" ]]; then
    echo "Removing image ${IMG_NAME}"
    docker rmi -f ${IMG_NAME}
  fi
done

mkdir -p tmp/k8dns
cp ${K8S_DNS_RPM_FILE} tmp/k8dns/
pushd ./tmp/k8dns
cmd="cd '${PWD}' && rpm2cpio '${K8S_DNS_RPM}' | cpio -vid"
run_cmd "${cmd}" "${PH_BUILDER_TAG}"
popd

start_repo_server

for K8S_BIN in ${K8S_DNS_BINS[*]}; do
  IMG_NAME=vmware/photon-${DIST_VER}-k8s-dns-${K8S_BIN}-amd64:${K8S_DNS_VER}
  K8S_TAR_NAME=k8s-dns-${K8S_BIN}-${K8S_DNS_VER_REL}.${ARCH}.tar
  create_container_img_archive "${IMG_NAME}" "./Dockerfile.${K8S_BIN}" "." \
                               "${K8S_TAR_NAME}" "${STAGE_DIR}/docker_images/"
done

rm -rf ./tmp
