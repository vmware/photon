# Upgrading to Photon OS 3.0

You can upgrade your existing Photon OS 2.0 VMs to take advantage of the functionality enhancements in Photon OS 3.0. For details, see What is New in Photon OS 3.0.

Photon OS 3.0 provides a seamless upgrade for Photon OS 2.0 implementations. You simply download an upgrade package, run a script, and reboot the VM. The upgrade script will update your packages and retain your 2.0 customizations in your new OS 3.0 VM.

**Note**: If your 2.0 VM is a full install, then you will have a 3.0 VM that represents a full install (all packages and dependencies). Upgrading a minimal installation takes less time due to fewer packages.

For each Photon OS 2.0 VM that you want to upgrade, complete the following steps:

1.	Back up all existing settings and data for the Photon OS 2.0 VM.
2.	Stop any services (for example, docker) that are currently running in the VM.
3.	Install photon-upgrade package
    
    ```
    # tdnf -y install photon-upgrade
    ```

4.	Run the upgrade script
    
    ```
    # photon-upgrade.sh
    ```

5.	Answer Y to reboot the VM. The upgrade script powers down the Photon OS 2.0 VM and powers it on as a Photon OS 3.0 VM.

After the upgrade, before you deploy into production, test all previous functionality to ensure that everything works as expected.

