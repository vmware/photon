#!/bin/bash -e

DIST=ph1
DIST_VER=1.0
ARCH=x86_64
BLD_ROOT=`readlink -f ../../..`
SPEC_DIR=${BLD_ROOT}/SPECS
STAGE_DIR=${BLD_ROOT}/stage

#
# Docker images for kubernetes-dashboard
#
K8S_DASH_VER=`cat ${SPEC_DIR}/kubernetes-dashboard/kubernetes-dashboard.spec | grep Version | cut -d: -f2 | tr -d ' '`
K8S_DASH_VER_REL=${K8S_DASH_VER}-`cat ${SPEC_DIR}/kubernetes-dashboard/kubernetes-dashboard.spec | grep Release | cut -d: -f2 | tr -d ' ' | cut -d% -f1`
K8S_DASH_RPM=kubernetes-dashboard-${K8S_DASH_VER_REL}.${DIST}.${ARCH}.rpm
K8S_DASH_RPM_FILE=${STAGE_DIR}/RPMS/x86_64/${K8S_DASH_RPM}
K8S_DASH_TAR=k8s-dashboard.tar

if [ ! -f ${K8S_DASH_RPM_FILE} ]
then
    echo "Kubernetes Dashboard RPM ${K8S_DASH_RPM_FILE} not found. Exiting.."
    exit 1
fi

IMG_NAME=vmware/k8s-dashboard-${DIST_VER}:v${K8S_DASH_VER}

IMG_ID=`docker images -q ${IMG_NAME} 2> /dev/null`
if [[ ! -z "${IMG_ID}" ]]; then
    echo "Removing image ${IMG_NAME}"
    docker rmi -f ${IMG_NAME}
fi

mkdir -p tmp/k8dash
cp ${K8S_DASH_RPM_FILE} tmp/k8dash/
pushd ./tmp/k8dash
rpm2cpio ${K8S_DASH_RPM} | cpio -vid
mkdir -p img
cp -p usr/bin/dashboard img/
cp -p -r opt/k8dashboard/* img/
cd img
docker build --rm -t ${IMG_NAME} .
docker save -o ${K8S_DASH_TAR} ${IMG_NAME}
mv -f ${K8S_DASH_TAR} ${STAGE_DIR}/
popd

rm -rf ./tmp
