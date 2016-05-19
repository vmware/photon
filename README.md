![Photon](http://storage.googleapis.com/project-photon/vmw-logo-photon.svg "VMware Photon")

VMware Photon: Minimal Linux Container Host
===========================================

Photon OS is a minimal Linux container host designed to have a small footprint and tuned for VMware platforms. Photon is intended to invite collaboration around running containerized applications in a virtualized environment.

- Optimized for vSphere - Validated on and tuned for VMware product and provider platforms.
- Container support - Supports Docker, rkt, and the Pivotal Garden container specifications.
- Efficient lifecycle management - contains a new, open-source, yum-compatible package manager that will help make the system as small as possible, but preserve the robust yum package management capabilities.

This repository is intended for developers wishing to modify Photon and build their own customized ISO images or contribute to the code base.

Download pre-built [OVA](https://bintray.com/artifact/download/vmware/photon/photon-custom-1.0-37d64ad-RC1.ova) and [ISO](https://bintray.com/artifact/download/vmware/photon/photon-1.0-37d64ad.iso) versions of the 1.0, Release Candidate.

An official Vagrant box is available on Hashicorp Atlas, to get started: `vagrant init vmware/photon`. A plugin to support Photon OS guests in Vagrant is available at https://github.com/vmware/vagrant-guests-photon.

For up-to-date documentation, see the [Docs](docs/) folder.

