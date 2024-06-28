# List Disk Partitions with `fdisk`

The `fdisk` command manipulates the disk partition table. You can, for example, use `fdisk` to list the disk partitions so that you can identify the root Linux file system. 

The following example shows `/dev/sda1` to be the root Linux partition: 

	fdisk -l
	Disk /dev/ram0: 4 MiB, 4194304 bytes, 8192 sectors
	Units: sectors of 1 * 512 = 512 bytes
	Sector size (logical/physical): 512 bytes / 4096 bytes
	I/O size (minimum/optimal): 4096 bytes / 4096 bytes
	...
	Disk /dev/sda: 8 GiB, 8589934592 bytes, 16777216 sectors
	Units: sectors of 1 * 512 = 512 bytes
	Sector size (logical/physical): 512 bytes / 512 bytes
	I/O size (minimum/optimal): 512 bytes / 512 bytes
	Disklabel type: gpt
	Disk identifier: 3CFA568B-2C89-4290-8B52-548732A3972D

	Device        Start      End  Sectors Size Type
	/dev/sda1      2048 16771071 16769024   8G Linux filesystem
	/dev/sda2  16771072 16777182     6111   3M BIOS boot




