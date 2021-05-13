---
title: What is New in Photon OS 4
linkTitle: Whats New in Photon 4
weight: 15
---

Photon OS 4.0  provides support for the Real Time flavor of kernel linux-rt, SELinux , installer improvements, PMD role management improvements and critical updates to OSS packages including linux kernel, systemd, and glibc. This topic summarizes what's new and different in Photon OS 4.0. 

## New Features

- Photon OS 4.0 features a kernel flavor called 'linux-rt' to support low-latency real time applications. `linux-rt` is based on the Linux kernel PREEMPT_RT patchset that turns Linux into a hard real time operating system. In addition to the real time kernel itself, Photon OS 4.0 supports several userspace packages such as tuned, tuna, stalld etc., that are useful to configure the operating system for real time workloads. The linux-rt kernel and the associated userspace packages together are referred to as Photon Real Time (RT).

- SELinux is an implementation of mandatory access controls (MAC) on Linux. Photon OS 4.0 provides an opportunity for the appliance to enable SElinux, either in Permissive or Enforcement mode. Photon OS ships will also include a default policy which the appliance can choose to customise depending on their needs during the build time. Photon also supports SELinux for containers.

- Photon 4.0 brings out a completely revamped network configuration management library. It is a totally new avatar of the previous netmgr and has been developed with the goal of providing a set of APIs for common tasks such as configuring IP addresses, network routes, interface states, DNS, etc. This allows the user to configure the network on a Photon OS through simpler API calls that handle much of the complexity of configuring the network, which the user would have to do if they took the route of directly manipulating the various configuration files. 

- Photon OS 4.0 provides support for Raspberry Pi 4.

- OVA and AMI images for ARM architecture are available in Photon OS 4.0.

- In `tdnf`, support is added for the following:

1. Validation of externally configured GPGkeys
2. `tdnf-automatic` to allow administrators to configure systems to automatically download and perform updates without manual intervention
3. Metalink in the `tdnf` repositories allows configuration of multiple mirrors to download the repository data
4. Local and remote URL package installation
5. SSL Options 

### Installer and Build System Updates

- Support for distributed builds using Kubernetes
- Availability of Photon OS installer as RPM
- Support for multiple disks in image builder
- Support for untrusted (self-signed) HTTPS in kickstart ISO installation
- `zstd` as the default compression mechanism for RPM


### Package and Binary Maintenance

- Cloud-ready images for rapid deployment on Microsoft Azure (new), Google Compute Engine (GCE), Amazon Elastic Compute Cloud (EC2), and VMware products (vSphere, Fusion, and Workstation)
- Critical updates to the following base OS packages:
    - Linux kernel 5.10 LTS
    - Glibc 2.32
    - systemd 247
    - Python3 3.9
    - Openjdk : 1.8.0.265, 11.0.9
    - Openssl : 1.1.1
    - Cloud-init: 20.4.1
    - GCC: 10.2.0
- Up-to-date versions for most packages available in the repository.


## Notes
Openjdk 1.10 is end of life and is being shipped to serve the sole purpose of build dependency. There will no future updates - Updates to security or otherwise will be done to the openjdk10 package.

