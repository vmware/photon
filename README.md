![Photon](http://storage.googleapis.com/project-photon/vmw-logo-photon.svg "VMware Photon")

# Photon OS: Linux Container Host

### Contents
- [What is Photon OS](#what-is-photon)
- [Getting Photon OS](#getting-photon)
- [Getting Started](#getting-started)
- [Contributing](#contributing)
- [License](#license)
- [Photon OS Resources](#resources)

## What is Photon OS?
Photon OS&trade; is an open source Linux container host optimized for cloud-native applications, cloud platforms, and VMware infrastructure. Photon OS provides a secure run-time environment for efficiently running containers. Some of the key highlights of Photon OS are:

- **Optimized for VMware hypervisor:** The Linux kernel is tuned for performance when Photon OS runs on VMware ESXi.

- **Support for containers:** Photon OS includes the Docker daemon and works with container orchestration frameworks, such as Mesos and Kubernetes.

- **Efficient lifecycle management:** Photon OS is easy to manage, patch, and update, using the [tdnf package manager](https://github.com/vmware/photon/blob/master/docs/photon-admin-guide.md#tiny-dnf-for-package-management) and the [Photon Management Daemon (pmd)](https://github.com/vmware/pmd).

- **Security hardened:** Photon OS provides secure and up-to-date kernel and other packages, and its policies are designed to govern the system securely.

For an overview of Photon OS, see [https://vmware.github.io/photon/](https://vmware.github.io/photon/)

## Getting Photon OS

Photon OS binaries are available in a number of formats, including ISO, OVA and cloud images such as Amazon AMI, Google Cloud GCE image and Azure VHD.

For download instructions and links to Photon OS binaries, go to the [Download Guide](https://github.com/vmware/photon/wiki/Downloading-Photon-OS).

*Photon OS 3.0 Beta is here!*
--------------------------
Photon OS 3.0 Beta introduces new devices support including ARM64 (Raspberry Pi 3), installer improvements and up-to-date OSS packages including linux kernel, systemd and glibc.

For an overview of changes, see [What's New in Photon OS 3.0](https://github.com/vmware/photon/wiki/What-is-New-in-Photon-OS-3.0).

Photon OS 2.0
--------------------------
Photon OS 2.0 introduces new security and OS management capabilities, along with new and updated packages for Cloud native applications and VMware appliances. 

For an overview of changes, see [What's New in Photon OS 2.0](https://github.com/vmware/photon/wiki/What-is-New-in-Photon-OS-2.0).

## Getting Started
Begin your Photon OS journey by browsing our extensive guides on getting started in the [Photon OS Wiki](https://github.com/vmware/photon/wiki).

## Contributing
The Photon OS project team welcomes contributions from the community.

If you wish to contribute code and you have not signed our Contributor License Agreement (CLA), our CLA-bot will take you through the process and update the issue when you open a [Pull Request](https://help.github.com/articles/creating-a-pull-request). If you have questions about the CLA process, see our CLA [FAQ](https://cla.vmware.com/faq) or contact us through the GitHub issue tracker.

To help you get started making contributions to Photon OS, we have collected some helpful best practices in the [Contributing guidelines](https://github.com/vmware/photon/blob/master/contributing.md).

Before you start to code, we recommend discussing your plans through a GitHub issue or discuss it first with the official project [maintainers](https://github.com/vmware/photon/blob/dev/AUTHORS.md) via the [#photon Slack Channel](https://vmwarecode.slack.com/messages/photon/), especially for more ambitious contributions. This gives other contributors a chance to point you in the right direction, give you feedback on your design, and help you find out if someone else is working on the same thing.

## License
The Photon OS ISO and OVA images are distributed under the [Photon OS EULA](https://github.com/vmware/photon/blob/2.0/installer/EULA.txt).

With the exception of the 'libtdnf' source code, Photon OS source code is distributed under GNU GPL v2. The 'libtdnf' source code is distributed under GNU LGPL v2.1. For more details, please refer to the [Photon OS Open Source License file](https://github.com/vmware/photon/blob/master/COPYING).

## Photon OS Resources

- **Documentation**: See the [Docs](docs/) folder.
- **Security Updates**: Visit [Security-Advisories](https://github.com/vmware/photon/wiki/Security-Advisories).
- **Vagrant box**: An official Vagrant box is available on Hashicorp Atlas, to get started: `vagrant init vmware/photon`. A plugin to support Photon OS guests in Vagrant is available at [https://github.com/vmware/vagrant-guests-photon](#https://github.com/vmware/vagrant-guests-photon). Some users have found that our Vagrant box requires VirtualBox 4.3 or later. If you have issues, please check your version.
