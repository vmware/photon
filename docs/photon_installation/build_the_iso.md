# Building the ISO

Perform the following steps to install the packages on Ubuntu: 

1. Install the packages: 

    ```
    sudo apt-get -y install bison gawk g++ createrepo python-aptdaemon genisoimage texinfo python-requests libfuse-dev libssl-dev uuid-dev libreadline-dev kpartx git bc
    ```

1. Get Docker:

    ```
    wget -qO- https://get.docker.com/ | sh
    ```

1. Install pip and docker 2.3.0 
   
    ```
    sudo apt install python3-pip
    pip3 install docker==2.3.0
    ```
    
    If you encounter an error for LOCALE when you run these commands, then export the following variables in the terminal:
    
    ```
    export LC_ALL="en_US.UTF-8"
    export LC_CTYPE="en_US.UTF-8"
    ```

1. Make the ISO. The example below assumes that you checked out the workspace under `$HOME/workspaces/photon`:
    ```
    cd $HOME/workspaces/photon
    sudo make iso
    ```
    
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

The ISO is created at `$HOME/workspaces/photon/stage/photon.iso`.
