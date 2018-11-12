# Managing Packages in Photon OS with `tdnf`

## Introduction

Photon OS manages packages with an open source, yum-compatible package manager called tdnf, for [Tiny Dandified Yum](https://github.com/vmware/tdnf). Tdnf keeps the operating system as small as possible while preserving yum's robust package-management capabilities. 

On Photon OS, tdnf is the default package manager for installing new packages. It is a C implementation of the DNF package manager without Python dependencies. DNF is the next upcoming major version of yum. 

Tdnf appears in the minimal and full versions of Photon OS. Tdnf reads yum repositories and works like yum. The full version of Photon OS also includes yum, and you can install packages by using yum if you want. 

In the minimal version of Photon OS, you can manage packages by using yum, but you must install it first by running the following tdnf command as root: 

	tdnf install yum

## How to Configure a Repository

Photon OS comes with a preconfigured repository called `photon-iso` that resides in `\etc\yum.repos.d.` If you receive an access error message when working with the `photon-iso` repository, it is probably because you do not have the Photon OS ISO mounted. Mount the ISO and the run the following command to update the metadata for all known repositories, including `photon-iso`: 

	mount /dev/cdrom /media/cdrom
	tdnf makecache
	
	Refreshing metadata for: 'VMware Lightwave 1.0(x86_64)'
	Refreshing metadata for: 'VMware Photon Linux 1.0(x86_64)Updates'
	Refreshing metadata for: 'VMware Photon Extras 1.0(x86_64)'
	Refreshing metadata for: 'VMware Photon Linux 1.0(x86_64)'
	Metadata cache created.


## Basic `tdnf` Commands

Here's how to install a package:

	tdnf install pkgname

Remove a package: 

	tdnf erase pkgname

List enabled repositories:

	tdnf repolist

## Other Commands, Options, and Examples

Tdnf implements a subset of the dnf commands as listed in the [dnf guide](http://dnf.readthedocs.org/en/latest/).

For a description of the tdnf commands and options, including examples, see the [Photon OS Administration Guide](photon-admin-guide.md).