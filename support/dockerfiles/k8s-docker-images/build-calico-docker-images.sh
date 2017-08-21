#!/bin/bash -e

DIST_TAG=$1
DIST_VER=$2
SPEC_DIR=$3
STAGE_DIR=$4
ARCH=x86_64
CALICO_NODE_TAR=calico-node.tar

#
# Docker images for Calico
#
CALICO_VER=`cat ${SPEC_DIR}/calico/calico.spec | grep Version | cut -d: -f2 | tr -d ' '`
CALICO_VER_REL=${CALICO_VER}-`cat ${SPEC_DIR}/calico/calico.spec | grep Release | cut -d: -f2 | tr -d ' ' | cut -d% -f1`
CALICO_RPM=calico-${CALICO_VER_REL}${DIST_TAG}.${ARCH}.rpm
CALICO_RPM_FILE=${STAGE_DIR}/RPMS/x86_64/${CALICO_RPM}

CALICO_BGP_VER=`cat ${SPEC_DIR}/calico-bgp-daemon/calico-bgp-daemon.spec | grep Version | cut -d: -f2 | tr -d ' '`
CALICO_BGP_VER_REL=${CALICO_BGP_VER}-`cat ${SPEC_DIR}/calico-bgp-daemon/calico-bgp-daemon.spec | grep Release | cut -d: -f2 | tr -d ' ' | cut -d% -f1`
CALICO_BGP_RPM=calico-bgp-daemon-${CALICO_BGP_VER_REL}${DIST_TAG}.${ARCH}.rpm
CALICO_BGP_RPM_FILE=${STAGE_DIR}/RPMS/x86_64/${CALICO_BGP_RPM}

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

IMG_NAME=vmware_photon2/calico-node:v${CALICO_VER}

IMG_ID=`docker images -q ${IMG_NAME} 2> /dev/null`
if [[ ! -z "${IMG_ID}" ]]; then
    echo "Removing image ${IMG_NAME}"
    docker rmi -f ${IMG_NAME}
fi

mkdir -p tmp/calico
cp ${CALICO_RPM_FILE} tmp/calico/
cp ${CALICO_BGP_RPM_FILE} tmp/calico/
cp ${CALICO_BIRD_RPM_FILE} tmp/calico/
cp ${CALICO_CONFD_RPM_FILE} tmp/calico/
cp ${CALICO_FELIX_RPM_FILE} tmp/calico/
cp ${CALICO_LIBNET_RPM_FILE} tmp/calico/
pushd ./tmp/calico
rpm2cpio ${CALICO_RPM} | cpio -vid
rpm2cpio ${CALICO_BGP_RPM} | cpio -vid
rpm2cpio ${CALICO_BIRD_RPM} | cpio -vid
rpm2cpio ${CALICO_CONFD_RPM} | cpio -vid
rpm2cpio ${CALICO_FELIX_RPM} | cpio -vid
rpm2cpio ${CALICO_LIBNET_RPM} | cpio -vid
popd
docker build --rm -t ${IMG_NAME} -f Dockerfile.calico-node .
docker save -o ${CALICO_NODE_TAR} ${IMG_NAME}
mv -f ${CALICO_NODE_TAR} ${STAGE_DIR}/

rm -rf ./tmp
