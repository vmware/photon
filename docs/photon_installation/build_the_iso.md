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

The ISO is created at `$HOME/workspaces/photon/stage/photon.iso`.