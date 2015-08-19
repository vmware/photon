## Folder Layout
```
photon/
├── Makefile
├── README
├── Dockerfile
├── Vagrantfile
├── SPECS        # RPM SPEC files
├── common       # Build, Packaging config
├── docs         # Documentation
├── installer    # Installer used at runtime
├── support      # Build scripts
└── tools
```

## How to build the ISO?

Pre-requisites :

 * Build O/S : Ubuntu 14.04 (or later) 64 bit
 * Packages: bison, gawk, g++, createrepo, python-aptdaemon, genisoimage, texinfo, python-requests
```
sudo apt-get -y install bison gawk g++ createrepo python-aptdaemon genisoimage texinfo python-requests
```
 * Docker:
```
wget -qO- https://get.docker.com/ | sh
```

Make sure `/bin/sh` is a symbolic link pointing to `/bin/bash`

If `/bin/sh` is pointing `/bin/dash`, execute the following:
```
sudo ln -sf /bin/bash /bin/sh
```

Assuming you checked out the workspace under `$HOME/workspaces/photon`.
```
cd $HOME/workspaces/photon
sudo make iso
```
Deliverable will be created at `$HOME/workspaces/photon/stage/photon.iso`

## How to use cached toolchain and RPMS?
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
## How to use cached sources?
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

## Where are the build logs?
```
$HOME/workspaces/photon/stage/LOGS
```

## Complete build environment using Vagrant
A `Vagrantfile` is available to ensure a quick standup of a development/build environment for Photon, this Vagrantfile uses a box called `photon-build-machine` box that is created through a [Packer](http://packer.io) template available under `support/packer-templates`, see the [README.md](https://github.com/vmware/photon/blob/master/support/packer-templates/README.md) for more information on how to build `photon-build-machine`.

## Photon Vagrant box
As with the build-machine a Packer template is available under `support/packer-templates` to build a Photon based Vagrant box running Docker, see the [README.md](https://github.com/vmware/photon/blob/master/support/packer-templates/README.md) for more information on how to build.

## Automated build environment and Vagrant boxes
Convenience make targets also exist to build both the `photon-build-machine` and the `photon` Packer templates as well as building a fresh ISO using the `photon-build-machine`. See the [README.md](https://github.com/vmware/photon/blob/master/support/packer-templates/README.md) for more details.
