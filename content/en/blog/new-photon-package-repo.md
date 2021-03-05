---
title: "New Photon Package Repo"
date: 2020-10-20
author: "Kishan Malur"
---

## Important Package Repo Information

Photon OS currently hosts the required packages and other artifacts using public servers on Bintray. As such, when a user issues any tdnf commands, Photon OS looks for the package updates in the Bintray repository.  Going forward, we will be transitioning away from this service to one that is hosted at [packages.vmware.com/photon](https://packages.vmware.com/photon). 

Over the last few weeks the team has been busy getting things ready, and the new repository is already populated with all the packages and artifacts and is ready to take over to continue serving packages and updates. Many VMware appliances have already migrated to the new package repository.

The existing Bintray repository is scheduled to be retired on 25-Nov-2020. Photon OS consumers who have not already transitioned to the new package repository are required to migrate before as soon as possible.  

Customers of Virtual Appliances provided by VMware do not need to take any action as this option should be managed by the Appliance itself.

If you are consuming Photon, i.e. users who have downloaded Photon OS from GitHub to run your applications, you just need to make a simple update to the configuration to ensure your instance is pointed to the new repository.  

This KB article has a detailed instruction on how to update the package repository configuration.  - [Photon OS Migration to New Package Repository (81304)](https://kb.vmware.com/s/article/81304?lang=en_US) 


### About Photon OS 

Photon OS™ is an open source Linux operating system from VMware. It is optimised to run cloud-native applications, cloud platforms and virtual infrastructure efficiently. Photon OS provides secure, up-to-date kernel and other packages with timely security vulnerability fixes. Designed for efficient lifecycle management, consumers would find it easy to manage, patch and update using the tdnf package manager and the Photon Management Daemon (PMD). Photon OS binaries are available in several formats, including ISO, OVA and cloud images such as Amazon AMI, Google Cloud GCE image and Azure VHD for consumers to use.  

Photon OS is specially optimized for vSphere and host of other VMware virtual appliances running on VMware virtual infrastructure.  Photon OS is also a minimalistic, light weight Linux container host providing secure run-time environment for efficiently running containers.  

