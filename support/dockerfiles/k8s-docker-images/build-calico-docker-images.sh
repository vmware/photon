#!/bin/bash -e

source common.inc

DIST_TAG=$1
DIST_VER=$2
SPEC_DIR=$3
STAGE_DIR=$4
ARCH=x86_64

#
# Docker images for calico-node, calico-cni
#
CALICO_VER=`cat ${SPEC_DIR}/calico/calico.spec | grep Version | cut -d: -f2 | tr -d ' '`
CALICO_VER_REL=${CALICO_VER}-`cat ${SPEC_DIR}/calico/calico.spec | grep Release | cut -d: -f2 | tr -d ' ' | cut -d% -f1`
CALICO_RPM=calico-${CALICO_VER_REL}${DIST_TAG}.${ARCH}.rpm
CALICO_RPM_FILE=${STAGE_DIR}/RPMS/x86_64/${CALICO_RPM}

CALICO_BGP_VER=`cat ${SPEC_DIR}/calico-bgp-daemon/calico-bgp-daemon.spec | grep Version | cut -d: -f2 | tr -d ' '`
CALICO_BGP_VER_REL=${CALICO_BGP_VER}-`cat ${SPEC_DIR}/calico-bgp-daemon/calico-bgp-daemon.spec | grep Release | cut -d: -f2 | tr -d ' ' | cut -d% -f1`
CALICO_BGP_RPM=calico-bgp-daemon-${CALICO_BGP_VER_REL}${DIST_TAG}.${ARCH}.rpm
CALICO_BGP_RPM_FILE=${STAGE_DIR}/RPMS/x86_64/${CALICO_BGP_RPM}

GO_BGP_VER=`cat ${SPEC_DIR}/gobgp/gobgp.spec | grep Version | cut -d: -f2 | tr -d ' '`
GO_BGP_VER_REL=${GO_BGP_VER}-`cat ${SPEC_DIR}/gobgp/gobgp.spec | grep Release | cut -d: -f2 | tr -d ' ' | cut -d% -f1`
GO_BGP_RPM=gobgp-${GO_BGP_VER_REL}${DIST_TAG}.${ARCH}.rpm
GO_BGP_RPM_FILE=${STAGE_DIR}/RPMS/x86_64/${GO_BGP_RPM}

CALICO_BIRD_VER=`cat ${SPEC_DIR}/calico-bird/calico-bird.spec | grep Version | cut -d: -f2 | tr -d ' '`
CALICO_BIRD_VER_REL=${CALICO_BIRD_VER}-`cat ${SPEC_DIR}/calico-bird/calico-bird.spec | grep Release | cut -d: -f2 | tr -d ' ' | cut -d% -f1`
CALICO_BIRD_RPM=calico-bird-${CALICO_BIRD_VER_REL}${DIST_TAG}.${ARCH}.rpm
CALICO_BIRD_RPM_FILE=${STAGE_DIR}/RPMS/x86_64/${CALICO_BIRD_RPM}

CALICO_CONFD_VER=`cat ${SPEC_DIR}/calico-confd/calico-confd.spec | grep Version | cut -d: -f2 | tr -d ' '`
CALICO_CONFD_VER_REL=${CALICO_CONFD_VER}-`cat ${SPEC_DIR}/calico-confd/calico-confd.spec | grep Release | cut -d: -f2 | tr -d ' ' | cut -d% -f1`
CALICO_CONFD_RPM=calico-confd-${CALICO_CONFD_VER_REL}${DIST_TAG}.${ARCH}.rpm
CALICO_CONFD_RPM_FILE=${STAGE_DIR}/RPMS/x86_64/${CALICO_CONFD_RPM}

CALICO_FELIX_VER=`cat ${SPEC_DIR}/calico-felix/calico-felix.spec | grep ^Version | cut -d: -f2 | tr -d ' '`
CALICO_FELIX_VER_REL=${CALICO_FELIX_VER}-`cat ${SPEC_DIR}/calico-felix/calico-felix.spec | grep Release | cut -d: -f2 | tr -d ' ' | cut -d% -f1`
CALICO_FELIX_RPM=calico-felix-${CALICO_FELIX_VER_REL}${DIST_TAG}.${ARCH}.rpm
CALICO_FELIX_RPM_FILE=${STAGE_DIR}/RPMS/x86_64/${CALICO_FELIX_RPM}

