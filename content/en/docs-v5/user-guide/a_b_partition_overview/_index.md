---
title:  Seamless Update with A/B Partition System
weight: 6
---

You can seamlessly update or roll back Photon OS with the support for A/B partition system. You can create a shadow partition set of the system and maintain the two partition sets. For example, an active set of partitions (partition A) and an inactive set of partitions (shadow partition or partition B). 

The two partition sets ensure that the working system runs seamlessly on the active partition set while the update is performed on the inactive partition set. After the inactive partition set is updated, you can execute a kexec to boot quickly into the updated partition set. If the updated partition set does not work, the system can reboot and roll back to the previously working state on partition A. 

**Note**: The kexec boot is executed with the `abupdate switch` command. The kexec boot does not modify the EFI boot manager (or MBR in the case of BIOS).

