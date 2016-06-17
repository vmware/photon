## Photon Packer templates

This directory contains [Packer](http://packer.io) templates for `photon-build-machine` to build a generic `photon` Vagrant box with `docker` binding on `0.0.0.0:2375`.

The `photon-build-machine` is a Ubuntu 14.04.4 that contains all the prerequisites to build Photon from scratch, and it is the box referenced by the top-level Vagrantfile. To build this machine, you will need:

- VMware Workstation (on Windows and Linux) or Fusion (on Mac OS X)
- A recent Packer install (tested on v0.7.5)
- Packer OVF Post Processor from [GitHub](https://github.com/gosddc/packer-post-processor-vagrant-vmware-ovf) (Optional for vCloud Air build)
- Vagrant vCloud Air Provider from [GitHub](https://github.com/gosddc/vagrant-vcloudair) (Optional for vCloud Air usage)

### Automatic build machine
To automatically build the `photon-build-machine` and push into the local Vagrant box repository, use the make target from the root of the Photon source:
```
make photon-build-machine
```

### Build an ISO using a Vagrant based build machine
Assuming that the `photon-build-machine` has been created and resides in your local Vagrant repository, running `vagrant up` from the source root will automatically build a new `photon.iso` using the `photon-build-machine` Vagrant box and copy this into the host's `stage` directory. The machine will be halted at the completion of the build and can be reused or destroyed using `vagrant destroy`.

Alternatively, you can use the convenience make target to run the build process and destroy the machine on completion:
```
make photon-vagrant-build
```

#### Troubleshooting

By default Packer will run headless when building the `photon-build-machine` vm. If your packer build fails, try switching `"headless": true,` to `"headless": false,` in [`photon-build-machine.json`](https://github.com/frapposelli/photon/blob/master/support/packer-templates/photon-build-machine.json#L8). This will open the Workstation/Fusion GUI when the build starts so you can watch the process. Make sure not to send any input to the VM during the build as it may interfere with the process.

## Photon Vagrant box with Docker
To build a new Photon Vagrant box and make it available in the `stage` directory, use the make target from the root of the Photon source:
```
make photon-vagrant-local
```
By default this process will build a Vagrant box using the VMware provider which can be used with VMware Fusion or Workstation. Setting the VAGRANT_BUILD variable allows finer control of the build output:

1. Vagrant only (default) ```make photon-vagrant-local``` or explicit version ```make photon-vagrant-local VAGRANT_BUILD=vagrant```
2. vCloud Air or vCloud ```make photon-vagrant-local VAGRANT_BUILD=vcloudair```
3. All builds ```make photon-vagrant-local VAGRANT_BUILD=all```

The Vagrant box is configured to start a Docker service daemon bound to 0.0.0.0:2375 which is remapped to your host for convenience: Export DOCKER_HOST=tcp://127.0.0.1:2375.

A sample Vagrantfile for use with vCloud Air resides in ```support/vagrant/Vagrantfile_VCA_Sample```. Refer to [vagrant-vcloudair](https://github.com/gosddc/vagrant-vcloudair) for advanced usage details.

The box is configured to match the Vagrant base box standards; however, it is not meant as an official Vagrant box build for Photon but rather as a starting point to create your own.
