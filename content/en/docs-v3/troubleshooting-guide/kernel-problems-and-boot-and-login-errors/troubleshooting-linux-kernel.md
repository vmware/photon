---
title:  Linux Kernel
weight: 7
---

The Linux kernel is the main component of Photon OS and is the core interface between a computer’s hardware and its processes. It communicates between the two, managing resources as efficiently as possible.

##Kernel Flavours and Versions
The following list contains the different Linux kernel flavours available:

- `linux` - A generic kernel designed to run everywhere and support everything.
- `linux-esx` - Optimized to run only on VMware hypervisor (ESXi, WS, Fusion). It has minimal set of device drivers to support VMware virtual devices. `uname -r` displays `Linux` . For additional features switch to the generic flavour.
- `linux-secure` - Security hardened variant of the generic kernel. `uname -r` displays `-secure` suffix.
- `linux-rt` - This is a Photon Real Time kernel. `uname -r` displays `-rt` suffix.
- `linux-aws` - Optimized for AWS hypervisor kernel. `uname -r` displays `-aws` suffix.

To see the version of kernel installed, run the following command:
```
# rpm -qa | grep -e "^linux\(\|-esx\|-secure\|rt\|aws\)-[[:digit:]]"
linux-4.9.111-1.ph2.x86_64
linux-esx-4.9.111-1.ph2.x86_64
```

To see the version of the Kernel that is running currently, run the following command:
```
# uname -r
4.9.107-1.ph2-esx
```
From the output, you can see that the kernel running currently doesn't match the installer. This happens when linux-* rpms were updated but was not restarted. Restart is required.

##Configuration

To find the configurations of the installed Kernel, check the **/boot** directory by running the following command:
```
# ls /boot/config-*
config-4.9.111-1.ph2 config-4.9.111-1.ph2-esx
```
To get a copy of the kernel configuration (Not all flavours support this feature), run the `zcat /proc/config.gz` command.

##Boot Parameters and initrd
Several kernel flavors can be installed on the system, but only one is used during boot.
**/boot/photon.cfg** symlink points to the kernel which is used for boot.
```
# ls -l /boot/photon.cfg
lrwxrwxrwx 1 root root 23 Jun 12  2018 /boot/photon.cfg -> linux-4.9.111-1.ph2.cfg
```

Its contents can be checked by running the following command:
```
# cat /boot/photon.cfg

# GRUB Environment Block

photon_cmdline=init=/lib/systemd/systemd ro loglevel=3 quiet no-vmw-sta

photon_linux=vmlinuz-4.9.111-1.ph2

photon_initrd=initrd.img-4.9.111-1.ph2
```

Where:

- `photon_cmdline` - Kernel parameters. This list will be extended by values from **/boot/systemd.cfg** file and the values are hardcoded to **/boot/grub2/grub.cfg** file (For example: root=).
- `photon_linux` - Kernel image to boot.
- `photon_initrd` - Initrd to use at boot.

Parameters of the kernel loading currently can be found by running the `/proc/cmdline` command:
```
# cat /proc/cmdline

BOOT_IMAGE=/boot/vmlinuz-4.9.107-1.ph2-esx root=PARTUUID=29194d05-4a6e-4e0c-b1f4-5020e5e8472c net.ifnames=0 init=/lib/systemd/systemd ro loglevel=3 quiet no-vmw-sta
```

##Dmesg

To view message buffer of the kernel run the `dmesg` command.

##Sysctl State

To view a list of all active units run the `systemctl list-units` command.

##Kernel Statistics

The kernel statitics can be found by running the following commands:

- `procfs`
- `sysfs`
- `debugfs`

##Kernel Modules

To view the kernel log buffer run the `journalctl -k` command.

To view a list of available kernel modules run the `lsmod` command.

To view detailed information about all connected PCI buses run the `lspci` command.

