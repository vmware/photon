---
title: Upgrading to Photon OS 4.0
linkTitle: Upgrading to Photon 4
weight: 2
---

You can upgrade your existing Photon OS 3.0 VMs to take advantage of the functionality enhancements in Photon OS 4.0. For details, see [What's New in Photon OS 4.0](./whats-new/).

For Photon OS older than Photon OS 3.0 Revision 3, Photon OS repositories changed. Because of this for any existing deployments, manual changes are required. Update Photon OS repos to packages.vmware.com.
```console
if [ `cat /etc/yum.repos.d/photon.repo | grep -o "packages.vmware.com/photon" | wc -l` -eq 0 ]; then
   cd /etc/yum.repos.d/
   sed -i 's/dl.bintray.com\/vmware/packages.vmware.com\/photon\/$releasever/g' photon.repo photon-updates.repo photon-extras.repo photon-debuginfo.repo
fi
```

Photon OS 4.0 provides a seamless upgrade for Photon OS 3.0 implementations. You simply download an upgrade package, run a script, and reboot the VM. The upgrade script will update your packages and retain your 3.0 customizations in your new OS 4.0 VM.

**Note**: If your 3.0 VM is a full install, then you will have a 4.0 VM that represents a full install (all packages and dependencies). Upgrading a minimal installation takes less time due to fewer packages.

For each Photon OS 3.0 VM that you want to upgrade, complete the following steps:

1.	Back up all existing settings and data for the Photon OS 3.0 VM.
1.	Stop any services (for example, docker) that are currently running in the VM.
1.	Install photon-upgrade package
    
    ```
    # tdnf -y install photon-upgrade
    ```

1.	Run the upgrade script
    
    ```
    # photon-upgrade.sh --upgrade-os
    ```

1.	Answer y to reboot the VM. The upgrade script powers down the Photon OS 3.0 VM and powers it on as a Photon OS 4.0 VM.

After the upgrade, before you deploy into production, test all previous functionality to ensure that everything works as expected.

