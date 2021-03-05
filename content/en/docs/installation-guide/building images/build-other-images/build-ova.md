---
title:  Building OVA image
weight: 2
---

Perform the following steps to build OVA on Ubuntu: 

1. Install the packages: 

    ```
    sudo apt-get -y install bison gawk g++ createrepo python-aptdaemon genisoimage texinfo python-requests libfuse-dev libssl-dev uuid-dev libreadline-dev kpartx git bc
    ```

2. Get Docker:

    ```
    wget -qO- https://get.docker.com/ | sh
    ```
 
3.  Install pip 
   
    ```
    sudo apt install python3-pip
    pip3 install git+https://github.com/vmware/photon-os-installer.git
    git clone https://github.com/vmware/photon.git
    
    
    
    If you encounter an error for LOCALE when you run these commands, then export the following variables in the terminal:
    
    
        export LC_ALL="en_US.UTF-8"
    `export LC_CTYPE="en_US.UTF-8"`


4.  Clone the Photon project:
  
        git clone https://github.com/vmware/photon.git
    `cd $HOME/workspaces/photon`

5. Download latest VDDK from below link:

   [https://my.vmware.com/web/vmware/downloads/details?downloadGroup=VDDK670&productId=742](https://my.vmware.com/web/vmware/downloads/details?downloadGroup=VDDK670&productId=742 "Link to VMware ovftool site")

6. Search for `VMware-ovftool` in the same site and install it.

   For example:

   ovftool downloaded file:

    `VMware-ovftool-4.3.0-13981069-lin.x86_64.bundle`

   Add exec permission and run it as sudo:

    `  $ chmod +x VMware-ovftool-4.3.0-13981069-lin.x86_64.bundle && sudo ./VMware-ovftool-4.3.0-13981069-lin.x86_64.bundle --eulas-agreed --required`

6. For VDDK, if the downloaded file is `VMware-vix-disklib-6.7.0-8173251.x86_64.tar.gz`, untar the downloaded tarball:

    `$ tar xf VMware-vix-disklib-6.7.0-8173251.x86_64.tar.gz`

7. Navigate to extracted directory.  

- Move the header files to /usr/include

    $ `sudo mv include/*.h /usr/include`


- Move the shared libs to /usr/lib/vmware
    `$ sudo mkdir -p /usr/lib/vmware && sudo mv lib64/* /usr/lib/vmware && sudo rm /usr/lib/vmware/libstdc++.so*`

8.  Export /usr/lib/vmware library path(only for current session). Do this step every time you try to build an ova image.

      `$ export LD_LIBRARY_PATH=/usr/lib/vmware`

7. Navigate to your intended Photon source repository and run the following command. 
    ```
    
    `sudo make image IMG_NAME=ova`

1. Make the image for OVA UEFI

 `sudo make image IMG_NAME=ova_uefi`
    
**Result**

This command first builds all RPMs corresponding to the SPEC files in your Photon repository and then builds a bootable ISO containing those RPMs.


The RPMs thus built are stored under `stage/RPMS/` directory within the repository, using the following directory hierarchy:

```
$HOME/workspaces/photon/stage/:
├──RPMS/:
    ├──noarch/*.noarch.rpm    [Architecture-independent RPMs]
    ├──x86_64/*.x86_64.rpm    [RPMs built for the x86-64 architecture]
    ├──aarch64/*.aarch64.rpm  [RPMs built for the aarch64 (ARM64) architecture]
```

The cloud image is created at `$HOME/workspaces/photon.
