---
title: Upgrading to Photon OS 5.0
linkTitle: Upgrading to Photon OS 5.0
weight: 2
---

You can upgrade your existing Photon OS VMs to take advantage of the functionality enhancements in Photon OS 5.0. For details, see [What's New in Photon OS 5.0](../whats-new/).

Photon OS 5.0 provides a seamless upgrade. You simply download an upgrade package, run a script, and reboot the VM. The upgrade script will update your packages and retain your 4.0 customizations in your new Photon OS 5.0 VM.

**Note**: If your 4.0 VM is a full install, then you will have a 5.0 VM that represents a full install (all packages and dependencies). Upgrading a minimal installation takes less time due to fewer packages.

For each Photon OS 4.0 VM that you want to upgrade, complete the following steps:

1.	Back up all existing settings and data for the Photon 4.0 VM.
2.	Stop any services (for example, docker) that are currently running in the VM.
3.	Install photon-upgrade package
    
    ```
    # tdnf -y install photon-upgrade
    ```

4.	Run the upgrade script
    
    ```
    # photon-upgrade.sh --upgrade-os
    ```

5.	Answer y to reboot the VM. The upgrade script powers down the Photon OS 4.0 VM and powers it on as a Photon OS 5.0 VM.

After the upgrade, before you deploy into production, test all previous functionality to ensure that everything works as expected.

