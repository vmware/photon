# Expanding Disk Partition

If you require more space, you can expand the last partition of your disk after resizing the disk. 

The commands in this section assume `sda` as disk device.

1. After the disk is resized in the virtual machine, use the following command to enable the system to recognize the new disk ending boundary without rebooting:
    
    ```
    echo 1 > /sys/class/block/sda/device/rescan
    ```

1. Install the `parted` package to resize the disk partition by running the following command to install it:
      
   ```
    `tdnf install parted`.
   
   	# parted /dev/sda
   	GNU Parted 3.2
   	Using /dev/sda
   	Welcome to GNU Parted! Type 'help' to view a list of commands.
   ```

1. List all partitions available to fix the GPT and check the last partition number:

    ```
   
   (parted) print
   
   	Warning: Not all of the space available to /dev/sda appears to be used, you can
   	fix the GPT to use all of the space (an extra 4194304 blocks) or continue with
   	the current setting? 
   	Fix/Ignore?
   
   Press `f` to fix the GPT layout.
   
   	Model: VMware Virtual disk (scsi)
   	Disk /dev/sda: 34.4GB
   	Sector size (logical/physical): 512B/512B
   	Partition Table: gpt
   	Disk Flags: 
   
   	Number  Start   End     Size    File system  Name  Flags
   	1      1049kB  3146kB  2097kB                     bios_grub
   	2      3146kB  8590MB  8587MB  ext4
   
   ```
```

    In this case we have the partition `2` as last, then we extend the partition to 100% of the remaining size:
    
    	(parted) resizepart 2 100%

1. Expand the filesystem to the new size:
	
    ```
    resize2fs /dev/sda2
    	resize2fs 1.42.13 (17-May-2015)
    	Filesystem at /dev/sda2 is mounted on /; on-line resizing required
    	old_desc_blocks = 1, new_desc_blocks = 2
    	The filesystem on /dev/sda2 is now 8387835 (4k) blocks long.
    ```

    The new space is already available in the system:
    
    	df -h
    	Filesystem      Size  Used Avail Use% Mounted on
    	/dev/root        32G  412M   30G   2% /
    	devtmpfs       1001M     0 1001M   0% /dev
    	tmpfs          1003M     0 1003M   0% /dev/shm
    	tmpfs          1003M  252K 1003M   1% /run
    	tmpfs          1003M     0 1003M   0% /sys/fs/cgroup
    	tmpfs          1003M     0 1003M   0% /tmp
    	tmpfs           201M     0  201M   0% /run/user/0