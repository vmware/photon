#!/bin/bash

set -x

if [ "$#" -lt 0 ]; then
  echo "Script to create new Photon OSTree repo inside a docker container."
  echo "Usage: $0"
  exit 1
fi

PROGRAM=$0
SRCROOT=$1
PH_DOCKER_IMG=$2

cat > ${SRCROOT}/support/image-builder/ostree-tools/mk-ostree-server.sh << EOF
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

chmod +x ${SRCROOT}/support/image-builder/ostree-tools/mk-ostree-server.sh

rm -rf ${SRCROOT}/stage/ostree-repo
mkdir -p ${SRCROOT}/stage/ostree-repo

sudo docker run --privileged -v ${SRCROOT}:/photon -v ${SRCROOT}/stage/RPMS:/RPMS \
  -v ${SRCROOT}/stage/ostree-repo:/srv/rpm-ostree \
  -w="/photon/support/image-builder/ostree-tools/" \
  ${PH_DOCKER_IMG} ./mk-ostree-server.sh /

REPODIR=${SRCROOT}/stage/ostree-repo/repo
if [ -d "$REPODIR" ]; then
  tar -zcf ${SRCROOT}/stage/ostree-repo.tar.gz -C ${REPODIR} .
fi

sudo rm -rf ${SRCROOT}/support/image-builder/ostree-tools/mk-ostree-server.sh \
             ${SRCROOT}/stage/ostree-repo
