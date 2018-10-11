# Kickstart Support in Photon OS

Photon OS works with kickstart for unattended, automated installations. The kickstart configuration file can either reside in the CD-ROM attached to the host or be served through an HTTP server.

## Kickstart Capabilities

Photon OS supports the following configurations with kickstart:

* Setting the hostname
* Setting the password
* Setting the disk to install
* Selecting whether to install the full or the minimal version of Photon OS 
* Applying a post-installation script
* Adding public keys to allow the root account to log in through SSH

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

