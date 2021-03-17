---
title:  Kickstart Support in Photon OS
weight: 2
---

Photon OS works with kickstart for unattended, automated installations. The kickstart configuration file can either reside in the CD-ROM attached to the host or be served through an HTTP server.

* [Kickstart Capabilities](#kickstart-capabilities)
* [Permitted JSON Fields](#permitted-json-fields)
* [Sample Configuration File](#sample-configuration-file)
* [Unattended Installation Through Kickstart](#unattended-installation-through-kickstart)


## Kickstart Capabilities

Photon OS supports the following configurations with kickstart:

* Setting the hostname
* Setting the password
* Setting the disk to install
* Selecting whether to install the full or the minimal version of Photon OS 
* Applying a post-installation script
* Adding public keys to allow the root account to log in through SSH

## Permitted JSON Fields

The following is a list of allowed JSON fields and their descriptions:

<table style="height: 170px;" border="1" width="250" cellspacing="0" cellpadding="10">
	<tbody>
	<tr>
	<td><b>Field</b></td>
	<td><b>Description</b></td>
	</tr>
	<tr>
	<td>hostname</td>
	<td>The host name as string. You can also specify the name in printf format. 
<p> The hostname must not start with a number or "-" and must be less than 64 characters.  
<p> Example: "photon-$((RANDOM%4096))"
</p></td>
	</tr>
	<tr>
	<td>password:
  <p>crypted: true/false
  <p>text: password text </td>
	<td> <b>crypted: true</b>: 
This indicates that the "text" field is already encrypted. In this case, the specified password is used as is for the root user.
<p> <b>crypted: false:</b>
This indicates that the "text" field is plain text. It is then encrypted and used to create the root user's password.
<p> <b>text</b>: Plain text or encrypted password.
</td>
	</tr>
	<tr>
	<td>disk</td>
	<td>Indicates the install disk.
<p> Example: /dev/sda </td>
	</tr>
	<tr>
	<td>partitions</td>
	<td>An array of partition definitions.
	<p><b>To create GPT partitions</b>
<p> Example:
<p>[
 <p>                       {"mountpoint": "/", "size": 0, "filesystem": "ext4"},
 <p>                       {"mountpoint": "/boot", "size": 128, "filesystem": "ext4"},
 <p>                      {"mountpoint": "/root", "size": 128, "filesystem": "ext4"},
 <p>                       {"size": 128, "filesystem": "swap"}
<p>]
<p><b>To create LVM partitions</b>
<p> Example:<p>[
                <p>{"mountpoint": "/", "size": 0, "filesystem": "ext4", "lvm":{"vg_name":"vg1", "lv_name":"rootfs"}},
               <p> {"mountpoint": "/boot", "size": 128, "filesystem": "ext4"},

                <p>{"mountpoint": "/root", "size": 128, "filesystem": "ext4","lvm":{"vg_name":"vg1", "lv_name":"root"}},

                <p>{"size": 128, "filesystem": "swap","lvm":{"vg_name":"vg2", "lv_name":"swap"}}
]
<p><b>Note</b>: Mounting '/boot' partition as lvm is not supported.
</td>
	</tr></tr>
	<tr>
	<td>packagelist_file</td>
	<td>Indicates the name of the file that contains the list of packages to install.
	<p>Example: { "packagelist_file": "packages_minimal.json" }
</td>
	</tr><tr>
	<td>additional_packages</td>
	<td>Specify an array of additional packages.
</td>
	</tr><tr>
	<td>install_linux_esx</td>
	<td>Specify a boolean value to use linux esx instead of generic linux.
</td>
	</tr><tr>
	<td>postinstall</td>
	<td>Specify an array of bash commands to execute after install. <p> See the example for partitions.
	<p>Example:
	{ "postinstall": [
			"#!/bin/sh",
			"echo \"Hello World\" > /etc/postinstall" ] }
</td>
	</tr><tr>
	<td>public_key</td>
	<td>Optional. <p>The public key that you require to install for password-less logins. <p> This key is created in authorized_keys in the .ssh directory.
</td>
</tr><tr>
	<td>additional_files</td>
	<td>Optional. <p>Contains a list of pairs {source file (or directory), destination file
	(or directory)} to copy to the target system. Source file
	(directory) will be looked up in "search_path" list.
	<p>Example: { "additional_files": [
		{"resizefs.sh": "/usr/local/bin/resizefs.sh"},
		{"resizefs.service": "/lib/systemd/system/resizefs.service"}]}
</td>
</tr><tr>
	<td>additional_rpms_path</td>
	<td>Optional. <p>Provide a path containing additional RPMS that are to be bundled into
	the image.
</td>
</tr><tr>
	<td>arch</td>
	<td>Optional. <p>Target system architecture. Should be set if target architecture is
	different from the host, for instance x86_64 machine building RPi
	image.
	Acceptable values are: "x86_64", "aarch64"
	Default value: autodetected host architecture
	<p>Example: { "arch": "aarch64" }
</td>
</tr><tr>
	<td>bootmode</td>
	<td>Optional. <p>Sets the boot type to support: EFI, BIOS or both.
	<p>Acceptable values are: bios, efi, dualboot
	<p><b>bios</b>
	<p>Adds special partition (very first) for first stage grub.
	<p><b>efi</b>
	<p>Adds ESP (Efi Special Partition), format is as FAT and copy there EFI binaries including grub.efi
	<p><b>dualboot</b>
	<p>Adds two extra partitions for "bios" and "efi" modes. This target will support both modes that can be switched in bios settings without extra actions in the OS.
	<p>Default value: "dualboot" for x86_64 and "efi" for aarch64
	<p>Example: { "bootmode": "bios" }
</td>
</tr><tr>
	<td>eject_cdrom</td>
	<td>Optional. <p>Ejects cdrom after installation completed if set to true.
	<p>Boolean: true or false
	<p>Default value: true
	<p>Example: { "eject_cdrom": false }
</td>
</tr><tr>
	<td>live</td>
	<td>Optional. <p>Should be set to flase if target system is not being run on
	host machine. When it set to false, installer will not add EFI boot
	entries, and will not generate unique machine-id.
	<p>Default value: false if "disk" is /dev/loop and true otherwise.
	<p>Example: { "live": false }
</td>
</tr><tr>
	<td>log_level</td>
	<td>Optional. <p>Set installer logging level.
	<p>Acceptable values are: <b>error</b>, <b>warning</b>, <b>info</b>, <b>debug</b>
	<p>Default value: </b>info</b>
	<p>Example: { "log_level": "debug" }
</td>
</tr><tr>
	<td>ostree</td>
	<td>Optional. <p>Atomic flavour of Photon OS.
        <p><b>default_repo</b>
        <p>(required)
                 <p>Define the type of repo data used for installing the OS
                 There are two type: <p>1. Default Repo(comes with ISO) <p>2. Custom Repo (Remote server)
                 <p>Boolean: true or false
                   <p>where true : Default Repo is selected
                         <p>false: Custom Repo is selected
                 <p>Default value: true
        Example: { "ostree": {"default_repo": true}}
        <p><b>repo_url</b> 
        <p>(Required, Only If Custom Repo is selected)
                 Supported Value: Valid "repo" URL of remote server where repo data exists
        <p><b>repo_ref</b>
        <p>(Required, Only If Custom Repo is selected)
                 Supported Value: Valid "ref" path which was mentioned for
                                  creation of Base Tree on remote server
        <p>Example: { "ostree": {
                              "default_repo": false,
                              "repo_url": "http://<ip>:<port>/repo",
                              "repo_ref": "photon/3.0/x86_64/minimal"
                             }
                 }
</td>
</tr><tr>
	<td>packages</td>
	<td>Optional if packagelist_file set. <p>Contains list of packages to install.
	<p>Example: { "packages": ["minimal", "linux", "initramfs"] }
</td>
</tr><tr>
	<td>partition_type</td>
	<td>Optional. <p>Set partition table type. Supported values are: gpt, msdos.
	<p>Default value: gpt
	<p>Example: { "partition_type": "msdos" }
</td>
</tr><tr>
	<td>network</td>
	<td>Optional. <p>Used to configure network on a live/installed system.
	<p><b>type</b>
	<p>required
	<p>String; must be one of dhcp/static/vlan. Indicates how the network is being configured.
	<p><b>hostname</b>
	<p>optional; when type == dhcp
	<p>String; DHCP client hostname
	<p><b>ip_addr</b>
	<p>required; when type == static
	<p>IP String; IP address to be configured
	<p><b>netmask</b>
	<p>required; when type == static
	<p>IP String; Netmask to be configured
	<p><b>gateway</b>
	<p>required; when type == static
	<p>IP String; Gateway IP address to be configured
	<p><b>nameserver</b>
	<p>required; when type == static
	<p>IP String; Name server IP address to be configured
	<p><b>vlan_id</b>
	<p>required; when type == vlan
	<p>ID String. (1-4094); VLAN ID number expressed as string
</td>
</tr><tr>
	<td>postinstallscripts</td>
	<td>Optional. <p>Contains list of scripts to run on the target after installation.
	Scripts will be looked up in "search_path" list.
	<p>Example: { "postinstallscripts": ["rpi3-custom-patch.sh"] }
</td>
</tr><tr>
	<td>search_path</td>
	<td>Optional. <p>List of directories to search for additional files and scripts.
	<p>Example: { "search_path": ["/home/user", "/tmp"] }
</td>
</tr><tr>
	<td>shadow_password</td>
	<td>Optional. <p>Contains encrypted root password.
	Short form of: { "password": {
				"crypted": true,
				"text": "encrypted password here"} }
</td>
</tr><tr>
	<td>ui</td>
	<td>Optional. <p>Installer will show progress status in the UI, if it set to true.
	Or logging output will be printed to console - default behavior.
	<p>Boolean: true or false
	<p>Default value: false
	<p>Example: { "ui": true }
</td>
	</tr>
	</tbody>
	</table>
	

## Sample Configuration File

Here is a sample kickstart configuration file:

```
{
    "hostname": "photon-machine",
    "password":
        {
            "crypted": false,
            "text": "changeme"
        },
    "disk": "/dev/sda",
    "partitions": [
                        {"mountpoint": "/", "size": 0, "filesystem": "ext4"},
                        {"mountpoint": "/boot", "size": 128, "filesystem": "ext4"},
                        {"mountpoint": "/root", "size": 128, "filesystem": "ext4"},
                        {"size": 128, "filesystem": "swap"}
                    ],
    "packagelist_file": "packages_minimal.json",
    "additional_packages": ["vim"],
    "postinstall": [
                		"#!/bin/sh",
                    	"echo \"Hello World\" > /etc/postinstall"
                   ],
    "public_key": "<ssh-key-here>",
    "install_linux_esx": false,
    "network": {
        "type": "dhcp"
    }    
}
```
##Installing Root Partition as LVM

In the kickstart file modify the **partitions** field to mount root partition as LVM.

For example:


```
"disk": "/dev/sda"
"partitions":[
                {"mountpoint": "/", "size": 0, "filesystem": "ext4", "lvm":{"vg_name":"vg1", "lv_name":"rootfs"}},
                {"mountpoint": "/boot", "size": 128, "filesystem": "ext4"},

                {"mountpoint": "/root", "size": 128, "filesystem": "ext4","lvm":{"vg_name":"vg1", "lv_name":"root"}},

                {"size": 128, "filesystem": "swap","lvm":{"vg_name":"vg2", "lv_name":"swap"}}
]

```
**Note**:

- vg_name : Volume Group Name
- lv_name : Logical Volume Name


In above example **rootfs**, **root** are logical volumes in the volume group **vg1** and **swap** is logical volume in volume group **vg2**, physical volumes are part of disk **/dev/sda**.

Multiple disks are also supported. For example:


```
"disk": "/dev/sda"
"partitions":[
                {"mountpoint": "/", "size": 0, "filesystem": "ext4", "lvm":{"vg_name":"vg1", "lv_name":"rootfs"}},
                {"mountpoint": "/boot", "size": 128, "filesystem": "ext4"},

                {"disk": "/dev/sdb", "mountpoint": "/root", "size": 128, "filesystem": "ext4","lvm":{"vg_name":"vg1", "lv_name":"root"}},

                {"size": 128, "filesystem": "swap","lvm":{"vg_name":"vg1", "lv_name":"swap"}}
]
```

If disk name is not specified, the physical volumes will be part of the default disk: **dev/sda**.
In above example **rootfs**,**root** and **swap** are logical volumes in volume group **vg1**, physical volumes are in the disk **/dev/sdb** and partitions are present in **/dev/sda**.

**Note**: Mounting **/boot** partition as LVM is not supported.

## Unattended Installation Through Kickstart

For an unattended installation, you pass the `ks=<config_file>` parameter to the kernel command. To pass the config file, there are two options: by providing it on the ISO or by serving it from an HTTP server. 

The syntax to pass the config-file to the kernel through the ISO takes the following form: 

    ks=cdrom:/<config_file_path>

Here is an example: 

    ks=cdrom:/isolinux/my_ks.cfg

The syntax to serve the config-file to the kernel from an HTTP server (NOTE: DO NOT use https:// here) takes the following form: 

    ks=http://<server>/<config_file_path>

## Building an ISO with a Kickstart Config File

Here's an example of how to add a kickstart config file to the Photon OS ISO by mounting the ISO on an Ubuntu machine and then rebuilding the ISO. The following example assumes you can adapt the sample kickstart configuration file that comes with the Photon OS ISO to your needs. You can obtain the Photon OS ISO for free from Bintray at the following URL: 

[https://packages.vmware.com/photon](https://packages.vmware.com/photon)

Once you have the ISO, mount it. 

    mkdir /tmp/photon-iso
    sudo mount photon.iso /tmp/photon-iso

Then copy the content of the ISO to a writable directory and push it into the directory stack: 

    mkdir /tmp/photon-ks-iso
    cp -r /tmp/photon-iso/* /tmp/photon-ks-iso/
    pushd /tmp/photon-ks-iso/

Next, copy the sample kickstart configuration file that comes with the Photon OS ISO and modify it to suit your needs. In the ISO, the sample kickstart config file appears in the `isolinux` directory and is named `sample_ks.cfg.` The name of the directory and the name of the file might be in all uppercase letters. 

    cp isolinux/sample_ks.cfg isolinux/my_ks.cfg
    nano isolinux/my_ks.cfg

With a copy of the sample kickstart config file open in nano, make the changes that you want. 

Now add a new item to the installation menu by modifying `isolinux/menu.cfg`:

    cat >> isolinux/menu.cfg << EOF
    label my_unattended
    	menu label ^My Unattended Install
    	menu default
    	kernel vmlinuz
    	append initrd=initrd.img root=/dev/ram0 loglevel=3 photon.media=cdrom
    EOF

Finally, rebuild the ISO so that it includes your kickstart config file: 

    mkisofs -R -l -L -D -b isolinux/isolinux.bin -c isolinux/boot.cat \
    		-no-emul-boot -boot-load-size 4 -boot-info-table -V "PHOTON_$(date +%Y%m%d)" \
    		. > <new_iso_path>.iso

    popd

