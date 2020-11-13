#Network PXE Boot

Photon supports pxe boot over netwrok, this is describe how you can setup a PXE boot server to install Photon.

#Server Setup

To setup PXE server you will need to have:
* DHCP server to allow hosts to get an IP address.
* TFTP server which is file transfer protocol which is similar to FTP with no authintication.
* Optionally http server, this http serevr is going to serve the RPMs yum repo, or you can use the official Photon repo on https://packages.vmware.com/photon/1.0. Also this http serevr can be used if you want to provide kickstart config for unattended installation.

Setting up server instruction is based on an Ubuntu 14.04 machine assuming that it has an static IP adderess `172.16.78.134`.

##DHCP Setup
* Intall dhcp server
```
  sudo apt-get install isc-dhcp-server
```
* Edit ethernet interface in `/etc/default/isc-dhcp-server` to `INTERFACES="eth0"`
* Edit dhcp configuration in `/etc/dhcp/dhcpd.conf`, will allow machines to boot and get IP address via DHCP in the range `172.16.78.230 - 172.16.78.250`
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
* Restart dhcp server
```
  sudo service isc-dhcp-server restart
```

##TFTP Setup
* Install TFTP server
```
  sudo apt-get install tftpd-hpa
```
* Enable boot service, and restrat the service
```
  sudo update-inetd --enable BOOT
  sudo service tftpd-hpa restart
```
##Optional: http server setup
This is step is only needed if:
* Planning to serve the ks config file through this server, please refer to [Kickstart support](kickstart.md) for more details.
* Serving your local yum repo.
You can install apache http web server
```
sudo apt-get install apache2
```
Mount the photon iso to get the RPMS repo and sample ks config file.
```
mkdir /mnt/photon-iso
sudo mount <photon_iso> /mnt/photon-iso/
```
Copy the RPMS repo.
```
cp -r /mnt/photon-iso/RPMS /var/www/html/
```
To support ks, may be you can copy the sample config from the iso and editing it, please refer to [Kickstart support](kickstart.md) for more details.
```
cp /mnt/photon-iso/isolinux/sample_ks.cfg /var/www/html/my_ks.cfg
```

##PXE boot files setup
* Mount photon.iso to get linux and initrd images
```
mkdir /mnt/photon-iso
sudo mount <photon_iso> /mnt/photon-iso/
```
* Setting the PXE boot files
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
* Update repo param to point to http yum repo, you may pass official photon https://packages.vmware.com/photon/1.0 repo.
```
sed -i "s/append/append repo=http:\/\/172.16.78.134\/RPMS/g" menu.cfg
popd
```
* Optionally, you can add your ks config file, please refer [Kickstart support](kickstart.md) for more details.

