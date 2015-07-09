#Kickstart Support

Photon supports kickstart for unattended installations, the kickstart config file can reside in either the CD attached to the host or served through an http server.

##Kickstart capabilities

Photon supports the following configurations:
* Setting hostname
* Setting password
* Setting disk to install
* Choose Photon flavor to install (minimal or full)
* Apply post installation script
* Add public keys, this will allow root ssh login.

Here is a sample configuration file:

```
{
    "hostname": "<hostname>",
    "password": 
        {
            "crypted": <true|false>,
            "text": "<password whether it's plain text or encrypted>"
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

##Unattended installation though kickstart
To have unattended installation, you have to pass `ks=<config_file>` parameter to the kernel command. The config file should be either:
* on the iso `ks=cdrom:\<config_file_path>`,
* or served over http server `ks=http://<server>/<config_file_path>`

##Building an iso with your kickstart config file
Given a recent build photon.iso
```
# mount the photon.iso
mkdir /tmp/photon-iso
sudo mount photon.iso /tmp/photon-iso

#copy the content of the iso to a writable folder
mkdir /tmp/photon-ks-iso
cp -r /tmp/photon-iso/* /tmp/photon-ks-iso/

pushd /tmp/photon-ks-iso/

# write your ks config file
cp isolinux/sample_ks.cfg isolinux/my_ks.cfg
vim isolinux/my_ks.cfg

# add new item in the installation menu by modyfing isolinux/menu.cfg
cat >> isolinux/menu.cfg << EOF
label my_unattended
	menu label ^My Unattended Install
	kernel vmlinuz
	append initrd=initrd.img root=/dev/ram0 ks=cdrom:/isolinux/my_ks.cfg loglevel=3
EOF

# rebuild the iso
mkisofs -R -l -L -D -b isolinux/isolinux.bin -c isolinux/boot.cat \
		-no-emul-boot -boot-load-size 4 -boot-info-table -V "PHOTON_$(date +%Y%m%d)" \
		. > <new_iso_path>.iso

popd
```
