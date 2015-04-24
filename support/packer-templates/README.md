## Photon Packer templates

This directory contains [Packer](http://packer.io) templates for `photon-build-machine` and to build a generic `photon` Vagrant box with `docker` binding on `0.0.0.0:2375`.

`photon-build-machine` is a Ubuntu 14.04.1 that contains all the prerequisites to build Photon from scratch, and is the box referenced by the top-level Vagrantfile, to build this machine you will need:

- VMware Workstation (on Windows and Linux) or Fusion (on Mac OS X)
- A recent Packer install (tested on v0.7.5)

### Automatic build machine
To automatically build the `photon-build-machine` and push into the local Vagrant box repository use the make target from the root of the Photon source:
```
sudo make photon-build-machine
```

### Build an ISO using the photon-build-machine
Running `vagrant up` from the source root will automatically build a new `photon.iso` using the `photon-build-machine` Vagrant box and copy this onto the host into the `stage` directory. The machine will be halted at the completion of the build and can be reused by running ```vagrant up``` again or destroyed using `vagrant destroy`.

#### Troubleshooting

By default Packer will run headless when building the `photon-build-machine` vm. If your packer build fails, try switching `"headless": true,` to `"headless": false,` in [`photon-build-machine.json`](https://github.com/vmware/photon/blob/master/support/packer-templates/photon-build-machine.json#L8), this will open the Workstation/Fusion GUI when the build starts so you can watch the process, just make sure not to send any input to the VM during the build as it may interfere with the process.

## Photon Vagrant box with Docker
To build a new Photon Vagrant box and make it available in the `stage` directory use the make target from the root of the Photon source:
```
sudo make photon-vagrant-box
```
The Vagrant box is configured to start a Docker service daemon bound to 0.0.0.0:2375 which is remapped to your host for convenience.

Run ```export DOCKER_HOST=tcp://127.0.0.1:2375``` before trying to connect to the Docker engine with the Docker client..

The box is configured to match the Vagrant base box standards, however it is not meant as an official Vagrant box build for Photon but rather as a starting point to create your own.
