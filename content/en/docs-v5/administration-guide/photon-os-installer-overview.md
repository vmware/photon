---
title:  Photon OS Installer Overview
weight: 17
---

The Photon OS Installer is an initiative that aims to separate out installer source code from the Photon project and use it as a python library. You can use this Photon OS Installer project to create a photon-installer binary that can install Photon OS when invoked with the appropriate arguments.


## Features

You can use the Photon OS Installer to perform the following tasks:

- Generate Photon Installer executable
- Create Photon Images (ISO, GCE, AMI, AZURE, OVA, and so on)
- Make Photon Installer Source code installable through  the pip interface and use it as a python library.


## Dependencies

The Photon OS installer has the following dependencies:

**Build Dependecies:**

- python3
- python3-pyinstaller 
- python3-setuptools
- python3-devel
- python3-requests
- python3-cracklib
- python3-curses


**Run time dependecies:**

- dosfstools
- efibootmgr
- glibc
- gptfdisk
- grub2
- kpartx
- lvm2
- zlib
- cdrkit
- findutils

**Note**: If the architecture is x86, then we need to add `grub2-pc` also in runtime dependency.


## Building from source

To build the Photon OS Installer executable on Photon OS, run the following commands:

```
➜  ~ tdnf install -y python3 python3-setuptools python3-pyinstaller
➜  ~ git clone https://github.com/vmware/photon-os-installer.git
➜  ~ cd photon-os-installer
➜  ~ pyinstaller --onefile photon-installer.spec
```   

To build the Photon Installer executable on other distros, run the following commands:

```
➜  ~ pip3 install setuptools pyinstaller
➜  ~ git clone https://github.com/vmware/photon-os-installer.git
➜  ~ cd photon-os-installer
➜  ~ pyinstaller --onefile photon-installer.spec
```   
You can find the generated executable in the dist directory created.

Presently, you can build the following images with the Photon OS Installer:

|x86_64	|	arm64	|
|-------|-----------|
|iso	|	iso		|
ova		|	ova		|
ova_uefi|	ova_uefi |
minimal-iso	|	|
rt-iso	|	|	|
ami		|	|	|
gce		|	|	|
azure	|	|	|
rpi3	|	|	|


To build Photon Cloud images using Photon OS Installer, run the following commands:

```
➜  ~ pip3 install git+https://github.com/vmware/photon-os-installer.git
➜  ~ git clone https://github.com/vmware/photon.git
➜  ~ cd photon
➜  ~ make image IMG_NAME=ami
```   


To use Photon OS Installer as a python library, run the following commands:

```
import photon_installer
from photon_installer.installer import Installer
import json
with open('path_to_file/config.json') as f:
    install_config = json.load(f)
installer = Installer(working_directory='/root/photon/stage/ova', repo_paths='/root/photon/stage/RPMS', log_path='/root/photon/stage/LOGS')
installer.configure(install_config)
installer.execute()
```    

You can refer to the sample installation configuration files on the following page: [Sample Kickstart Files](https://github.com/vmware/photon-os-installer/blob/master/sample_ks/sample_ks.cfg)


Developers or contributors can refer to the Photon OS Installer project here: [Photo OS Installer](https://github.com/vmware/photon-os-installer/tree/master)