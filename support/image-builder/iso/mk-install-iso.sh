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

set -o errexit        # exit if error...insurance ;)
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

rpm --root $INITRD --initdb

PACKAGES="filesystem glibc zlib file gmp libgcc libstdc++ bash sed haveged ncurses-terminfo \
    bzip2 pkg-config python3-curses ncurses cracklib cracklib-dicts python3-cracklib \
    shadow coreutils grep readline findutils xz util-linux e2fsprogs \
    libffi expat linux cpio Linux-PAM attr libcap systemd dbus \
    gzip sqlite nspr nss popt lua rpm gptfdisk tar \
    hawkey python3 python3-libs pcre glib tdnf python3-requests grub2 \
    grub2-pc grub2-efi efivar efibootmgr dracut curl dosfstools ostree ostree-grub2 ostree-libs"

TDNF_CMD="tdnf install -y --installroot $INITRD --rpmverbosity 10 -c ${WORKINGDIR}/tdnf.conf -q $PACKAGES"

# run host's tdnf, if fails - try one from photon:3.0 docker image
$TDNF_CMD || docker run -v $RPMS_PATH:$RPMS_PATH -v $WORKINGDIR:$WORKINGDIR photon:3.0 $TDNF_CMD

rm ${WORKINGDIR}/photon-local.repo
rm ${WORKINGDIR}/tdnf.conf

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

