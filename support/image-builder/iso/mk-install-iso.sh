#!/bin/bash

set -ex

SCRIPT_PATH=$(dirname $(realpath -s $0))
PRGNAME=${0##*/}    # script name minus the path

# Should be changed when there is a python version change
PY_VER="3.11"

WORKINGDIR=$1
shift 1
ISO_OUTPUT_NAME=$1
RPMS_PATH=$2
PACKAGE_LIST_FILE=$3
RPM_LIST=$4
STAGE_PATH=$5
ADDITIONAL_FILES_TO_COPY_FROM_STAGE=$6
OUTPUT_DATA_PATH=$7
PHOTON_COMMON_DIR=$(dirname "${PACKAGE_LIST_FILE}")
PACKAGE_LIST_FILE_BASE_NAME=$(basename "${PACKAGE_LIST_FILE}")
INITRD=${WORKINGDIR}/photon-chroot
PACKAGES=$8
PHOTON_DOCKER_IMAGE=$9
PH_BUILDER_TAG=${10}
PH_VERSION=${11}
ARCH="$(uname -m)"
LICENSE_TEXT="VMWARE $PH_VERSION"

if ! eval "$(grep -m 1 -w 'BETA LICENSE AGREEMENT' $STAGE_PATH/EULA.txt)"; then
  LICENSE_TEXT+=" BETA"
fi

LICENSE_TEXT+=" LICENSE AGREEMENT"

rm -rf $WORKINGDIR/*
mkdir -m 755 -p $INITRD

tar -xf $SCRIPT_PATH/open_source_license.tar.gz -C $WORKINGDIR/

cp $STAGE_PATH/NOTICE-Apachev2 \
   $STAGE_PATH/NOTICE-GPL2.0 \
   $WORKINGDIR/

# 1. install rpms into initrd path
cat > ${WORKINGDIR}/photon-local.repo <<EOF
[photon-local]
name=VMware Photon Linux
baseurl=file://${RPMS_PATH}
gpgcheck=0
enabled=1
skip_if_unavailable=True
EOF

# we need to remove repodir & use --setopt=reposdir option once we use
# tdnf-3.2.x in Photon-3.0 docker images
cat > ${WORKINGDIR}/tdnf.conf <<EOF
[main]
gpgcheck=0
installonly_limit=3
clean_requirements_on_remove=true
repodir=${WORKINGDIR}
EOF

TDNF_CMD="tdnf install -qy \
          --releasever $PHOTON_RELEASE_VER \
          --installroot $INITRD \
          --rpmverbosity 10 \
          -c ${WORKINGDIR}/tdnf.conf \
          ${PACKAGES}"

# Run host's tdnf, if fails - try one from photon:latest docker image
$TDNF_CMD || docker run --ulimit nofile=1024:1024 --rm -v $RPMS_PATH:$RPMS_PATH -v $WORKINGDIR:$WORKINGDIR $PHOTON_DOCKER_IMAGE /bin/bash -c "$TDNF_CMD"

rm -f ${WORKINGDIR}/photon-local.repo ${WORKINGDIR}/tdnf.conf

# 3. finalize initrd system (mk-finalize-system.sh)
chroot ${INITRD} /usr/sbin/pwconv
chroot ${INITRD} /usr/sbin/grpconv

# Workaround Failed to generate randomized machine ID: Function not implemented
chroot ${INITRD} /bin/systemd-machine-id-setup || chroot ${INITRD} date -Ins | md5sum | cut -f1 -d' ' > /etc/machine-id

echo "LANG=en_US.UTF-8" > $INITRD/etc/locale.conf
echo "photon-installer" > $INITRD/etc/hostname
# locales/en_GB should be moved to glibc main package to make it working
#chroot ${INITRD} /usr/bin/localedef -c -i en_US -f UTF-8 en_US.UTF-8
# Importing the pubkey (photon-repos required)
#chroot ${INITRD} rpm --import /etc/pki/rpm-gpg/*

rm -rf ${INITRD}/var/cache/tdnf

# Move entire /boot from initrd to ISO
mv ${INITRD}/boot ${WORKINGDIR}/

cp -pr $SCRIPT_PATH/BUILD_DVD/isolinux \
       $SCRIPT_PATH/BUILD_DVD/boot \
       ${WORKINGDIR}/

#Generate efiboot image
# efiboot is a fat16 image that has at least EFI/BOOT/bootx64.efi

EFI_IMAGE=boot/grub2/efiboot.img
EFI_FOLDER=$(readlink -f ${STAGE_PATH}/efiboot)
dd if=/dev/zero of=${WORKINGDIR}/${EFI_IMAGE} bs=3K count=1024
mkdosfs ${WORKINGDIR}/${EFI_IMAGE}
mkdir -p $EFI_FOLDER
mount -o loop ${WORKINGDIR}/${EFI_IMAGE} $EFI_FOLDER
mv ${WORKINGDIR}/boot/efi/EFI $EFI_FOLDER/
ls -lR $EFI_FOLDER
umount $EFI_FOLDER
rm -rf $EFI_FOLDER
#mcopy -s -i ${WORKINGDIR}/${EFI_IMAGE} ./EFI '::/'

mkdir -p $INITRD/installer
cp $SCRIPT_PATH/sample_ks.cfg ${WORKINGDIR}/isolinux
cp $SCRIPT_PATH/sample_ui.cfg ${INITRD}/installer
cp $STAGE_PATH/EULA.txt ${INITRD}/installer

mv ${WORKINGDIR}/boot/vmlinuz* ${WORKINGDIR}/isolinux/vmlinuz

# Copy package list json files, dereference symlinks
cp -rf -L $OUTPUT_DATA_PATH/*.json ${INITRD}/installer/
#ID in the initrd.gz now is PHOTON_VMWARE_CD . This is how we recognize that the cd is actually ours. touch this file there.
touch ${WORKINGDIR}/PHOTON_VMWARE_CD

# Step 4.5 Create necessary devices
mkfifo ${INITRD}/dev/initctl
mknod ${INITRD}/dev/ram0 b 1 0
mknod ${INITRD}/dev/ram1 b 1 1
mknod ${INITRD}/dev/ram2 b 1 2
mknod ${INITRD}/dev/ram3 b 1 3
mknod ${INITRD}/dev/sda b 8 0

#- Step 5 - Creating the boot script
mkdir -p ${INITRD}/etc/systemd/scripts

# Step 6 create fstab
cp $SCRIPT_PATH/BUILD_DVD/fstab ${INITRD}/etc/fstab

mkdir -p ${INITRD}/etc/yum.repos.d
cat > ${INITRD}/etc/yum.repos.d/photon-iso.repo << EOF
[photon-iso]
name=VMWare Photon Linux ${PH_VERSION}(${ARCH})
baseurl=file:///mnt/media/RPMS
gpgkey=file:///etc/pki/rpm-gpg/VMWARE-RPM-GPG-KEY
gpgcheck=1
enabled=1
skip_if_unavailable=True
EOF

#- Step 7 - Create installer script
cat >> ${INITRD}/bin/bootphotoninstaller << EOF
#!/bin/bash
cd /installer

ACTIVE_CONSOLE="\$(< /sys/devices/virtual/tty/console/active)"

install() {
  LANG=en_US.UTF-8 photon-installer -i iso -o $PACKAGE_LIST_FILE_BASE_NAME -e EULA.txt -t "$LICENSE_TEXT" -v $PHOTON_RELEASE_VER && shutdown -r now
}

try_run_installer() {
  if [ "\$ACTIVE_CONSOLE" == "tty0" ]; then
    [ "\$(tty)" == '/dev/tty1' ] && install
  else
    [ "\$(tty)" == "/dev/\$ACTIVE_CONSOLE" ] && install
  fi
}

try_run_installer || exec /bin/bash
EOF

chmod 755 ${INITRD}/bin/bootphotoninstaller

cat >> ${INITRD}/init << EOF
mount -t proc proc /proc
/lib/systemd/systemd
EOF
chmod 755 ${INITRD}/init

# Adding autologin to the root user and set TERM=linux for installer
sed -i "s/ExecStart.*/ExecStart=-\/sbin\/agetty --autologin root --noclear %I linux/g" ${INITRD}/lib/systemd/system/getty@.service
sed -i "s/ExecStart.*/ExecStart=-\/sbin\/agetty --autologin root --keep-baud 115200,38400,9600 %I screen/g" ${INITRD}/lib/systemd/system/serial-getty@.service
rm -rf ${INITRD}/etc/systemd/system/getty.target.wants/console-getty.service

# Step 7 - Create installer script
sed -i "s/root:.*/root:x:0:0:root:\/root:\/bin\/bootphotoninstaller/g" ${INITRD}/etc/passwd

mkdir -p ${INITRD}/mnt/photon-root/photon-chroot
rm -rf ${INITRD}/RPMS

echo ${RPMS_PATH}
#cp -r ${RPMS_PATH} ${WORKINGDIR}/
(
cd ${RPMS_PATH}
mkdir -p ${WORKINGDIR}/RPMS
cp --verbose --parents ${RPM_LIST} ${WORKINGDIR}/RPMS/
chmod 644 ${WORKINGDIR}/RPMS/${ARCH}/*.rpm ${WORKINGDIR}/RPMS/noarch/*.rpm
)

# Work in sub-shell using ( ... ) to come back to original folder.
(
file_list=""
cd $STAGE_PATH
for file_name in $ADDITIONAL_FILES_TO_COPY_FROM_STAGE; do
  [ -n "$file_name" ] && file_list+="${file_name} "
done
if [ -n "${file_list}" ]; then
  cp ${file_list} ${WORKINGDIR}
fi
)

# Creating rpm repo in cd..
createrepo --update --database ${WORKINGDIR}/RPMS

repodatadir=${WORKINGDIR}/RPMS/repodata
if [ -d $repodatadir ]; then
  pushd $repodatadir
  metaDataFile=$(find -type f -name "*primary.xml.gz")
  ln -sfv $metaDataFile primary.xml.gz
  popd
fi

rm -rf ${INITRD}/LOGS

# Cleaning up
find ${INITRD}/usr/lib/ -maxdepth 1 -mindepth 1 -type f -print0 | \
  xargs -0 -r -P$(nproc) -n32 sh -c "file \"\$@\" | \
  sed -n -e 's/^\(.*\):[ 	]*ELF.*, not stripped.*/\1/p' | \
  xargs -I\{\} strip \{\}" ARG0

rm -rf ${INITRD}/home/* \
        ${INITRD}/var/lib/rpm* \
        ${INITRD}/var/lib/.rpm* \
        ${INITRD}/usr/lib/sysimage/rpm* \
        ${INITRD}/usr/lib/sysimage/.rpm* \
        ${INITRD}/cache \
        ${INITRD}/boot \
        ${INITRD}/usr/include \
        ${INITRD}/usr/sbin/sln \
        ${INITRD}/usr/bin/iconv \
        ${INITRD}/usr/bin/oldfind \
        ${INITRD}/usr/bin/localedef \
        ${INITRD}/usr/bin/sqlite3 \
        ${INITRD}/usr/bin/grub2-* \
        ${INITRD}/usr/bin/bsdcpio \
        ${INITRD}/usr/bin/bsdtar \
        ${INITRD}/usr/bin/networkctl \
        ${INITRD}/usr/bin/machinectl \
        ${INITRD}/usr/bin/pkg-config \
        ${INITRD}/usr/bin/openssl \
        ${INITRD}/usr/bin/timedatectl \
        ${INITRD}/usr/bin/localectl \
        ${INITRD}/usr/bin/systemd-cgls \
        ${INITRD}/usr/bin/systemd-analyze \
        ${INITRD}/usr/bin/systemd-nspawn \
        ${INITRD}/usr/bin/systemd-inhibit \
        ${INITRD}/usr/bin/systemd-studio-bridge \
        ${INITRD}/usr/lib/python${PY_VER}/lib2to3 \
        ${INITRD}/usr/lib/python${PY_VER}/lib-tk \
        ${INITRD}/usr/lib/python${PY_VER}/ensurepip \
        ${INITRD}/usr/lib/python${PY_VER}/distutils \
        ${INITRD}/usr/lib/python${PY_VER}/pydoc_data \
        ${INITRD}/usr/lib/python${PY_VER}/idlelib \
        ${INITRD}/usr/lib/python${PY_VER}/unittest \
        ${INITRD}/usr/lib/librpmbuild.so* \
        ${INITRD}/usr/lib/libdb_cxx* \
        ${INITRD}/usr/lib/libnss_compat* \
        ${INITRD}/usr/lib/grub/i386-pc/*.module \
        ${INITRD}/usr/lib/grub/x86_64-efi/*.module \
        ${INITRD}/usr/lib/grub/arm64-efi/*.module \
        ${INITRD}/lib/libmvec* \
        ${INITRD}/usr/lib/gconv

find "${INITRD}/usr/sbin" -mindepth 1 -maxdepth 1 -name "grub2*" \
                        ! -name grub2-install -print0 | \
                        xargs -0 -r -P$(nproc) -n32 rm -rvf

find "${INITRD}/usr/share" -mindepth 1 -maxdepth 1 \
                        ! -name terminfo \
                        ! -name cracklib \
                        ! -name grub \
                        ! -name factory \
                        ! -name dbus-1 -print0 |
                        xargs -0 -r -P$(nproc) -n32 rm -rvf

# Set password max days to 99999 (disable aging)
chroot ${INITRD} /bin/bash -c "chage -M 99999 root"

# Generate the initrd
pushd $INITRD
(find . | cpio -o -H newc --quiet | gzip -9) > ${WORKINGDIR}/isolinux/initrd.img
popd
rm -rf $INITRD

# Step 9 Generate the ISO!!!!
pushd $WORKINGDIR
mkisofs -R -l -L -D -b isolinux/isolinux.bin \
        -c isolinux/boot.cat \
        -no-emul-boot \
        -boot-load-size 4 \
        -boot-info-table \
        -eltorito-alt-boot -e ${EFI_IMAGE} \
        -no-emul-boot \
        -V "PHOTON_$(date +%Y%m%d)" \
        $WORKINGDIR > $ISO_OUTPUT_NAME
popd
