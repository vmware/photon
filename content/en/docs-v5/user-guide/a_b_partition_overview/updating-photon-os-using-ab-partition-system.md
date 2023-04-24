---
title:  Executing Update and Rollback Using A/B Partition System
weight: 3
---

To modify or rollback Photon OS updates using A/B partition system, perform the following workflow:

1. Edit the files on the inactive partition set.
	You can use the command options like `mount`, `update`, and `deploy` to mount and edit the files based on your requirements.

2. Switch to an inactive partition set using the `abupdate switch` command.

3. If you are not satisfied with the update, execute `abupdate switch` or `reboot` to roll back to the old active partition set.
 
4.  If you are satisfied with the update on the inactive partition set, finalize the switch with the `abupdate finish` command.
	**Note**: Once you execute the `abupdate finish` command, a reboot does not roll back to the previous partition set. 


To know more about the commands for various operations, visit the following topic: **Commands for Operations**


