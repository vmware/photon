# Network PXE Boot

Photon OS supports the Preboot Execution Environment, or PXE, over a network connection. This document describes how to set up a PXE boot server to install Photon OS.

# Server Setup

To set up a PXE server, you will need to have the following:

* A DHCP server to allow hosts to get an IP address.
* A TFTP server, which is a file transfer protocol similar to FTP with no authentication.
* Optionally, an HTTP server. The HTTP server will serve the RPMs yum repo, or you can use the official Photon OS repo on Bintray. Also, this HTTP server can be used if you want to provide a kickstart config for unattended installation.

The instructions to set up the servers assume you have an Ubuntu 14.04 machine with a static IP address of `172.16.78.134`.

## DHCP Setup
* Install the DHCP server:
```
  sudo apt-get install isc-dhcp-server
```
* Edit the Ethernet interface in `/etc/default/isc-dhcp-server` to `INTERFACES="eth0"`
* Edit the DHCP configuration in `/etc/dhcp/dhcpd.conf` to allow machines to boot and get an IP address via DHCP in the range `172.16.78.230 - 172.16.78.250`
```
  subnet 172.16.78.0 netmask 255.255.255.0 {
    range 172.16.78.230 172.16.78.250;
    option subnet-mask 255.255.255.0;
    option routers 172.16.78.134;
    option broadcast-address 172.16.78.255;
    filename "pxelinux.0";
    next-server 172.16.78.134;
  }

```
* Restart the DHCP server: 
```
  sudo service isc-dhcp-server restart
```

## TFTP Setup
* Install the TFTP server:
```
  sudo apt-get install tftpd-hpa
```
* Enable the boot service and restart the service:
```
  sudo update-inetd --enable BOOT
  sudo service tftpd-hpa restart
```

## Optional: HTTP server setup

This step is only needed if you are planning to serve the ks (kickstart) config file through this server; refer to [Kickstart support](kickstart.md) for details.
* Serving your local yum repo.
You can install apache http web server
```
sudo apt-get install apache2
```
Mount the Photon iso to get the RPMS repo and sample ks config file.
```
mkdir /mnt/photon-iso
sudo mount <photon_iso> /mnt/photon-iso/
```
Copy the RPMS repo.
```
cp -r /mnt/photon-iso/RPMS /var/www/html/
```
To support ks, you can copy the sample config file from the iso and edit it; refer to [Kickstart support](kickstart.md) for details.
```
cp /mnt/photon-iso/isolinux/sample_ks.cfg /var/www/html/my_ks.cfg
```

## PXE boot files setup
* Mount photon.iso to get Linux and initrd images:
```
mkdir /mnt/photon-iso
sudo mount <photon_iso> /mnt/photon-iso/
```
* Setting the PXE boot files:
```
wget https://www.kernel.org/pub/linux/utils/boot/syslinux/syslinux-6.03.tar.gz
tar -xvf syslinux-6.03.tar.gz
pushd /var/lib/tftpboot
cp -r /mnt/photon-iso/isolinux/* .
cp ~/syslinux-6.03/bios/com32/elflink/ldlinux/ldlinux.c32 .
cp ~/syslinux-6.03/bios/com32/lib/libcom32.c32 .
cp ~/syslinux-6.03/bios/com32/libutil/libutil.c32 .
cp ~/syslinux-6.03/bios/com32/menu/vesamenu.c32 .
cp ~/syslinux-6.03/bios/core/pxelinux.0 .
mkdir pxelinux.cfg
mv isolinux.cfg pxelinux.cfg/default
```
* Update repo param to point to http yum repo; you may pass official photon bintray repo.
```
sed -i "s/append/append repo=http:\/\/172.16.78.134\/RPMS/g" menu.cfg
popd
```
* Optionally, you can add your ks config file; see [Kickstart support](kickstart.md) for details.

