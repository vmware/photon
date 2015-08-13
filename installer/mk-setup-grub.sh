#!/bin/bash
#################################################
#       Title:  mk-setup-grub                   #
#        Date:  2014-11-26                      #
#     Version:  1.0                             #
#      Author:  sharathg@vmware.com             #
#     Options:                                  #
#################################################
#	Overview
#		This is a precursor for the vmware build system.
#		This assumes that an empty hard disk is attached to the build VM.
#		The path to this empty disk is specified in the HDD variable in config.inc
#	End
#
grub_efi_install()
{
    mkdir $BUILDROOT/boot/efi
    mkfs.vfat /dev/sda1
    mount -t vfat /dev/sda1 $BUILDROOT/boot/efi
    cp boot/unifont.pf2 /usr/share/grub/
    grub2-efi-install --target=x86_64-efi --efi-directory=$BUILDROOT/boot/efi --bootloader-id=Boot --root-directory=$BUILDROOT --recheck --debug
    mv $BUILDROOT/boot/efi/EFI/Boot/grubx64.efi $BUILDROOT/boot/efi/EFI/Boot/bootx64.efi
    umount $BUILDROOT/boot/efi
}

grub_mbr_install()
{
    $grubInstallCmd --force --boot-directory=$BUILDROOT/boot "$HDD"
}

set -o errexit		# exit if error...insurance ;)
set -o nounset		# exit if variable not initalized
set +h			# disable hashall
PRGNAME=${0##*/}	# script name minus the path
source config.inc		#	configuration parameters
source function.inc		#	commonn functions
LOGFILE=/var/log/"${PRGNAME}-${LOGFILE}"	#	set log file name
#LOGFILE=/dev/null		#	uncomment to disable log file
ARCH=$(uname -m)	# host architecture
[ ${EUID} -eq 0 ]	|| fail "${PRGNAME}: Need to be root user: FAILURE"
> ${LOGFILE}		#	clear/initialize logfile

# Check if passing a HHD and partition
if [ $# -eq 3 ] 
	then
        BOOTMODE=$1
		HDD=$2
		PARTITION=$3
fi

#
#	Install grub2.
#
UUID=$(blkid -s UUID -o value $PARTITION)

grubInstallCmd=""
mkdir -p $BUILDROOT/boot/grub2
ln -sfv grub2 $BUILDROOT/boot/grub
command -v grub-install >/dev/null 2>&1 && grubInstallCmd="grub-install" && { echo >&2 "Found grub-install"; }
command -v grub2-install >/dev/null 2>&1 && grubInstallCmd="grub2-install" && { echo >&2 "Found grub2-install"; }
if [ -z $grubInstallCmd ]; then
echo "Unable to found grub install command"
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
cat > "$BUILDROOT"/boot/grub2/grub.cfg << "EOF"
# Begin /boot/grub2/grub.cfg
set default=0
set timeout=5
set root=(hd0,2)
loadfont /boot/grub2/unifont.pf2

insmod gfxterm
insmod vbe
insmod tga

set gfxmode="640x480"
gfxpayload=keep

terminal_output gfxterm

set theme=/boot/grub2/themes/photon/theme.txt

menuentry "Photon" {
	insmod ext2
    insmod part_gpt
	linux /boot/vmlinuz-4.0.9 init=/lib/systemd/systemd root=UUID=UUID_PLACEHOLDER loglevel=3 ro
	initrd /boot/initrd.img-no-kmods
}
# End /boot/grub2/grub.cfg
EOF

sed -i "s/UUID_PLACEHOLDER/$UUID/" "$BUILDROOT"/boot/grub2/grub.cfg > ${LOGFILE}	

#Cleanup the workspace directory
rm -rf "$BUILDROOT"/tools
rm -rf "$BUILDROOT"/RPMS

#umount $BUILDROOT
