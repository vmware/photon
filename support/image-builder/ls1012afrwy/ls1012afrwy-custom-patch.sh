#!/bin/bash

echo -e "changeme\nchangeme" | passwd root
chage -d 0 -M 999 root

echo "/dev/mmcblk0p4 swap swap defaults 0 0" >> /etc/fstab

chmod +x /usr/local/bin/resizefs.sh
ln -s /lib/systemd/system/resizefs.service /etc/systemd/system/multi-user.target.wants/resizefs.service
ln -s /lib/systemd/system/sshd-keygen.service /etc/systemd/system/multi-user.target.wants/sshd-keygen.service
ln -s /lib/systemd/system/sshd.service /etc/systemd/system/multi-user.target.wants/sshd.service

