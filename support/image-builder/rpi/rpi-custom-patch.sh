#!/bin/bash

echo "/dev/mmcblk0p3 none swap defaults 0 0" >> /etc/fstab

chmod +x /usr/local/bin/resizefs.sh
ln -s /lib/systemd/system/resizefs.service /etc/systemd/system/multi-user.target.wants/resizefs.service
ln -s /lib/systemd/system/sshd-keygen.service /etc/systemd/system/multi-user.target.wants/sshd-keygen.service
ln -s /lib/systemd/system/sshd.service /etc/systemd/system/multi-user.target.wants/sshd.service

cat > /etc/modules-load.d/genet.conf << "EOF"
# To fix https://github.com/raspberrypi/linux/issues/3108
# Issue: bcmgenet_mii_probe() is getting called before unimac_mdio_probe() finishes
#        which causes the ethernet "failed to connect PHY" in rpi4
# Sol:   Load the modules in below order using systemd-modules

mdio_bcm_unimac
genet
EOF
