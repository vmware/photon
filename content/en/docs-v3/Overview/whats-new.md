---
title: What is New in Photon OS 3.0
weight: 3
---

Photon OS 3.0 Rev2 introduces RPM Ostree Install, Trusted Platform Module Support (TPM), installer improvements, PMD role management Improvements and critical updates to OSS packages including linux kernel, systemd and glibc. This topic summarizes what's new and different in Photon OS 3.0 Rev2. 

## Features

### Installer Updates

- Deployment using RPM OStree.
- Network configuration support using the installer.
- LVM support for root partition.
- Trusted Platform Module Support (TPM).
- Ability to run installer from multiple media such as USB, CDROM, kickstart etc. on to a wider range of storage devices.

### Package and Binary Maintenance

- Cloud-ready images for rapid deployment on Microsoft Azure (new), Google Compute Engine (GCE), Amazon Elastic Compute Cloud (EC2), and VMware products (vSphere, Fusion, and Workstation)
- Critical updates to the following base OS packages:
    - Linux kernel 4.19
    - Glibc 2.28
    - systemd 239
    - Python3 3.7
    - Openjdk : 1.8.0.232, 1.11.0.28 and 1.10.0.23
    - Openssl : 1.0.2t and 1.1.1d
    - Cloud-init: 19.1
- Up-to-date versions for most packages available in the repository.
- Ability to support multiple versions of the same package (For example, go-1.9, go-1.10, go-1.11 and go-1.13).
- Support for new packages including Ostree, tpm2-tss, tpm2-tools, tpm2-abrmd and so on.

##Notes
Openjdk 1.10 is end of life and is being shipped to serve the sole purpose of build dependency. There will no future updates - Updates to security or otherwise will be done to the openjdk10 package.

## Known Issues

- The OVA does not deploy on Workstation 14 but works on later and earlier versions.
- Not all packages in the x86-64 repo are available for ARM64. Notable ones include mysql, mariadb and dotnet libraries.