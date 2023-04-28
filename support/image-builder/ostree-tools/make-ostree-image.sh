#!/bin/bash

set -x

if [ "$#" -lt 0 ]; then
	echo "Script to create new Photon OSTree repo inside a docker container."
	echo "Usage: $0"
	exit 1
fi

SRCROOT="$1"
STAGE_DIR="$2"
PH_VERSION="$3"
PHOTON_DOCKER_IMAGE="$4"
ARCHITECTURE="$(uname -m)"
SCRIPT_PATH="$(dirname "$(realpath ${BASH_SOURCE[0]})")"

cat > ${SCRIPT_PATH}/photon-base.json << EOF
{
    "comment": "Photon Minimal OSTree",

    "osname": "photon",

    "releasever": "${PH_VERSION}",

    "ref": "photon/${PH_VERSION}/${ARCHITECTURE}/minimal",

    "automatic_version_prefix": "${PH_VERSION}_minimal",

    "repos": ["photon-ostree"],

    "selinux": false,

    "initramfs-args": ["--no-hostonly"],

    "bootstrap_packages": ["filesystem"],

    "documentation": false,

    "tmp-is-dir": true,

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

cat > ${SCRIPT_PATH}/mk-ostree-server.sh << EOF
#!/bin/bash

ROOT=$1

cat > photon-ostree.repo << EOT
[photon-ostree]
name=VMware Photon OSTree Linux ${PH_VERSION}($ARCHITECTURE)
gpgkey=file:///etc/pki/rpm-gpg/VMWARE-RPM-GPG-KEY file:///etc/pki/rpm-gpg/VMWARE-RPM-GPG-KEY-4096
gpgcheck=0
enabled=1
skip_if_unavailable=True
baseurl=file:///RPMS
EOT

cp photon-ostree.repo /etc/yum.repos.d

if ! tdnf install -y rpm ostree rpm-ostree --disablerepo=* --enablerepo=photon-ostree; then
  echo "ERROR: failed to install packages while preparing ostree server" 1>&2
  exit 1
fi

mkdir -p ${ROOT}/srv/rpm-ostree
if ! ostree --repo=${ROOT}/srv/rpm-ostree/repo init --mode=archive-z2; then
  echo "ERROR: ostree init failed" 1>&2
  exit 1
fi

if ! rpm-ostree compose tree --repo=${ROOT}/srv/rpm-ostree/repo photon-base.json; then
  echo "ERROR: rpm-ostree compose failed" 1>&2
  exit 1
fi
ostree summary --repo=${ROOT}/srv/rpm-ostree/repo --update
ostree summary -v --repo=${ROOT}/srv/rpm-ostree/repo

rm -f photon-ostree.repo
EOF

chmod +x ${SCRIPT_PATH}/mk-ostree-server.sh

rm -rf ${STAGE_DIR}/ostree-repo
mkdir -p ${STAGE_DIR}/ostree-repo

sudo docker run --ulimit nofile=1024:1024 --rm --privileged -v ${SRCROOT}:/photon \
      -v ${STAGE_DIR}/RPMS:/RPMS \
      -v ${STAGE_DIR}/ostree-repo:/srv/rpm-ostree \
      -w="/photon/support/image-builder/ostree-tools/" \
      ${PHOTON_DOCKER_IMAGE} ./mk-ostree-server.sh /

if [ $? -ne 0 ]; then
  echo "ERROR: mk-ostree-server.sh failed" 1>&2
  exit 1
fi

REPODIR=${STAGE_DIR}/ostree-repo/repo
if [ -d "$REPODIR" ]; then
  if ! tar -zcf ${STAGE_DIR}/ostree-repo.tar.gz -C ${REPODIR} .; then
    echo "ERROR: tar ostree-repo.tar.gz failed" 1>&2
    exit 1
  fi
fi

sudo rm -rf ${SCRIPT_PATH}/mk-ostree-server.sh \
            ${STAGE_DIR}/ostree-repo \
            ${SCRIPT_PATH}/photon-base.json
