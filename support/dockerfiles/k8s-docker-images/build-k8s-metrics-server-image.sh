#!/bin/bash -e

DIST_TAG=$1
DIST_VER=$2
SPEC_DIR=$3
STAGE_DIR=$4
ARCH=x86_64

#
# Docker images for kubernetes-metrics-server
#
K8S_MET_SERV_VER=`cat ${SPEC_DIR}/kubernetes-metrics-server/kubernetes-metrics-server.spec | grep Version: | cut -d: -f2 | tr -d ' '`
K8S_MET_SERV_VER_REL=${K8S_MET_SERV_VER}-`cat ${SPEC_DIR}/kubernetes-metrics-server/kubernetes-metrics-server.spec | grep Release: | cut -d: -f2 | tr -d ' ' | cut -d% -f1`
K8S_MET_SERV_RPM=kubernetes-metrics-server-${K8S_MET_SERV_VER_REL}${DIST_TAG}.${ARCH}.rpm
K8S_MET_SERV_RPM_FILE=${STAGE_DIR}/RPMS/x86_64/${K8S_MET_SERV_RPM}
K8S_MET_SERV_TAR=kubernetes-metrics-server-v${K8S_MET_SERV_VER_REL}.tar

if [ ! -f ${K8S_MET_SERV_RPM_FILE} ]
then
    echo "Kubernetes Metrics Server RPM ${K8S_MET_SERV_RPM_FILE} not found. Exiting.."
    exit 1
fi

IMG_NAME=vmware/photon-${DIST_VER}-kubernetes-metrics-server-amd64:v${K8S_MET_SERV_VER}

IMG_ID=`docker images -q ${IMG_NAME} 2> /dev/null`
if [[ ! -z "${IMG_ID}" ]]; then
    echo "Removing image ${IMG_NAME}"
    docker rmi -f ${IMG_NAME}
fi

mkdir -p tmp/k8smetserv
cp ${K8S_MET_SERV_RPM_FILE} tmp/k8smetserv/
pushd ./tmp/k8smetserv
rpm2cpio ${K8S_MET_SERV_RPM} | cpio -vid
popd

docker build --rm -t ${IMG_NAME} -f ./Dockerfile.metrics-server .
docker save -o ${K8S_MET_SERV_TAR} ${IMG_NAME}
gzip ${K8S_MET_SERV_TAR}
mv -f ${K8S_MET_SERV_TAR}.gz ${STAGE_DIR}/docker_images/

rm -rf ./tmp
