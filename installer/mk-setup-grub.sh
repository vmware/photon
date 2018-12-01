#!/bin/bash
#################################################
#       Title:  mk-setup-grub                   #
#        Date:  2014-11-26                      #
#     Version:  1.0                             #
#      Author:  sharathg@vmware.com             #
#     Options:                                  #
#################################################
#    Overview
#        This is a precursor for the vmware build system.
#        This assumes that an empty hard disk is attached to the build VM.
#        The path to this empty disk is specified in the HDD variable in config.inc
#    End
#

grub_efi_install()
{
    mkdir -p $BUILDROOT/boot/efi
    #
    # if it is a loop device then we should mount the dev mapped boot partition
    #
    if [[ $HDD == *"loop"* ]]
    then
         BOOT_PARTITION=/dev/mapper/`basename ${HDD}`p$EFI_PARTITION_NUMBER
    elif [[ $HDD == *"nvme"* || $HDD == *"mmcblk"* ]]
    then
         BOOT_PARTITION=${HDD}p$EFI_PARTITION_NUMBER
    else
         BOOT_PARTITION=${HDD}$EFI_PARTITION_NUMBER
    fi
    mkfs.fat $BOOT_PARTITION
    mount -t vfat $BOOT_PARTITION $BUILDROOT/boot/efi
    cp $INSTALLER_PATH/boot/unifont.pf2 /usr/share/grub/
    mkdir -p $BUILDROOT/boot/efi/EFI/Boot/
    if [ $(uname -m) == "aarch64" ]
    then
        cp $INSTALLER_PATH/EFI_aarch64/BOOT/* $BUILDROOT/boot/efi/EFI/Boot/
        local EXE_NAME="bootaa64.efi"
    elif [ $(uname -m) == "x86_64" ]
    then
        cp $INSTALLER_PATH/EFI_x86_64/BOOT/* $BUILDROOT/boot/efi/EFI/Boot/
        local EXE_NAME="bootx64.efi"
    fi

    mkdir -p $BUILDROOT/boot/efi/boot/grub2
    cat > $BUILDROOT/boot/efi/boot/grub2/grub.cfg << EOF
search -n -u ${BOOT_UUID} -s
configfile ${BOOT_DIRECTORY}grub2/grub.cfg
EOF
    # Some platforms do not support adding boot entry. Thus, ignore failures.
    efibootmgr --create --remove-dups --disk "$HDD" --part $EFI_PARTITION_NUMBER --loader "/EFI/Boot/$EXE_NAME" --label Photon --verbose >&2 || :
    umount $BUILDROOT/boot/efi
}

grub_mbr_install()
{
    $grubInstallCmd --target=i386-pc --force --boot-directory=$BUILDROOT/boot "$HDD"
}
set -o errexit        # exit if error...insurance ;)
set -o nounset        # exit if variable not initalized
set +h            # disable hashall
PRGNAME=${0##*/}    # script name minus the path
SCRIPT_PATH=$(dirname $(realpath -s $0))
INSTALLER_PATH=$SCRIPT_PATH
source $SCRIPT_PATH/config.inc        #    configuration parameters
source $SCRIPT_PATH/function.inc        #    commonn functions
LOGFILE=/var/log/"${PRGNAME}-${LOGFILE}"    #    set log file name
ARCH=$(uname -m)    # host architecture
[ ${EUID} -eq 0 ]    || fail "${PRGNAME}: Need to be root user: FAILURE"
> ${LOGFILE}        #    clear/initialize logfile
# Check if passing a HHD and partition
if [ $# -ge 6 ]
    then
        BOOTMODE=$1
    HDD=$2
    ROOT_PARTITION_PATH=$3
    BOOT_PARTITION_PATH=$4
    BOOT_DIRECTORY=$5
    BOOT_PARTITION_NUMBER=$6
    EFI_PARTITION_NUMBER="1"
    DUALBOOT="false"
fi

if [ $# -eq 7 ]
    then
        DUALBOOT=$7
        EFI_PARTITION_NUMBER="2"
fi

#
#    Install grub2.
#
PARTUUID=$(blkid -s PARTUUID -o value $ROOT_PARTITION_PATH)
BOOT_UUID=$(blkid -s UUID -o value $BOOT_PARTITION_PATH)

if [ "$BOOTMODE" == "efi" ]; then
    grub_efi_install
    if [ "$DUALBOOT" == "true" ]; then
        #Cleanup the workspace directory
        rm -rf "$BUILDROOT"/tools
        rm -rf "$BUILDROOT"/RPMS
        exit 0
    fi
fi

grubInstallCmd=""
mkdir -p $BUILDROOT/boot/grub2
ln -sfv grub2 $BUILDROOT/boot/grub
command -v grub-install >/dev/null 2>&1 && grubInstallCmd="grub-install" && { echo >&2 "Found grub-install"; }
command -v grub2-install >/dev/null 2>&1 && grubInstallCmd="grub2-install" && { echo >&2 "Found grub2-install"; }

if [ "$BOOTMODE" == "bios" ]; then
    if [ -z $grubInstallCmd ]; then
        echo "Unable to find grub install command"
        exit 1
    fi
    grub_mbr_install
fi

rm -rf ${BUILDROOT}/boot/grub2/fonts
cp $INSTALLER_PATH/boot/ascii.pf2 ${BUILDROOT}/boot/grub2/
mkdir -p ${BUILDROOT}/boot/grub2/themes/photon
cp $INSTALLER_PATH/boot/splash.png ${BUILDROOT}/boot/grub2/themes/photon/photon.png
cp $INSTALLER_PATH/boot/terminal_*.tga ${BUILDROOT}/boot/grub2/themes/photon/
cp $INSTALLER_PATH/boot/theme.txt ${BUILDROOT}/boot/grub2/themes/photon/
# linux-esx tries to mount rootfs even before nvme got initialized.
# rootwait fixes this issue
EXTRA_PARAMS=""
if [[ $HDD == *"nvme"* ]]; then
    EXTRA_PARAMS=rootwait
fi

cat > $BUILDROOT/boot/grub2/grub.cfg << EOF
# Begin /boot/grub2/grub.cfg

set default=0
set timeout=5
search -n -u $BOOT_UUID -s
loadfont ${BOOT_DIRECTORY}grub2/ascii.pf2

insmod gfxterm
insmod vbe
insmod tga
insmod png
insmod ext2
insmod part_gpt

set gfxmode="640x480"
gfxpayload=keep

terminal_output gfxterm

set theme=${BOOT_DIRECTORY}grub2/themes/photon/theme.txt
load_env -f ${BOOT_DIRECTORY}photon.cfg
if [ -f  ${BOOT_DIRECTORY}systemd.cfg ]; then
    load_env -f ${BOOT_DIRECTORY}systemd.cfg
else
    set systemd_cmdline=net.ifnames=0
fi
set rootpartition=PARTUUID=$PARTUUID

menuentry "Photon" {
    linux ${BOOT_DIRECTORY}\$photon_linux root=\$rootpartition \$photon_cmdline \$systemd_cmdline $EXTRA_PARAMS
    if [ -f ${BOOT_DIRECTORY}\$photon_initrd ]; then
        initrd ${BOOT_DIRECTORY}\$photon_initrd
    fi
}
# End /boot/grub2/grub.cfg
EOF

#Cleanup the workspace directory
rm -rf "$BUILDROOT"/tools
rm -rf "$BUILDROOT"/RPMS

