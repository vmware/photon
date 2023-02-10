#!/bin/bash

set -x

if [ "$#" -lt 0 ]; then
  echo "Script to create new Photon OSTree repo inside a docker container."
  echo "Usage: $0"
  exit 1
fi

SRCROOT=$1
PH_DOCKER_IMG=$2

STAGE_DIR="${SRCROOT}/stage"
SCRIPT_PATH="$(dirname "$(realpath ${BASH_SOURCE[0]})")"
REPODIR=${STAGE_DIR}/ostree-repo/repo

cat > ${SCRIPT_PATH}/mk-ostree-server.sh << EOF
#!/bin/bash

ROOT=$1

cp photon-ostree.repo /etc/yum.repos.d

if ! tdnf install -y rpm ostree rpm-ostree --disablerepo=* --enablerepo=photon-ostree; then
  echo "ERROR: failed to install packages while preparing ostree server"
  exit 1
fi

mkdir -p ${ROOT}/srv/rpm-ostree
ostree --repo=${ROOT}/srv/rpm-ostree/repo init --mode=archive-z2
rpm-ostree compose tree --repo=${ROOT}/srv/rpm-ostree/repo photon-base.json
EOF

chmod +x ${SCRIPT_PATH}/mk-ostree-server.sh

rm -rf ${STAGE_DIR}/ostree-repo
mkdir -p ${STAGE_DIR}/ostree-repo

docker run --ulimit nofile=1024:1024 --rm --privileged \
  -v ${SRCROOT}:/photon \
  -v ${STAGE_DIR}/RPMS:/RPMS \
  -v ${STAGE_DIR}/ostree-repo:/srv/rpm-ostree \
  -w="/photon/support/image-builder/ostree-tools/" \
  ${PH_DOCKER_IMG} ./mk-ostree-server.sh /

if [ -d "$REPODIR" ]; then
  tar -zcf ${STAGE_DIR}/ostree-repo.tar.gz -C ${REPODIR} .
fi

rm -rf ${SCRIPT_PATH}/mk-ostree-server.sh \
       ${STAGE_DIR}/ostree-repo
