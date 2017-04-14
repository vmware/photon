#! /bin/bash

# efiboot is a fat16 image that has at least EFI/BOOT/bootx64.efi
#
# let's assume given /home/user/EFI/BOOT/bootx64.efi,
# then EFI_DIR=/home/user/EFI

EFI_DIR=./EFI
IMAGE=./BUILD_DVD/boot/grub2/efiboot.img
dd if=/dev/zero of=$IMAGE bs=3K count=1024
mkdosfs $IMAGE
mcopy -s -i $IMAGE $EFI_DIR '::/'

# as a bootx64.efi we use shim.efi from shim-0.9
# # make VENDOR_CERT_FILE=<VMware cert> RELEASE=1 EFI_PATH=/usr/lib 'DEFAULT_LOADER=\\\\grubx64.efi' shim.efi
# # mv shim.efi bootx64.efi

# grubx64.efi is generated on Photon OS by using grub2-efi >= 2.02-7:
# # grub2-efi-mkimage -o grubx64.efi -p /boot/grub2 -O x86_64-efi  fat iso9660 part_gpt part_msdos  normal boot linux configfile loopback chain  efifwsetup efi_gop efi_uga  ls search search_label search_fs_uuid search_fs_file  gfxterm gfxterm_background gfxterm_menu test all_video loadenv  exfat ext2 udf halt gfxmenu png tga lsefi help linuxefi

# both bootx64.efi and grubx64.efi are signed with VMware key

