# File System Consistency Check Tool

You can manually check the file system by using the file system consistency check tool, `fsck`, after you unmount the file system.

The Photon OS file system includes btrfs and ext4. The default root file system is ext4, which you can see by looking at the file system configuration file, `/etc/fstab`: 

    ```
    cat /etc/fstab
    	#system mnt-pt  type    options dump    fsck
    	/dev/sda1       /       ext4    defaults,barrier,noatime,noacl,data=ordered     1       1
    	/dev/cdrom      /mnt/cdrom      iso9660 ro,noauto       0       0
    ```

The `1` in the fifth column, under `fsck`, indicates that fsck checks the file system when the system boots.

You can also perform a read-only check without unmounting it:
	
    ```
    fsck -nf /dev/sda1
    	fsck from util-linux 2.27.1
    	e2fsck 1.42.13 (17-May-2015)
    	Warning!  /dev/sda1 is mounted.
    	Warning: skipping journal recovery because doing a read-only filesystem check.
    	Pass 1: Checking inodes, blocks, and sizes
    	Pass 2: Checking directory structure
    	Pass 3: Checking directory connectivity
    	Pass 4: Checking reference counts
    	Pass 5: Checking group summary information
    	Free blocks count wrong (1439651, counted=1423942).
    	Fix? no
    	Free inodes count wrong (428404, counted=428397).
    	Fix? no
    	/dev/sda1: 95884/524288 files (0.3% non-contiguous), 656477/2096128 blocks
    ```

The inodes count might be wrong because the file system is mounted and in use. 

To fix errors, you must first unmount the file system and then run fsck again: 
	
    ```
    umount /dev/sda1
    umount: /: target is busy
    ```

You can find information about processes that use the device by using `lsof` or `fuser`.
    
    	
    ```
    lsof | grep ^jbd2/sd
    	jbd2/sda1   99                root  cwd       DIR                8,1     4096          2 /
    	jbd2/sda1   99                root  rtd       DIR                8,1     4096          2 /
    	jbd2/sda1   99                root  txt   unknown                                        /proc/99/exe
    ```

The above example indicates that file system is in use. 

