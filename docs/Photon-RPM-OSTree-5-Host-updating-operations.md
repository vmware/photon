### 5.1 Is it an update or an upgrade?
If you've used yum, dnf (and now tdnf for Photon) in RPM systems or apt-get in Debian based Unix, you understand what "install" is for packages and the subtle difference between "update" and "upgrade".

OSTree and RPM-OSTree don't distringuish between them and the term "upgrade" has a slightly different meaning - to bring the system in sync with the remote repo, to the top of the Refspec (branch), just like in Git, by pulling the latest changes.

In fact, ostree and rpm-ostree commands support a single "upgrade" verb for a file image tree and a package list in the same refspec (branch). ```rpm-ostree upgrade``` will install a package if it doesn't exist, will not touch it if it has same version in the new image, will upgrade it if the version number is higher and it may actually downgrade it, if the package has been downgraded in the new image. I wish this operation had a different name, to avoid any confusion.

The reverse operation of an upgrade is a "rollback" and fortunately it's not named "downgrade" because it may upgrade packages in the last case describe above.

As we'll see in a future chapter, a jump to a different Refspec (branch) is also supported and it's named "rebase".


### 5.2 Incremental upgrade
To check if there are any updates available, one would execute:
```
root@photon-host-def [ ~ ]# rpm-ostree upgrade
Updating from: photon:photon/1.0/x86_64/minimal


No upgrade available.
```  
It's good idea to check periodically for updates. In fact, VMware released in July 2016 Photon OS 1.0 Revision 2, that included an ISO containing an updated OSTree repo, mirrored online at same bintray site location. The updated OSTree repo contains new versions all packages that have been updated between since the 1.0 GA (general availability) in September 2015.  

To simplify our example, let's assume that an updated Photon OS release for this branch (Refspec) contains three new packages: **gawk**, **sudo** and **wget**.
To check if there are any new updates without actually applying them, we will pass the --check-diff flag, that would list the different packages as added, modified or deleted - if such operations were to happen.
```
root@photon-host [ ~ ]# rpm-ostree upgrade --check-diff
Updating from: photon:photon/1.0/x86_64/minimal

8 metadata, 13 content objects fetched; 1026 KiB transferred in 0 seconds
+gawk-4.1.3-2.ph1.x86_64
+sudo-1.8.15-3.ph1.x86_64
+wget-1.17.1-2.ph1.x86_64
```

We like what we see and now let's upgrade for real. This command will deploy a new bootable filetree. 
```
root@photon-host [ ~ ]# rpm-ostree upgrade             
Updating from: photon:photon/1.0/x86_64/minimal

98 metadata, 189 content objects fetched; 14418 KiB transferred in 0 seconds
Copying /etc changes: 6 modified, 0 removed, 16 added
Transaction complete; bootconfig swap: yes deployment count change: 1
Added:
  gawk-4.1.3-2.ph1.x86_64
  sudo-1.8.15-3.ph1.x86_64
  wget-1.17.1-2.ph1.x86_64
Upgrade prepared for next boot; run "systemctl reboot" to start a reboot
```
By looking at the commit history, notice that the new commit has the original commit as parent. 
```
root@photon-host [ ~ ]# ostree log photon/1.0/x86_64/minimal
commit 184d9bbcecd4e8401d4a5073a248082f7a8888d232ef9678b6942002547a14e3
Date:  2016-06-13 22:23:25 +0000
Version: 1.0_minimal.1


commit 56ef687f1319604b7900a232715718d26ca407de7e1dc89251b206f8e255dcb4
Date:  2016-06-07 14:06:17 +0000
Version: 1.0_minimal 
```

Notice that now we have a new reference, that corresponds to the newly deployed image.
```
root@photon-host [ ~ ]# ostree refs
ostree/1/1/0
ostree/1/1/1
photon:photon/1.0/x86_64/minimal
```

