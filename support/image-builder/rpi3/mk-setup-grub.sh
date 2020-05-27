#! /bin/bash

set -o errexit        # exit if error...insurance ;)
set -o nounset        # exit if variable not initalized
set +h            # disable hashall
SCRIPT_PATH=$(dirname $(realpath -s $0))

BUILDROOT=$1
ROOT_PARTITION_PATH=$2
BOOT_PARTITION_PATH=$3
BOOT_DIRECTORY=$4

# Raspberry prorpiaetary GPU bootloader (1st stage)
cp -r $SCRIPT_PATH/esp/* $BUILDROOT/boot/efi/

EXTRA_PARAMS="rootwait rw console=ttyS0,115200n8 console=tty0 cma=256M"

cat > $BUILDROOT/boot/grub2/grub.cfg << EOF
# Begin /boot/grub2/grub.cfg

set default=0
set timeout=2
loadfont ${BOOT_DIRECTORY}grub2/ascii.pf2

insmod all_video
insmod gfxterm
insmod png
insmod ext2

set gfxmode="800x600"
gfxpayload=keep

terminal_output gfxterm

set theme=${BOOT_DIRECTORY}grub2/themes/photon/theme.txt
load_env -f ${BOOT_DIRECTORY}photon.cfg
if [ -f  ${BOOT_DIRECTORY}systemd.cfg ]; then
    load_env -f ${BOOT_DIRECTORY}systemd.cfg
else
    set systemd_cmdline=net.ifnames=0
fi
set rootpartition=/dev/mmcblk0p2

menuentry "Photon" {
    linux ${BOOT_DIRECTORY}\$photon_linux root=\$rootpartition \$photon_cmdline \$systemd_cmdline $EXTRA_PARAMS
    if [ -f ${BOOT_DIRECTORY}\$photon_initrd ]; then
        initrd ${BOOT_DIRECTORY}\$photon_initrd
    fi
}
# End /boot/grub2/grub.cfg
EOF
