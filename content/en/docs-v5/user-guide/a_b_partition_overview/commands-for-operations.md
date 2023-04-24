---
title:  Commands for Operations
weight: 4
---

You can perform various operations in the A/B partition system using the following commands:

- `abupdate mount/unmount`: Use this command to mount or unmount the inactive partition set. The partition set is mounted as a tree at the following location: `/mnt/abupdate/`. After you mount the partition set, the files are accessible for modifications. 

- `abupdate update`: Use this command to automatically upgrade the packages on the inactive partition set. This command supports tdnf and rpm as the package managers.

- `abupdate sync`: Use this command to synchronize the active partition set with the inactive partition set. Note that this command eliminates the ability to rollback to a safe system anymore as both becomes mirrored partition sets after the command is executed.
 
- `abupdate clean`: Use this command to erase everything on the inactive partition set.
 
- `abupdate deploy <tar.gz>`: Use this command to erase and clean the inactive partition set, mount the inactive partition set, and then install or unpack the specified OS image in the inactive partition set from a tar file.
 

- `abupdate check`:  Use this command to run checks on the inactive partition set from the active partition set. Execute this command before you execute the switch command to ensure that the inactive partition set is not broken. This command also runs checks on tools needed to update or switch from the active partition set.

- `abupdate switch`: Use this command to switch from the active partition set to the inactive partition set. Note that this command does not modify the EFI boot manager (or MBR in case of BIOS), and hence, any subsequent reboot rolls back to the previously active partition set. 
	
	If the `AUTO_SWITCH` parameter is set to yes in the configuration file, then the system automatically switches into the updated partition set after the update is complete.	
 
- `abupdate finish`: Use this command to finalize the update. This command modifies the EFI boot manager (or MBR in case of BIOS). After you execute this command, the subsequent reboots load this partition set instead of rolling back to the previous partition set.

	Note:  If the `AUTO_FINISH` parameter is set to `yes` in the configuration file, then the system automatically finalizes the switch with the finish command.

- `abupdate help`: Use this command to print the help menu.



