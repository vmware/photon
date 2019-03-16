#!/bin/bash -e

DIST_TAG=$1
DIST_VER=$2
SPEC_DIR=$3
STAGE_DIR=$4
ARCH=x86_64

#
# Docker images for kubernetes artifacts
#
for file in ${SPEC_DIR}/kubernetes/kubernetes.spec; do
    K8S_VER=`cat ${file} | grep "^Version:" | cut -d: -f2 | tr -d ' '`
    K8S_VER_REL=${K8S_VER}-`cat ${file} | grep "^Release:" | cut -d: -f2 | tr -d ' ' | cut -d% -f1`
    K8S_RPM=kubernetes-${K8S_VER_REL}${DIST_TAG}.${ARCH}.rpm
    K8S_RPM_FILE=../../../stage/RPMS/x86_64/${K8S_RPM}
    K8S_PAUSE_RPM=kubernetes-pause-${K8S_VER_REL}${DIST_TAG}.${ARCH}.rpm
    K8S_PAUSE_RPM_FILE=../../../stage/RPMS/x86_64/${K8S_PAUSE_RPM}

    if [ ! -f ${K8S_RPM_FILE} ]
    then
        echo "Kubernetes RPM ${K8S_RPM_FILE} not found. Exiting.."
        exit 1
    fi

    K8S_BINS=(kube-apiserver kube-controller-manager kube-proxy kube-scheduler)
    for K8S_BIN in ${K8S_BINS[*]}; do
        IMG_NAME=vmware/photon-${DIST_VER}-${K8S_BIN}-amd64:v${K8S_VER}
        IMG_ID=`docker images -q ${IMG_NAME} 2> /dev/null`
        if [[ ! -z "${IMG_ID}" ]]; then
            echo "Removing image ${IMG_NAME}"
            docker rmi -f ${IMG_NAME}
        fi
    done

    mkdir -p tmp/k8s
    cp ${K8S_RPM_FILE} tmp/k8s/
    cp ${K8S_PAUSE_RPM_FILE} tmp/k8s/
    pushd ./tmp/k8s
    rpm2cpio ${K8S_RPM} | cpio -vid
    rpm2cpio ${K8S_PAUSE_RPM} | cpio -vid
    popd

    for K8S_BIN in ${K8S_BINS[*]}; do
        IMG_NAME=vmware/photon-${DIST_VER}-${K8S_BIN}-amd64:v${K8S_VER}
        K8S_TAR_NAME=${K8S_BIN}-v${K8S_VER_REL}.tar
        docker build --rm -t ${IMG_NAME} -f ./Dockerfile.${K8S_BIN} .
        docker save -o ${K8S_TAR_NAME} ${IMG_NAME}
        gzip ${K8S_TAR_NAME}
        mv -f ${K8S_TAR_NAME}.gz ${STAGE_DIR}/docker_images/
    done


    #
    # K8S Pause container
    #
    PAUSE_IMG_NAME=vmware/photon-${DIST_VER}-pause-amd64:v${K8S_VER}
    PAUSE_TAR_NAME=k8s-pause-v${K8S_VER_REL}.tar

    PAUSE_IMG_ID=`docker images -q ${PAUSE_IMG_NAME} 2> /dev/null`
    if [[ ! -z "${PAUSE_IMG_ID}" ]]; then
        echo "Removing image ${PAUSE_IMG_NAME}"
        docker rmi -f ${PAUSE_IMG_NAME}
    fi

    docker build --rm -t ${PAUSE_IMG_NAME} -f ./Dockerfile.pause .
    docker save -o ${PAUSE_TAR_NAME} ${PAUSE_IMG_NAME}
    gzip ${PAUSE_TAR_NAME}
    mv -f ${PAUSE_TAR_NAME}.gz ${STAGE_DIR}/docker_images/

    rm -rf ./tmp
done
