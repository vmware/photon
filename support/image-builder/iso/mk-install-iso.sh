#! /bin/bash
#################################################
#       Title:  mk-install-iso                  #
#        Date:  2014-11-26                      #
#     Version:  1.0                             #
#      Author:  dthaluru@vmware.com             #
#     Options:                                  #
#################################################
#   Overview
#       Generates a photon iso
#   End
#

set -e
set -x

SCRIPT_PATH=$(dirname $(realpath -s $0))
PRGNAME=${0##*/}    # script name minus the path

INSTALLER_PATH=$1
WORKINGDIR=$2
shift 2
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

rm -rf $WORKINGDIR/*
mkdir -p $INITRD
chmod 755 $INITRD

cp $SCRIPT_PATH/open_source_license.txt $WORKINGDIR/
cp $STAGE_PATH/NOTICE $WORKINGDIR/

# 1. install rpms into initrd path
cat > ${WORKINGDIR}/photon-local.repo <<EOF
[photon-local]
name=VMware Photon Linux
baseurl=file://${RPMS_PATH}
gpgcheck=0
enabled=1
skip_if_unavailable=True
EOF

cat > ${WORKINGDIR}/tdnf.conf <<EOF
[main]
gpgcheck=0
installonly_limit=3
clean_requirements_on_remove=true
repodir=${WORKINGDIR}
EOF

rpm --root $INITRD --initdb --dbpath /var/lib/rpm

TDNF_CMD="tdnf install -y --installroot $INITRD --rpmverbosity 10 -c ${WORKINGDIR}/tdnf.conf -q $PACKAGES"

# run host's tdnf, if fails - try one from photon:3.0 docker image
$TDNF_CMD || docker run -v $RPMS_PATH:$RPMS_PATH -v $WORKINGDIR:$WORKINGDIR photon:3.0 $TDNF_CMD

rm -f ${WORKINGDIR}/photon-local.repo ${WORKINGDIR}/tdnf.conf

# 2. copy installer code to initrd
cp -r $INSTALLER_PATH $INITRD

# 3. finalize initrd system (mk-finalize-system.sh)
chroot ${INITRD} /usr/sbin/pwconv
chroot ${INITRD} /usr/sbin/grpconv
chroot ${INITRD} /bin/systemd-machine-id-setup
echo "LANG=en_US.UTF-8" > $INITRD/etc/locale.conf
echo "photon-installer" > $INITRD/etc/hostname
# locales/en_GB should be moved to glibc main package to make it working
#chroot ${INITRD} /usr/bin/localedef -c -i en_US -f UTF-8 en_US.UTF-8
# Importing the pubkey (photon-repos required)
#chroot ${INITRD} rpm --import /etc/pki/rpm-gpg/*

# Move entire /boot from initrd to ISO
mv ${INITRD}/boot ${WORKINGDIR}/

cp -r $SCRIPT_PATH/BUILD_DVD/isolinux $SCRIPT_PATH/BUILD_DVD/boot ${WORKINGDIR}/

#Generate efiboot image
# efiboot is a fat16 image that has at least EFI/BOOT/bootx64.efi

EFI_IMAGE=boot/grub2/efiboot.img
EFI_FOLDER=`readlink -f ${STAGE_PATH}/efiboot`
dd if=/dev/zero of=${WORKINGDIR}/${EFI_IMAGE} bs=3K count=1024
mkdosfs ${WORKINGDIR}/${EFI_IMAGE}
mkdir $EFI_FOLDER
mount -o loop ${WORKINGDIR}/${EFI_IMAGE} $EFI_FOLDER
mv ${WORKINGDIR}/boot/efi/EFI $EFI_FOLDER/
ls -lR $EFI_FOLDER
umount $EFI_FOLDER
rm -rf $EFI_FOLDER
#mcopy -s -i ${WORKINGDIR}/${EFI_IMAGE} ./EFI '::/'

cp $INSTALLER_PATH/sample_ks.cfg ${WORKINGDIR}/isolinux/

mv ${WORKINGDIR}/boot/vmlinuz* ${WORKINGDIR}/isolinux/vmlinuz

rm -f ${INITRD}/installer/*.pyc
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
name=VMWare Photon Linux 1.0(x86_64)
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
  LANG=en_US.UTF-8 ./isoInstaller.py --json-file=$PACKAGE_LIST_FILE_BASE_NAME && shutdown -r now
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

#adding autologin to the root user
# and set TERM=linux for installer
sed -i "s/ExecStart.*/ExecStart=-\/sbin\/agetty --autologin root --noclear %I linux/g" ${INITRD}/lib/systemd/system/getty@.service
sed -i "s/ExecStart.*/ExecStart=-\/sbin\/agetty --autologin root --keep-baud 115200,38400,9600 %I screen/g" ${INITRD}/lib/systemd/system/serial-getty@.service

#- Step 7 - Create installer script
sed -i "s/root:.*/root:x:0:0:root:\/root:\/bin\/bootphotoninstaller/g" ${INITRD}/etc/passwd

mkdir -p ${INITRD}/mnt/photon-root/photon-chroot
rm -rf ${INITRD}/RPMS

echo ${RPMS_PATH}
#cp -r ${RPMS_PATH} ${WORKINGDIR}/
(
cd ${RPMS_PATH}
mkdir ${WORKINGDIR}/RPMS
for rpm_name in $RPM_LIST; do
    cp --parent $rpm_name ${WORKINGDIR}/RPMS/
    chmod 644 ${WORKINGDIR}/RPMS/$rpm_name
done
)

# Work in sub-shell using ( ... ) to come back to original folder.
(
cd $STAGE_PATH
for file_name in $ADDITIONAL_FILES_TO_COPY_FROM_STAGE; do
    [ -n "$file_name" ] &&  cp $file_name ${WORKINGDIR}
done
)

#creating rpm repo in cd..
createrepo --database ${WORKINGDIR}/RPMS

repodatadir=${WORKINGDIR}/RPMS/repodata
if [ -d $repodatadir ]; then
    pushd $repodatadir
    metaDataFile=`find -type f -name "*primary.xml.gz"`
    ln -sfv $metaDataFile primary.xml.gz
    popd
fi

rm -rf ${INITRD}/LOGS

# Cleaning up
find ${INITRD}/usr/lib/ -maxdepth 1 -mindepth 1 -type f | xargs -i sh -c "grep ELF {} >/dev/null 2>&1 && strip {} || :"

rm -rf ${INITRD}/home/*         \
        ${INITRD}/var/lib/rpm   \
        ${INITRD}/cache         \
        ${INITRD}/boot          \
        ${INITRD}/usr/include   \
        ${INITRD}/usr/sbin/sln  \
        ${INITRD}/usr/bin/iconv \
        ${INITRD}/usr/bin/oldfind       \
        ${INITRD}/usr/bin/localedef     \
        ${INITRD}/usr/bin/sqlite3       \
        ${INITRD}/usr/bin/grub2-*       \
        ${INITRD}/usr/bin/bsdcpio       \
        ${INITRD}/usr/bin/bsdtar        \
        ${INITRD}/usr/bin/networkctl    \
        ${INITRD}/usr/bin/machinectl    \
        ${INITRD}/usr/bin/pkg-config    \
        ${INITRD}/usr/bin/openssl       \
        ${INITRD}/usr/bin/timedatectl   \
        ${INITRD}/usr/bin/localectl     \
        ${INITRD}/usr/bin/systemd-cgls  \
        ${INITRD}/usr/bin/systemd-analyze       \
        ${INITRD}/usr/bin/systemd-nspawn        \
        ${INITRD}/usr/bin/systemd-inhibit       \
        ${INITRD}/usr/bin/systemd-studio-bridge \
        ${INITRD}/usr/lib/python2.7/lib2to3     \
        ${INITRD}/usr/lib/python2.7/lib-tk      \
        ${INITRD}/usr/lib/python2.7/ensurepip   \
        ${INITRD}/usr/lib/python2.7/distutils   \
        ${INITRD}/usr/lib/python2.7/pydoc_data  \
        ${INITRD}/usr/lib/python2.7/idlelib     \
        ${INITRD}/usr/lib/python2.7/unittest    \
        ${INITRD}/usr/lib/librpmbuild.so*       \
        ${INITRD}/usr/lib/libdb_cxx*            \
        ${INITRD}/usr/lib/libnss_compat*        \
        ${INITRD}/usr/lib/grub/i386-pc/*.module \
        ${INITRD}/usr/lib/grub/x86_64-efi/*.module \
        ${INITRD}/lib64/libmvec*        \
        ${INITRD}/usr/lib64/gconv

find "${INITRD}/usr/sbin" -mindepth 1 -maxdepth 1 -name "grub2*" \
                        ! -name grub2-install -exec rm -rvf {} \;

find "${INITRD}/usr/share" -mindepth 1 -maxdepth 1 \
                        ! -name terminfo \
                        ! -name cracklib \
                        ! -name grub    \
                        ! -name factory \
                        ! -name dbus-1 -exec rm -rvf {} \;

# Set password max days to 99999 (disable aging)
chroot ${INITRD} /bin/bash -c "chage -M 99999 root"

# Generate the initrd
pushd $INITRD
(find . | cpio -o -H newc --quiet | gzip -9) > ${WORKINGDIR}/isolinux/initrd.img
popd
rm -rf $INITRD

#Step 9 Generate the ISO!!!!
pushd $WORKINGDIR
mkisofs -R -l -L -D -b isolinux/isolinux.bin -c isolinux/boot.cat \
        -no-emul-boot -boot-load-size 4 -boot-info-table \
        -eltorito-alt-boot -e ${EFI_IMAGE} -no-emul-boot \
        -V "PHOTON_$(date +%Y%m%d)" \
        $WORKINGDIR >$ISO_OUTPUT_NAME
popd
