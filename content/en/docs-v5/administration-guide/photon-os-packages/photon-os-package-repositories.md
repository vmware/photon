---
title:  Photon OS Package Repositories
weight: 4
---

The default installation of Photon OS includes yum-compatible repositories and the repository on the Photon OS ISO when it is available on a CD-ROM drive:  

```
# ls -l /etc/yum.repos.d/
total 24
-rw-r--r-- 1 root root 313 Apr 17 13:19 photon-debuginfo.repo
-rw-r--r-- 1 root root 238 Apr 17 13:19 photon-iso.repo
-rw-r--r-- 1 root root 299 Apr 17 13:19 photon-release.repo
-rw-r--r-- 1 root root 303 Apr 17 13:19 photon.repo
-rw-r--r-- 1 root root 331 Apr 17 13:19 photon-srpms.repo
-rw-r--r-- 1 root root 305 Apr 19 06:00 photon-updates.repo
```

The Photon ISO repository (`photon-iso.repo`) contains the installation packages for Photon OS. All the packages that Photon builds and publishes reside in the RPMs directory of the ISO when it is mounted. The RPMs directory contains metadata that lets it act as a yum repository. Mounting the ISO gives you all the packages corresponding to a Photon OS build. If, however, you built Photon OS yourself from the source code, the packages correspond only to your build, though they will typically be the latest. In contrast, the ISO that you obtain from the [VMware Photon Packages](https://packages.vmware.com/photon) web site contains only the packages that are in the ISO at the point of publication. As a result, the packages may no longer match those on in the ISO, because they are updated more frequently.  

The Photon repository (`photon.repo`) contains all the rpms released for a particular Photon release. This repository is disabled by default but can be enabled in case the end user wants to install an older version of an rpm. 

The Photon Updates repository (`photon-updates.repo`) contains the latest versions of all the rpms for a particular Photon release. This repository is updated with the new rpm releases. This repository is enabled by default. 

The Photon debuginfo repository (`photon-debuginfo.repo`) contains the debuginfo rpms which can be installed for debugging coredumps or issues. This repository is disabled by default.

The Photon release repository (`photon-release.repo`) contains the rpms snapped at the major release time. This repository is not updated after GA. This repository is disabled by default. 

The Photon SRPM repository (`photon-srpms.repo`) contains all the source rpms for a particular Photon release. This can be used to extract the source which was used to build the rpm. This repository is disabled by default. 
