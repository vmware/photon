# Procedure

To build Photon OS using the Packer template, set the variables that the template uses and run the build commands.

- [Set Variables](#set-variables)
- [Kick Start Build](#kick-start-build)
- [Build VMware Workstation or Fusion Vagrant Box](#build-vmware-workstation-or-fusion-vagrant-box)

## Set Variables

To use the Packer template, you must set the variables that the template uses. You can set the variables through command line or a JSON file.

Set the following variables:

    - `iso_file` - The photon ISO for the build. This file can be local or remote.
    - `iso_sha1sum` – The SHA1 sum of the ISO you want to build.
    - `product_version` - The Photon OS release version that you want to build. This version is added to the image filename. 

Preset JSON files with the required parameters are located in the `photon-packer-templates/vars` folder.

## Kick Start Build

To kick start a build using the JSON file, run the following command:

```
packer build -var-file=vars/iso-3.0GA.json packer-photon.json
```

To build Photon OS manually, run the following:

```
packer build \
        -var 'iso_file=http://dl.bintray.com/vmware/photon/3.0/GA/iso/photon-3.0-26156e2.iso' \
        -var 'iso_sha1sum=1c38dd6d00e11d3cbf7768ce93fc3eb8913a9673' \
        -var 'product_version=3.0GA' \
        packer-photon.json
```

## Build VMware Workstation or Fusion Vagrant Box

To build only a VMware Workstation or Fusion vagrant box, run:

```
packer build -only=vagrant-vmware_desktop -var-file=vars/iso-3.0GA.json packer-photon.json
```

or:

```
packer build \
       -only=vagrant-vmware_desktop \
       -var 'iso_file= http://dl.bintray.com/vmware/photon/3.0/GA/iso/photon-3.0-26156e2.iso ' \
       -var 'iso_sha1sum= 1c38dd6d00e11d3cbf7768ce93fc3eb8913a9673' \
       -var 'product_version=3.0GA' \
       packer-photon.json
```

You can build to one of the following targets:

- `vagrant-vmware_desktop` - Generates the `vmware_desktop` compatible box found on Atlas as `vmware/photon`.
- `vagrant-virtualbox` - Generates the `virtualbox` compatible box found on Atlas as `vmware/photon`.
