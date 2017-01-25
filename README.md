![Photon](http://storage.googleapis.com/project-photon/vmw-logo-photon.svg "VMware Photon")

**Update - January 19th, 2017**
-------------------------------
**Updated Photon OS 1.0 binaries are available.** 
We've been busy updating RPMs in our repository for months, now, to address both functional and security issues. However, our binaries have remained fixed since their release back in September 2015. In order to make it faster and easier to get a up-to-date Photon OS system, we've repackaged all of our binaries to include all of these RPM updates. For clarity, we'll call these updated binaries, which are still backed by the 1.0 repos - **1.0, Revision 2**.

We recommend downloading these newer images and building new systems from these refreshed binaries, so that new systems won't have as many initial package updates.

You can find the updated links in the [Download Guide in the github wiki](https://github.com/vmware/photon/wiki/Downloading-Photon-OS).

**VMware Photon: Minimal Linux Container Host**
-------------------------------------------

Photon OS is a minimal Linux container host designed to have a small footprint and tuned for VMware platforms. Photon is intended to invite collaboration around running containerized applications in a virtualized environment.

- Optimized for vSphere - Validated on and tuned for VMware product and provider platforms.
- Container support - Supports Docker, rkt, and the Pivotal Garden container specifications.
- Efficient lifecycle management - contains a new, open-source, yum-compatible package manager that will help make the system as small as possible, but preserve the robust yum package management capabilities.

This repository is intended for developers wishing to modify Photon and build their own customized ISO images or contribute to the code base.

For instructions and links to download Photon OS binaries, see the [Download Guide in the github wiki](https://github.com/vmware/photon/wiki/Downloading-Photon-OS).

For Security Updates, visit [Security-Advisories](https://github.com/vmware/photon/wiki/Security-Advisories).

An official Vagrant box is available on Hashicorp Atlas, to get started: `vagrant init vmware/photon`. A plugin to support Photon OS guests in Vagrant is available at https://github.com/vmware/vagrant-guests-photon. Some users have found that our Vagrant box requires VirtualBox 4.3 or later. If you have issues, please check your version.

For up-to-date documentation, see the [Docs](docs/) folder.

