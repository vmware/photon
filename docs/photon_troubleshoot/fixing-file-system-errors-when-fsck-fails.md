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

1. Restart the virtual machine.

