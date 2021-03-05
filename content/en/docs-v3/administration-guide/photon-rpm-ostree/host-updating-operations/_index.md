---
title:  Host Updating Operations
weight: 5
---

- [Upgrade Overview](#upgrade-overview)
- [Incremental upgrade](#incremental-upgrade)
- [Listing file differences](#listing-file-differences)
- [Listing package differences](#listing-package-differences)
- [Rollback](#rollback)
- [Installing Packages](#installing-packages)
- [Uninstalling Packages](#uninstalling-packages)
- [Deleting a deployed filetree](#deleting-a-deployed-filetree)
- [Version skipping upgrade](#version-skipping-upgrade)
- [Tracking parent commits](#tracking-parent-commits)
- [Resetting a branch to a previous commit](#resetting-a-branch-to-a-previous-commit)

## Upgrade overview

If you've used yum, dnf (and now tdnf for Photon) in RPM systems or apt-get in Debian based Unix, you understand what "install" is for packages and the subtle difference between "update" and "upgrade".

OSTree and RPM-OSTree don't distinguish between them and the term "upgrade" has a slightly different meaning - to bring the system in sync with the remote repo, to the top of the Refspec (branch), just like in Git, by pulling the latest changes.

In fact, ostree and rpm-ostree commands support a single "upgrade" verb for a file image tree and a package list in the same refspec (branch). ```rpm-ostree upgrade``` will install a package if it doesn't exist, will not touch it if it has same version in the new image, will upgrade it if the version number is higher and it may actually downgrade it, if the package has been downgraded in the new image. I wish this operation had a different name, to avoid any confusion.

The reverse operation of an upgrade is a "rollback" and fortunately it's not named "downgrade" because it may upgrade packages in the last case describe above.

As we'll see in a future chapter, a jump to a different Refspec (branch) is also supported and it's named "rebase".

## Incremental upgrade

To check if there are any updates available, one would execute:
```
root@photon-host-def [ ~ ]# rpm-ostree upgrade
Updating from: photon:photon/3.0/x86_64/minimal


No upgrade available.
```
It is good idea to check periodically for updates.

To check if there are any new updates without actually applying them, we will pass the --check-diff flag, that would list the different packages as added, modified or deleted - if such operations were to happen.
```
root@photon-host [ ~ ]# rpm-ostree upgrade --check-diff
Updating from: photon:photon/3.0/x86_64/minimal

8 metadata, 13 content objects fetched; 1026 KiB transferred in 0 seconds
+gawk-4.1.3-2.ph1.x86_64
+sudo-1.8.15-3.ph1.x86_64
+wget-1.17.1-2.ph1.x86_64
```

We like what we see and now let's upgrade for real. This command will deploy a new bootable filetree.
```
root@photon-host [ ~ ]# rpm-ostree upgrade
Receiving metadata objects: 134/(estimating) 14.1 MB/s 14.1 MB... done
Checking out tree c8f2b11... done
Enabled rpm-md repositories: repo photon-updates photon photon-extras
rpm-md repo 'repo' (cached); generated: 2019-09-18T05:26:00Z
rpm-md repo 'photon-updates' (cached); generated: 2019-09-11T00:02:44Z
rpm-md repo 'photon' (cached); generated: 2019-02-06T08:56:24Z
rpm-md repo 'photon-extras' (cached); generated: 2018-11-02T18:09:56Z
Importing rpm-md... done
Resolving dependencies... done
Checking out packages... done
Running pre scripts... done
Running post scripts... done
Writing rpmdb... done
Writing OSTree commit... done
Staging deployment... done
Freed: 20.7 MB (pkgcache branches: 0)
  zlib 1.2.11-1.ph3 -> 1.2.11-2.ph3
Downgraded:
  ostree 2019.2-15.ph3 -> 2019.2-2.ph3
  ostree-grub2 2019.2-15.ph3 -> 2019.2-2.ph3
  ostree-libs 2019.2-15.ph3 -> 2019.2-2.ph3
Removed:
  chkconfig-1.9-1.ph3.x86_64
  elasticsearch-6.7.0-2.ph3.x86_64
  kibana-6.7.0-2.ph3.x86_64
  logstash-6.7.0-2.ph3.x86_64
  newt-0.52.20-1.ph3.x86_64
  nodejs-10.15.2-1.ph3.x86_64
  openjdk8-1.8.0.212-2.ph3.x86_64
  openjre8-1.8.0.212-2.ph3.x86_64
  ruby-2.5.3-2.ph3.x86_64
  slang-2.3.2-1.ph3.x86_64
Added:
  nss-3.44-2.ph3.x86_64
  xmlsec1-1.2.26-2.ph3.x86_64
Run "systemctl reboot" to start a reboot
```
By looking at the commit history, notice that the new commit has the original commit as parent.

```
root@photon-host [ ~ ]# ostree log photon/3.0/x86_64/minimal
commit c8f2b116b067d7695f9033bf2a99505198269354e157c0f2d5b78266cb874239
ContentChecksum:  9bc2079ad70df6dc9373752b254711f3413ae8a07628016c7de7f7d3fa505a6f
Date:  2019-09-18 08:22:15 +0000
Version: 3.0_minimal.2
(no subject)

commit 28dc49ecb4604c0bc349e4445adc659491a1874c01198e6253a261f4d59708b7
ContentChecksum:  c3650c76e2bb0e9b6b063cda2dd55939c965c54fd0b0f5ce2cfb7e801403e610
Date:  2019-09-16 09:51:33 +0000
Version: 3.0_minimal.1
```

Notice that now we have a new reference, that corresponds to the newly deployed image.

```
root@photon-host [ ~ ]# ostree refs
rpmostree/pkg/createrepo__c/0.11.1-2.ph3.x86__64
rpmostree/pkg/wget/1.20.3-1.ph3.x86__64
photon-1:photon/3.0/x86_64/minimal
rpmostree/base/0
rpmostree/base/1
ostree/0/0/0
ostree/0/0/1
ostree/0/0/2
rpmostree/pkg/rpm/4.14.2-4.ph3.x86__64
```

Let us look at the status. The new filetree version .1 has the expected Commit ID and a newer timestamp, that is actually the server date/time when the image has been generated, not the time/date when it was downloaded or installed at the host. The old image has a star next to it, showing that's the image the system is booted currently into. 

```
root@photon-host [ ~ ]# rpm-ostree status
State: idle
AutomaticUpdates: disabled
Deployments:
  ostree://photon-1:photon/3.0/x86_64/minimal
                   Version: 3.0_minimal.2 (2019-09-18T08:22:15Z)
                BaseCommit: c8f2b116b067d7695f9033bf2a99505198269354e157c0f2d5b78266cb874239
                      Diff: 1 upgraded, 3 downgraded, 10 removed, 2 added
           LayeredPackages: createrepo_c rpm wget

* ostree://photon-1:photon/3.0/x86_64/minimal
                   Version: 3.0_minimal.1 (2019-09-16T09:51:33Z)
                BaseCommit: 28dc49ecb4604c0bc349e4445adc659491a1874c01198e6253a261f4d59708b7
           LayeredPackages: createrepo_c rpm wget

  ostree://photon:photon/3.0/x86_64/minimal
                   Version: 3.0_minimal.1 (2019-09-16T09:51:33Z)
                BaseCommit: 28dc49ecb4604c0bc349e4445adc659491a1874c01198e6253a261f4d59708b7
           LayeredPackages: createrepo_c rpm wget
```

Now let's type 'reboot'. Grub will list the new filetree as the first image, marked with a star, as the default bootable image. If the keyboard is not touched and order is not changed, grub will timeout and will boot into that image.

![Grub-dual-boot-1-0](../images/rpmostree-grub.png)

Let's look again at the status. It's identical, just that the star is next to the newer image, to show it's the current image it has booted from.
```
root@photon-host [ ~ ]# rpm-ostree status
State: idle
AutomaticUpdates: disabled
Deployments:
* ostree://photon-1:photon/3.0/x86_64/minimal
                   Version: 3.0_minimal.2 (2019-09-18T08:22:15Z)
                BaseCommit: c8f2b116b067d7695f9033bf2a99505198269354e157c0f2d5b78266cb874239
           LayeredPackages: createrepo_c rpm wget

  ostree://photon-1:photon/3.0/x86_64/minimal
                   Version: 3.0_minimal.1 (2019-09-16T09:51:33Z)
                BaseCommit: 28dc49ecb4604c0bc349e4445adc659491a1874c01198e6253a261f4d59708b7
           LayeredPackages: createrepo_c rpm wget
```

Also, the current deployment directory is based on the new commit:

```
root@photon-host-def [ ~ ]# ostree admin config-diff --print-current-dir
/ostree/deploy/photon/deploy/63fd7a46dac6c169ee997039c229dd1d626f9b13eaf47b7a183f7a449eb4076f.0
```
A fresh upgrade for a new version will delete the older, original image and bring a new one, that will become the new default image. The previous 'default' image will move down one position as the backup image.

## Listing file differences

Now we can look at what files have been **A**dded, **M**odified, **D**eleted due to the addition of those three packages and switching of the boot directories, by comparing the two commits.
```
root@photon-host-def [ ~ ]# ostree diff 63fd 37e2
M    /usr/etc/ld.so.cache
M    /usr/lib/sysimage/rpm-ostree-base-db/Basenames
M    /usr/lib/sysimage/rpm-ostree-base-db/Conflictname
M    /usr/lib/sysimage/rpm-ostree-base-db/Dirnames
M    /usr/lib/sysimage/rpm-ostree-base-db/Enhancename
M    /usr/lib/sysimage/rpm-ostree-base-db/Filetriggername
M    /usr/lib/sysimage/rpm-ostree-base-db/Group
M    /usr/lib/sysimage/rpm-ostree-base-db/Installtid
M    /usr/lib/sysimage/rpm-ostree-base-db/Name
M    /usr/lib/sysimage/rpm-ostree-base-db/Obsoletename
M    /usr/lib/sysimage/rpm-ostree-base-db/Packages
M    /usr/lib/sysimage/rpm-ostree-base-db/Providename
M    /usr/lib/sysimage/rpm-ostree-base-db/Recommendname
M    /usr/lib/sysimage/rpm-ostree-base-db/Requirename
M    /usr/lib/sysimage/rpm-ostree-base-db/Sha1header
M    /usr/lib/sysimage/rpm-ostree-base-db/Sigmd5
M    /usr/lib/sysimage/rpm-ostree-base-db/Suggestname
M    /usr/lib/sysimage/rpm-ostree-base-db/Supplementname
M    /usr/lib/sysimage/rpm-ostree-base-db/Transfiletriggername
M    /usr/lib/sysimage/rpm-ostree-base-db/Triggername
M    /usr/share/rpm/Basenames
M    /usr/share/rpm/Conflictname
M    /usr/share/rpm/Dirnames
M    /usr/share/rpm/Enhancename
M    /usr/share/rpm/Filetriggername
M    /usr/share/rpm/Group
M    /usr/share/rpm/Installtid
M    /usr/share/rpm/Name
M    /usr/share/rpm/Obsoletename
M    /usr/share/rpm/Packages
M    /usr/share/rpm/Providename
M    /usr/share/rpm/Recommendname
M    /usr/share/rpm/Requirename
M    /usr/share/rpm/Sha1header
M    /usr/share/rpm/Sigmd5
M    /usr/share/rpm/Suggestname
M    /usr/share/rpm/Supplementname
M    /usr/share/rpm/Transfiletriggername
M    /usr/share/rpm/Triggername
M    /usr/share/rpm-ostree/treefile.json
D    /usr/bin/certutil
D    /usr/bin/nss-config
D    /usr/bin/pk12util
D    /usr/bin/xmlsec1
D    /usr/lib/libfreebl3.chk
D    /usr/lib/libfreebl3.so
D    /usr/lib/libfreeblpriv3.chk
D    /usr/lib/libgtest1.so
D    /usr/lib/libgtestutil.so
D    /usr/lib/libnssckbi.so
D    /usr/lib/libnssdbm3.chk
D    /usr/lib/libnssdbm3.so
D    /usr/lib/libnsssysinit.so
D    /usr/lib/libsmime3.so
D    /usr/lib/libsoftokn3.chk
D    /usr/lib/libssl3.so
D    /usr/lib/libxmlsec1-nss.so
D    /usr/lib/libxmlsec1-nss.so.1
D    /usr/lib/libxmlsec1-nss.so.1.2.26
D    /usr/lib/libxmlsec1-openssl.so
D    /usr/lib/libxmlsec1-openssl.so.1
D    /usr/lib/libxmlsec1-openssl.so.1.2.26
D    /usr/lib/libxmlsec1.so
D    /usr/lib/libxmlsec1.so.1
D    /usr/lib/libxmlsec1.so.1.2.26
```

## Listing package differences

We can also look at package differences, as you expect, using the right tool for the job.
```
root@photon-host-def [ ~ ]# rpm-ostree db diff 63fd 37e2
ostree diff commit old: rollback deployment (63fd7a46dac6c169ee997039c229dd1d626f9b13eaf47b7a183f7a449eb4076f)
ostree diff commit new: booted deployment (37e2ecfa34eb808962fdfed28623bbc457184bcd6bb788b79143d33e3569084f)
Removed:
  nss-3.44-2.ph3.x86_64
  xmlsec1-1.2.26-2.ph3.x86_64
```

## Rollback

If we want to go back to the previous image, we can rollback. The order of the images will be changed, so the old filetree will become the default bootable image. If -r option is passed, the rollback will continue with a reboot.
```
root@photon-host-def [ ~ ]# rpm-ostree rollback
Moving 'e663b2872efa01d80e4c34c823431472beb653373af32de83c7d2480316b8a6a.0' to be first deployment
Transaction complete; bootconfig swap: yes; deployment count change: 0
Upgraded:
  ostree 2019.2-2.ph3 -> 2019.2-15.ph3
  ostree-grub2 2019.2-2.ph3 -> 2019.2-15.ph3
  ostree-libs 2019.2-2.ph3 -> 2019.2-15.ph3
  zlib 1.2.11-2.ph3 -> 1.2.11-1.ph3
Removed:
  nss-3.44-2.ph3.x86_64
  xmlsec1-1.2.26-2.ph3.x86_64
Added:
  chkconfig-1.9-1.ph3.x86_64
  elasticsearch-6.7.0-2.ph3.x86_64
  kibana-6.7.0-2.ph3.x86_64
  logstash-6.7.0-2.ph3.x86_64
  newt-0.52.20-1.ph3.x86_64
  nodejs-10.15.2-1.ph3.x86_64
  openjdk8-1.8.0.212-2.ph3.x86_64
  openjre8-1.8.0.212-2.ph3.x86_64
  ruby-2.5.3-2.ph3.x86_64
  slang-2.3.2-1.ph3.x86_64
Run "systemctl reboot" to start a reboot
```
In fact, we can repeat the rollback operation as many times as we want before reboot. On each execution, it's going to change the order. It will not delete any image.  
However, an upgrade will keep the current default image and will eliminate the other image, whichever that is. So if Photon installation rolled back to an older build, an upgrade will keep that, eliminate the newer version and will replace it with an even newer version at the next upgrade.  

The boot order moved back to original:

```
root@photon-host-def [ ~ ]# rpm-ostree status
State: idle
AutomaticUpdates: disabled
Deployments:
* ostree://photon-2:photon/3.0/x86_64/minimal
                   Version: 3.0_minimal.3 (2019-09-18T12:48:03Z)
                    Commit: cf357c0f376decb3bae42326737db7e36bcf3568ab901c33dc57800c3718f07b

  ostree://photon:photon/3.0/x86_64/minimal
                   Version: 3.0_minimal (2019-08-29T11:20:19Z)
                    Commit: a31a843985e314a9e70bcf09afe8d59f7351817d9fb743c2b6dab84f20833650

```
The current bootable image path moved also back to the original value:
```
root@photon-host-def [ ~ ]# ostree admin config-diff --print-current-dir
/ostree/deploy/photon/deploy/47899767bdd4276266383fce13c4a26a51ca0304ae754609283d75f7d8aad36e.0
```

## Installing Packages

You can add more packages onto the system that are not part of the commit composed on the server.

```
rpm-ostree install <packages>
```

**Example**:

```
rpm-ostree install https://kojipkgs.fedoraproject.org//packages/wget/1.19.5/5.fc29/x86_64/wget-1.19.5-5.fc29.x86_64.rpm

```

## Uninstalling Packages

To remove layered packages installed from a repository, use

```
rpm-ostree uninstall <pkg>
```

To remove layered packages installed from a local package, you must specify the full NEVRA of the package. 

For example:

```
rpm-ostree uninstall ltrace-0.7.91-16.fc22.x86_64
```

To uninstall a package that is a part of the base layer, use 

```
rpm-ostree override remove <pkg>
```

For example: 

```
rpm-ostree override remove firefox
```

## Deleting a deployed filetree

It is possible to delete a deployed tree. You won't need to do that normally, as upgrading to a new image will delete the old one, but if for some reason deploying failed (loss of power, networking issues), you'll want to delete the partially deployed image.  
The only supported index is 1. (If multiple bootable images will be supported in the future, a larger than one, zero-based index of the image to delete will be supported).  
You cannot delete the default bootable filetree, so passing 0 will result in an error. 
```
root@photon-host-def [ ~ ]# ostree admin undeploy -v 1
OT: Using bootloader: OstreeBootloaderGrub2
Transaction complete; bootconfig swap: yes deployment count change: -1
Deleted deployment a31a843985e314a9e70bcf09afe8d59f7351817d9fb743c2b6dab84f20833650

root@photon-host-cus1 [ ~ ]# ostree admin undeploy -v 0
OT: Deployment cf357c0f376decb3bae42326737db7e36bcf3568ab901c33dc57800c3718f07b.0 unlocked=0
error: Cannot undeploy currently booted deployment 0
```
Now, we can see that the newer image is gone, the deployment directory for commit a31a has been removed.
```
root@photon-host-def [ ~ ]# rpm-ostree status
State: idle
AutomaticUpdates: disabled
Deployments:
* ostree://photon-2:photon/3.0/x86_64/minimal
                   Version: 3.0_minimal.3 (2019-09-18T12:48:03Z)
                    Commit: cf357c0f376decb3bae42326737db7e36bcf3568ab901c33dc57800c3718f07b

root@photon-host-cus1 [ ~ ]# ls /ostree/deploy/photon/deploy/
cf357c0f376decb3bae42326737db7e36bcf3568ab901c33dc57800c3718f07b.0
cf357c0f376decb3bae42326737db7e36bcf3568ab901c33dc57800c3718f07b.0.origin 
```

However the commit is still there in the OSTree repo.

```
root@photon-host-def [ ~ ]# ostree log cf35                 
commit cf357c0f376decb3bae42326737db7e36bcf3568ab901c33dc57800c3718f07b
ContentChecksum:  c24d108c7b7451374b474456a47f512e648833040bfbd4f43d862456bd6d5a18
Date:  2019-09-18 12:48:03 +0000
Version: 3.0_minimal.3
```
But there is nothing to rollback to.
```
root@photon-host-def [ ~ ]# rpm-ostree rollback
error: Found 1 deployments, at least 2 required for rollback
```
If we were to upgrade again, it would bring these packages back, but let's just check the differeneces.
```
root@photon-host-def [ ~ ]# rpm-ostree upgrade --check-diff
Updating from: photon:photon/3.0/x86_64/minimal


+gawk-4.1.0-2.ph1.x86_64
+sudo-1.8.11p1-4.ph1.x86_64
+wget-1.15-1.ph1.x86_64
```

## Version skipping upgrade

Let's assume that after a while, VMware releases version 2 that removes **sudo** and adds **bison** and **tar**. Now, an upgrade will skip version 1 and go directly to 2. Let's first look at what packages are pulled (notice sudo missing, as expected), then upgrade with reboot option.

```
root@photon-host-def [ ~ ]# rpm-ostree upgrade --check-diff
Updating from: photon:photon/3.0/x86_64/minimal

7 metadata, 13 content objects fetched; 1287 KiB transferred in 0 seconds
+bison-3.0.2-2.ph1.x86_64
+gawk-4.1.0-2.ph1.x86_64
+tar-1.27.1-1.ph1.x86_64
+wget-1.15-1.ph1.x86_64

root@photon-host-def [ ~ ]# rpm-ostree upgrade -r
Updating from: photon:photon/3.0/x86_64/minimal

107 metadata, 512 content objects fetched; 13064 KiB transferred in 1 seconds
Copying /etc changes: 5 modified, 0 removed, 16 added
Transaction complete; bootconfig swap: yes deployment count change: 1
Freed objects: 19.3 MB
```
After reboot, let's check the booting filetrees, the current dir for the current filetree and look at commit differences:
```
root@photon-host-def [ ~ ]# rpm-ostree status
State: idle
AutomaticUpdates: disabled
Deployments:
* ostree://photon-1:photon/3.0/x86_64/minimal
                   Version: 3.0_minimal.1 (2019-09-16T09:51:33Z)
                BaseCommit: 28dc49ecb4604c0bc349e4445adc659491a1874c01198e6253a261f4d59708b7
           LayeredPackages: createrepo_c rpm wget

  ostree://photon:photon/3.0/x86_64/minimal
                   Version: 3.0_minimal.1 (2019-09-16T09:51:33Z)
                BaseCommit: 28dc49ecb4604c0bc349e4445adc659491a1874c01198e6253a261f4d59708b7
           LayeredPackages: createrepo_c rpm wget
```

```
root@photon-host-cus1 [ ~ ]# ostree admin config-diff --print-current-dir
/ostree/deploy/photon/deploy/e663b2872efa01d80e4c34c823431472beb653373af32de83c7d2480316b8a6a.0

root@photon-host-cus1 [ ~ ]# rpm-ostree db diff  8b4b e663
ostree diff commit old: rollback deployment (8b4b9d4ec033d1eb816711bfdda595d1013fecbe5cd340f6a619cdc9d83a3bf2)
ostree diff commit new: booted deployment (e663b2872efa01d80e4c34c823431472beb653373af32de83c7d2480316b8a6a)

root@photon-host-cus1 [ ~ ]# rpm-ostree db diff  82bc 092e
error: Refspec '82bc' not found
```
Interesting fact: The metadata for commit 82bc has been removed from the local repo.

## Tracking parent commits

OSTree will display limited commit history - maximum 2 levels, so if you want to traverse the history even though it may not find a commitment by its ID, you can refer to its parent using '^' suffix, grandfather via '^^' and so on. We know that 82bc is the parent of 092e:


```
root@photon-host-def [ ~ ]# rpm-ostree db diff  092e^ 092e
error: No such metadata object 82bca728eadb7292d568404484ad6889c3f6303600ca8c743a4336e0a10b3817.commit
error: Refspec '82cb' not found
root@photon-host-def [ ~ ]# rpm-ostree db diff  092e^^ 092e
error: No such metadata object 82bca728eadb7292d568404484ad6889c3f6303600ca8c743a4336e0a10b3817.commit
```

So commit 092e knows who its parent is, but its metadata is no longer in the local repo, so it cannot traverse further to its parent to find an existing grandfather.

## Resetting a branch to a previous commit

We can reset the head of a branch in a local repo to a previous commit, for example corresponding to version 0 (3.0_minimal).

```
root@photon-host-def [ ~ ]# ostree reset photon:photon/3.0/x86_64/minimal cf35
```

Now if we look again at the branch commit history, the head is at version 0.

```
root@photon-host-def [ ~ ]# ostree log photon/3.0/x86_64/minimal
commit cf357c0f376decb3bae42326737db7e36bcf3568ab901c33dc57800c3718f07b
ContentChecksum:  c24d108c7b7451374b474456a47f512e648833040bfbd4f43d862456bd6d5a18
Date:  2019-09-18 12:48:03 +0000
Version: 3.0_minimal
```
