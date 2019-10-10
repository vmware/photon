#! /bin/bash

set -o errexit        # exit if error...insurance ;)
set -o nounset        # exit if variable not initalized
set +h            # disable hashall
set -x
SCRIPT_PATH=$(dirname $(realpath -s $0))

BUILDROOT=$1
ROOT_PARTITION_PATH=$2
BOOT_PARTITION_PATH=$3
BOOT_DIRECTORY=$4

#
#    Install grub2.
#
PARTUUID=$(blkid -s PARTUUID -o value $ROOT_PARTITION_PATH)
BOOT_UUID=$(blkid -s UUID -o value $BOOT_PARTITION_PATH)

# linux-esx tries to mount rootfs even before nvme got initialized.
# rootwait fixes this issue
EXTRA_PARAMS=""
if [[ $ROOT_PARTITION_PATH == *"nvme"* ]]; then
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

if [ "$PARTUUID" != ""  ]; then
    set rootpartition=PARTUUID=$PARTUUID
else
    set rootpartition=$ROOT_PARTITION_PATH
fi

menuentry "Photon" {
    linux ${BOOT_DIRECTORY}\$photon_linux root=\$rootpartition \$photon_cmdline \$systemd_cmdline $EXTRA_PARAMS
    if [ -f ${BOOT_DIRECTORY}\$photon_initrd ]; then
        initrd ${BOOT_DIRECTORY}\$photon_initrd
    fi
}
# End /boot/grub2/grub.cfg
EOF
