        *** Removing lost grub password during boot ****

Suppose you have a VM running on VMWare ESXi 6 that prompts for grub password
upon booting but you have lost/forgotten password, you will reach a point where
system won't boot and you can't access anything.

This document describes in detail how to overcome such situation.
That is, how to remove grub password from PhotonOS.

Under regular circumstances where you are able to login as `root` user, you can
simply remove `/etc/grub.d/01_users` or modify `/etc/grub.d/40_custom` file to
not have a password in it and by regenerating grub configuration.

```
Important Note:
 - Do not miss to take a VM snapshot or take a backup of your VM before
 proceeding with the next operations.

 - You need to be super cautious while performing this task., unless you are
 100% sure, do not proceed.

 - If you are not careful while doing steps mentioned below, you might end up
 with an unusable system.
```

But in a situation where you can't proceed to grub menu because you don't know
grub password, here are the steps you need to follow.

1. Boot the affected Photon VM from a live CD.

2. Mount the VM's root fs from live system.

3. Remove grub password from the mounted partition by modifying relevant files.

4. Sync the mounted file system and unmount the partition.

5. Reboot with original VM and observe that you won't be prompted for grub
password anymore.

The first step in the above list is bit tricky.
This document assumes that you are managing VM from either ESXi or vCenter.

Steps to boot with live CD and How to remove grub password:

1. Download a live CD ISO image to somewhere accessible to either
(a) the vSphere client or
(b) the ESXi host running the VM

2. Poweroff the VM which you are troubleshooting.

3. On the VM(from ESXi or vCenter UI) go to

Edit Settings -> Options -> Boot Options
Tick "Force BIOS Setup" to force entry into the BIOS setup screen on the next boot.

Attach the live CD's datastore ISO image as a Virtual CD by going to VM Edit Settings option.
Tick the 'Connect at boot option'

4. Reboot the VM.

5. Observe direct entry into the BIOS setup.

6. Go to the Boot page in the PhoenixBIOS Setup Utility, and select the
"Hard Drive" entry, and then use "-" to move it down the order to below the "CD-ROM" entry.

7. F10 to save the change, and exit.

8. Observe VM booting from the virtual live CD and after boot enter `sudo su`
command to act as root user.

9. Now get all the block devices available by running `lsblk` command.

10. You might see a list of devices `/dev/sda1, /dev/sda2, ...` now you need to
mount the partition one by one to check which is the actual root fs.

For example:
```
# mount /dev/sda1 /mnt
Exampine the files under /mnt and if the /etc/grub.d is present in the mounted
location we can proceed to next step.
```

In my case while creating this document, it was `/dev/sda3`

11. Once you have mounted root fs to /mnt location, just navigate through
/etc/grub.d directory and carefully revert your password related changes.

If you have password settings in /etc/grub.d/01_users file, move
/etc/grub.d/01_users file to some back up location and search for `password`
string in /etc/grub.d/10_linux file and comment them out.

If your changes are in /etc/grub.d/40_custom file, just comment the password
related configs and modify password settings in /etc/grub.d/10_linux file as
explained above.

12. Once you are done, run `sync` command to flush changes from file system
buffer to disk and poweroff the VM from ESXi or vCenter menu.

13. Remove attached ISO file from VM settings and if you want to revert boot
order you modified in Step. 6 above, enter to BIOS menu again by follwing
Step. 3, change boot order to your desired order, save settings and continue
booting.

If everything goes right and you have done everything correctly grub won't ask
for password anymore and you should be prompted to enter user credentials to
login to system.
