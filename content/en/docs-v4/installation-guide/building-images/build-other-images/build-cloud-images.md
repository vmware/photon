```
title:  Building Cloud Images
weight: 1
---

Perform the following steps to build the cloud images on Ubuntu: 

1. Install the packages: 

    ```bash
    sudo apt-get -y install bison gawk g++ createrepo python-aptdaemon genisoimage texinfo python-requests libfuse-dev libssl-dev uuid-dev libreadline-dev kpartx git bc
    ```

2. Get Docker:

    ```bash
    wget -qO- https://get.docker.com/ | sh
    ```
 
3.  Install pip 
   
    ```bash
    sudo apt install python3-pip
    ```

    ```bash
    pip3 install git+https://github.com/vmware/photon-os-installer.git
    ```

    ```bash
    git clone https://github.com/vmware/photon.git
    ```
    
    
   If you encounter an error for LOCALE when you run these commands, then export the following variables in the terminal:
    
   
    ```bash
    export LC_ALL="en_US.UTF-8"
    ```

    ```bash
    export LC_CTYPE="en_US.UTF-8"
    ```

3.  Clone the Photon project:
   
    ```bash
    git clone https://github.com/vmware/photon.git
    ```

    ```bash
    cd $HOME/workspaces/photon
    ```

4. Make the cloud image for AMI. 

    ```bash
    sudo make image IMG_NAME=ami
    ```

4. Make the cloud image for Azure. 
  
    ```bash
    sudo make image IMG_NAME=azure
    ```

4. Make the cloud image for GCE. 
    
    ```bash
    sudo make image IMG_NAME=gce
    ```
    
    
**Result**

This command first builds all RPMs corresponding to the SPEC files in your Photon repository and then builds a bootable ISO containing those RPMs.


The RPMs thus built are stored under ` stage/RPMS/` directory within the repository, using the following directory hierarchy:

Output:
```text
$HOME/workspaces/photon/stage/:
├──RPMS/:
    ├──noarch/*.noarch.rpm    [Architecture-independent RPMs]
    ├──x86_64/*.x86_64.rpm    [RPMs built for the x86-64 architecture]
    ├──aarch64/*.aarch64.rpm  [RPMs built for the aarch64 (ARM64) architecture]
```

The cloud image is created at `$HOME/workspaces/photon.
```