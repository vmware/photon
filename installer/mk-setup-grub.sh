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
    mkdir $BUILDROOT/boot/efi
    #
    # if it is a loop device then we should mount the dev mapped boot partition
    #
    if [[ $HDD == *"loop"* ]]
    then
         BOOT_PARTITION=/dev/mapper/`basename ${HDD}`p1
    else
         BOOT_PARTITION=${HDD}1
    fi
    mkfs.vfat $BOOT_PARTITION
    mount -t vfat $BOOT_PARTITION $BUILDROOT/boot/efi
    cp boot/unifont.pf2 /usr/share/grub/
    grub2-efi-install --target=x86_64-efi --efi-directory=$BUILDROOT/boot/efi --bootloader-id=Boot --root-directory=$BUILDROOT --recheck
    rm $BUILDROOT/boot/efi/EFI/Boot/grubx64.efi
    cp efi/bootx64.efi $BUILDROOT/boot/efi/EFI/Boot/bootx64.efi
    umount $BUILDROOT/boot/efi
}

grub_mbr_install()
{
    $grubInstallCmd --force --boot-directory=$BUILDROOT/boot "$HDD"
}

set -o errexit        # exit if error...insurance ;)
set -o nounset        # exit if variable not initalized
set +h            # disable hashall
PRGNAME=${0##*/}    # script name minus the path
source config.inc        #    configuration parameters
source function.inc        #    commonn functions
LOGFILE=/var/log/"${PRGNAME}-${LOGFILE}"    #    set log file name
ARCH=$(uname -m)    # host architecture
[ ${EUID} -eq 0 ]    || fail "${PRGNAME}: Need to be root user: FAILURE"
> ${LOGFILE}        #    clear/initialize logfile

# Check if passing a HHD and partition
if [ $# -eq 5 ] 
    then
        BOOTMODE=$1
    HDD=$2
    ROOT_PARTITION_PATH=$3
    BOOT_PARTITION_PATH=$4
    BOOT_DIRECTORY=$5
fi

#
#    Install grub2.
#
UUID=$(blkid -s UUID -o value $ROOT_PARTITION_PATH)
BOOT_UUID=$(blkid -s UUID -o value $BOOT_PARTITION_PATH)

grubInstallCmd=""
mkdir -p $BUILDROOT/boot/grub2
ln -sfv grub2 $BUILDROOT/boot/grub
command -v grub-install >/dev/null 2>&1 && grubInstallCmd="grub-install" && { echo >&2 "Found grub-install"; }
command -v grub2-install >/dev/null 2>&1 && grubInstallCmd="grub2-install" && { echo >&2 "Found grub2-install"; }
if [ -z $grubInstallCmd ]; then
echo "Unable to find grub install command"
exit 1
fi

if [ "$BOOTMODE" == "bios" ]; then 
    grub_mbr_install
fi
if [ "$BOOTMODE" == "efi" ]; then 
    grub_efi_install
fi

cp boot/unifont.pf2 ${BUILDROOT}/boot/grub2/
mkdir -p ${BUILDROOT}/boot/grub2/themes/photon
cp boot/splash.tga ${BUILDROOT}/boot/grub2/themes/photon/photon.tga
cp boot/terminal_*.tga ${BUILDROOT}/boot/grub2/themes/photon/
cp boot/theme.txt ${BUILDROOT}/boot/grub2/themes/photon/
cat > $BUILDROOT/boot/grub2/grub.cfg << EOF
# Begin /boot/grub2/grub.cfg

function set_rootpartition {
    if [ "\$photon_initrd" ]; then
        set rootpartition=UUID=$UUID
    else
        search -n -u $UUID -s rootpartition_device
        regexp -s dev '.{2}(.)' \$rootpartition_device
        regexp -s part '.*(.)' \$rootpartition_device
        regexp -s char '.{'\$dev'}(.)' abcdefghij
        set rootpartition=/dev/sd\$char\$part
    fi
}

set default=0
set timeout=5
search -n -u $BOOT_UUID -s
loadfont "$BOOT_DIRECTORY"grub2/unifont.pf2

insmod gfxterm
insmod vbe
insmod tga
insmod ext2
insmod part_gpt

set gfxmode="640x480"
gfxpayload=keep

terminal_output gfxterm

set theme="$BOOT_DIRECTORY"grub2/themes/photon/theme.txt
load_env -f "$BOOT_DIRECTORY"photon.cfg
set_rootpartition

menuentry "Photon" {
    linux "$BOOT_DIRECTORY"\$photon_linux root=\$rootpartition \$photon_cmdline
    if [ "\$photon_initrd" ]; then
        initrd "$BOOT_DIRECTORY"\$photon_initrd
    fi
}
# End /boot/grub2/grub.cfg
EOF

#Cleanup the workspace directory
rm -rf "$BUILDROOT"/tools
rm -rf "$BUILDROOT"/RPMS