Let's look at the status. The new filetree version .1 has the expected Commit ID and a newer timestamp, that is actually the server date/time when the image has been generated, not the time/date when it was downloaded or installed at the host. The old image has a star next to it, showing that's the image the system is booted currently into. 
```
root@photon-host [ ~ ]# rpm-ostree status
  TIMESTAMP (UTC)        VERSION          ID            OSNAME    REFSPEC                              
  2016-06-13 22:23:25    1.0_minimal.1    184d9bbcec    photon    photon:photon/1.0/x86_64/minimal     
* 2016-06-07 14:06:17    1.0_minimal      56ef687f13    photon    photon:photon/1.0/x86_64/minimal     
```

Now let's type 'reboot'. Grub will list the new filetree as the first image, marked with a star, as the default bootable image. If the keyboard is not touched and order is not changed, grub will timeout and will boot into that image.

![Grub-dual-boot-1-0](https://cloud.githubusercontent.com/assets/13158414/16056451/68275a40-322a-11e6-8289-b1c82d617a9c.png)

Let's look again at the status. It's identical, just that the star is next to the newer image, to show it's the current image it has booted from.
```
root@photon-host [ ~ ]# rpm-ostree status
  TIMESTAMP (UTC)        VERSION          ID            OSNAME    REFSPEC                              
* 2016-06-13 22:23:25    1.0_minimal.1    184d9bbcec    photon    photon:photon/1.0/x86_64/minimal     
  2016-06-07 14:06:17    1.0_minimal      56ef687f13    photon    photon:photon/1.0/x86_64/minimal         
```

Also, the current deployment directory is based on the new 82bca commit:
```
root@photon-host-def [ ~ ]# ostree admin config-diff --print-current-dir
/ostree/deploy/photon/deploy/82bca728eadb7292d568404484ad6889c3f6303600ca8c743a4336e0a10b3817.0
```
A fresh upgrade for a new version will delete the older, original image and bring a new one, that will become the new default image. The previous 'default' image will move down one position as the backup image.

### 5.3 Listing file differences   
Now we can look at what files have been **A**dded, **M**odified, **D**eleted due to the addition of those three packages and switching of the boot directories, by comparing the two commits.
```
root@photon-host-def [ ~ ]# ostree diff 2940 82bc
M    /usr/etc/group-
M    /usr/etc/gshadow
M    /usr/etc/passwd-
M    /usr/etc/shadow
M    /usr/share/rpm/Basenames
M    /usr/share/rpm/Conflictname
M    /usr/share/rpm/Dirnames
M    /usr/share/rpm/Group
M    /usr/share/rpm/Installtid
M    /usr/share/rpm/Name
M    /usr/share/rpm/Obsoletename
M    /usr/share/rpm/Packages
M    /usr/share/rpm/Providename
M    /usr/share/rpm/Requirename
M    /usr/share/rpm/Sha1header
M    /usr/share/rpm/Sigmd5
M    /usr/share/rpm/Triggername
M    /usr/share/rpm-ostree/treefile.json
D    /boot/initramfs-4.0.9.img-49c11628bc4b702fcbf4a01abbb5249ddc845a81570a5616010f38b8967db197
D    /boot/vmlinuz-4.0.9-49c11628bc4b702fcbf4a01abbb5249ddc845a81570a5616010f38b8967db197
D    /usr/etc/gshadow-
D    /usr/etc/shadow-
D    /usr/lib/ostree-boot/initramfs-4.0.9.img-49c11628bc4b702fcbf4a01abbb5249ddc845a81570a5616010f38b8967db197
D    /usr/lib/ostree-boot/vmlinuz-4.0.9-49c11628bc4b702fcbf4a01abbb5249ddc845a81570a5616010f38b8967db197
A    /boot/initramfs-4.0.9.img-334842d15b642e70fac149bd5bbb7dd48965a3aca9da6a42d289a267a142f32f
A    /boot/vmlinuz-4.0.9-334842d15b642e70fac149bd5bbb7dd48965a3aca9da6a42d289a267a142f32f
A    /usr/bin/awk
A    /usr/bin/gawk
A    /usr/bin/gawk-4.1.0
A    /usr/bin/igawk
A    /usr/bin/sudo
A    /usr/bin/sudoedit
A    /usr/bin/sudoreplay
A    /usr/bin/wget
A    /usr/etc/pam.d/sudo
A    /usr/etc/group.rpmnew
A    /usr/etc/passwd.rpmnew
A    /usr/etc/sudoers
A    /usr/etc/wgetrc
A    /usr/etc/sudoers.d
A    /usr/include/gawkapi.h
A    /usr/include/sudo_plugin.h
A    /usr/lib/ostree-boot/initramfs-4.0.9.img-334842d15b642e70fac149bd5bbb7dd48965a3aca9da6a42d289a267a142f32f
A    /usr/lib/ostree-boot/vmlinuz-4.0.9-334842d15b642e70fac149bd5bbb7dd48965a3aca9da6a42d289a267a142f32f
A    /usr/lib/gawk
A    /usr/lib/gawk/filefuncs.so
A    /usr/lib/gawk/fnmatch.so
A    /usr/lib/gawk/fork.so
A    /usr/lib/gawk/inplace.so
A    /usr/lib/gawk/ordchr.so
A    /usr/lib/gawk/readdir.so
A    /usr/lib/gawk/readfile.so
A    /usr/lib/gawk/revoutput.so
A    /usr/lib/gawk/revtwoway.so
A    /usr/lib/gawk/rwarray.so
A    /usr/lib/gawk/testext.so
A    /usr/lib/gawk/time.so
A    /usr/lib/sudo
A    /usr/lib/sudo/group_file.so
A    /usr/lib/sudo/libsudo_util.so
A    /usr/lib/sudo/libsudo_util.so.0
A    /usr/lib/sudo/libsudo_util.so.0.0.0
A    /usr/lib/sudo/sudo_noexec.so
A    /usr/lib/sudo/sudoers.so
A    /usr/lib/sudo/system_group.so
A    /usr/libexec/awk
A    /usr/libexec/awk/grcat
A    /usr/libexec/awk/pwcat
A    /usr/sbin/visudo
A    /usr/share/doc/gawk-4.1.0
A    /usr/share/doc/gawk-4.1.0/api-figure1.eps
A    /usr/share/doc/gawk-4.1.0/api-figure1.pdf
A    /usr/share/doc/gawk-4.1.0/api-figure2.eps
A    /usr/share/doc/gawk-4.1.0/api-figure2.pdf
A    /usr/share/doc/gawk-4.1.0/api-figure3.eps
A    /usr/share/doc/gawk-4.1.0/api-figure3.pdf
A    /usr/share/doc/gawk-4.1.0/awkforai.txt
A    /usr/share/doc/gawk-4.1.0/general-program.eps
A    /usr/share/doc/gawk-4.1.0/general-program.pdf
A    /usr/share/doc/gawk-4.1.0/lflashlight.eps
A    /usr/share/doc/gawk-4.1.0/lflashlight.pdf
A    /usr/share/doc/gawk-4.1.0/process-flow.eps
A    /usr/share/doc/gawk-4.1.0/process-flow.pdf
A    /usr/share/doc/gawk-4.1.0/rflashlight.eps
A    /usr/share/doc/gawk-4.1.0/rflashlight.pdf
A    /usr/share/doc/gawk-4.1.0/statist.eps
A    /usr/share/doc/gawk-4.1.0/statist.jpg
A    /usr/share/doc/gawk-4.1.0/statist.pdf
A    /usr/share/doc/sudo-1.8.11p1
A    /usr/share/doc/sudo-1.8.11p1/CONTRIBUTORS
A    /usr/share/doc/sudo-1.8.11p1/ChangeLog
A    /usr/share/doc/sudo-1.8.11p1/HISTORY
A    /usr/share/doc/sudo-1.8.11p1/LICENSE
A    /usr/share/doc/sudo-1.8.11p1/NEWS
A    /usr/share/doc/sudo-1.8.11p1/README
A    /usr/share/doc/sudo-1.8.11p1/TROUBLESHOOTING
A    /usr/share/doc/sudo-1.8.11p1/UPGRADE
A    /usr/share/doc/sudo-1.8.11p1/sample.pam
A    /usr/share/doc/sudo-1.8.11p1/sample.sudo.conf
A    /usr/share/doc/sudo-1.8.11p1/sample.sudoers
A    /usr/share/doc/sudo-1.8.11p1/sample.syslog.conf
A    /usr/share/locale/be/LC_MESSAGES/wget.mo
A    /usr/share/locale/bg/LC_MESSAGES/wget.mo
A    /usr/share/locale/ca/LC_MESSAGES/sudo.mo
A    /usr/share/locale/ca/LC_MESSAGES/sudoers.mo
A    /usr/share/locale/ca/LC_MESSAGES/wget.mo
A    /usr/share/locale/cs/LC_MESSAGES/sudo.mo
A    /usr/share/locale/cs/LC_MESSAGES/sudoers.mo
A    /usr/share/locale/cs/LC_MESSAGES/wget.mo
A    /usr/share/locale/da/LC_MESSAGES/gawk.mo
A    /usr/share/locale/da/LC_MESSAGES/sudo.mo
A    /usr/share/locale/da/LC_MESSAGES/sudoers.mo
A    /usr/share/locale/da/LC_MESSAGES/wget.mo
A    /usr/share/locale/de/LC_MESSAGES/gawk.mo
A    /usr/share/locale/de/LC_MESSAGES/sudo.mo
A    /usr/share/locale/de/LC_MESSAGES/sudoers.mo
A    /usr/share/locale/de/LC_MESSAGES/wget.mo
A    /usr/share/locale/el/LC_MESSAGES/sudoers.mo
A    /usr/share/locale/el/LC_MESSAGES/wget.mo
A    /usr/share/locale/en_GB/LC_MESSAGES/wget.mo
A    /usr/share/locale/eo/LC_MESSAGES/sudo.mo
A    /usr/share/locale/eo/LC_MESSAGES/sudoers.mo
A    /usr/share/locale/eo/LC_MESSAGES/wget.mo
A    /usr/share/locale/es/LC_MESSAGES/gawk.mo
A    /usr/share/locale/es/LC_MESSAGES/sudo.mo
A    /usr/share/locale/es/LC_MESSAGES/wget.mo
A    /usr/share/locale/et/LC_MESSAGES/wget.mo
A    /usr/share/locale/eu/LC_MESSAGES/sudo.mo
A    /usr/share/locale/eu/LC_MESSAGES/sudoers.mo
A    /usr/share/locale/eu/LC_MESSAGES/wget.mo
A    /usr/share/locale/fi/LC_MESSAGES/gawk.mo
A    /usr/share/locale/fi/LC_MESSAGES/sudo.mo
A    /usr/share/locale/fi/LC_MESSAGES/sudoers.mo
A    /usr/share/locale/fi/LC_MESSAGES/wget.mo
A    /usr/share/locale/fr/LC_MESSAGES/gawk.mo
A    /usr/share/locale/fr/LC_MESSAGES/sudo.mo
A    /usr/share/locale/fr/LC_MESSAGES/wget.mo
A    /usr/share/locale/ga/LC_MESSAGES/wget.mo
A    /usr/share/locale/gl/LC_MESSAGES/sudo.mo
A    /usr/share/locale/gl/LC_MESSAGES/wget.mo
A    /usr/share/locale/he/LC_MESSAGES/wget.mo
A    /usr/share/locale/hr/LC_MESSAGES/sudo.mo
A    /usr/share/locale/hr/LC_MESSAGES/sudoers.mo
A    /usr/share/locale/hr/LC_MESSAGES/wget.mo
A    /usr/share/locale/hu/LC_MESSAGES/wget.mo
A    /usr/share/locale/id/LC_MESSAGES/wget.mo
A    /usr/share/locale/it/LC_MESSAGES/gawk.mo
A    /usr/share/locale/it/LC_MESSAGES/sudo.mo
A    /usr/share/locale/it/LC_MESSAGES/sudoers.mo
A    /usr/share/locale/it/LC_MESSAGES/wget.mo
A    /usr/share/locale/ja/LC_MESSAGES/gawk.mo
A    /usr/share/locale/ja/LC_MESSAGES/sudo.mo
A    /usr/share/locale/ja/LC_MESSAGES/sudoers.mo
A    /usr/share/locale/ja/LC_MESSAGES/wget.mo
A    /usr/share/locale/lt/LC_MESSAGES/sudoers.mo
A    /usr/share/locale/lt/LC_MESSAGES/wget.mo
A    /usr/share/locale/ms/LC_MESSAGES/gawk.mo
A    /usr/share/locale/nb/LC_MESSAGES/sudo.mo
A    /usr/share/locale/nb/LC_MESSAGES/sudoers.mo
A    /usr/share/locale/nb/LC_MESSAGES/wget.mo
A    /usr/share/locale/nl/LC_MESSAGES/gawk.mo
A    /usr/share/locale/nl/LC_MESSAGES/sudo.mo
A    /usr/share/locale/nl/LC_MESSAGES/sudoers.mo
A    /usr/share/locale/nl/LC_MESSAGES/wget.mo
A    /usr/share/locale/pl/LC_MESSAGES/gawk.mo
A    /usr/share/locale/pl/LC_MESSAGES/sudo.mo
A    /usr/share/locale/pl/LC_MESSAGES/sudoers.mo
A    /usr/share/locale/pl/LC_MESSAGES/wget.mo
A    /usr/share/locale/pt/LC_MESSAGES/wget.mo
A    /usr/share/locale/pt_BR/LC_MESSAGES/sudo.mo
A    /usr/share/locale/pt_BR/LC_MESSAGES/sudoers.mo
A    /usr/share/locale/pt_BR/LC_MESSAGES/wget.mo
A    /usr/share/locale/ro/LC_MESSAGES/wget.mo
A    /usr/share/locale/ru/LC_MESSAGES/sudo.mo
A    /usr/share/locale/ru/LC_MESSAGES/wget.mo
A    /usr/share/locale/sk/LC_MESSAGES/wget.mo
A    /usr/share/locale/sl/LC_MESSAGES/sudo.mo
A    /usr/share/locale/sl/LC_MESSAGES/sudoers.mo
A    /usr/share/locale/sl/LC_MESSAGES/wget.mo
A    /usr/share/locale/sr/LC_MESSAGES/sudo.mo
A    /usr/share/locale/sr/LC_MESSAGES/sudoers.mo
A    /usr/share/locale/sr/LC_MESSAGES/wget.mo
A    /usr/share/locale/sv/LC_MESSAGES/gawk.mo
A    /usr/share/locale/sv/LC_MESSAGES/sudo.mo
A    /usr/share/locale/sv/LC_MESSAGES/sudoers.mo
A    /usr/share/locale/sv/LC_MESSAGES/wget.mo
A    /usr/share/locale/tr/LC_MESSAGES/sudo.mo
A    /usr/share/locale/tr/LC_MESSAGES/sudoers.mo
A    /usr/share/locale/tr/LC_MESSAGES/wget.mo
A    /usr/share/locale/uk/LC_MESSAGES/sudo.mo
A    /usr/share/locale/uk/LC_MESSAGES/sudoers.mo
A    /usr/share/locale/uk/LC_MESSAGES/wget.mo
A    /usr/share/locale/vi/LC_MESSAGES/gawk.mo
A    /usr/share/locale/vi/LC_MESSAGES/sudo.mo
A    /usr/share/locale/vi/LC_MESSAGES/sudoers.mo
A    /usr/share/locale/vi/LC_MESSAGES/wget.mo
A    /usr/share/locale/zh_CN/LC_MESSAGES/sudo.mo
A    /usr/share/locale/zh_CN/LC_MESSAGES/sudoers.mo
A    /usr/share/locale/zh_CN/LC_MESSAGES/wget.mo
A    /usr/share/locale/zh_TW/LC_MESSAGES/wget.mo
A    /usr/share/man/man1/gawk.1.gz
A    /usr/share/man/man1/igawk.1.gz
A    /usr/share/man/man1/wget.1.gz
A    /usr/share/man/man3/filefuncs.3am.gz
A    /usr/share/man/man3/fnmatch.3am.gz
A    /usr/share/man/man3/fork.3am.gz
A    /usr/share/man/man3/ordchr.3am.gz
A    /usr/share/man/man3/readdir.3am.gz
A    /usr/share/man/man3/readfile.3am.gz
A    /usr/share/man/man3/revoutput.3am.gz
A    /usr/share/man/man3/revtwoway.3am.gz
A    /usr/share/man/man3/rwarray.3am.gz
A    /usr/share/man/man3/time.3am.gz
A    /usr/share/man/man5/sudo.conf.5.gz
A    /usr/share/man/man5/sudoers.5.gz
A    /usr/share/man/man8/sudo.8.gz
A    /usr/share/man/man8/sudo_plugin.8.gz
A    /usr/share/man/man8/sudoedit.8.gz
A    /usr/share/man/man8/sudoreplay.8.gz
A    /usr/share/man/man8/visudo.8.gz
A    /usr/share/awk
A    /usr/share/awk/assert.awk
A    /usr/share/awk/bits2str.awk
A    /usr/share/awk/cliff_rand.awk
A    /usr/share/awk/ctime.awk
A    /usr/share/awk/ftrans.awk
A    /usr/share/awk/getopt.awk
A    /usr/share/awk/gettime.awk
A    /usr/share/awk/group.awk
A    /usr/share/awk/inplace.awk
A    /usr/share/awk/join.awk
A    /usr/share/awk/libintl.awk
A    /usr/share/awk/noassign.awk
A    /usr/share/awk/ord.awk
A    /usr/share/awk/passwd.awk
A    /usr/share/awk/quicksort.awk
A    /usr/share/awk/readable.awk
A    /usr/share/awk/rewind.awk
A    /usr/share/awk/round.awk
A    /usr/share/awk/strtonum.awk
A    /usr/share/awk/walkarray.awk
A    /usr/share/awk/zerofile.awk
```
 
### 5.4 Listing package differences
We can also look at package differences, as you expect, using the right tool for the job.
```
root@photon-host-def [ ~ ]# rpm-ostree db diff 2940 82bc    
ostree diff commit old: 2940 (2940e10c4d90ce6da572cbaeeff7b511cab4a64c280bd5969333dd2fca57cfa8)
ostree diff commit new: 82bc (82bca728eadb7292d568404484ad6889c3f6303600ca8c743a4336e0a10b3817)
Added:
 gawk-4.1.0-2.ph1.x86_64
 sudo-1.8.11p1-4.ph1.x86_64
 wget-1.15-1.ph1.x86_64
```

### 5.5 Rollback
If we want to go back to the previous image, we can rollback. The order of the images will be changed, so the old filetree will become the default bootable image. If -r option is passed, the rollback will continue with a reboot.
```
root@photon-host-def [ ~ ]# rpm-ostree rollback
Moving '2940e10c4d90ce6da572cbaeeff7b511cab4a64c280bd5969333dd2fca57cfa8.0' to be first deployment
Transaction complete; bootconfig swap: yes deployment count change: 0
Removed:
  gawk-4.1.0-2.ph1.x86_64
  sudo-1.8.11p1-4.ph1.x86_64
  wget-1.15-1.ph1.x86_64
Successfully reset deployment order; run "systemctl reboot" to start a reboot
```
In fact, we can repeat the rollback operation as many times as we want before reboot. On each execution, it's going to change the order. It will not delete any image.  
However, an upgrade will keep the current default image and will eliminate the other image, whichever that is. So if Photon installation rolled back to an older build, an upgrade will keep that, eliminate the newer version and will replace it with an even newer version at the next upgrade.  

![grub-boot-0-1](https://cloud.githubusercontent.com/assets/13158414/9673725/3d33162a-525c-11e5-8292-5b79c48e0c6b.png)  
The boot order moved back to original:
```
root@photon-host-def [ ~ ]# rpm-ostree status
  TIMESTAMP (UTC)       VERSION             ID           OSNAME   REFSPEC                              
* 2015-08-20 22:27:43   1.0_minimal     2940e10c4d   photon   photon:photon/1.0/x86_64/minimal     
  2015-09-03 00:34:41   1.0_minimal.1   82bca728ea   photon   photon:photon/1.0/x86_64/minimal   
```
The current bootable image path moved also back to the original value:
```
root@photon-host-def [ ~ ]# ostree admin config-diff --print-current-dir
/ostree/deploy/photon/deploy/2940e10c4d90ce6da572cbaeeff7b511cab4a64c280bd5969333dd2fca57cfa8.0 
```

### 5.6 Deleting a deployed filetree
It is possible to delete a deployed tree. You won't need to do that normally, as upgrading to a new image will delete the old one, but if for some reason deploying failed (loss of power, networking issues), you'll want to delete the partially deployed image.  
The only supported index is 1. (If multiple bootable images will be supported in the future, a larger than one, zero-based index of the image to delete will be supported).  
You cannot delete the default bootable filetree, so passing 0 will result in an error.  
```
root@photon-host-def [ ~ ]# ostree admin undeploy -v 1
OT: Using bootloader: OstreeBootloaderGrub2
Transaction complete; bootconfig swap: yes deployment count change: -1
Deleted deployment 82bca728eadb7292d568404484ad6889c3f6303600ca8c743a4336e0a10b3817.0

root@photon-host-cus1 [ ~ ]# ostree admin undeploy -v 0
error: Cannot undeploy currently booted deployment 0
```
Now, we can see that the newer image is gone, the deployment directory for commit 82bc has been removed.  
```
root@photon-host-def [ ~ ]# rpm-ostree status
  TIMESTAMP (UTC)        VERSION        ID            OSNAME    REFSPEC                              
* 2015-08-20 22:27:43    1.0_minimal    2940e10c4d    photon    photon:photon/1.0/x86_64/minimal 
root@photon-host-cus1 [ ~ ]# ls /ostree/deploy/photon/deploy/                                        
2940e10c4d90ce6da572cbaeeff7b511cab4a64c280bd5969333dd2fca57cfa8.0
2940e10c4d90ce6da572cbaeeff7b511cab4a64c280bd5969333dd2fca57cfa8.0.origin   
```
However the commit is still there in the OSTree repo.
```
root@photon-host-def [ ~ ]# ostree log 82bc                 
commit 82bca728eadb7292d568404484ad6889c3f6303600ca8c743a4336e0a10b3817
Date:  2015-09-03 00:34:41 +0000
Version: 1.0_minimal.1


commit 2940e10c4d90ce6da572cbaeeff7b511cab4a64c280bd5969333dd2fca57cfa8
Date:  2015-08-20 22:27:43 +0000
Version: 1.0_minimal
```
But there is nothing to rollback to.
```
root@photon-host-def [ ~ ]# rpm-ostree rollback
error: Found 1 deployments, at least 2 required for rollback
```
If we were to upgrade again, it would bring these packages back, but let's just check the differeneces.
```
root@photon-host-def [ ~ ]# rpm-ostree upgrade --check-diff
Updating from: photon:photon/1.0/x86_64/minimal


+gawk-4.1.0-2.ph1.x86_64
+sudo-1.8.11p1-4.ph1.x86_64
+wget-1.15-1.ph1.x86_64
```

### 5.7 Version skipping upgrade

Let's assume that after a while, VMware releases version 2 that removes **sudo** and adds **bison** and **tar**. Now, an upgrade will skip version 1 and go directly to 2. Let's first look at what packages are pulled (notice sudo missing, as expected), then upgrade with reboot option.
```
root@photon-host-def [ ~ ]# rpm-ostree upgrade --check-diff
Updating from: photon:photon/1.0/x86_64/minimal

7 metadata, 13 content objects fetched; 1287 KiB transferred in 0 seconds
+bison-3.0.2-2.ph1.x86_64
+gawk-4.1.0-2.ph1.x86_64
+tar-1.27.1-1.ph1.x86_64
+wget-1.15-1.ph1.x86_64

root@photon-host-def [ ~ ]# rpm-ostree upgrade -r          
Updating from: photon:photon/1.0/x86_64/minimal

107 metadata, 512 content objects fetched; 13064 KiB transferred in 1 seconds
Copying /etc changes: 5 modified, 0 removed, 16 added
Transaction complete; bootconfig swap: yes deployment count change: 1
Freed objects: 19.3 MB
```
After reboot, let's check the booting filetrees, the current dir for the current filetree and look at commit differences:
```
root@photon-host-def [ ~ ]# rpm-ostree status 
  TIMESTAMP (UTC)        VERSION          ID            OSNAME    REFSPEC                              
* 2015-09-04 00:36:37    1.0_minimal.2    092e21d292    photon    photon:photon/1.0/x86_64/minimal
  2015-08-20 22:27:43    1.0_minimal      2940e10c4d    photon    photon:photon/1.0/x86_64/minimal

root@photon-host-cus1 [ ~ ]# ostree admin config-diff --print-current-dir
/ostree/deploy/photon/deploy/092e21d2928090d507ce711d482e4402e310b5a7f46532c5e24e0789590d0373.0

root@photon-host-cus1 [ ~ ]# rpm-ostree db diff  2940 092e
ostree diff commit old: 2940 (2940e10c4d90ce6da572cbaeeff7b511cab4a64c280bd5969333dd2fca57cfa8)
ostree diff commit new: 092e (092e21d2928090d507ce711d482e4402e310b5a7f46532c5e24e0789590d0373)
Added:
 bison-3.0.2-2.ph1.x86_64
 gawk-4.1.0-2.ph1.x86_64
 tar-1.27.1-1.ph1.x86_64
 wget-1.15-1.ph1.x86_64

root@photon-host-cus1 [ ~ ]# rpm-ostree db diff  82bc 092e
error: Refspec '82bc' not found
```
Interesting fact: The metadata for commit 82bc has been removed from the local repo!  

### 5.8 Tracking parent commits
OSTree will display limited commit history - maximum 2 levels, so if you want to traverse the history even though it may not find a commitment by its ID, you can refer to its parent using '^' suffix, grandfather via '^^' and so on. We know that 82bc is the parent of 092e:
```
root@photon-host-def [ ~ ]# rpm-ostree db diff  092e^ 092e
error: No such metadata object 82bca728eadb7292d568404484ad6889c3f6303600ca8c743a4336e0a10b3817.commit
error: Refspec '82cb' not found
root@photon-host-def [ ~ ]# rpm-ostree db diff  092e^^ 092e
error: No such metadata object 82bca728eadb7292d568404484ad6889c3f6303600ca8c743a4336e0a10b3817.commit
````
So commit 092e knows who its parent is, but its metadata is no longer in the local repo, so it cannot traverse further to its parent to find an existing grandfather.

### 5.9 Resetting a branch to a previous commit
We can reset the head of a branch in a local repo to a previous commit, for example corresponding to version 0 (1.0_minimal).
```
root@photon-host-def [ ~ ]# ostree reset photon:photon/1.0/x86_64/minimal 2940
```
Now if wee look again at the branch commit history, the head is at version 0.  
```
root@photon-host-def [ ~ ]# ostree log photon/1.0/x86_64/minimal
commit 2940e10c4d90ce6da572cbaeeff7b511cab4a64c280bd5969333dd2fca57cfa8
Date:  2015-08-20 22:27:43 +0000
Version: 1.0_minimal
```

[[Back to main page|Photon-RPM-OSTree:-a-simple-guide]] | [[Previous page|Photon-RPM-OSTree:-4-Querying-for-commit,-file-and-package-metadata]] | [[ Next page >|Photon-RPM-OSTree:-6-Installing-a-server]]