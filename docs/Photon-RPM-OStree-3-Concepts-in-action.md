# Concepts in Action

Now that we have a fresh installed host (either as [[default|Photon-RPM-OSTree:-2-Installing-a-host-against-default-server-repository]] or [[custom|Photon-RPM-OSTree:-7-Installing-a-host-against-a-custom-server-repository]]), I can explain better the OStree concepts and see them in action.  
## 3.1 Querying the deployed filetrees
The first thing to do is to run a command that tells us what is installed on the machine and when. Since it's a fresh install from the CD, there is only one bootable filetree image deployed.
``` 
root@photon-host [ ~ ]# rpm-ostree status
  TIMESTAMP (UTC)       VERSION       ID           OSNAME  REFSPEC               
* 2016-06-07 14:06:17   1.0_minimal   56ef687f13   photon  photon:photon/1.0/x86_64/minimal
```  
## 3.2 Bootable filetree version
**1.0_minimal** is not the Linux Photon OS release version, nor daily build, but rather a human readable, self-incrementing version associated with every commit that brings file/package updates. Think of this as version 0. The following versions are going to be 1.0_minimal.1, 1.0_minimal.2, 1.0_minimal.3 and so on.

## 3.3 Commit ID
The ID listed is actually the first 5 bytes (10 hex digits) of the commit hash. If you want to see the entire 32 bytes hex number, just add the 'pretty' formatting option. The .0 at the end means that this is the default bootable deployment. This will change to 1 when another deployment will take its place as the default.
```
root@photon-host [ ~ ]# rpm-ostree status -p
============================================================
  * DEFAULT ON BOOT
----------------------------------------
  version    1.0_minimal
  timestamp  2016-06-07 14:06:17
  id         56ef687f1319604b7900a232715718d26ca407de7e1dc89251b206f8e255dcb4.0
  osname     photon     
  refspec    photon:photon/1.0/x86_64/minimal
============================================================
```
## 3.4 OSname
The OS Name identifies the operating system installed. All bootable filetrees for the same OS will share the /var directory, in other words applications installed in one booted image into this directory will be available in all other images.  
If a new set of images are created for a different OS, they will receive a fresh copy of /var that is not shared with the previous OS images for the initial OS. In other words, if a machine is dual boot for different operating systems, they will not share each other's /var content, however they will still merge 3-way /etc.

## 3.5 Refspec
The **Refspec** is a branch inside the repo, expressed in a hierarchical way. In this case, it's the default branch that will receive package updates for the Photon OS 1.0 Minimal installation profile on Intel platforms. There could be other branches in the future, for example photon/1.0/x86_64/full that will match the Full installation profile (full set of packages installed).  
Think of Refspec as the head of the minimal branch (just like in git) at the origin repo. On the replicated, local repo at the host, **minimal** is a file that contains the latest commit ID known for that branch.  
```
root@photon-host [ ~ ]# cat /ostree/repo/refs/remotes/photon/photon/1.0/x86_64/minimal 
56ef687f1319604b7900a232715718d26ca407de7e1dc89251b206f8e255dcb4
```
Why are there two 'photon' directory levels in the remotes path? The **photon:** prefix in the Refspec listed by `rpm-ostree status` corresponds to the first **photon** directory in the remotes path and is actually the name given to the remote that the host is connected to, which points to an http or https URL. We'll talk about remotes later, but for now think of it as a namespace qualifier.  The second **photon** is part of the Refspec path itself.

