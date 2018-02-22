#!/bin/bash

cd /lib/systemd/system/multi-user.target.wants/

# Create links in multi-user.target to auto-start these scripts and services.

sed -i 's/Wants=network-online.*/Wants=systemd-networkd-wait-online.service sshd.service sshd-keygen.service/' /usr/lib/systemd/system/waagent.service
sed -i 's/After=network-online.target/After=systemd-networkd-wait-online.service cloud-init.service/' /usr/lib/systemd/system/waagent.service

ln -s ../docker.service docker.service
ln -s ../waagent.service waagent.service
ln -s ../sshd-keygen.service sshd-keygen.service

#Disable cloud-init
#rm -rf /etc/systemd/system/cloud-init.target.wants
# Remove ssh host keys and add script to regenerate them at boot time.

rm -f /etc/ssh/ssh_host_*

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
echo "HostbasedAuthentication no" >> /etc/ssh/ssh_config
echo "StrictHostKeyChecking no" >> /etc/ssh/ssh_config
echo "Ciphers aes128-ctr,aes192-ctr,aes256-ctr,arcfour256,arcfour128,aes128-cbc,3des-cbc" >> /etc/ssh/ssh_config
echo "Tunnel no" >> /etc/ssh/ssh_config
echo "ServerAliveInterval 180" >> /etc/ssh/ssh_config

sed -i 's/$photon_cmdline/init=\/lib\/systemd\/systemd loglevel=3 ro console=tty1 console=ttyS0,115200n8 earlyprintk=ttyS0,115200 fsck.repair=yes rootdelay=300/' /boot/grub/grub.cfg
sed -i 's/Provisioning.Enabled=y/Provisioning.Enabled=n/g' /etc/waagent.conf
sed -i 's/Provisioning.UseCloudInit=n/Provisioning.UseCloudInit=y/g' /etc/waagent.conf
sed -i 's/ResourceDisk.Format=y/ResourceDisk.Format=n/g' /etc/waagent.conf


# Remove kernel symbols
rm /boot/system.map*

waagent -force -deprovision+user
export HISTSIZE=0
useradd -m -d /home/test test
usermod -aG sudo test
mkdir -p /home/test/.ssh
echo "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDKb6dU6WNdrKvhcxYvmP+Hr8EUzakpuFp1zxHFM6/0h38PGlI2EpitVoTBVP0DJiuMfJlR0o6WzYiNijdS07doJJryWEXoe/kAzIqGaew4jC45mjpbpdSv5PhMu95orPhLIrUqZ5htUtzwU1iWNiGQVEJ+c+8+xiTbNDqR/wWmqcLy6dK0YxpjpRQE/WTCvSvOrehfWrx5U+CRI1YE3HXi3Lz5vwKQ98Ez8kBIA/BTvXZVo+bb3OTKBIgWxf5gr0wyzCwRuLdHq9IUdjjOJqcNfzNjEgw9t4gZeohce5fllvFdSOe0DHEF9K5iiIzQsZMQ8+TtW45WbxHo4s2eHLmZ" > /home/test/.ssh/authorized_keys
echo "ALL            ALL = (ALL) NOPASSWD: ALL" >> /etc/sudoers
echo "test            ALL = (ALL) NOPASSWD: ALL" >> /etc/sudoers

