![Photon](http://storage.googleapis.com/project-photon/vmw-logo-photon.svg "VMware Photon")


VMware Photon: Minimal Linux Container Host
===========================================

Photon OS is a minimal Linux container host designed to have a small footprint and tuned for VMware platforms. Photon is intended to invite collaboration around running containerized and Linux applications in a virtualized environment.

- Optimized for vSphere - Leveraging more than a decade of experience validating guest operating systems, Photon OS is thoroughly validated on vSphere; and, because VMware is focused on the vSphere platform, we're able to highly tune the Photon OS kernel for VMware product and provider platforms
- Container support - Compatible with container runtimes, like Docker, and container scheduling frameworks, like Kubernetes.
- Efficient lifecycle management - contains a new, open-source, yum-compatible package manager that will help make the system as small as possible, but preserve the robust yum package management capabilities.

This repository is intended for developers wishing to modify Photon, build their own customized ISO images or contribute to the code base.

To download Photon OS binaries, visit [Downloading Photon OS](https://github.com/vmware/photon/wiki/Downloading-Photon-OS).

An official Vagrant box is available on Hashicorp Atlas, to get started: `vagrant init vmware/photon`. A plugin to support Photon OS guests in Vagrant is available at https://github.com/vmware/vagrant-guests-photon. Some users have found that our Vagrant box requires VirtualBox 4.3 or later. If you have issues, please check your version.

For up-to-date documentation, see the [Docs](docs/) folder.

