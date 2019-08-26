#!/bin/bash

set -x

if [ "$#" -lt 0 ]; then
	echo "Script to create new Photon OSTree repo inside a docker container."
	echo "Usage: $0 "
	exit -1
fi

PROGRAM=$0
SRCROOT=$1

cat > ${SRCROOT}/support/image-builder/ostree-tools/mk-ostree-server.sh << EOF
#!/bin/bash

ROOT=$1

mkdir -p ${ROOT}/srv/rpm-ostree
ostree --repo=${ROOT}/srv/rpm-ostree/repo init --mode=archive-z2
rpm-ostree compose tree --repo=${ROOT}/srv/rpm-ostree/repo photon-base.json
EOF

chmod +x ${SRCROOT}/support/image-builder/ostree-tools/mk-ostree-server.sh

cp ${SRCROOT}/support/image-builder/ostree-tools/photon-ostree.repo ${SRCROOT}/support/image-builder/ostree-tools/photon-ostree.repo.bak
echo "baseurl=file:///RPMS" >> ${SRCROOT}/support/image-builder/ostree-tools/photon-ostree.repo

rm -rf stage/ostree-repo
mkdir -p stage/ostree-repo

sudo docker run -it --privileged -v ${SRCROOT}:/photon -v $(pwd)/stage/RPMS:/RPMS -v $(pwd)/stage/ostree-repo:/srv/rpm-ostree -w="/photon/support/image-builder/ostree-tools/" ankitaj/photon-build:rpm-ostree-3.0 ./mk-ostree-server.sh /

(cd stage/ostree-repo/repo/; tar -zcf ../../ostree-repo.tar.gz .; )

# Restore file
mv -f ${SRCROOT}/support/image-builder/ostree-tools/photon-ostree.repo.bak ${SRCROOT}/support/image-builder/ostree-tools/photon-ostree.repo
sudo rm ${SRCROOT}/support/image-builder/ostree-tools/mk-ostree-server.sh
sudo rm -rf ${SRCROOT}/stage/ostree-repo
