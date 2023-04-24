---
title:  Configuring A/B Partition System
weight: 2
---

You need to create a shadow partition set and configure the A/B partition system to use it for Photon OS updates and modifications. 

To use the A/B partition system, ensure the following prerequisites:


- If you boot with BIOS, only a root filesystem pair is needed. If you boot with UEFI, an EFI partition pair is also needed.

- In the kickstart configuration file, when you create a partition, set the value of the `ab` parameter as `true` to create a shadow partition of the user-defined partition.

	To know more about the kickstart configuration, see the following page: [Kickstart Support in Photon OS](https://vmware.github.io/photon./user-guide/working-with-kickstart/)

	The following example shows how to create a shadow partition mounted at `/`:

	```
	{
	  "partitions": [
	                  {
	                    "disk": "/dev/sda",
	                    "mountpoint": "/",
	                    "size": 0,
	                    "filesystem": "ext4",
	                    "ab": true
	                  },
	                  {
	                    "disk": "/dev/sda",
	                    "mountpoint": "/sda",
	                    "size": 100,
	                    "filesystem": "ext4"
	                  }
	                ]
	}
	```   


- Configure the system details of the partitions for A/B update in the following configuration file: `/etc/abupdate.conf` 

	The following template shows how a configuration file looks like:
	
	```
	# either UEFI, BIOS, or BOTH
	# BOOT_TYPE=<boot type>
	 
	# automatically switch to other partition set after update?
	# AUTO_SWITCH=NO
	 
	# automatically finalize the update after a switch?
	# AUTO_FINISH=no
	 
	# can choose to either use tdnf or rpm as a package manager
	# if not specified, tdnf is used
	# PACKAGE_MANAGER=tdnf
	 
	# Provide information about partition sets
	# PartUUID info can be found with the "blkid" command
	#
	# EFI is needed if booting with UEFI
	# Format: PARTUUID A, PARTUUID B, mount point
	#
	# Example: HOME=("PARTUUID A" "PARTUUID B" "/home")
	 
	# Note that the / partition should be labeled as _ROOT
	# EFI=("PARTUUID A" "PARTUUID B" "/boot/efi")
	# _ROOT=("PARTUUID A" "PARTUUID B" "/")
	 
	# List of all partition sets
	# SETS=( "ROOT" )
	 
	# exclude the following directories/files from being synced
	# note that these directory paths are absolute, not relative to current working directory
	#
	# Format: <set name>_EXCLUDE=( "/dir1/" "/dir2" "/dir3/subdir/file" ... "/dirN/" )
	#
	# Example:
	# HOME_EXCLUDE=( "/mnt" "lost+found" )
	
	```   

You can use the `abupdate init` command to auto-populate all the fields. However, it is recommended that you manually enter the fields for better accuracy.


**Note**: Persistent or shared partitions that exist outside the active and inactive partition sets are also supported in the A/B partition system. You need not specify the persistent or shared partitions in the configuration files.



