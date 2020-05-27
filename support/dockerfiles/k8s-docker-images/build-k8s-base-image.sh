#!/bin/bash -e

DIST_VER=$1
BUILD_NUM=$2
STAGE_DIR=$3

#
# Base docker image for kubernetes containers
#
PHOTON_ROOTFS_FILE=${STAGE_DIR}/photon-rootfs-${DIST_VER}-${BUILD_NUM}.tar.gz
K8S_BASE_IMG_NAME=k8s-base-image:${DIST_VER}

if [ ! -f ${PHOTON_ROOTFS_FILE} ]
then
    echo "Photon rootfs file ${PHOTON_ROOTFS_FILE} not found. Exiting.."
    exit 1
fi

IMG_ID=`docker images -q ${K8S_BASE_IMG_NAME} 2> /dev/null`
if [[ ! -z "${IMG_ID}" ]]; then
    echo "Removing image ${K8S_BASE_IMG_NAME}"
    docker rmi -f ${K8S_BASE_IMG_NAME}
fi

mkdir -p tmp/k8sbase
cp ${PHOTON_ROOTFS_FILE} tmp/k8sbase/photon-rootfs-${DIST_VER}.tar.gz
cp Dockerfile.k8sbase tmp/k8sbase/
pushd ./tmp/k8sbase
docker build --rm -t ${K8S_BASE_IMG_NAME} -f Dockerfile.k8sbase .
popd

rm -rf ./tmp
