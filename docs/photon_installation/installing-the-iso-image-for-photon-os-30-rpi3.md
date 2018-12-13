# Installing Photon OS on Raspberry Pi 3

You can get Photon OS up and running on an RPi3 board, by flashing the Photon RPi3 image onto the board's SD card. 


- [Flash Photon OS on Raspberry Pi 3](#flash-photon-os-on-raspberry-pi-3)
- [Boot Photon OS on Raspberry Pi 3](#boot-photon-os-on-raspberry-pi-3)
- [Update login credentials](#update-login-credentials)


## Flash Photon OS on Raspberry Pi 3

After you have downloaded the Photon RPi3 image with the file extension `.raw.xz`, you can choose one of the methods below to flash it onto the RPi3 SD card.

1. **Flash Photon to RPi3 using Etcher**
    
    - Install Etcher [https://etcher.io/](https://etcher.io/), which is a utility to flash SD cards attached to your host computer.
    - Plug the RPi3 SD card into your host computer's SD card reader.
    - Perform the following steps on the Etcher GUI: **Select image** -> **Select drive** -> **Flash**, by selecting the Photon OS RPi3 as image and the RPi3 SD card as drive.

2. **Flash Photon to RPi3 using Linux CLI**
   
    - If you have Linux running on your host computer, install the `xz` package, which provides the `xz` compression utility and related tools, from your distribution package manager.
    - Plug the RPi3's SD card into your host computer's SD card reader.
    - Identify the device file under `/dev` that refers to the RPi3 SD card. For example, `/dev/sdc`. This file path is used to flash the Photon image onto the RPi3 in the next step.
    
        **Note**: Make sure that you are flashing to the device file that refers to your RPi3 SD card. Running the below command with an incorrect device file will overwrite that device without warning and might result in a corrupted disk. The device file '/dev/sdc` is an example and might not be the device file in your case. 
        
    - Run the following command to flash Photon onto th RPi3 SD card:
        
        `xzcat <photon-rpi3-image.raw.xz> | sudo dd of=/dev/sdc bs=4M conv=fsync`

## Boot Photon OS on Raspberry Pi 3

After you flash Photon OS successfully onto the RPi3 SD card, eject the card from your host computer and plug it back into the RPi3 board.
	    
When you power on the Raspberry Pi 3, it boots with Photon OS.
	    
After the splash screen, Photon OS prompts you to log in.

## Update login credentials

The Photon OS RPi3 image is configured with a default password. However, all Photon OS instances that are created using this image will require an immediate password change upon login. The default account credentials are:
	    
 - Username: ``root`` 
 - Password: ``changeme``
	    
After you provide these credentials, Photon OS prompts you to create a new password and type it a second time to verify it. Photon OS does not allow common dictionary words for the root password. When you are logged in, you will see the shell prompt.
    
You can now run `tdnf list` to view all the ARM packages that you can install on Photon OS.

