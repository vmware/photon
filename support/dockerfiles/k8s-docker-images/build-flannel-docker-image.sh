#!/bin/bash -e

DIST_TAG=$1
DIST_VER=$2
SPEC_DIR=$3
STAGE_DIR=$4
ARCH=x86_64

#
# Docker image for flannel
#
FLANNEL_VER=`cat ${SPEC_DIR}/flannel/flannel.spec | grep Version | cut -d: -f2 | tr -d ' '`
FLANNEL_VER_REL=${FLANNEL_VER}-`cat ${SPEC_DIR}/flannel/flannel.spec | grep Release | cut -d: -f2 | tr -d ' ' | cut -d% -f1`
FLANNEL_RPM=flannel-${FLANNEL_VER_REL}${DIST_TAG}.${ARCH}.rpm
FLANNEL_RPM_FILE=${STAGE_DIR}/RPMS/x86_64/${FLANNEL_RPM}
FLANNEL_TAR=flannel-v${FLANNEL_VER_REL}.tar

if [ ! -f ${FLANNEL_RPM_FILE} ]
then
    echo "flannel RPM ${FLANNEL_RPM_FILE} not found. Exiting.."
    exit 1
fi

IMG_NAME=vmware/photon-${DIST_VER}-flannel:v${FLANNEL_VER}

IMG_ID=`docker images -q ${IMG_NAME} 2> /dev/null`
if [[ ! -z "${IMG_ID}" ]]; then
    echo "Removing image ${IMG_NAME}"
    docker rmi -f ${IMG_NAME}
fi

mkdir -p tmp/flannel
cp ${FLANNEL_RPM_FILE} tmp/flannel/
pushd ./tmp/flannel
rpm2cpio ${FLANNEL_RPM} | cpio -vid
popd

docker build --rm -t ${IMG_NAME} -f Dockerfile.flannel .
docker save -o ${FLANNEL_TAR} ${IMG_NAME}
gzip ${FLANNEL_TAR}
mv -f ${FLANNEL_TAR}.gz ${STAGE_DIR}/docker_images/

rm -rf ./tmp
