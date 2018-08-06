#!/bin/bash -e

DIST_TAG=$1
DIST_VER=$2
SPEC_DIR=$3
STAGE_DIR=$4
ARCH=x86_64

#
# Docker images for coredns
#
K8S_COREDNS_VER=`cat ${SPEC_DIR}/coredns/coredns.spec | grep Version | cut -d: -f2 | tr -d ' '`
K8S_COREDNS_VER_REL=${K8S_COREDNS_VER}-`cat ${SPEC_DIR}/coredns/coredns.spec | grep Release | cut -d: -f2 | tr -d ' ' | cut -d% -f1`
K8S_COREDNS_RPM=coredns-${K8S_COREDNS_VER_REL}${DIST_TAG}.${ARCH}.rpm
K8S_COREDNS_RPM_FILE=${STAGE_DIR}/RPMS/x86_64/${K8S_COREDNS_RPM}
K8S_COREDNS_TAR=coredns-v${K8S_COREDNS_VER_REL}.tar

if [ ! -f ${K8S_COREDNS_RPM_FILE} ]
then
    echo "Core DNS RPM ${K8S_COREDNS_RPM_FILE} not found. Exiting.."
    exit 1
fi

IMG_NAME=vmware/photon-${DIST_VER}-coredns-amd64:v${K8S_COREDNS_VER}

IMG_ID=`docker images -q ${IMG_NAME} 2> /dev/null`
if [[ ! -z "${IMG_ID}" ]]; then
    echo "Removing image ${IMG_NAME}"
    docker rmi -f ${IMG_NAME}
fi

mkdir -p tmp
cp ${K8S_COREDNS_RPM_FILE} tmp
pushd ./tmp
rpm2cpio ${K8S_COREDNS_RPM} | cpio -vid
popd

docker build --rm -t ${IMG_NAME} -f ./Dockerfile.coredns .
docker save -o ${K8S_COREDNS_TAR} ${IMG_NAME}
gzip ${K8S_COREDNS_TAR}
mv -f ${K8S_COREDNS_TAR}.gz ${STAGE_DIR}/docker_images/

rm -rf ./tmp
