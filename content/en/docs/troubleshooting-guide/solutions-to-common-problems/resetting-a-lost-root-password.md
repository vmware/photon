---
title:  Resetting a Lost Root Password
weight: 2
---

Perform the following steps to rest a lost password:

1. Restart the Photon OS machine or the virtual machine running Photon OS. 
    
    When the Photon OS splash screen appears as it restarts, type the letter `e` to go to the GNU GRUB edit menu quickly. Because Photon OS reboots so quickly, you won't have much time to type `e`. Remember that in vSphere and Workstation, you might have to give the console focus by clicking in its window before it will register input from the keyboard.

Second, in the GNU GRUB edit menu, go to the end of the line that starts with `linux`, add a space, and then add the following code exactly as it appears below:

	rw init=/bin/bash

After you add this code, the GNU GRUB edit menu should look exactly like this:

![The modified GNU GRUB edit menu](/docs/images/grub-edit-menu-changepw.png) 

Now type `F10`.

At the command prompt, type `passwd` and then type (and re-enter) a new root password that conforms to the password complexity rules of Photon OS. Remember the password. 

Next, type the following command:

	umount /

Finally, type the following command. You must include the `-f` option to force a reboot; otherwise, the kernel enters a state of panic.

	reboot -f

This sequence of commands should look like this:

![The series of commands to reset the root password](/docs/images/resetpw.png)

After the Photon OS machine reboots, log in with the new root password. 

## Resetting the failed logon count
Resetting the root password will not reset the failed logon count, if you've had to many failed attempts, you may not be able to logon after resetting the password.

You will know if this is the case, if you see `Account locked due to X failed logins` at the photon console.

To reset the count, before you unmount the filesystem, run the following...

	/sbin/pam_tally2 --reset --user root
