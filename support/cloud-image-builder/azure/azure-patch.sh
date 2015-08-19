#!/bin/bash
set -x

cd /lib/systemd/system/multi-user.target.wants/

# Create links in multi-user.target to auto-start these scripts and services.

ln -s ../docker.service docker.service
ln -s ../eth0.service eth0.service
ln -s ../waagent.service waagent.service
ln -s ../sshd-keygen.service sshd-keygen.service



# Remove ssh host keys and add script to regenerate them at boot time.

rm /etc/ssh/ssh_host_*

sudo groupadd docker
sudo groupadd sudo

rm /root/.ssh/authorized_keys   

# ssh server config
# Override old values
rm /etc/ssh/sshd_config

echo "AuthorizedKeysFile .ssh/authorized_keys" >> /etc/ssh/sshd_config
echo "UsePrivilegeSeparation sandbox" >> /etc/ssh/sshd_config
echo "PasswordAuthentication no" >> /etc/ssh/sshd_config
echo "PermitRootLogin without-password" >> /etc/ssh/sshd_config
echo "PermitTunnel no" >> /etc/ssh/sshd_config
echo "AllowTcpForwarding yes" >> /etc/ssh/sshd_config
echo "X11Forwarding no" >> /etc/ssh/sshd_config
echo "ClientAliveInterval 180" >> /etc/ssh/sshd_config
echo "ChallengeResponseAuthentication no" >> /etc/ssh/sshd_config
echo "UsePAM yes" >> /etc/ssh/sshd_config


# ssh client config
# Override old values

rm /etc/ssh/ssh_config

echo "Host *" >> /etc/ssh/ssh_config
echo "Protocol 2" >> /etc/ssh/ssh_config
echo "ForwardAgent no" >> /etc/ssh/ssh_config
echo "ForwardX11 no" >> /etc/ssh/ssh_config
echo "X11Forwarding no" >> /etc/ssh/ssh_config
echo "HostbasedAuthentication no" >> /etc/ssh/ssh_config
echo "StrictHostKeyChecking no" >> /etc/ssh/ssh_config
echo "Ciphers aes128-ctr,aes192-ctr,aes256-ctr,arcfour256,arcfour128,aes128-cbc,3des-cbc" >> /etc/ssh/ssh_config
echo "Tunnel no" >> /etc/ssh/ssh_config
echo "ServerAliveInterval 180" >> /etc/ssh/ssh_config

sed -i '/.*linux.*vmlinuz/ s/$/ console=ttyS0 earlyprintk=ttyS0 rootdelay=30/' /boot/grub/grub.cfg


# Disable loading/unloading of modules
echo 1 > /proc/sys/kernel/modules_disabled

# Remove kernel symbols
rm /boot/system.map*

sudo waagent -force -deprovision
export HISTSIZE=0
systemctl enable waagent.service
