# Install the VirtualBox guest additions
# Mostly taken from https://github.com/aseigneurin/vms/blob/master/packer/ubuntu-13.04-server-amd64/scripts/vbox.sh
VBOX_ISO=VBoxGuestAdditions.iso
mount -o loop $VBOX_ISO /mnt
yes|sh /mnt/VBoxLinuxAdditions.run
umount /mnt

# Cleanup
rm $VBOX_ISO
