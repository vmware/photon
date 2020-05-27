#!/bin/bash

cd /lib/systemd/system/multi-user.target.wants/

ln -s ../docker.service docker.service
cd /

echo "127.0.0.1 localhost" >> /etc/hosts

echo "DNS=169.254.169.253" >> /etc/systemd/resolved.conf
echo "Domains=ec2.internal" >> /etc/systemd/network/99-dhcp-en.network

# Add a DHCP section, but comment out the MTU setting that enables
# jumbo frames (9001 byte MTU) on AWS. Users who have the right
# overall setup (eg: who have configured the necessary ICMP rules in
# their security group to handle large MTUs correctly for
# internet-bound traffic) can then choose to enable jumbo frames on
# the system by simply uncommenting this line.
echo -e "\n[DHCP]\n#UseMTU=true" >> /etc/systemd/network/99-dhcp-en.network

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
echo "HostbasedAuthentication no" >> /etc/ssh/ssh_config
echo "StrictHostKeyChecking no" >> /etc/ssh/ssh_config
echo "Ciphers aes128-ctr,aes192-ctr,aes256-ctr,arcfour256,arcfour128,aes128-cbc,3des-cbc" >> /etc/ssh/ssh_config
echo "Tunnel no" >> /etc/ssh/ssh_config
echo "ServerAliveInterval 420" >> /etc/ssh/ssh_config

sed -i 's/net.ifnames=0//' /boot/grub/grub.cfg
sed -i 's/$photon_cmdline/init=\/lib\/systemd\/systemd loglevel=3 ro console=ttyS0 earlyprintk=ttyS0 nvme_core.io_timeout=4294967295/' /boot/grub/grub.cfg

# Disable loading/unloading of modules
#echo "kernel.modules_disabled = 1" > /etc/sysctl.d/modules_disabled.conf

# Remove kernel symbols
rm -f /boot/System.map*
