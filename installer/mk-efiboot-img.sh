#! /bin/bash

# efiboot is a fat16 image that has only one file EFI/BOOT/bootx64.efi
#
# let's assume given /home/user/EFI/BOOT/bootx64.efi,
# then EFI_DIR=/home/user/EFI

EFI_DIR=./EFI
IMAGE=./BUILD_DVD/boot/grub2/efiboot.img
dd if=/dev/zero of=$IMAGE bs=1K count=1024
mkdosfs $IMAGE
mcopy -s -i $IMAGE $EFI_DIR '::/'

# bootx64.efi is generated on Photon OS by:
#
# # grub2-efi-mkimage -o bootx64.efi -p /boot/grub2 -O x86_64-efi  fat iso9660 part_gpt part_msdos  normal boot linux configfile loopback chain  efifwsetup efi_gop efi_uga  ls search search_label search_fs_uuid search_fs_file  gfxterm gfxterm_background gfxterm_menu test all_video loadenv  exfat ext2 udf halt gfxmenu png tga
