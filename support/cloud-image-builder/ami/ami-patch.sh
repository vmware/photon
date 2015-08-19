#!/bin/bash


cd /lib/systemd/system/multi-user.target.wants/

ln -s ../docker.service docker.service
ln -s ../eth0.service eth0.service

cd /

echo "127.0.0.1 localhost" >> /etc/hosts

# Set UTC timezone
# ln -sf /usr/share/zoneinfo/UTC /etc/localtime

# Update /etc/resolv.conf

rm /etc/resolv.conf

echo "nameserver 172.31.0.2" >> /etc/resolv.conf
echo "search ec2.internal" >> /etc/resolv.conf


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
echo "PubkeyAuthentication yes" >> /etc/ssh/sshd_config
echo "PasswordAuthentication no" >> /etc/ssh/sshd_config
echo "PermitRootLogin without-password" >> /etc/ssh/sshd_config
echo "PermitTunnel no" >> /etc/ssh/sshd_config
echo "AllowTcpForwarding yes" >> /etc/ssh/sshd_config
echo "X11Forwarding no" >> /etc/ssh/sshd_config
echo "ClientAliveInterval 420" >> /etc/ssh/sshd_config
echo "UseDNS no" >> /etc/ssh/sshd_config
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
echo "ServerAliveInterval 420" >> /etc/ssh/ssh_config

sed -i '/.*linux.*vmlinuz/ s/$/ console=ttyS0/' /boot/grub/grub.cfg

# Disable loading/unloading of modules
echo 1 > /proc/sys/kernel/modules_disabled

# Remove kernel symbols
rm /boot/system.map*

