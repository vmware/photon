#!/bin/bash -e

DIST_TAG=$1
DIST_VER=$2
SPEC_DIR=$3
STAGE_DIR=$4
ARCH=noarch

#
# Docker image for wavefront-proxy
#
WAVEFRONT_PROXY_VER=`cat ${SPEC_DIR}/wavefront-proxy/wavefront-proxy.spec | grep Version | cut -d: -f2 | tr -d ' '`
WAVEFRONT_PROXY_VER_REL=${WAVEFRONT_PROXY_VER}-`cat ${SPEC_DIR}/wavefront-proxy/wavefront-proxy.spec | grep Release | cut -d: -f2 | tr -d ' ' | cut -d% -f1`
WAVEFRONT_PROXY_RPM=wavefront-proxy-${WAVEFRONT_PROXY_VER_REL}${DIST_TAG}.${ARCH}.rpm
WAVEFRONT_PROXY_RPM_FILE=${STAGE_DIR}/RPMS/${ARCH}/${WAVEFRONT_PROXY_RPM}
WAVEFRONT_PROXY_TAR=wavefront-proxy.tar

if [ ! -f ${WAVEFRONT_PROXY_RPM_FILE} ]
then
    echo "wavefront-proxy RPM ${WAVEFRONT_PROXY_RPM_FILE} not found. Exiting.."
    exit 1
fi

IMG_NAME=vmware_photon_${DIST_VER}/wavefront-proxy:v${WAVEFRONT_PROXY_VER}

IMG_ID=`docker images -q ${IMG_NAME} 2> /dev/null`
if [[ ! -z "${IMG_ID}" ]]; then
    echo "Removing image ${IMG_NAME}"
    docker rmi -f ${IMG_NAME}
fi

mkdir -p tmp/wavefront-proxy
cp ${WAVEFRONT_PROXY_RPM_FILE} tmp/wavefront-proxy/
pushd ./tmp/wavefront-proxy
rpm2cpio ${WAVEFRONT_PROXY_RPM} | cpio -vid
popd
docker build --rm -t ${IMG_NAME} -f Dockerfile.wavefront-proxy .
docker save -o ${WAVEFRONT_PROXY_TAR} ${IMG_NAME}
gzip ${WAVEFRONT_PROXY_TAR}
mv -f ${WAVEFRONT_PROXY_TAR}.gz ${STAGE_DIR}/

rm -rf ./tmp
