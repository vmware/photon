This repository contains signed binaries: bootx64.efi and bootaa64.efi

# As a bootx64.efi we use shimx64.efi from shim-12
# # make VENDOR_CERT_FILE=<VMware cert> EFI_PATH=/usr/lib 'DEFAULT_LOADER=\\\\grubx64.efi' shimx64.efi
# # mv shimx64.efi bootx64.efi

# grubx64.efi is generated on Photon OS by using grub2-efi-2.02-12:
# # grub2-mkimage -o grubx64.efi -p /boot/grub2 -O x86_64-efi fat iso9660 part_gpt part_msdos normal boot linux configfile loopback chain efifwsetup efi_gop efi_uga ls search search_label search_fs_uuid search_fs_file gfxterm gfxterm_background gfxterm_menu test all_video loadenv exfat ext2 udf halt gfxmenu png tga lsefi help probe echo lvm

# grubaa64.efi is generated on Photon OS (aarch64) by using grub2-efi >= 2.02-11:
# cat > /tmp/grub-embed-config.cfg << EOF
#search.fs_label rootfs root
#configfile /boot/grub2/grub.cfg
#EOF
#grub2-mkimage -o bootaa64.efi -p /boot/grub2 -O arm64-efi -c /tmp/grub-embed-config.cfg fat iso9660 part_gpt part_msdos  normal boot linux configfile loopback chain efifwsetup efi_gop efinet ls search search_label search_fs_uuid search_fs_file  gfxterm gfxterm_background gfxterm_menu test all_video loadenv  exfat ext2 udf halt gfxmenu png tga lsefi help all_video probe echo

# both bootx64.efi and grubx64.efi are signed with VMware key
