---
title:  Kickstart Support in Photon OS
weight: 2
---

Photon OS works with kickstart for unattended and automated installations. The kickstart configuration file can be served through an HTTP server. You can also provide the kickstart configuration file through a secondary device or a CD-ROM attached to the host. 

Kickstart also allows you to configure the installer and deploy virtual machines.

* [Ways to Provide Kickstart File](#ways-to-provide-kickstart-file)
* [Kickstart Capabilities](#kickstart-capabilities)
* [Sample Configuration File](#sample-configuration-file)
* [Unattended Installation Through Kickstart](#unattended-installation-through-kickstart)

## Ways to Provide Kickstart File

You can provide the path to the kickstart file in the following way:

### Remote kickstart

To provide a remote path for the kickstart file, use the following format:

```
ks=http://<kickstart-link>
```

### Kickstart from CD-ROM attached with ISO

To provide a path for the kickstart file in a CD-ROM with ISO, use the following format:

```
ks=cdrom:/isolinux/sample_ks.cfg
```

### Secondary Device Kickstart

To provide a secondary device path for the kickstart file, use the following format:

```
ks=<device-path>:<path-referential-to-device>
Example:
ks=/dev/sr1:/isolinux/sample_ks.cfg
```


## Kickstart Capabilities

On Photon OS, you can configure many settings such as the hostname, password, disk to install, post installation script, and so on. 

To find out more about the Kickstart capabilities and the permitted JSON parameters in Kickstart, see the following page: [Kickstart Features](https://github.com/vmware/photon-os-installer/blob/master./ks_config.md)


## Sample Configuration File

Example kickstart configuration file:

```json
{
    "hostname": "photon-machine",
    "password":
        {
            "crypted": false,
            "text": "changeme"
        },
    "disk": "/dev/sda",
    "partitions":[
		{
			"mountpoint":"/",
			"size":0,
			"filesystem":"ext4"
		},
		{
			"mountpoint":"/boot",
			"size":128,
			"filesystem":"ext4"
		},
		{
			"mountpoint":"/root",
			"size":128,
			"filesystem":"ext4"
		},
		{
			"size":128,
			"filesystem":"swap"
		}
		],
	"bootmode": "bios",
    "packagelist_file": "packages_minimal.json",
    "additional_packages": [
		"vim"
		],
    "postinstall": [
		"#!/bin/sh",
        "echo \"Hello World\" > /etc/postinstall"
        ],
    "public_key": "<ssh-key-here>",
    "linux_flavor": "linux",
    "network": {
        "type": "dhcp"
    }    
}
```


To see more such sample Kickstart configuration files, see the following page: [Kickstart Sample Configuration Files](https://github.com/vmware/photon-os-installer/tree/master/sample_ks)


## Installing Root Partition as LVM

In the kickstart file modify the **partitions** field to mount root partition as LVM.

For example:

```json
"disk":"/dev/sda"
"partitions":[
   {
      "mountpoint":"/",
      "size":0,
      "filesystem":"ext4",
      "lvm":{
         "vg_name":"vg1",
         "lv_name":"rootfs"
      }
   },
   {
      "mountpoint":"/boot",
      "size":128,
      "filesystem":"ext4"
   },
   {
      "mountpoint":"/root",
      "size":128,
      "filesystem":"ext4",
      "lvm":{
         "vg_name":"vg1",
         "lv_name":"root"
      }
   },
   {
      "size":128,
      "filesystem":"swap",
      "lvm":{
         "vg_name":"vg2",
         "lv_name":"swap"
      }
   }
]
```
**Note**:

- vg_name : Volume Group Name
- lv_name : Logical Volume Name

In above example **rootfs**, **root** are logical volumes in the volume group **vg1** and **swap** is logical volume in volume group **vg2**, physical volumes are part of disk **/dev/sda**.

Multiple disks are also supported. For example:

```json
"disk": "/dev/sda"
"partitions":[
   {
      "mountpoint":"/",
      "size":0,
      "filesystem":"ext4",
      "lvm":{
         "vg_name":"vg1",
         "lv_name":"rootfs"
      }
   },
   {
      "mountpoint":"/boot",
      "size":128,
      "filesystem":"ext4"
   },
   {
      "disk":"/dev/sdb",
      "mountpoint":"/root",
      "size":128,
      "filesystem":"ext4",
      "lvm":{
         "vg_name":"vg1",
         "lv_name":"root"
      }
   },
   {
      "size":128,
      "filesystem":"swap",
      "lvm":{
         "vg_name":"vg1",
         "lv_name":"swap"
      }
   }
]
```

If disk name is not specified, the physical volumes will be part of the default disk: **dev/sda**.

In above example **rootfs**,**root** and **swap** are logical volumes in volume group **vg1**, physical volumes are in the disk **/dev/sdb** and partitions are present in **/dev/sda**.

**Note**: Mounting **/boot** partition as LVM is not supported.


## Unattended Installation Through Kickstart

For an unattended installation, you pass the `ks=<config_file>` parameter to the kernel command. To pass the config file, there are three options: 

1. Provide it in the ISO through a CD-ROM attached to the host.
2. Provide it in the ISO through a specified secondary device.
3. Serving it from an HTTP server. 

The syntax to pass the configuration file to the kernel through the CD-ROM takes the following form:

```console
ks=cdrom:/<config_file_path>
```

For example: 

```console
ks=cdrom:/isolinux/ks.cfg
```

The syntax to pass the configuration file to the kernel through a secondary device takes the following form:

```console
ks=<device-path>:<path-referential-to-device>
```

For example:

```console
ks=/dev/sr1:/isolinux/sample_ks.cfg
```

The syntax to serve the configuration file to the kernel from a HTTPS server takes the following form: 

```console
ks=https://<server>/<config_file_path>
```

To use HTTP path or self-signed HTTPS path, you have to enable `insecure_installation` by using insecure_installation=1 along with defining the ks path. The kernel command line argument, `insecure_installation`, acts as a flag that user can set to 1 to allow some operations that are not normally allowed due to security concerns. This is disabled by default and it is up to the user to the ensure security when this options is enabled.
  
HTTP example:  

```console
ks=http://<server>/<config_file_path> insecure_installation=1
```

HTTPS (self-signed) example: 

```console
ks=https://<server>/<config_file_path> insecure_installation=1
```

## Building an ISO with a Kickstart Config File

Here's an example of how to add a kickstart config file to the Photon OS ISO by mounting the ISO on an Ubuntu machine and then rebuilding the ISO. The following example assumes you can adapt the sample kickstart configuration file that comes with the Photon OS ISO to your needs. You can obtain the Photon OS ISO for free from VMware at the following URL: 

[https://packages.vmware.com/photon](https://packages.vmware.com/photon)

Once you have the ISO, mount it. 

```console
mkdir /tmp/photon-iso
sudo mount photon.iso /tmp/photon-iso
```

Then copy the content of the ISO to a writable directory and push it into the directory stack: 

```console
mkdir /tmp/photon-ks-iso
cp -r /tmp/photon-iso/* /tmp/photon-ks-iso/
pushd /tmp/photon-ks-iso/
```

Next, copy the sample kickstart configuration file that comes with the Photon OS ISO and modify it to suit your needs. In the ISO, the sample kickstart config file appears in the `isolinux` directory and is named `sample_ks.cfg.` The name of the directory and the name of the file might be in all uppercase letters. 

```console
cp isolinux/sample_ks.cfg isolinux/my_ks.cfg
nano isolinux/my_ks.cfg
```

With a copy of the sample kickstart config file open in nano, make the changes that you want. 

Now add a new item to the installation menu by modifying `isolinux/menu.cfg` and `boot/grub2/grub.cfg`:

```console
cat >> isolinux/menu.cfg << EOF
label my_unattended
	menu label ^My Unattended Install
	menu default
	kernel vmlinuz
	append initrd=initrd.img root=/dev/ram0 ks=<ks_path>/my_ks.cfg loglevel=3 photon.media=cdrom
EOF


cat >> boot/grub2/grub.cfg << EOF
set default=0
set timeout=3
loadfont ascii
set gfxmode="1024x768"
gfxpayload=keep
set theme=/boot/grub2/themes/photon/theme.txt
terminal_output gfxterm
probe -s photondisk -u ($root)

menuentry "Install" {
    linux /isolinux/vmlinuz root=/dev/ram0 ks=<ks_path>/my_ks.cfg loglevel=3 photon.media=UUID=$photondisk
    initrd /isolinux/initrd.img
}
EOF 
```
Following is an example of the ks path:

	`ks_path=cdrom:/isolinux`

**Note:** You can specify any mount media through which you want to boot Photon OS. To specify the mount media, specify the path of the mount media device in the `photon.media` field. You can specify the path as shown in the following syntax:

```console
photon.media=/dev/<path of the Photon OS ISO>
```

Finally, rebuild the ISO so that it includes your kickstart config file: 

```console
mkisofs -R -l -L -D -b isolinux/isolinux.bin -c isolinux/boot.cat \
                -no-emul-boot -boot-load-size 4 -boot-info-table \
                -eltorito-alt-boot --eltorito-boot boot/grub2/efiboot.img -no-emul-boot \
                -V "PHOTON_$(date +%Y%m%d)" . > <new_iso_path>.iso


popd
```