# Building an ISO from the Source Code for Photon OS

This document describes how to build an ISO from the source code for Photon OS, the open-source minimalist Linux operating system from VMware that is optimized for cloud computing platforms, VMware vSphere deployments, and applications native to the cloud. 

## Folder Layout

Here is the structure of the directories on GitHub that contain the source code for Photon OS:

```
photon/
├── Makefile
├── README
├── Dockerfile
├── Vagrantfile
├── SPECS        # RPM SPEC files
├── common       # Build, packaging config
├── docs         # Documentation
├── installer    # Installer used at runtime
├── support      # Build scripts
└── tools
```

## How to Build the ISO

The following process for building the ISO assumes that the following prerequisites are in place:

* A build operating system running the 64-bit version of Ubuntu 14.04 or later
* Packages: bison, gawk, g++, createrepo, python-aptdaemon, genisoimage, texinfo, python-requests
* Docker
* Downloaded the source code from the Photon OS repository on GitHub into `$HOME/workspaces/photon`.

Here's how to install the packages on Ubuntu: 

```
sudo apt-get -y install bison gawk g++ createrepo python-aptdaemon genisoimage texinfo python-requests libfuse-dev libssl-dev uuid-dev libreadline-dev kpartx git bc
```
Here's how to get Docker:
```
wget -qO- https://get.docker.com/ | sh
```

Here's how to make the ISO, assuming you checked out the workspace under `$HOME/workspaces/photon`:
```
cd $HOME/workspaces/photon
sudo make iso
```
The ISO is created at `$HOME/workspaces/photon/stage/photon.iso`


## How to Use the Cached Toolchain and RPMS
```
mkdir $HOME/photon-cache
sudo make iso PHOTON_CACHE_PATH=$HOME/photon-cache
```
Directory format of `PHOTON_CACHE_PATH` is as follows.
```
photon-cache/
├──tools-build.tar.gz
├──RPMS/x86-64/*.rpm
└──RPMX/noarch/*.rpm
```
## How to Use Cached Sources
```
mkdir $HOME/photon-sources
sudo make iso PHOTON_SOURCES_PATH=$HOME/photon-sources
```
Directory format of `PHOTON_SOURCES_PATH` is as follows.
```
photon-sources/
├──src1.tar.gz
├──src2.tar.gz
└──...
```

## Where are the Build Logs?
```
$HOME/workspaces/photon/stage/LOGS
```

## Building RPMs from their Source RPMs

For instructions on how to install and build a package on Photon OS from the package's source RPM, see the [Photon OS Administration Guide](https://github.com/vmware/photon/blob/master/docs/photon-admin-guide.md#building-a-package-from-a-source-rpm).

## Complete Build Environment Using Vagrant
A `Vagrantfile` is available to ensure a quick standup of a development or build environment for Photon. This Vagrantfile uses a box called `photon-build-machine` that is created through a [Packer](http://packer.io) template available under `support/packer-templates`; see the [README.md](https://github.com/vmware/photon/blob/master/support/packer-templates/README.md) for more information on how to build `photon-build-machine`.

## Photon Vagrant Box
As with the build-machine a Packer template is available under `support/packer-templates` to build a Photon based Vagrant box running Docker, see the [README.md](https://github.com/vmware/photon/blob/master/support/packer-templates/README.md) for more information on how to build it. 

## Automated Build Environment and Vagrant Boxes
Convenience `make` targets also exist to build both the `photon-build-machine` and the `photon` Packer templates as well as building a fresh ISO using the `photon-build-machine`. See the [README.md](https://github.com/vmware/photon/blob/master/support/packer-templates/README.md) for details.
