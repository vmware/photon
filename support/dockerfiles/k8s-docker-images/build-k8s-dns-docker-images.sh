#!/bin/bash -e

source common.inc

DIST_TAG=$1
DIST_VER=$2
SPEC_DIR=$3
STAGE_DIR=$4
ARCH=x86_64

#
# Docker images for kubernetes-dns artifacts
#
K8S_DNS_VER=`cat ${SPEC_DIR}/kubernetes-dns/kubernetes-dns.spec | grep Version | cut -d: -f2 | tr -d ' '`
K8S_DNS_VER_REL=${K8S_DNS_VER}-`cat ${SPEC_DIR}/kubernetes-dns/kubernetes-dns.spec | grep Release | cut -d: -f2 | tr -d ' ' | cut -d% -f1`
K8S_DNS_RPM=kubernetes-dns-${K8S_DNS_VER_REL}${DIST_TAG}.${ARCH}.rpm
K8S_DNS_RPM_FILE=${STAGE_DIR}/RPMS/x86_64/${K8S_DNS_RPM}
K8S_DNS_BINS=(dnsmasq-nanny kube-dns sidecar)

if [ ! -f ${K8S_DNS_RPM_FILE} ]
then
    echo "Kubernetes DNS RPM ${K8S_DNS_RPM_FILE} not found. Exiting.."
    exit 1
fi

for K8S_BIN in ${K8S_DNS_BINS[*]}; do
    IMG_NAME=vmware/photon-${DIST_VER}-k8s-dns-${K8S_BIN}-amd64:${K8S_DNS_VER}
    IMG_ID=`docker images -q ${IMG_NAME} 2> /dev/null`
    if [[ ! -z "${IMG_ID}" ]]; then
        echo "Removing image ${IMG_NAME}"
        docker rmi -f ${IMG_NAME}
    fi
done

mkdir -p tmp/k8dns
cp ${K8S_DNS_RPM_FILE} tmp/k8dns/
pushd ./tmp/k8dns
rpm2cpio ${K8S_DNS_RPM} | cpio -vid
popd

setup_repo

for K8S_BIN in ${K8S_DNS_BINS[*]}; do
    IMG_NAME=vmware/photon-${DIST_VER}-k8s-dns-${K8S_BIN}-amd64:${K8S_DNS_VER}
    K8S_TAR_NAME=k8s-dns-${K8S_BIN}-${K8S_DNS_VER_REL}.tar
    docker build --rm -t ${IMG_NAME} -f ./Dockerfile.${K8S_BIN} .
    docker save -o ${K8S_TAR_NAME} ${IMG_NAME}
    gzip ${K8S_TAR_NAME}
    mv -f ${K8S_TAR_NAME}.gz ${STAGE_DIR}/docker_images/
done

rm -rf ./tmp
