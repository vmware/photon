# Adding a Disk and Partitioning It

If the `df` command shows that the file system is indeed nearing capacity, you can add a new disk on the fly and partition it to increase capacity. 

1. Add a new disk. 
    
    For example, you can add a new disk to a virtual machine by using the VMware vSphere Client. After adding a new disk, check for the new disk by using `fdisk`. In the following example, the new disk is named `/dev/sdb`:
    
    	fdisk -l
    	Device        Start      End  Sectors Size Type
    	/dev/sda1      2048 16771071 16769024   8G Linux filesystem
    	/dev/sda2  16771072 16777182     6111   3M BIOS boot
    	
    	Disk /dev/sdb: 1 GiB, 1073741824 bytes, 2097152 sectors
    	Units: sectors of 1 * 512 = 512 bytes
    	Sector size (logical/physical): 512 bytes / 512 bytes
    	I/O size (minimum/optimal): 512 bytes / 512 bytes

1. Partition it with the `parted` wizard. 
    
    The command to partition the disk on Photon OS is as follows:

	parted /dev/sdb

    Use the `parted` wizard to create it as follows:

	mklabel gpt
	mkpart ext3 1 1024

1. Create a file system on the partition:

	   mkfs -t ext3 /dev/sdb1

1. Make a directory where you will mount the new file system: 

	   mkdir /newdata

1. Open `/etc/fstab` and add the new file system with the options that you require:

    ```
       	#system mnt-pt  type    options dump    fsck
       	/dev/sda1       /       ext4    defaults,barrier,noatime,noacl,data=ord$
       	/dev/cdrom      /mnt/cdrom      iso9660 ro,noauto       0       0
       	/dev/sdb1       /newdata        ext3    defaults        0		0
    ```

1. Mount it using the following command: 

	   `mount /newdata`

    Verify the results: 
	
    ```
df -h
	Filesystem      Size  Used Avail Use% Mounted on
	/dev/root       7.8G  4.4G  3.1G  59% /
	devtmpfs        172M     0  172M   0% /dev
	tmpfs           173M     0  173M   0% /dev/shm
	tmpfs           173M  664K  172M   1% /run
	tmpfs           173M     0  173M   0% /sys/fs/cgroup
	tmpfs           173M   36K  173M   1% /tmp
	tmpfs            35M     0   35M   0% /run/user/0
	/dev/sdb1       945M  1.3M  895M   1% /newdata
```

