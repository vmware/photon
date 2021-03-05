---
title:  Concepts in Action
weight: 3
---

Now that we have a fresh installed host (either as [[default|Photon-RPM-OSTree:-2-Installing-a-host-against-default-server-repository]] or [[custom|Photon-RPM-OSTree:-7-Installing-a-host-against-a-custom-server-repository]]), I can explain better the OStree concepts and see them in action.  

## Querying the deployed filetrees

The first thing to do is to run a command that tells us what is installed on the machine and when. Since it's a fresh install from the CD, there is only one bootable filetree image deployed.
``` 
root@photon-host [ ~ ]# rpm-ostree status
  * ostree://photon:photon/3.0/x86_64/minimal
                   Version: 3.0_minimal (2019-08-29T11:20:19Z)
                    Commit: a31a843985e314a9e70bcf09afe8d59f7351817d9fb743c2b6dab84f20833650
```  
## Bootable filetree version

**3.0_minimal** is not the Linux Photon OS release version, nor daily build, but rather a human readable, self-incrementing version associated with every commit that brings file/package updates. Think of this as version 0. The following versions are going to be 3.0_minimal.1, 3.0_minimal.2, 3.0_minimal.3 and so on.

## Commit ID

The ID listed is actually the first 5 bytes (10 hex digits) of the commit hash. If you want to see the verbose mode, use the `-v` option.

```
root@photon-host [ ~ ]# rpm-ostree status -v
State: idle
AutomaticUpdates: disabled
Deployments:
* ostree://photon:photon/3.0/x86_64/minimal
                   Version: 3.0_minimal (2019-08-29T11:20:19Z)
                    Commit: a31a843985e314a9e70bcf09afe8d59f7351817d9fb743c2b6dab84f20833650
                            `- photon (2019-08-29T11:18:53Z)
                    Staged: no
                 StateRoot: photon
```

### RPM OStree Options

To see the list of options available with the rpm-ostree command, use the -h option.

```
root@photon-host [ ~ ]# rpm-ostree -h
Usage:
  rpm-ostree [OPTION?] COMMAND

Builtin Commands:
  compose          Commands to compose a tree
  cleanup          Clear cached/pending data
  db               Commands to query the RPM database
  deploy           Deploy a specific commit
  rebase           Switch to a different tree
  rollback         Revert to the previously booted tree
  status           Get the version of the booted system
  upgrade          Perform a system upgrade
  reload           Reload configuration
  usroverlay       Apply a transient overlayfs to /usr
  cancel           Cancel an active transaction
  initramfs        Enable or disable local initramfs regeneration
  install          Overlay additional packages
  uninstall        Remove overlayed additional packages
  override         Manage base package overrides
  reset            Remove all mutations
  refresh-md       Generate rpm repo metadata
  kargs            Query or modify kernel arguments

Help Options:
  -h, --help       Show help options

Application Options:
  --version        Print version information and exit
```  

## OSname

The OS Name identifies the operating system installed. All bootable filetrees for the same OS will share the /var directory, in other words applications installed in one booted image into this directory will be available in all other images.  
If a new set of images are created for a different OS, they will receive a fresh copy of /var that is not shared with the previous OS images for the initial OS. In other words, if a machine is dual boot for different operating systems, they will not share each other's /var content, however they will still merge 3-way /etc.

## Refspec

The **Refspec** is a branch inside the repo, expressed in a hierarchical way. In this case, it's the default branch that will receive package updates for the Photon OS 1.0 Minimal installation profile on Intel platforms. There could be other branches in the future, for example photon/3.0/x86_64/full that will match the Full installation profile (full set of packages installed).  
Think of Refspec as the head of the minimal branch (just like in git) at the origin repo. On the replicated, local repo at the host, **minimal** is a file that contains the latest commit ID known for that branch.  

```
root@photon-host [ ~ ]# cat /ostree/repo/refs/remotes/photon/photon/3.0/x86_64/minimal 
a31a843985e314a9e70bcf09afe8d59f7351817d9fb743c2b6dab84f20833650
```
Why are there two 'photon' directory levels in the remotes path? The **photon:** prefix in the Refspec listed by `rpm-ostree status` corresponds to the first **photon** directory in the remotes path and is actually the name given to the remote that the host is connected to, which points to an http or https URL. We'll talk about remotes later, but for now think of it as a namespace qualifier.  The second **photon** is part of the Refspec path itself.

## Deployments

We've used so far `rpm-ostree`. The same information can be obtained running an `ostree` command:

```
root@photon-host [ ~ ]# ostree admin status
* photon a31a843985e314a9e70bcf09afe8d59f7351817d9fb743c2b6dab84f20833650.0
    Version: 3.0_minimal
    origin refspec: photon:photon/3.0/x86_64/minimal
