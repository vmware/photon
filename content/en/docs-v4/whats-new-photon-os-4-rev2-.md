---
title: What is New in Photon OS 4 Rev2
linkTitle: What is New in Photon OS 4 Rev2
weight: 14
---

Photon OS 4.0 Rev2 supports OpenSSL 3.0.0, RPM packages 4.16.1.3, eBPF, GNU tarfs. This release adds critical updates to the base OS packages. The release also includes installer improvements, Photon Real-Time OS performance improvements, tdnf upgrade, and the implementation of the `pmd-nextgen` package.  This topic summarizes what's new and different in Photon OS 4.0 Rev2.


## New Features

- **OpenSSL 3.0.0** : In Photon OS 4.0 Rev2, the default OpenSSL version is 3.0.0. To support OpenSSL 3.0.0, all the dependent packages are updated and published.


- **`pmd-nextgen`**: The `pmd-nextgen` package introduces the `photon-mgmtd` tool. Use `photon-mgmtd` to manage systems, networks, services, and applications. `photon-mgmtd` features a plugin-based architecture with platform-independent APIs that you can use for remote access, performance analysis, configuration, and health monitoring.

- **`tdnf`**: In Photon OS 4.0 Rev2, `tdnf` is updated to version 3.2.3. This version of `tdnf` includes bug fixes and new features such as the `repoquery` command. Use of the metalink library has been deprecated. For more information about the features in version 3.2.3 refer to the following link: [tdnf Releases](https://github.com/vmware/tdnf/releases "tdnf Releases")  

- **Installer**: In Photon OS 4.0 Rev2, the following enhancements are added to the installer:
	- Support for Kickstart files in secondary devices.
	- Support for a user-specified mount media to boot the operating system.

- **Photon Real-Time Operating System**: The Photon Real-Time Operating System is improved with lower latency and reduced operating system jitters. Other improvements include better stability of the real-time applications and enhanced application-debugging capability. 

- **eBPF**: Support for eBPF in the Linux kernel is added.

- **GNU tarfs**: Support for GNU tarfs in Linux-ESX kernel is added.


### Package and Binary Maintenance 


- Cloud-ready images for rapid deployment on Microsoft Azure (new), Google Compute Engine (GCE), Amazon Elastic Compute Cloud (EC2), and VMware products (vSphere, Fusion, and Workstation)

- Critical updates to the following base OS packages:
	- Linux kernel 5.10.83
	- Glibc 2.32
	- systemd 247.10
	- Python3 3.10.0
	- Openjdk : 11.0.9
	- Openssl : 3.0.0
	- Cloud-init: 21.4

- RPM packages are updated to version 4.16.1.3 with SQLite as the default database.

- Critical updates for most packages available in the repo.