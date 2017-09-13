#!/bin/bash -e

DIST_TAG=$1
DIST_VER=$2
SPEC_DIR=$3
STAGE_DIR=$4
ARCH=x86_64

#
# Docker images for heapster - kubernetes cluster monitoring tool.
#

K8S_HEAPSTER_VER=`cat ${SPEC_DIR}/heapster/heapster.spec | grep Version | cut -d: -f2 | tr -d ' '`
K8S_HEAPSTER_VER_REL=${K8S_HEAPSTER_VER}-`cat ${SPEC_DIR}/heapster/heapster.spec | grep Release | cut -d: -f2 | tr -d ' ' | cut -d% -f1`
K8S_HEAPSTER_RPM=heapster-${K8S_HEAPSTER_VER_REL}${DIST_TAG}.${ARCH}.rpm
K8S_HEAPSTER_RPM_FILE=${STAGE_DIR}/RPMS/x86_64/${K8S_HEAPSTER_RPM}

if [ ! -f ${K8S_HEAPSTER_RPM_FILE} ]
then
    echo "Kubernetes HEAPSTER RPM ${K8S_HEAPSTER_RPM_FILE} not found. Exiting.."
    exit 1
fi

IMG_NAME=vmware_photon/k8s-heapster-amd64:${K8S_HEAPSTER_VER}
IMG_ID=`docker images -q ${IMG_NAME} 2> /dev/null`
if [[ ! -z "${IMG_ID}" ]]; then
    echo "Removing image ${IMG_NAME}"
    docker rmi -f ${IMG_NAME}
fi

mkdir -p tmp/k8heapster
cp ${K8S_HEAPSTER_RPM_FILE} tmp/k8heapster/
pushd ./tmp/k8heapster
rpm2cpio ${K8S_HEAPSTER_RPM} | cpio -vid
popd

K8S_TAR_NAME=k8s-heapster.tar
docker build --rm -t ${IMG_NAME} -f ./Dockerfile.heapster .
docker save -o ${K8S_TAR_NAME} ${IMG_NAME}
mv -f ${K8S_TAR_NAME} ${STAGE_DIR}/

rm -rf ./tmp