```

But where is this information stored? As you may have guessed, the local repo stores the heads of the deployed trees - the most recent commitment ID, just like Git does: 

```
root@photon-host [ ~ ]# cat /ostree/repo/refs/heads/ostree/0/1/0 
a31a843985e314a9e70bcf09afe8d59f7351817d9fb743c2b6dab84f20833650
```
This also where this command that lists the references (local heads and remotes) takes its data from:

```
root@photon-host [ ~ ]# ostree refs
ostree/0/1/0
photon:photon/3.0/x86_64/minimal
```
Based on that, it could find the root of the deployment that it boots from. The actual filetree is deployed right here:

```
root@photon-host [ ~ ]#  ls -l /ostree/deploy/photon/deploy/a31a843985e314a9e70bcf09afe8d59f7351817d9fb743c2b6dab84f20833650.0
total 36
lrwxrwxrwx  2 root root    7 Sep  4 04:58 bin -> usr/bin
drwxr-xr-x  2 root root 4096 Jan  1  1970 boot
drwxr-xr-x  2 root root 4096 Jan  1  1970 dev
drwxr-xr-x 34 root root 4096 Sep  4 05:00 etc
lrwxrwxrwx  2 root root    8 Sep  4 04:58 home -> var/home
lrwxrwxrwx  3 root root    7 Sep  4 04:58 lib -> usr/lib
lrwxrwxrwx  3 root root    7 Sep  4 04:58 lib64 -> usr/lib
lrwxrwxrwx  2 root root    9 Sep  4 04:58 media -> run/media
lrwxrwxrwx  2 root root    7 Sep  4 04:58 mnt -> var/mnt
lrwxrwxrwx  2 root root    7 Sep  4 04:58 opt -> var/opt
lrwxrwxrwx  2 root root   14 Sep  4 04:58 ostree -> sysroot/ostree
drwxr-xr-x  2 root root 4096 Jan  1  1970 proc
lrwxrwxrwx  2 root root   12 Sep  4 04:58 root -> var/roothome
drwxr-xr-x  2 root root 4096 Jan  1  1970 run
lrwxrwxrwx  2 root root    8 Sep  4 04:58 sbin -> usr/sbin
lrwxrwxrwx  2 root root    7 Sep  4 04:58 srv -> var/srv
drwxr-xr-x  2 root root 4096 Jan  1  1970 sys
drwxr-xr-x  2 root root 4096 Jan  1  1970 sysroot
lrwxrwxrwx  2 root root   11 Sep  4 04:58 tmp -> sysroot/tmp
drwxr-xr-x 10 root root 4096 Jan  1  1970 usr
drwxr-xr-x  8 root root 4096 Sep  4 04:59 var
```  

So how is a deployment linked to a specific branch, originating from a remote repo? Well, there is a file next to the deployed filetree root directory with the same name and **.origin** suffix, that contains exactly this info:

```
root@photon-host [ ~ ]# cat /ostree/deploy/photon/deploy/a31a843985e314a9e70bcf09afe8d59f7351817d9fb743c2b6dab84
f20833650.0.origin
[origin]
refspec=photon:photon/3.0/x86_64/minimal
```  

Fast forwarding a bit, if there is a new deployment due to an upgrade or rebase, a new filetree will be added at the same level, and a new .origin file will tie it to the remote branch it originated from.  

The **photon** directory in the path is the actual OSname. Multiple deployments of same OS will share a writable /var folder.

```
root@photon-host [ ~ ]# ls -l /ostree/deploy/photon/var/
total 52
drwxr-xr-x  4 root root 4096 Sep  4 05:00 cache
drwxr-xr-x  2 root root 4096 Sep  4 05:00 home
drwxr-xr-x 14 root root 4096 Sep  4 05:00 lib
drwxr-xr-x  2 root root 4096 Sep  4 05:00 local
lrwxrwxrwx  1 root root   11 Sep  4 04:59 lock -> ../run/lock
drwxr-xr-x  4 root root 4096 Sep  4 05:00 log
drwxr-xr-x  2 root root 4096 Sep  4 05:00 mail
drwxr-xr-x  2 root root 4096 Sep  4 05:00 mnt
drwxr-xr-x  4 root root 4096 Sep  4 05:00 opt
drwx------  3 root root 4096 Sep  4 05:25 roothome
lrwxrwxrwx  1 root root    6 Sep  4 04:59 run -> ../run
drwxr-xr-x  2 root root 4096 Sep  4 05:00 spool
drwxr-xr-x  2 root root 4096 Sep  4 05:00 srv
drwxrwxrwt  5 root root 4096 Sep  4 05:34 tmp
drwxr-xr-x 11 root root 4096 Sep  4 05:00 usrlocal
```


