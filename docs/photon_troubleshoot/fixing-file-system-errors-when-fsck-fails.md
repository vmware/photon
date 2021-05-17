# Fixing File System Errors When fsck Fails

Sometimes when `fsck` runs during startup, it encounters an error that prevents the system from fully booting until you fix the issue by running `fsck` manually. This error might occur when Photon OS is the operating system for a VM running an appliance. 

If `fsck` fails when the computer boots and an error message says to run fsck manually, you can troubleshoot by restarting the VM, altering the GRUB edit menu to enter emergency mode before Photon OS fully boots, and running `fsck`.

Perform the following steps:

1. Take a snapshot of the virtual machine. 

1. Restart the virtual machine running Photon OS. 

    When the Photon OS splash screen appears as it restarts, type the letter `e` quickly to go to the `GNU GRUB` edit menu. 
    
    **Note**: You must type `e` quickly as Photon OS reboots quickly. Also, in VMware vSphere or VMware Workstation Pro, you might have to give the console focus by clicking in its window before it will register input from the keyboard. 

1. In the `GNU GRUB` edit menu, go to the end of the line that starts with `linux`, add a space, and then add the following code exactly as it appears below:

	`systemd.unit=emergency.target`

1. Type `F10`.

1. In the bash shell, run one of the following commands to fix the file system errors, depending on whether `sda1` or `sda2` represents the root file system: 

   	`e2fsck -y /dev/sda1`
   
   	or
   
   	`e2fsck -y /dev/sda2`

1. If the partition type is logical volume, then the device mapper modules create a device-special file `/dev/dm-X` to which symbolic links with the original names points to `/dev/mapper/vg_root_0-lv_root_0 or /dev/vg_root_0/lv_root_0`. Here `vg_root_0` is volume group and `lv_root_0` is logical volume name.

 Run the  `lsblk` command to determine the logical volumes associated with the devices.

      `root@sc-rdops-vm12-dhcp-98-247 [ ~ ]# lsblk
       NAME                           MAJ:MIN RM  SIZE RO TYPE MOUNTPOINT
       sda                              8:0    0 48.6G  0 disk
       ├─sda1                           8:1    0    4M  0 part
       ├─sda2                           8:2    0   10M  0 part /boot/efi
       ├─sda3                           8:3    0  512M  0 part /boot
       └─sda4                           8:4    0   48G  0 part
         └─vg_root_0-lv_root_0        254:0    0   48G  0 lvm  /
       sdb                              8:16   0    5G  0 disk
       sdc                              8:32   0   25G  0 disk
       └─swap_vg-swap1                254:1    0   25G  0 lvm  [SWAP]
       sdd                              8:48   0   50G  0 disk
       └─core_vg-core                 254:2    0   50G  0 lvm  /storage/core
       sde                              8:64   0   10G  0 disk
       └─log_vg-log                   254:3    0   10G  0 lvm  /storage/log
       sdf                              8:80   0   10G  0 disk
       └─db_vg-db                     254:4    0   10G  0 lvm  /storage/db
       sdg                              8:96   0   15G  0 disk
       └─dblog_vg-dblog               254:5    0   15G  0 lvm  /storage/dblog
       sdh                              8:112  0   25G  0 disk
       └─seat_vg-seat                 254:6    0   25G  0 lvm  /storage/seat
       sdi                              8:128  0    1G  0 disk
       └─netdump_vg-netdump           254:7    0 1016M  0 lvm  /storage/netdump
       sdj                              8:144  0   10G  0 disk
       └─autodeploy_vg-autodeploy     254:8    0   10G  0 lvm  /storage/autodeploy
       sdk                              8:160  0   10G  0 disk
       └─imagebuilder_vg-imagebuilder 254:9    0   10G  0 lvm  /storage/imagebuilder
       sdl                              8:176  0  100G  0 disk
       └─updatemgr_vg-updatemgr       254:10   0  100G  0 lvm  /storage/updatemgr
       sdm                              8:192  0   50G  0 disk
       └─archive_vg-archive           254:11   0   50G  0 lvm  /storage/archive
       sdn                              8:208  0   25G  0 disk
       └─vtsdb_vg-vtsdb               254:12   0   25G  0 lvm  /storage/vtsdb
       sdo                              8:224  0   15G  0 disk
       └─vtsdblog_vg-vtsdblog         254:13   0   15G  0 lvm  /storage/vtsdblog
       sdp                              8:240  0  100G  0 disk
       └─lifecycle_vg-lifecycle       254:14   0  100G  0 lvm  /storage/lifecycle
       sr0                             11:0    1 1024M  0 rom
`
In the above example, `vg_root_0-lv_root_0` is the logical volume mapped to the `sda4` device. This logical volume is a symbolic link to the device mapper module or device.

    root@sc-rdops-vm12-dhcp-98-247 [ ~ ]# ls -l /dev/mapper/vg_root_0-lv_root_0
    lrwxrwxrwx 1 root root 7 Apr 28 11:56 /dev/mapper/vg_root_0-lv_root_0 -> ../dm-0

 Run the following command to fix the errors in case device partition type is logical volume:

    e2fsck -y /dev/mapper/ vg_root_0-lv_root_0  

 Or

    e2fsck -y  e2fsck -y /dev/ vg_root_0/lv_root_0

 Or

    e2fsck -y /dev/mapper/dm-0


1. Restart the virtual machine.

