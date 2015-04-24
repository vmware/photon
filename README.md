![Photon](http://storage.googleapis.com/project-photon/vmw-logo-photon.svg "VMware Photon")

[ ![Download](https://api.bintray.com/packages/vmware/photon/iso/images/download.svg) ](https://bintray.com/vmware/photon/iso/_latestVersion)
VMware Photon: Minimal Linux Container Host
===========================================

Photon is a technology preview of a minimal Linux container host. It is designed to have a small footprint and boot extremely quickly on VMware platforms. Photon is intended to invite collaboration around running containerized applications in a virtualized environment.

- Optimized for vSphere - Validated on VMware product and provider platforms.
- Container support - Supports Docker, rkt, and the Pivotal Garden container specifications.
- Efficient lifecycle management - contains a new, open-source, yum-compatible package manager that will help make the system as small as possible, but preserve the robust yum package management capabilities.

This repository is intended for developers wishing to modify Photon and build their own customized ISO images.

Official ISOs are available for download at [Bintray](https://bintray.com/vmware/photon/iso/view).

An official Vagrant box is available on Hashicorp Atlas, to get started: `vagrant init vmware/photon`. A plugin to support Photon guests in Vagrant is available at https://github.com/vmware/vagrant-guests-photon.

For up-to-date documentation, see the [Docs](docs/) folder.
