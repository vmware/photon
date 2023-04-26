---
title:  Photon OS Installation Issue
weight: 12
---

When you try to install Photon OS 5.0 as a guest operating system on a virtual machine with an installation medium connected to an IDE interface, the installation might fail with the following error:

```
Cannot proceed with the installation because the installation medium is not readable...
```    

The issue occurs because Photon OS do not supports the IDE interface from version 5.0 onwards.

### Workaround:

To install Photon OS on a virtual machine, ensure that you select an installation medium connected to a SATA interface, and then install the Photon OS as the guest operating system.