## 3.6 Deployments
We've used so far `rpm-ostree`. The same information can be obtained running an `ostree` command:
```
root@photon-host [ ~ ]# ostree admin status
* photon 56ef687f1319604b7900a232715718d26ca407de7e1dc89251b206f8e255dcb4.0
    Version: 1.0_minimal
    origin refspec: photon:photon/1.0/x86_64/minimal
```
But where is this information stored? As you may have guessed, the local repo stores the heads of the deployed trees - the most recent commitment ID, just like Git does:  
```
root@photon-host [ ~ ]# cat /ostree/repo/refs/heads/ostree/0/1/0 
56ef687f1319604b7900a232715718d26ca407de7e1dc89251b206f8e255dcb4
```
This also where this command that lists the references (local heads and remotes) takes its data from:
```
root@photon-host [ ~ ]# ostree refs
photon:photon/1.0/x86_64/minimal
ostree/0/1/0
```
Based on that, it could find the root of the deployment that it boots from. The actual filetree is deployed right here:
```
root@photon-host [ ~ ]# ls -l /ostree/deploy/photon/deploy/56ef687f1319604b7900a232715718d26ca407de7e1dc89251b206f8e255dcb4.0
total 36
lrwxrwxrwx  1 root root    7 Jun  9 18:26 bin -> usr/bin
drwxr-xr-x  4 root root 4096 Jan  1  1970 boot
drwxr-xr-x  2 root root 4096 Jan  1  1970 dev
drwxr-xr-x 33 root root 4096 Jun 12 23:04 etc
lrwxrwxrwx  1 root root    8 Jun  9 18:26 home -> var/home
lrwxrwxrwx  1 root root    7 Jun  9 18:26 lib -> usr/lib
lrwxrwxrwx  1 root root    7 Jun  9 18:26 lib64 -> usr/lib
lrwxrwxrwx  1 root root    9 Jun  9 18:26 media -> run/media
lrwxrwxrwx  1 root root    7 Jun  9 18:26 mnt -> var/mnt
lrwxrwxrwx  1 root root    7 Jun  9 18:26 opt -> var/opt
lrwxrwxrwx  1 root root   14 Jun  9 18:26 ostree -> sysroot/ostree
drwxr-xr-x  2 root root 4096 Jan  1  1970 proc
lrwxrwxrwx  1 root root   12 Jun  9 18:26 root -> var/roothome
drwxr-xr-x  2 root root 4096 Jan  1  1970 run
lrwxrwxrwx  1 root root    8 Jun  9 18:26 sbin -> usr/sbin
lrwxrwxrwx  1 root root    7 Jun  9 18:26 srv -> var/srv
drwxr-xr-x  2 root root 4096 Jan  1  1970 sys
drwxr-xr-x  2 root root 4096 Jan  1  1970 sysroot
lrwxrwxrwx  1 root root   11 Jun  9 18:26 tmp -> sysroot/tmp
drwxr-xr-x 10 root root 4096 Jan  1  1970 usr
drwxr-xr-x  7 root root 4096 Jun  9 18:26 var
```  
So how is a deployment linked to a specific branch, originating from a remote repo? Well, there is a file next to the deployed filetree root directory with the same name and **.origin** suffix, that contains exactly this info:
```
root@photon-host [ ~ ]# cat /ostree/deploy/photon/deploy/56ef687f1319604b7900a232715718d26ca407de7e1dc89251b206f8e255dcb4.0.origin 
[origin]
refspec=photon:photon/1.0/x86_64/minimal
```  
Fast forwarding a bit, if there is a new deployment due to an upgrade or rebase, a new filetree will be added at the same level, and a new .origin file will tie it to the remote branch it originated from.  

The **photon** directory in the path is the actual OSname. Multiple deployments of same OS will share a writable /var folder.  
```
root@photon-host [ ~ ]# ls -l /ostree/deploy/photon/var/
total 52
drwxr-xr-x  4 root root 4096 Jun  9 18:26 cache
drwxr-xr-x  2 root root 4096 Jun  9 18:26 home
drwxr-xr-x 13 root root 4096 Jun  9 18:26 lib
drwxr-xr-x  2 root root 4096 Jun  9 18:26 local
lrwxrwxrwx  1 root root   11 Jun  9 18:26 lock -> ../run/lock
drwxr-xr-x  3 root root 4096 Jun  9 18:26 log
drwxr-xr-x  2 root root 4096 Jun  9 18:26 mail
drwxr-xr-x  2 root root 4096 Jun  9 18:26 mnt
drwxr-xr-x  2 root root 4096 Jun  9 18:26 opt
drwx------  2 root root 4096 Jun 12 23:06 roothome
lrwxrwxrwx  1 root root    6 Jun  9 18:26 run -> ../run
drwxr-xr-x  2 root root 4096 Jun  9 18:26 spool
drwxr-xr-x  2 root root 4096 Jun  9 18:26 srv
drwxrwxrwt  4 root root 4096 Jun 12 23:04 tmp
drwxr-xr-x 11 root root 4096 Jun  9 18:26 usrlocal
```


