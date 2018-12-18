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

1. Make the ISO. The example below assumes that you checked out the workspace under `$HOME/workspaces/photon`:
    ```
    cd $HOME/workspaces/photon
    sudo make iso
    ```
    
**Result**

This command first builds all RPMs corresponding to the SPEC files in your Photon repository and then builds a bootable ISO containing those RPMs.

For example: The ISO is created at `$HOME/workspaces/photon/stage/photon.iso`.
 
The RPMs thus built are stored under `stage/RPMS/` directory within the repository, using the following directory hierarchy:
 
    stage/:
            RPMS/:
                    noarch/*.rpm    [Architecture-independent RPMs]
                    x86-64/*.rpm    [RPMs built for the x86-64 architecture]
                    aarch64/*.rpm  [RPMs built for the aarch64 (ARM64) architecture]


