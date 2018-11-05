# Upgrading to Photon OS 2.0

You can upgrade your existing Photon OS 1.0 VMs to take advantage of security and functionality enhancements in Photon OS 2.0. For details, see [What is New in Photon OS 2.0](What-is-New-in-Photon-OS-2.0.md).

Photon OS 2.0 provides a seamless, in-place upgrade path for Photon OS 1.0 implementations. You simply download an upgrade package, run a script, and reboot the VM. The upgrade script will update your packages and retain your 1.0 customizations in your new OS 2.0 VM.

**Note:** If your 1.0 VM is a full install, then you will have a 2.0 VM that represents a full install (all packages and dependencies). Upgrading a minimal installation takes less time due to fewer packages.

For each Photon OS 1.0 VM that you want to upgrade, complete the following steps:

1. Back up all existing settings and data for the Photon OS 1.0 VM.

2. Stop any services (for example, docker) that are currently running in the VM.

3. Download the upgrade package. From the Photon OS 1.0 command line, run the following command:
~~~~
    # tdnf install photon-upgrade
~~~~    
4. Run the upgrade script (photon-upgrade.sh), which upgrades packages and dependencies. Answer Y to any questions.
~~~~
    # photon-upgrade.sh
~~~~
5. Answer Y to reboot the VM. The upgrade script powers down the Photon OS 1.0 VM and powers it on as a Photon OS 2.0 VM.

After upgrading but before you deploy into production, test all previous functionality to ensure that everything works as expected.