cp -r $SCRIPT_PATH/BUILD_DVD/isolinux ${WORKINGDIR}/
cp -r $SCRIPT_PATH/BUILD_DVD/boot ${WORKINGDIR}/
mkdir ${WORKINGDIR}/boot/grub2/fonts/
cp $INSTALLER_PATH/boot/ascii.pf2 ${WORKINGDIR}/boot/grub2/fonts/
mkdir -p ${WORKINGDIR}/boot/grub2/themes/photon/
cp $INSTALLER_PATH/boot/splash.png ${WORKINGDIR}/boot/grub2/themes/photon/photon.png
cp $INSTALLER_PATH/boot/terminal_*.tga ${WORKINGDIR}/boot/grub2/themes/photon/
cp $INSTALLER_PATH/boot/theme.txt ${WORKINGDIR}/boot/grub2/themes/photon/
echo ${WORKINGDIR}
cp $SCRIPT_PATH/BUILD_DVD/isolinux/splash.png ${INITRD}/installer/boot/.
mkdir -p ${INITRD}/installer/EFI/BOOT
cp $INSTALLER_PATH/EFI_$(uname -m)/BOOT/* ${INITRD}/installer/EFI/BOOT/

#Generate efiboot image
# efiboot is a fat16 image that has at least EFI/BOOT/bootx64.efi

EFI_IMAGE=boot/grub2/efiboot.img
EFI_FOLDER=`readlink -f ${STAGE_PATH}/efiboot`
dd if=/dev/zero of=${WORKINGDIR}/${EFI_IMAGE} bs=3K count=1024
mkdosfs ${WORKINGDIR}/${EFI_IMAGE}
mkdir $EFI_FOLDER
mount -o loop ${WORKINGDIR}/${EFI_IMAGE} $EFI_FOLDER
mkdir $EFI_FOLDER/EFI
mkdir ${WORKINGDIR}/EFI
cp -r $INSTALLER_PATH/EFI_$(uname -m)/BOOT $EFI_FOLDER/EFI/
cp -r $INSTALLER_PATH/EFI_$(uname -m)/BOOT ${WORKINGDIR}/EFI/
ls -lR $EFI_FOLDER
umount $EFI_FOLDER
rm -rf $EFI_FOLDER
#mcopy -s -i ${WORKINGDIR}/${EFI_IMAGE} ./EFI '::/'

cp $INSTALLER_PATH/sample_ks.cfg ${WORKINGDIR}/isolinux/

mv ${INITRD}/boot/vmlinuz* ${WORKINGDIR}/isolinux/vmlinuz

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
baseurl=file:///mnt/cdrom/RPMS
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
  LANG=en_US.UTF-8 ./isoInstaller.py --json-file=$PACKAGE_LIST_FILE_BASE_NAME -r /mnt/cdrom/RPMS 2>/var/log/installer && shutdown -r now
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
    if [ -f "$rpm_name" ]; then
        cp --parent $rpm_name ${WORKINGDIR}/RPMS/;
    fi
done
)

# Work in sub-shell using ( ... ) to come back to original folder.
(
cd $STAGE_PATH
for file_name in $ADDITIONAL_FILES_TO_COPY_FROM_STAGE; do
    if [ -n "$file_name" ]; then
        cp $file_name ${WORKINGDIR}/;
    fi
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
for filename in ${INITRD}/usr/lib/*; do
    if [[ -f ${filename} ]]; then
        file ${filename} | grep ELF >/dev/null 2>&1 && strip $filename ||:
    fi;
done

rm -rf ${INITRD}/home/*
rm -rf ${INITRD}/var/lib/rpm
rm -rf ${INITRD}/cache


# Remove the boot directory
rm -rf ${INITRD}/boot

#Remove the include files.
rm -rf ${INITRD}/usr/include

rm -f ${INITRD}/lib64/libmvec*
rm -f ${INITRD}/usr/sbin/sln
rm -f ${INITRD}/usr/bin/oldfind

rm -f ${INITRD}/usr/bin/localedef
rm -f ${INITRD}/usr/bin/systemd-nspawn
rm -f ${INITRD}/usr/bin/systemd-analyze
rm -rf ${INITRD}/usr/lib64/gconv
rm -f ${INITRD}/usr/bin/sqlite3

rm -f ${INITRD}/usr/bin/bsdcpio
rm -f ${INITRD}/usr/bin/bsdtar
rm -f ${INITRD}/usr/bin/networkctl
rm -f ${INITRD}/usr/bin/machinectl
rm -f ${INITRD}/usr/bin/pkg-config
rm -f ${INITRD}/usr/bin/openssl
rm -f ${INITRD}/usr/bin/timedatectl
rm -f ${INITRD}/usr/bin/localectl
rm -f ${INITRD}/usr/bin/systemd-cgls
rm -f ${INITRD}/usr/bin/systemd-inhibit
rm -f ${INITRD}/usr/bin/systemd-studio-bridge
rm -f ${INITRD}/usr/bin/iconv

rm -rf ${INITRD}/usr/lib/python2.7/lib2to3
rm -rf ${INITRD}/usr/lib/python2.7/lib-tk
rm -rf ${INITRD}/usr/lib/python2.7/ensurepip
rm -rf ${INITRD}/usr/lib/python2.7/distutils
rm -rf ${INITRD}/usr/lib/python2.7/pydoc_data
rm -rf ${INITRD}/usr/lib/python2.7/idlelib
rm -rf ${INITRD}/usr/lib/python2.7/unittest

rm -f ${INITRD}/usr/lib/librpmbuild.so*
rm -f ${INITRD}/usr/lib/libdb_cxx*
rm -f ${INITRD}/usr/lib/libnss_compat*

rm -f ${INITRD}/usr/bin/grub2-*
rm -f ${INITRD}/usr/lib/grub/i386-pc/*.module
rm -f ${INITRD}/usr/lib/grub/x86_64-efi/*.module

for j in `ls ${INITRD}/usr/sbin/grub2*`; do
    bsname=$(basename "$j")
    if [ $bsname != 'grub2-install' ]; then
        rm -f $j
    fi
done

# remove unused /usr/share
for i in `ls ${INITRD}/usr/share/`; do
    if [ $i != 'terminfo' -a $i != 'cracklib' -a $i != 'grub' -a $i != 'factory' -a $i != 'dbus-1' ]; then
        rm -rf ${INITRD}/usr/share/$i
    fi
done

# Set password max days to 99999 (disable aging)
chroot ${INITRD} /bin/bash -c "chage -M 99999 root"

# Generate the initrd
pushd $INITRD
(find . | cpio -o -H newc --quiet | gzip -9 ) > ${WORKINGDIR}/isolinux/initrd.img
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
