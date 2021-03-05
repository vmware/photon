---
title: "Photon OS 4.0 Beta"
linktitle: "Photon OS 4.0 Beta"
date: 2020-11-06
# featured is currnetly not implemented
# featured: "photon-768x205.png"
# featuredpath: "/img/"
---
<img class="float-right" src="/blog/images/photon-768x205.png" alt="" width="368" height="99" />

The Photon OS team at VMware is pleased to announce the Beta release of the Photon 4.0. Photon 4.0 builds upon the innovation of our enterprise class, Open Source virtual appliance OS, which can be found powering thousands of deployments the field. With exciting improvements to the 3.0 rev 2 release, Photon 4.0 comes with new features and capabilities, and important updates including upgrades to kernel 5.9, glibc 2.32, system 245, etc.

This release, like its predecessors is available in pre-packaged binary formats including: bootable ISO, pre-installed minimal OVA customized for a VMware hypervisor environment, Amazon AMI image, Google GCE image, Azure VHD, as well as a Raspberry Pi Image that has been pre-packed and tested on ARM64 architecture. The Photon OS 4.0 Beta images can be downloaded from here https://github.com/vmware/photon/wiki/Downloading-Photon-OS

## What’s New in Photon 4.0
 
### Photon Real Time Kernel for Powering the Telco vRAN Applications

Telco 5G is fuelling the growth of the Edge infrastructure as operators are increasingly adopting Virtual Radio Network applications. vRAN applications are expected to handle varying capacity demands, bring significant reduction in costs & enhance customer experience. This requires Edge Infrastructure to play vital role in providing a scalable & flexible platform to support the vRAN workloads

We are excited to announce the introduction of the Photon Real Time kernel in Photon 4.0, optimized to run vRAN applications that demand the lowest of latencies. While Photon RT will provide a performant stack to satisfy the needs of thousands of Telco Far Edge sites running critical real time applications, VMware ESXi will help the operators seamlessly manage the infrastructure.

### Security

Photon 4.0 brings in several Security capabilities like SELinux, Security Encrypted Virtualization – Encrypted Status, and support for Intel® Software Guard Extensions. With Mandatory Access Control system built directly into the Linux kernel, SELinux equips administrators with more granular access and increased flexibility. Photon OS ships with a default policy that can be customised at build time to support the needs of applications. Photon also supports SELinux for containers which has been tested against docker, containerd, and runc.

With support for Intel ® SGX drivers, applications can now leverage CPU hardware capabilities to create hardened ‘enclaves’ or trusted execution modules and secure these memory locations from other processes.

### Performance Optimization for vSphere with Tanzu

Photon historically has had linux-esx, a special kernel flavour, specially optimized for performance and capabilities when it is expected to run on VMware ESXi. Building on this, Photon 4.0 offers a variety of capabilities and performance improvements to the container runtime environment of vSphere with Tanzu, including faster launch times for containers and applications.

### Photon OS Components Improvements

Along with this, Photon 4.0 includes upgrades of more than 700 packages, and delivers improvements in core OS components like tdnf, pmd, network config manager etc.

This beta release also provides a preview of the features slated to ship in Photon 4.0Of course this is beta software, and while great effort have been made to ensure the build is free from any build or installer bugs, it is intended to be used to test and prepare applications for deployment on this new version. It is not intended for production workloads or use cases.

 

### Contribute to Photon OS

The Photon OS project team welcomes contributions from the community. Your comments, suggestions and bug reports would really help us to improve the future releases of Photon OS. You can find the resources in the following link to start contributing – https://github.com/vmware/photon#contributing