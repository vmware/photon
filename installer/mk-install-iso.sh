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

set +x                 # disable hashall
source config.inc       #   configuration parameters
source function.inc     #   commonn functions
PRGNAME=${0##*/}    # script name minus the path
LOGFILE=/var/log/"${PRGNAME}-${LOGFILE}"    #   set log file name


# Grab the name of the iso file 
if [ $# -lt 2 ]
then
    echo "Usage : " $0 " <output-iso-with-path>  <rpms-path> <pkg-list-path>"
    exit 1
fi
ISO_OUTPUT_NAME=$1
RPMS_PATH=$2
PACKAGE_LIST_FILE=$3
RPM_LIST=$4
STAGE_PATH=$5
ADDITIONAL_FILES_TO_COPY_FROM_STAGE=$6
LIVE_CD=$7
OUTPUT_DATA_PATH=$8
PHOTON_COMMON_DIR=$(dirname "${PACKAGE_LIST_FILE}")
PACKAGE_LIST_FILE_BASE_NAME=$(basename "${PACKAGE_LIST_FILE}")
#- Step 3 Setting up the boot loader
WORKINGDIR=${BUILDROOT}
BUILDROOT=${BUILDROOT}/photon-chroot

run_command "cp isolinux to working directory: ${WORKINGDIR}" "cp -r BUILD_DVD/isolinux ${WORKINGDIR}/" "${LOGFILE}"
run_command "cp boot/grub2 to working directory: ${WORKINGDIR}" "cp -r BUILD_DVD/boot ${WORKINGDIR}/" "${LOGFILE}"
run_command "# 1" "mkdir ${WORKINGDIR}/boot/grub2/fonts/" "${LOGFILE}"
run_command "# 2" "cp boot/ascii.pf2 ${WORKINGDIR}/boot/grub2/fonts/" "${LOGFILE}"
run_command "# 3" "mkdir -p ${WORKINGDIR}/boot/grub2/themes/photon/" "${LOGFILE}"
run_command "# 4" "cp boot/splash.png ${WORKINGDIR}/boot/grub2/themes/photon/photon.png" "${LOGFILE}"
run_command "# 5" "cp boot/terminal_*.tga ${WORKINGDIR}/boot/grub2/themes/photon/" "${LOGFILE}"
run_command "# 6" "cp boot/theme.txt ${WORKINGDIR}/boot/grub2/themes/photon/" "${LOGFILE}"
run_command "echo : ${WORKINGDIR}" "echo ${WORKINGDIR}" "${LOGFILE}"
cp BUILD_DVD/isolinux/splash.png ${BUILDROOT}/installer/boot/.
mkdir -p ${BUILDROOT}/installer/EFI/BOOT
cp EFI_$(uname -m)/BOOT/* ${BUILDROOT}/installer/EFI/BOOT/

#Generate efiboot image
# efiboot is a fat16 image that has at least EFI/BOOT/bootx64.efi

# As a bootx64.efi we use shimx64.efi from shim-12
# # make VENDOR_CERT_FILE=<VMware cert> EFI_PATH=/usr/lib 'DEFAULT_LOADER=\\\\grubx64.efi' shimx64.efi
# # mv shimx64.efi bootx64.efi

# grubx64.efi is generated on Photon OS by using grub2-efi >= 2.02-7:
# # grub2-efi-mkimage -o grubx64.efi -p /boot/grub2 -O x86_64-efi  fat iso9660 part_gpt part_msdos  normal boot linux configfile loopback chain  efifwsetup efi_gop efi_uga  ls search search_label search_fs_uuid search_fs_file  gfxterm gfxterm_background gfxterm_menu test all_video loadenv  exfat ext2 udf halt gfxmenu png tga lsefi help linuxefi probe echo

# grubaa64.efi is generated on Photon OS by using grub2-efi >= 2.02-7:
#grub2-mkimage -o bootaa64.efi -p /boot/grub2 -O arm64-efi  fat iso9660 part_gpt part_msdos  normal boot linux configfile loopback chain efifwsetup efi_gop efinet ls search search_label search_fs_uuid search_fs_file  gfxterm gfxterm_background gfxterm_menu test all_video loadenv  exfat ext2 udf halt gfxmenu png tga lsefi help all_video probe echo

# both bootx64.efi and grubx64.efi are signed with VMware key
EFI_IMAGE=boot/grub2/efiboot.img
EFI_FOLDER=`readlink -f ${STAGE_PATH}/efiboot`
dd if=/dev/zero of=${WORKINGDIR}/${EFI_IMAGE} bs=3K count=1024
mkdosfs ${WORKINGDIR}/${EFI_IMAGE}
mkdir $EFI_FOLDER
mount -o loop ${WORKINGDIR}/${EFI_IMAGE} $EFI_FOLDER
mkdir $EFI_FOLDER/EFI
mkdir ${WORKINGDIR}/EFI
cp -r ./EFI_$(uname -m)/BOOT $EFI_FOLDER/EFI/
cp -r ./EFI_$(uname -m)/BOOT ${WORKINGDIR}/EFI/
ls -lR $EFI_FOLDER
umount $EFI_FOLDER
rm -rf $EFI_FOLDER
#mcopy -s -i ${WORKINGDIR}/${EFI_IMAGE} ./EFI '::/'

if [ "$LIVE_CD" = true ] ; then
    mv ${WORKINGDIR}/isolinux/live-menu.cfg ${WORKINGDIR}/isolinux/menu.cfg
fi

cp sample_ks.cfg ${WORKINGDIR}/isolinux/

find ${BUILDROOT} -name linux-[0-9]*.rpm | head -1 | xargs rpm2cpio | cpio -iv --to-stdout ./boot/vmlinuz* > ${WORKINGDIR}/isolinux/vmlinuz

rm -f ${BUILDROOT}/installer/*.pyc
rm -rf ${BUILDROOT}/installer/BUILD_DVD
# Copy package list json files, dereference symlinks
cp -rf -L $OUTPUT_DATA_PATH/*.json ${BUILDROOT}/installer/
#ID in the initrd.gz now is PHOTON_VMWARE_CD . This is how we recognize that the cd is actually ours. touch this file there.
touch ${WORKINGDIR}/PHOTON_VMWARE_CD

# Step 4.5 Create necessary devices
mkfifo ${BUILDROOT}/dev/initctl
mknod ${BUILDROOT}/dev/ram0 b 1 0
mknod ${BUILDROOT}/dev/ram1 b 1 1
mknod ${BUILDROOT}/dev/ram2 b 1 2
mknod ${BUILDROOT}/dev/ram3 b 1 3
mknod ${BUILDROOT}/dev/sda b 8 0


#- Step 5 - Creating the boot script
mkdir -p ${BUILDROOT}/etc/systemd/scripts

# Step 6 create fstab

cp BUILD_DVD/fstab ${BUILDROOT}/etc/fstab

mkdir -p ${BUILDROOT}/etc/yum.repos.d
cat >> ${BUILDROOT}/etc/yum.repos.d/photon-iso.repo << EOF
[photon-iso]
name=VMWare Photon Linux 1.0(x86_64)
baseurl=file:///mnt/cdrom/RPMS
gpgkey=file:///etc/pki/rpm-gpg/VMWARE-RPM-GPG-KEY
gpgcheck=1
enabled=1
skip_if_unavailable=True
EOF

#- Step 7 - Create installer script
if [ "$LIVE_CD" = false ] ; then

cat >> ${BUILDROOT}/bin/bootphotoninstaller << EOF
#!/bin/bash
cd /installer
[ \$(tty) == '/dev/tty1' ] && LANG=en_US.UTF-8 ./isoInstaller.py --json-file=$PACKAGE_LIST_FILE_BASE_NAME 2> /var/log/installer && shutdown -r now
/bin/bash
EOF

chmod 755 ${BUILDROOT}/bin/bootphotoninstaller

fi

cat >> ${BUILDROOT}/init << EOF
mount -t proc proc /proc
/lib/systemd/systemd
EOF
chmod 755 ${BUILDROOT}/init

#adding autologin to the root user
# and set TERM=linux for installer
sed -i "s/ExecStart.*/ExecStart=-\/sbin\/agetty --autologin root --noclear %I linux/g" ${BUILDROOT}/lib/systemd/system/getty@.service

#- Step 7 - Create installer script
if [ "$LIVE_CD" = false ] ; then

    sed -i "s/root:.*/root:x:0:0:root:\/root:\/bin\/bootphotoninstaller/g" ${BUILDROOT}/etc/passwd

fi

mkdir -p ${BUILDROOT}/mnt/photon-root/photon-chroot
rm -rf ${BUILDROOT}/RPMS

run_command " echo ${RPMS_PATH}" "echo ${RPMS_PATH}" "${LOGFILE}"
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

rm -rf ${BUILDROOT}/LOGS

if [ "$LIVE_CD" = false ] ; then
    # Cleaning up
    #Remove our rpm database as it fills up the ramdisk
    for filename in ${BUILDROOT}/usr/lib/*; do 
        #run_command " echo ${filename}" "echo ${filename}" "${LOGFILE}"
        if [[ -f ${filename} ]]; then
            file ${filename} | grep ELF >/dev/null 2>&1
            #run_command " file ${filename}" "echo ${filename}" "${LOGFILE}"
            if [[ $? -eq 0 ]]; then
                run_command " strip ${filename}" "strip ${filename}" "${LOGFILE}"
            fi;
        fi;
    done

    #Remove our rpm database as it fills up the ramdisk
    for filename in $(find ${BUILDROOT}/usr/lib/modules); do 
        #run_command " echo ${filename}" "echo ${filename}" "${LOGFILE}"
        if [[ -f ${filename} ]]; then
            file ${filename} | grep ELF >/dev/null 2>&1
            #run_command " file ${filename}" "echo ${filename}" "${LOGFILE}"
            if [[ $? -eq 0 ]]; then
                run_command " strip ${filename}" "strip ${filename}" "${LOGFILE}"
            fi;
        fi;
    done
    rm -rf ${BUILDROOT}/home/*
    rm -rf ${BUILDROOT}/var/lib/rpm

    # Remove the boot directory
    rm -rf ${BUILDROOT}/boot

    #Remove the include files.
    rm -rf ${BUILDROOT}/usr/include

    rm ${BUILDROOT}/lib64/libmvec*
    rm ${BUILDROOT}/usr/sbin/sln
    rm ${BUILDROOT}/usr/bin/oldfind

    rm ${BUILDROOT}/usr/bin/localedef
    rm ${BUILDROOT}/usr/bin/systemd-nspawn
    rm ${BUILDROOT}/usr/bin/systemd-analyze
    rm -rf ${BUILDROOT}/usr/lib64/gconv
    rm ${BUILDROOT}/usr/bin/sqlite3

    rm ${BUILDROOT}/usr/bin/bsdcpio
    rm ${BUILDROOT}/usr/bin/bsdtar
    rm ${BUILDROOT}/usr/bin/networkctl
    rm ${BUILDROOT}/usr/bin/machinectl
    rm ${BUILDROOT}/usr/bin/pkg-config
    rm ${BUILDROOT}/usr/bin/openssl
    rm ${BUILDROOT}/usr/bin/timedatectl
    rm ${BUILDROOT}/usr/bin/localectl
    rm ${BUILDROOT}/usr/bin/systemd-cgls
    rm ${BUILDROOT}/usr/bin/systemd-inhibit
    rm ${BUILDROOT}/usr/bin/systemd-studio-bridge
    rm ${BUILDROOT}/usr/bin/iconv

    rm -rf ${BUILDROOT}/usr/lib/python2.7/lib2to3
    rm -rf ${BUILDROOT}/usr/lib/python2.7/lib-tk
    rm -rf ${BUILDROOT}/usr/lib/python2.7/ensurepip
    rm -rf ${BUILDROOT}/usr/lib/python2.7/distutils
    rm -rf ${BUILDROOT}/usr/lib/python2.7/pydoc_data
    rm -rf ${BUILDROOT}/usr/lib/python2.7/idlelib
    rm -rf ${BUILDROOT}/usr/lib/python2.7/unittest 

    rm ${BUILDROOT}/usr/lib/librpmbuild.so*
    rm ${BUILDROOT}/usr/lib/libdb_cxx*
    rm ${BUILDROOT}/usr/lib/libnss_compat*

    rm ${BUILDROOT}/usr/bin/grub2-*
    rm ${BUILDROOT}/usr/lib/grub/i386-pc/*.module
    rm ${BUILDROOT}/usr/lib/grub/x86_64-efi/*.module

    for j in `ls ${BUILDROOT}/usr/sbin/grub2*`; do
        bsname=$(basename "$j")
        if [ $bsname != 'grub2-install' ]; then
            rm $j
        fi
    done

    # TODO: mbassiouny, Find a clean way to do that
    for i in `ls ${BUILDROOT}/usr/share/`; do
        if [ $i != 'terminfo' -a $i != 'cracklib' -a $i != 'grub' -a $i != 'factory' -a $i != 'dbus-1' ]; then
            rm -rf ${BUILDROOT}/usr/share/$i
        fi
    done

fi

# Set password max days to 99999 (disable aging)
chage -R ${BUILDROOT} -M 99999 root

# Generate the intird
pushd $BUILDROOT
(find . | cpio -o -H newc --quiet | gzip -9 ) > ${WORKINGDIR}/isolinux/initrd.img
popd
rm -rf $BUILDROOT

#Step 9 Generate the ISO!!!!
pushd $WORKINGDIR
mkisofs -R -l -L -D -b isolinux/isolinux.bin -c isolinux/boot.cat \
        -no-emul-boot -boot-load-size 4 -boot-info-table \
        -eltorito-alt-boot -e ${EFI_IMAGE} -no-emul-boot \
        -V "PHOTON_$(date +%Y%m%d)" \
        $WORKINGDIR >$ISO_OUTPUT_NAME
popd
