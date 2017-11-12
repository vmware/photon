#!/bin/bash -e

source common.inc

DIST_TAG=$1
DIST_VER=$2
SPEC_DIR=$3
STAGE_DIR=$4
ARCH=x86_64

#
# Docker image for kubernetes nginx ingress controller
#
NGINX_INC_VER=`cat ${SPEC_DIR}/nginx-ingress/nginx-ingress.spec | grep Version | cut -d: -f2 | tr -d ' '`
NGINX_INC_VER_REL=${NGINX_INC_VER}-`cat ${SPEC_DIR}/nginx-ingress/nginx-ingress.spec | grep Release | cut -d: -f2 | tr -d ' ' | cut -d% -f1`
NGINX_INC_RPM=nginx-ingress-${NGINX_INC_VER_REL}${DIST_TAG}.${ARCH}.rpm
NGINX_INC_RPM_FILE=${STAGE_DIR}/RPMS/x86_64/${NGINX_INC_RPM}
NGINX_INC_TAR=nginx-ingress-v${NGINX_INC_VER_REL}.tar

if [ ! -f ${NGINX_INC_RPM_FILE} ]
then
    echo "nginx ingress RPM ${NGINX_INC_RPM_FILE} not found. Exiting.."
    exit 1
fi

IMG_NAME=vmware/photon-${DIST_VER}-nginx-ingress:v${NGINX_INC_VER}

IMG_ID=`docker images -q ${IMG_NAME} 2> /dev/null`
if [[ ! -z "${IMG_ID}" ]]; then
    echo "Removing image ${IMG_NAME}"
    docker rmi -f ${IMG_NAME}
fi

mkdir -p tmp/nginxinc
cp ${NGINX_INC_RPM_FILE} tmp/nginxinc/
pushd ./tmp/nginxinc
rpm2cpio ${NGINX_INC_RPM} | cpio -vid
popd

setup_repo

docker build --rm -t ${IMG_NAME} -f Dockerfile.nginx-ingress .
docker save -o ${NGINX_INC_TAR} ${IMG_NAME}
gzip ${NGINX_INC_TAR}
mv -f ${NGINX_INC_TAR}.gz ${STAGE_DIR}/docker_images/

rm -rf ./tmp
