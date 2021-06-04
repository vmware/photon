---
title:  Fixing File System Errors When fsck Fails
weight: 6
---

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

1. Restart the virtual machine.
	If the virtual machine fails to boot and finds any error then follow the steps below to recover.
7.  Log in to the root shell:
	Command>shell
    root@vc701-w4#
8. To know about the error, execute the following command:
	`journalctl -b 0 | grep -i “failed to start”`
	
	Below is output of above command:
![Output for the journalctl -b 0 | grep -i “failed to start” command](/docs/images/fsck-fails)

9. Referring to the `Failed to start the file system check on /dev/log_vg/log` error in the screenshot above, if the partition type is logical volume, then the device mapper modules create a device-special file `/dev/dm-X` to which symbolic links with the original names points to `/dev/mapper/log_vg-log or /dev/log_vg/log`. Here `log_vg` is volume group and `log` is logical volume name.

10. Execute the `lsblk` command to confirm the device type.
	Below is the output of `lsblk` command. Here `log_vg-log` is associated with the device `sde` and type `lvm`. Also, note that it is not mounted.
![lsblk command output](/docs/images/lsblk-command)

11. Execute the following command to fix the file system errors:
	`e2fsck /dev/log_vg/log`

12. Restart the virtual machine.
