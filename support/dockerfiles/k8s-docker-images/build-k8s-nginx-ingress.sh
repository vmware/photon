#!/bin/bash -e

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
NGINX_INC_TAR=nginx-ingress.tar

if [ ! -f ${NGINX_INC_RPM_FILE} ]
then
    echo "nginx ingress RPM ${NGINX_INC_RPM_FILE} not found. Exiting.."
    exit 1
fi

IMG_NAME=vmware_photon2/nginx-ingress:v${NGINX_INC_VER}

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
docker build --rm -t ${IMG_NAME} -f Dockerfile.nginx-ingress .
docker save -o ${NGINX_INC_TAR} ${IMG_NAME}
mv -f ${NGINX_INC_TAR} ${STAGE_DIR}/

rm -rf ./tmp
