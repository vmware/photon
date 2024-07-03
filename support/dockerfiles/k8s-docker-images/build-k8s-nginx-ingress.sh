#!/bin/bash

set -e

DIST_TAG=$1
DIST_VER=$2
STAGE_DIR=$3
PH_BUILDER_TAG=$4
ARCH=x86_64

source common.sh

# Docker image for kubernetes nginx ingress controller
fn=$(get_spec_path "*/nginx-ingress/nginx-ingress.spec" "${@:5}")

NGINX_INC_VER=$(get_spec_ver "${fn}")
NGINX_INC_VER_REL=${NGINX_INC_VER}-$(get_spec_rel "${fn}")
NGINX_INC_RPM=nginx-ingress-${NGINX_INC_VER_REL}${DIST_TAG}.${ARCH}.rpm
NGINX_INC_RPM_FILE=${STAGE_DIR}/RPMS/$ARCH/${NGINX_INC_RPM}
NGINX_INC_TAR=nginx-ingress-v${NGINX_INC_VER_REL}.${ARCH}.tar

if [ ! -f ${NGINX_INC_RPM_FILE} ]; then
  echo "nginx ingress RPM ${NGINX_INC_RPM_FILE} not found. Exiting.."
  exit 1
fi

IMG_NAME=vmware/photon-${DIST_VER}-nginx-ingress:v${NGINX_INC_VER}

IMG_ID=$(docker images -q ${IMG_NAME} 2> /dev/null)
if [[ ! -z "${IMG_ID}" ]]; then
  echo "Removing image ${IMG_NAME}"
  docker rmi -f ${IMG_NAME}
fi

mkdir -p tmp/nginxinc
cp ${NGINX_INC_RPM_FILE} tmp/nginxinc/
pushd ./tmp/nginxinc
cmd="cd '${PWD}' && rpm2cpio '${NGINX_INC_RPM}' | cpio -vid"
run_cmd "${cmd}" "${PH_BUILDER_TAG}"
popd

start_repo_server

create_container_img_archive "${IMG_NAME}" "Dockerfile.nginx-ingress" "." \
                             "${NGINX_INC_TAR}" "${STAGE_DIR}/docker_images/"

rm -rf ./tmp
