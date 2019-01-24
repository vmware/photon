# Installing Photon OS on Dell Edge Gateway 300X

You can install Photon OS 3.0 on Dell Gateway 300X. You can download Photon OS as an ISO file and install it.

- [Prerequisites](#prerequisites)
- [Installing the ISO Image for Photon OS](#installing-the-iso-image-for-photon-os)

## Prerequisites

1.	Verify that you have the following resources:
    - Dell Edge Gateway 300x.
    - USB pen drive. Format the pen drive with FAT32 with at least 8 GB of space.
2.	Download the Photon OS ISO image from [Bintray](https://bintray.com/vmware/photon/).

## Installing the ISO Image for Photon OS

1.	Mount the ISO image.
    
    For example, run the following command on macOS:

    `hdiutil mount photon-3.0-ec12f2c.iso` 

    Use a similar command in other operating systems.

1. Copy the contents of the ISO image to a writable directory so that you can edit files.
    For example, run the following commands on macOS.
        
    ```
mkdir -p /tmp/photonUsb
    
    cp /Volumes/PHOTON_<timestamp>/* /tmp/photonUsb/
    ```

    where, `/Volumes/PHOTON_<timestamp>` is the directory where the ISO is mounted with the command in the step above.

1. Edit the `grub.cfg` file to use the kickstart config file:
    
    `cd /tmp/photonUsb`

    Add the below (highlighted) parameters to the linux cmd line in `boot/grub2/grub.cfg`
    
    `linux /isolinux/vmlinuz root=/dev/ram0 loglevel=3 photon.media=UUID=$photondisk` **`ks=cdrom:/isolinux/sample_ks.cfg console=ttyS0,115200n8`**

1. Edit the `isolinux/sample_ks.cfg`  as follows:

    - Change `"disk": "/dev/sda”,` to **`"disk": "/dev/mmcblk0",`**
    - Change `"echo \"Hello World\" > /etc/postinstall"` to **`"sed -i 's/PermitRootLogin no/PermitRootLogin yes/g' /etc/ssh/sshd_config"`**
    
1. Format the pen drive with FAT-32 and copy all the contents of `/tmp/photonUsb` to the pen drive. 

1. Create a `UsbInvocationScript.txt` file in the root of the pen drive with below content:

    ```
usb_disable_secure_boot noreset;
usb_one_time_boot usb nolog;
```

1. Insert the pen drive in the Dell Gateway 300X and power on the gateway. 
    
    Photon OS installs automatically.

1. After the installation is complete, insert a network cable into the ethernet port and find the IP address corresponding to the MAC address of the Dell Gateway 3000X ethernet port through the DHCP Server or a network analyzer. The MAC address is available on the Dell Gateway 3000X.

1. You can then use `ssh` to access the gateway with the above IP address.





