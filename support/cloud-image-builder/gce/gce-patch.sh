#!/bin/bash

cd /lib/systemd/system/multi-user.target.wants/

# Create links in multi-user.target to auto-start these scripts and services.
for i in ../google*; do  ln -s $i `basename $i`; done
# for i in ../kube*; do  ln -s $i `basename $i`; done

ln -s ../ntpd.service ntpd.service
ln -s ../docker.service docker.service
ln -s ../eth0.service eth0.service


# Update /etc/hosts file with GCE values
echo "169.254.169.254 metadata.google.internal metadata" >> /etc/hosts

# Remove all servers from ntp.conf and add Google's ntp server.
sed -i -e "/server/d" /etc/ntp.conf
echo "server 169.254.169.254" >> /etc/ntp.conf


# Set UTC timezone
ln -sf /usr/share/zoneinfo/UTC /etc/localtime

# Update /etc/resolv.conf

rm /etc/resolv.conf

echo "nameserver 169.254.169.254" >> /etc/resolv.conf
echo "nameserver 8.8.8.8" >> /etc/resolv.conf


# Remove ssh host keys and add script to regenerate them at boot time.

rm -f /etc/ssh/ssh_host_*

printf "GOOGLE\n" > /etc/ssh/sshd_not_to_be_run

sudo groupadd docker
sudo groupadd sudo

rm /root/.ssh/authorized_keys   

# ssh server config
# Override old values
rm /etc/ssh/sshd_config

echo "AuthorizedKeysFile .ssh/authorized_keys" >> /etc/ssh/sshd_config
echo "PubkeyAuthentication yes" >> /etc/ssh/sshd_config
echo "UsePrivilegeSeparation sandbox" >> /etc/ssh/sshd_config
echo "PasswordAuthentication no" >> /etc/ssh/sshd_config
echo "PermitRootLogin no" >> /etc/ssh/sshd_config
echo "PermitTunnel no" >> /etc/ssh/sshd_config
echo "AllowTcpForwarding yes" >> /etc/ssh/sshd_config
echo "X11Forwarding no" >> /etc/ssh/sshd_config
echo "ClientAliveInterval 420" >> /etc/ssh/sshd_config
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

# Disable root login
usermod -L root

#disable ipv6
echo "net.ipv6.conf.all.disable_ipv6 = 1" > /etc/sysctl.d/ipv6-disable.conf

# Disable loading/unloading of modules
echo 1 > /proc/sys/kernel/modules_disabled

# Remove kernel symbols
rm /boot/system.map*

cat > /usr/bin/gcloud << "EOF"
docker inspect google/cloud-sdk &> /dev/null

if [ $? == 1 ]; then
        docker pull google/cloud-sdk &> /dev/null
fi

docker run --rm -it google/cloud-sdk gcloud $*
EOF

cat > /usr/bin/gsutil << "EOF"
docker inspect google/cloud-sdk &> /dev/null

if [ $? == 1 ]; then
        docker pull google/cloud-sdk &> /dev/null
fi

docker run --rm -it google/cloud-sdk gsutil $*
EOF

chmod a+x /usr/bin/gcloud
chmod a+x /usr/bin/gsutil
