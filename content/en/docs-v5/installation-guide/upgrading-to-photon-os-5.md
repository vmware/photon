---
title: Upgrading Photon OS 4.0 system to Photon OS 5.0
linkTitle: Upgrading Photon OS 4.0 system to Photon OS 5.0
weight: 2
---

You can upgrade the existing Photon OS 4.0 systems to Photon OS 5.0, and take advantage of the functionality enhancements in Photon OS 5.0. For details, see [What's New in Photon OS 5.0](https://github.com/vmware/photon/wiki/What-is-New-in-Photon-OS-5.0).

The  `photon-upgrade` package provides a seamless upgrade for Photon OS. To use the package, you need to perform the following steps:

1.  Install the `photon-upgrade` package on the Photon OS 4.0 system.
2. Run the following script:
	```
	/bin/photon-upgrade.sh
	```   
3. Follow the interactions with that script. 

Please note that the script also supports a non-interactive invocation using the `--assume-yes` option. The `--help` option of the `photon-upgrade.sh` script provides online help.

The `photon-upgrade.sh` script updates packages to the latest available versions in Photon OS 5.0. Also, the upgrade retains your 4.0 customizations in your new Photon OS 5.0 system.

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

