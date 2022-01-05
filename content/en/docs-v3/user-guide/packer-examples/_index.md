---
title:  Packer Examples for Photon OS
weight: 3
---

Packer is an open source tool that enables you to create identical machine images for multiple platforms.

VMware maintains a GitHub project that includes examples for creating Photon OS machine images using Packer.

## Vagrant Boxes

[vmware/photon-packer-templates][vmware/photon-packer-templates]

This project provides examples to automate the creation of Photon OS machine images as Vagrant boxes using Packer and the Packer Plugins for VMware (`vmware-iso`) and Virtualbox (`virtualbox`).

The Vagrant boxes included in the project can be run on the following providers:

* VMware Fusion (`vmware_desktop`)
* VMware Workstation Pro (`vmware_desktop`)
* VirtualBox (`virtualbox`)

This project is also used to generate the offical [`vmware/photon`][vmware/photon] Vagrant boxes.

All examples are authored in the HashiCorp Configuration Language ("HCL2").

[vmware/photon]: (https://app.vagrantup.com/vmware/boxes/photon)
[vmware/photon-packer-templates]: https://github.com/vmware/photon-packer-templates

