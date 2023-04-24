---
title:  Packer Examples for Photon OS
weight: 3
---

Packer is an open source tool that enables you to create identical machine images for multiple platforms.

VMware maintains two GitHub projects with that include examples for creating Photon OS machine images using Packer.

All examples are authored in the HashiCorp Configuration Language ("HCL2").

## vSphere Virtual Machine Images

**GitHub Project**: [vmware-samples/packer-examples-for-vsphere][vmware-samples/packer-examples-for-vsphere]

This project provides examples to automate the creation of virtual machine images and their guest operating systems on VMware vSphere using Packer and the Packer Plugin for VMware vSphere (`vsphere-iso`). This project includes Photon OS as one of the guest operating systems. 

## Vagrant Boxes

**GitHub Project**: [vmware/photon-packer-templates][vmware/photon-packer-templates]

This project provides examples to automate the creation of Photon OS machine images as Vagrant boxes using Packer and the Packer Plugins for VMware (`vmware-iso`) and Virtualbox (`virtualbox`).

The Vagrant boxes included in the project can be run on the following providers:

* VMware Fusion (`vmware_desktop`)
* VMware Workstation Pro (`vmware_desktop`)
* VirtualBox (`virtualbox`)

This project is also used to generate the offical [`vmware/photon`][vmware/photon] Vagrant boxes.

[vmware/photon]: (https://app.vagrantup.com/vmware/boxes/photon)
[vmware-samples/packer-examples-for-vsphere]: https://github.com/vmware-samples/packer-examples-for-vsphere
[vmware/photon-packer-templates]: https://github.com/vmware/photon-packer-templates