CALICO_LIBNET_VER=`cat ${SPEC_DIR}/calico-libnetwork/calico-libnetwork.spec | grep ^Version | cut -d: -f2 | tr -d ' '`
CALICO_LIBNET_VER_REL=${CALICO_LIBNET_VER}-`cat ${SPEC_DIR}/calico-libnetwork/calico-libnetwork.spec | grep Release | cut -d: -f2 | tr -d ' ' | cut -d% -f1`
CALICO_LIBNET_RPM=calico-libnetwork-${CALICO_LIBNET_VER_REL}${DIST_TAG}.${ARCH}.rpm
CALICO_LIBNET_RPM_FILE=${STAGE_DIR}/RPMS/x86_64/${CALICO_LIBNET_RPM}

CALICO_CNI_VER=`cat ${SPEC_DIR}/calico-cni/calico-cni.spec | grep Version | cut -d: -f2 | tr -d ' '`
CALICO_CNI_VER_REL=${CALICO_CNI_VER}-`cat ${SPEC_DIR}/calico-cni/calico-cni.spec | grep Release | cut -d: -f2 | tr -d ' ' | cut -d% -f1`
CALICO_CNI_RPM=calico-cni-${CALICO_CNI_VER_REL}${DIST_TAG}.${ARCH}.rpm
CALICO_CNI_RPM_FILE=${STAGE_DIR}/RPMS/x86_64/${CALICO_CNI_RPM}

K8S_CNI_VER=`cat ${SPEC_DIR}/cni/cni.spec | grep ^Version | cut -d: -f2 | tr -d ' '`
K8S_CNI_VER_REL=${K8S_CNI_VER}-`cat ${SPEC_DIR}/cni/cni.spec | grep Release | cut -d: -f2 | tr -d ' ' | cut -d% -f1`
K8S_CNI_RPM=cni-${K8S_CNI_VER_REL}${DIST_TAG}.${ARCH}.rpm
K8S_CNI_RPM_FILE=${STAGE_DIR}/RPMS/x86_64/${K8S_CNI_RPM}

CALICO_K8S_POLICY_VER=`cat ${SPEC_DIR}/calico-k8s-policy/calico-k8s-policy.spec | grep Version | cut -d: -f2 | tr -d ' '`
CALICO_K8S_POLICY_VER_REL=${CALICO_K8S_POLICY_VER}-`cat ${SPEC_DIR}/calico-k8s-policy/calico-k8s-policy.spec | grep Release | cut -d: -f2 | tr -d ' ' | cut -d% -f1`
CALICO_K8S_POLICY_RPM=calico-k8s-policy-${CALICO_K8S_POLICY_VER_REL}${DIST_TAG}.${ARCH}.rpm
CALICO_K8S_POLICY_RPM_FILE=${STAGE_DIR}/RPMS/x86_64/${CALICO_K8S_POLICY_RPM}

if [ ! -f ${CALICO_RPM_FILE} ]
then
    echo "Calico RPM ${CALICO_RPM_FILE} not found. Exiting.."
    exit 1
fi

if [ ! -f ${CALICO_BGP_RPM_FILE} ]
then
    echo "Calico BGP RPM ${CALICO_BGP_RPM_FILE} not found. Exiting.."
    exit 1
fi

if [ ! -f ${GO_BGP_RPM_FILE} ]
then
    echo "GoBGP RPM ${GO_BGP_RPM_FILE} not found. Exiting.."
    exit 1
fi

if [ ! -f ${CALICO_BIRD_RPM_FILE} ]
then
    echo "Calico BIRD RPM ${CALICO_BIRD_RPM_FILE} not found. Exiting.."
    exit 1
fi

if [ ! -f ${CALICO_CONFD_RPM_FILE} ]
then
    echo "Calico confd RPM ${CALICO_CONFD_RPM_FILE} not found. Exiting.."
    exit 1
fi

if [ ! -f ${CALICO_FELIX_RPM_FILE} ]
then
    echo "Calico felix RPM ${CALICO_FELIX_RPM_FILE} not found. Exiting.."
    exit 1
fi

if [ ! -f ${CALICO_LIBNET_RPM_FILE} ]
then
    echo "Calico libnetwork RPM ${CALICO_LIBNET_RPM_FILE} not found. Exiting.."
    exit 1
fi

if [ ! -f ${CALICO_CNI_RPM_FILE} ]
then
    echo "Calico CNI RPM ${CALICO_CNI_RPM_FILE} not found. Exiting.."
    exit 1
fi

if [ ! -f ${K8S_CNI_RPM_FILE} ]
then
    echo "K8S CNI RPM ${K8S_CNI_RPM_FILE} not found. Exiting.."
    exit 1
