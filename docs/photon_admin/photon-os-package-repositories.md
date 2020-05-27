# Photon OS Package Repositories

The default installation of Photon OS includes four yum-compatible repositories plus the repository on the Photon OS ISO when it is available in a CD-ROM drive:  

    ls /etc/yum.repos.d/
    lightwave.repo
    photon-extras.repo
    photon-iso.repo
    photon-updates.repo
    photon.repo 

The Photon ISO repository (`photon-iso.repo`) contains the installation packages for Photon OS. All the packages that Photon builds and publishes reside in the RPMs directory of the ISO when it is mounted. The RPMs directory contains metadata that lets it act as a yum repository. Mounting the ISO gives you all the packages corresponding to a Photon OS build. If, however, you built Photon OS yourself from the source code, the packages correspond only to your build, though they will typically be the latest. In contrast, the ISO that you obtain from the Bintray web site contains only the packages that are in the ISO at the point of publication. As a result, the packages may no longer match those on Bintray, which are updated regularly.  

The main Photon OS repository (`photon.repo`) contains all the packages that are built from the ISO or from another source. This repository points to a static batch of packages and spec files at the point of a release. 

The updates repository (`photon-updates.repo`) is irrelevant to a major release until after the release is installed. Thereafter, the updates repository holds the updated packages for that release. The repository points to updates for the installed version, such as a version of Kubernetes that supersedes the version installed during the major release. 

The Photon extras repository (`photon-extras.repo`) holds Likewise Open, an open source authentication engine, and other VMware software that you can add to Photon OS for free. Photon OS supports but does not build the packages in the extras repository. 

Similarly, the Lightwave repository (`lightwave.repo`) contains the packages that make up the VMware Lightwave security suite for cloud applications, including tools for identity management, access control, and certificate management.
