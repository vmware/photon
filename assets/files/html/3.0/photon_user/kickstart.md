# Kickstart Support in Photon OS

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
	<td>Indicates the install disk 
<p> Example: /dev/sda </td>
	</tr>
	<tr>
	<td>partitions</td>
	<td>An array of partition definitions.
<p> Example:
<p>[
 <p>                       {"mountpoint": "/", "size": 0, "filesystem": "ext4"},
 <p>                       {"mountpoint": "/boot", "size": 128, "filesystem": "ext4"},
 <p>                      {"mountpoint": "/root", "size": 128, "filesystem": "ext4"},
 <p>                       {"size": 128, "filesystem": "swap"}
<p>]</td>
	</tr></tr>
	<tr>
	<td>packagelist_file</td>
	<td>Indicates the name of the file that contains the list of packages to install.
</td>
	</tr><tr>
	<td>additional_packages</td>
	<td>Specify an array of additional packages.
</td>
	</tr><tr>
	<td>type</td>
	<td>Specify the type of package. Specify "full", "minimal" or "micro". 
</td>
	</tr><tr>
	<td>install_linux_esx</td>
	<td>Specify a boolean value to use linux esx instead of generic linux. 
</td>
	</tr><tr>
	<td>type</td>
	<td>Specify the type of package. 
<p> Specify "full", "minimal" or "micro". 
</td>
	</tr><tr>
	<td>postinstall</td>
	<td>Specify an array of bash commands to execute after install. <p> See the example for partitions.
</td>
	</tr><tr>
	<td>public_key</td>
	<td>Optional. <p>The public key that you require to install for password-less logins. <p> This key is created in authorized_keys in the .ssh directory.
</td>
	</tr>
	</tbody>
	</table>
	

  
## Sample Configuration File

Here is a sample kickstart configuration file:

```
{
    "hostname": "<hostname>",
    "password": 
        {
            "crypted": <true|false>,
            "text": "<password, either plain text or encrypted>"
        },
    "disk": "/dev/sda",
    "type": "minimal",
    "postinstall": [
                    "#!/bin/sh",
                    "echo \"Hello World\" > /etc/postinstall"
                   ],
    "public_key": "<public_key>"
}
```

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

[https://bintray.com/vmware/photon](https://bintray.com/vmware/photon)

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
    	kernel vmlinuz
    	append initrd=initrd.img root=/dev/ram0 ks=cdrom:/isolinux/my_ks.cfg loglevel=3
    EOF

Finally, rebuild the ISO so that it includes your kickstart config file: 

    mkisofs -R -l -L -D -b isolinux/isolinux.bin -c isolinux/boot.cat \
    		-no-emul-boot -boot-load-size 4 -boot-info-table -V "PHOTON_$(date +%Y%m%d)" \
    		. > <new_iso_path>.iso

    popd