fi

if [ ! -f ${CALICO_K8S_POLICY_RPM_FILE} ]
then
    echo "Calico k8s policy RPM ${CALICO_K8S_POLICY_RPM_FILE} not found. Exiting.."
    exit 1
fi

CALICO_NODE_IMG_NAME=vmware/photon-${DIST_VER}-calico-node:v${CALICO_VER}
CALICO_CNI_IMG_NAME=vmware/photon-${DIST_VER}-calico-cni:v${CALICO_CNI_VER}
CALICO_K8S_POLICY_IMG_NAME=vmware/photon-${DIST_VER}-calico-kube-policy-controller:v${CALICO_K8S_POLICY_VER}
CALICO_NODE_TAR=calico-node-v${CALICO_VER_REL}.tar
CALICO_CNI_TAR=calico-cni-v${CALICO_CNI_VER_REL}.tar
CALICO_K8S_POLICY_TAR=calico-k8s-policy-v${CALICO_K8S_POLICY_VER_REL}.tar

NODE_IMG_ID=`docker images -q ${CALICO_NODE_IMG_NAME} 2> /dev/null`
if [[ ! -z "${NODE_IMG_ID}" ]]; then
    echo "Removing image ${CALICO_NODE_IMG_NAME}"
    docker rmi -f ${CALICO_NODE_IMG_NAME}
fi

CNI_IMG_ID=`docker images -q ${CALICO_CNI_IMG_NAME} 2> /dev/null`
if [[ ! -z "${CNI_IMG_ID}" ]]; then
    echo "Removing image ${CALICO_CNI_IMG_NAME}"
    docker rmi -f ${CALICO_CNI_IMG_NAME}
fi

mkdir -p tmp/calico
cp ${CALICO_RPM_FILE} tmp/calico/
cp ${CALICO_BGP_RPM_FILE} tmp/calico/
cp ${GO_BGP_RPM_FILE} tmp/calico/
cp ${CALICO_BIRD_RPM_FILE} tmp/calico/
cp ${CALICO_CONFD_RPM_FILE} tmp/calico/
cp ${CALICO_FELIX_RPM_FILE} tmp/calico/
cp ${CALICO_LIBNET_RPM_FILE} tmp/calico/
cp ${CALICO_CNI_RPM_FILE} tmp/calico/
cp ${K8S_CNI_RPM_FILE} tmp/calico/
cp ${CALICO_K8S_POLICY_RPM_FILE} tmp/calico/
pushd ./tmp/calico
rpm2cpio ${CALICO_RPM} | cpio -vid
rpm2cpio ${CALICO_BGP_RPM} | cpio -vid
rpm2cpio ${GO_BGP_RPM} | cpio -vid
rpm2cpio ${CALICO_BIRD_RPM} | cpio -vid
rpm2cpio ${CALICO_CONFD_RPM} | cpio -vid
rpm2cpio ${CALICO_FELIX_RPM} | cpio -vid
rpm2cpio ${CALICO_LIBNET_RPM} | cpio -vid
rpm2cpio ${CALICO_CNI_RPM} | cpio -vid
rpm2cpio ${K8S_CNI_RPM} | cpio -vid
rpm2cpio ${CALICO_K8S_POLICY_RPM} | cpio -vid
popd

setup_repo

docker build --rm -t ${CALICO_NODE_IMG_NAME} -f Dockerfile.calico-node .
docker save -o ${CALICO_NODE_TAR} ${CALICO_NODE_IMG_NAME}
gzip ${CALICO_NODE_TAR}
mv -f ${CALICO_NODE_TAR}.gz ${STAGE_DIR}/docker_images/

docker build --rm -t ${CALICO_CNI_IMG_NAME} -f Dockerfile.calico-cni .
docker save -o ${CALICO_CNI_TAR} ${CALICO_CNI_IMG_NAME}
gzip ${CALICO_CNI_TAR}
mv -f ${CALICO_CNI_TAR}.gz ${STAGE_DIR}/docker_images/

docker build --rm -t ${CALICO_K8S_POLICY_IMG_NAME} -f Dockerfile.calico-k8s-policy .
docker save -o ${CALICO_K8S_POLICY_TAR} ${CALICO_K8S_POLICY_IMG_NAME}
gzip ${CALICO_K8S_POLICY_TAR}
mv -f ${CALICO_K8S_POLICY_TAR}.gz ${STAGE_DIR}/docker_images/

rm -rf ./tmp
