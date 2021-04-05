---
title:  Introduction
weight: 1
---

## RPM-OSTree Overview

OSTree is a tool to manage bootable, immutable, versioned filesystem trees. Unlike traditional package managers like rpm or dpkg that know how to install, uninstall, configure packages, OSTree has no knowledge of the relationship between files. But when you add rpm capabilities on top of OSTree, it becomes RPM-OSTree, meaning a filetree replication system that is also package-aware.

The idea behind it is to use a client/server architecture to keep your Linux installed machines (physical or VM) in sync with the latest bits, in a predictable and reliable manner. To achieve that, OSTree uses a git-like repository that records the changes to any file and replicate them to any subscriber.  

A system administrator or an image builder developer takes a base Linux image, prepares the packages and other configuration on a server box, executes a command to compose a filetree that the host machines will download and then incrementally upgrade whenever a new change has been committed.
You may read more about OSTree [here](https://ostree.readthedocs.org/en/latest/).

## Why use RPM-OSTree in Photon?

There are several important benefits:
* Reliable, efficient: The filetree replication is simple, reliable and efficient. It will only transfer deltas over the network. If you have deployed two almost identical bootable images on same box (differing just by several files), it will not take twice the space. The new tree will have a set of hardlinks to the old tree and only the different files will have a separate copy stored to disk.
* Atomic: the filetree replication is atomic. At the end of a deployment, you are either booting from one deployment, or the other. There is no "partial deployed bootable image". If anything bad happens during replication or deployment- power loss, network failure, your machine boots from the old image. There is even a tool option to cleanup old deployed (successfully or not) image.
* Manageable: You are provided simple tools to figure out exactly what packages have been installed, to compare files, configuration and package changes between versions.
* Predictable, repeatable: A big headache for a system administrator is to maintain a farm of computers with different packages, files and configuration installed in different order, that will result in exponential set of test cases. With RPM-OStree, you get identical, predictable installed systems. 

As drawbacks, I would mention:
* Some applications configured by user on host may have compatibility issues if they save configuration or download into read only directories like /usr.
* People not used with "read only" file systems will be disappointed that they could no longer use RPM, yum, tdnf to install whatever they want. Think of this as an "enterprise policy". They may circumvent this by customizing the target directory to a writable directory like /var or using rpm to install packages and record them using a new RPM repository in a writable place.
* Administrators need to be aware about the directories re-mapping specific to OSTree and plan accordingly.

## Photon with RPM-OSTree installation profiles
Photon takes advantage of RPM-OSTree and offers several installation choices:
* Photon RPM-OSTree server - used to compose customized Photon OS installations and to prepare updates. I will call it for short 'server'.
* Photon RPM-OSTree host connected to a default online server repository via http or https, maintained by VMware Photon OS team, where future updates will be published. This will create a minimal installation profile, but with the option to self-upgrade. I will call it for short 'default host'.
* Photon RPM-OSTree host connected to a custom server repository. It requires a Photon RPM-OSTree Server installed in advance. I will call it for short 'custom host'.

## Terminology

In this section, the term *OSTree* refers to the general use of this technology, the format of the repository or replication protocol. 

The term *RPM-OSTree* emphasizes the layer that adds RedHat Package Manager compatibility on both ends - at server and at host. However, since Photon OS is an RPM-based Linux, there are places in the documentation and even in the installer menus where *OSTree* may be used instead of *RPM-OSTree* when the distinction is not obvious or does not matter in that context.

When `ostree` and `rpm-ostree` are encountered, they refer to the usage of the specific Unix commands.   

Finally, *Photon RPM-OSTree* is the application or implementation of the RPM-OStree system into Photon OS, materialized into two options: Photon Server and Photon Host (or client). *Server* or *Host* may be used with or without the *Photon* and/or *RPM-OStree* qualifier, but it means the same thing. 

## Sample code

Codes samples used throughout the book are small commands that can be typed at shell command prompt and do not require downloading additional files. As an alternative, one can remote connect via ssh, so cut & paste sample code from outside sources or copy files via scp will work. See the Photon Administration guide to learn [how to enable ssh](/docs/troubleshooting-guide/solutions-to-common-problems/permitting-root-login-with-ssh/). 
The samples assume that the following VMs have been installed - see the steps in the next chapters:
* A default host VM named **photon-host-def**.
* Two server VMs named **photon-srv1** and **photon-srv2**.
* Two custom host VMs named **photon-host-cus1** and **photon-host-cus2**, connected each to the corresponding server during install.

## How to read this document

The RPM OSTree guide is structured to be used both as a sequential read and as a reference documentation.   
If you are just interested in deploying a host system and keeping it up to date, then read [Installing a Photon RPM-OSTree host against default server repository](/docs/administration-guide/photon-rpm-ostree/installing-a-host-against-default-server-repository/) and [Host updating operations](/docs/administration-guide/photon-rpm-ostree/host-updating-operations/).

If you want to install your own server and experiment with customizing packages for your Photon hosts, then read [Installing a Photon RPM-OSTree server](/docs/administration-guide/photon-rpm-ostree/creating-a-rpm-ostree-server/) onwards. There are references to the concepts discussed throughout the book, if you need to understand them better.  

## RPM OSTree in Photon OS 4.0

This section is relevant to RPM OSTree in Photon OS 4.0.

Version 4.0 supports the following features:

- Upgrade
- Rollback
- Remote, compose, and rebase server
- Installation and uninstallation of packages with URL
- Installation and uninstallation of packages from default repos
- Automatic updates
