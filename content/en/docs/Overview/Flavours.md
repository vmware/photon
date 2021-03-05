---
title: Flavours
weight: 2
---

Photon OS consists of a minimal version, a full version, RPM OSTree, and Photon Real-Time Operating System.


- The minimal version of Photon OS is lightweight container host runtime environment that is suited to managing and hosting containers. The minimal version contains just enough packaging and functionality to manage and modify containers while remaining a fast runtime environment. The minimal version is ready to work with appliances. 


- The Developer version of Photon OS includes additional packages to help you customize the system and create containerized applications. For running containers, the developer version is excessive. The devloper version helps you create, develop, test, and package an application that runs a container. 

- OSTree is a tool to manage bootable, immutable, versioned filesystem trees. Unlike traditional package managers like rpm or dpkg that know how to install, uninstall, configure packages, OSTree has no knowledge of the relationship between files. But when you add rpm capabilities on top of OSTree, it becomes RPM-OSTree, meaning a filetree replication system that is also package-aware.

- Photon OS features a kernel flavor called 'linux-rt' to support low-latency real time applications. linux-rt is based on the Linux kernel PREEMPT_RT patchset that turns Linux into a hard real time operating system. In addition to the real time kernel itself, Photon OS 4.0 supports several userspace packages such as tuned, tuna, stalld etc., that are useful to configure the operating system for real time workloads. The linux-rt kernel and the associated userspace packages together are referred to as Photon Real Time (RT).
