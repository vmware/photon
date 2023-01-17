#!/bin/bash

set -x

if [ "$#" -lt 0 ]; then
	echo "Script to create new Photon OSTree repo inside a docker container."
	echo "Usage: $0"
	exit 1
fi

PROGRAM=$0
SRCROOT=$1
STAGE_DIR=$2
ARCHITECTURE=$3
PHOTON_DOCKER_IMAGE=$4

cat > ${SRCROOT}/support/image-builder/ostree-tools/photon-base.json<< EOF
{
    "comment": "Photon Minimal OSTree",

    "osname": "photon",

    "releasever": "5.0",

    "ref": "photon/5.0/${ARCHITECTURE}/minimal",

    "automatic_version_prefix": "5.0_minimal",

    "repos": ["photon-ostree"],

    "selinux": false,

    "initramfs-args": ["--no-hostonly"],

    "bootstrap_packages": ["filesystem"],

    "documentation": false,

    "packages": ["bash", "bc", "bridge-utils", "bzip2","ca-certificates",
                 "cloud-init", "cpio", "cracklib-dicts", "dbus", "e2fsprogs",
                 "file", "findutils", "gdbm", "grep", "gzip", "iana-etc",
                 "iptables", "iproute2", "iputils", "libtool", "linux", "motd",
                 "net-tools", "pkg-config", "photon-release", "photon-repos",
                 "procps-ng", "rpm", "sed", "sudo", "tzdata", "util-linux",
                 "vim", "which", "dracut-tools", "rpm-ostree", "nss-altfiles",
                 "openssh", "systemd", "systemd-udev", "openssl", "grub2", "grub2-efi",
                 "grub2-efi-image", "shadow", "ncurses", "grub2-theme-ostree",
                 "selinux-policy"],

    "packages-x86_64": ["grub2-pc", "open-vm-tools"],

    "units": ["sshd-keygen.service", "sshd.service"]
}
EOF

cat > ${SRCROOT}/support/image-builder/ostree-tools/mk-ostree-server.sh << EOF
#!/bin/bash

ROOT=$1

cp photon-ostree.repo /etc/yum.repos.d
if ! tdnf install -y rpm ostree rpm-ostree --disablerepo=* --enablerepo=photon-ostree; then
  echo "ERROR: failed to install packages while preparing ostree server" 1>&2
  exit 1
fi

mkdir -p ${ROOT}/srv/rpm-ostree
ostree --repo=${ROOT}/srv/rpm-ostree/repo init --mode=archive-z2
rpm-ostree compose tree --repo=${ROOT}/srv/rpm-ostree/repo photon-base.json
EOF

chmod +x ${SRCROOT}/support/image-builder/ostree-tools/mk-ostree-server.sh

rm -rf ${STAGE_DIR}/ostree-repo
mkdir -p ${STAGE_DIR}/ostree-repo

sudo docker run --privileged -v ${SRCROOT}:/photon \
      -v ${STAGE_DIR}/RPMS:/RPMS \
      -v ${STAGE_DIR}/ostree-repo:/srv/rpm-ostree \
      -w="/photon/support/image-builder/ostree-tools/" \
      ${PHOTON_DOCKER_IMAGE} ./mk-ostree-server.sh /

REPODIR=${STAGE_DIR}/ostree-repo/repo
if [ -d "$REPODIR" ]; then
  tar -zcf ${STAGE_DIR}/ostree-repo.tar.gz -C ${REPODIR} .
fi

sudo rm -rf ${SRCROOT}/support/image-builder/ostree-tools/mk-ostree-server.sh \
            ${STAGE_DIR}/ostree-repo
