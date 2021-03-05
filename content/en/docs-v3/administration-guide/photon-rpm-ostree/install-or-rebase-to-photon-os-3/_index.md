---
title:  Install or rebase to Photon OS 3.0
weight: 13
---

Photon OS 3.0 provides full RPM-OSTree functionality, it lets the user drive it, rather than provide a pre-defined solution as part of the installation.  

The number of packages included in the RPMS repo in Photon OS 3.0 increased significantly, compared to 1.0. To keep the ISO at reasonable size, Photon OS 2.0 no longer includes the compressed ostree.repo file, that helped optimize both the server and host install in 1.0 or 1.0 Rev2. That decision affected the OSTree features we ship out of the box. Customer could achieve the same results by several additional simple steps, that will be explained in this chapter. In addition, there is a new way to create a host raw image at server.

## Composing your own RPM-OSTree Server

You can compose your own RPM-OSTRee server in the following two ways:

1. By Manually executing the below command:
    ```
    root [ /srv/rpm-ostree ]# ostree --repo=repo init --mode=archive-z2
    root [ /srv/rpm-ostree ]# rpm-ostree compose tree --repo=repo photon-base.json
    ```

2. By installing `rpm-ostree-repo package` . This provides the script to create the repo tree which act as server by executing a single command.

## Installing an RPM-OSTree host

Automated host install is supported, as explained in [Chapter 7.2 Automated install of a custom host via kickstart](../installing-a-host-against-custom-server-repository/#automated-install-of-a-custom-host-via-kickstart).  

## Rebasing a host from Photon 1.0 to 3.0

If kickstart sounds too complicated and we still want to go the UI way there is a workaround that requires an extra step. Also, if you have an installed Photon 1.0 or 1.0 Rev2 that you want to carry to 3.0, you need to rebase it. Notice that I didn't say "upgrade".   

Basically the OSTree repo will switch to a different branch on a different server, following the new server's branch versioning scheme. The net result is that the lots of packages will get changed to newer versions from newer OSTree repo, that has been composed from a newer Photon OS 3.0 RPMS repo. Again, I didn't say "upgraded", neither the rebase command output, that lists "changed" packages. Some obsolete packages will be removed, new packages will be added, either because they didn't exist in 2.0 repo, or because the new config file includes them.  
The OS name is the same (Photon), so the content in /var and /etc will be transferred over.

1. To install fresh, deploy a Photon 1.0 Rev2 host default, as described in [Chapter 2](../installing-a-host-against-default-server-repository/). Of course, if you already have an existing Photon OS 1.0 host that you want to move to 2.0, skip this step.
2. Edit /ostree/repo/config and substitute the url, providing the IP address for the Photon OS 2.0 RPM-OSTree server installed above. This was explained in [Chapter 10](../remotes/#switching-repositories).  
ostree should confirm that is the updated server IP for the "photon" remote.
```
root@ostree-host [ ~ ]# ostree remote show-url photon
http://10.197.103.175:8000/repo
```
3. Rebase your host to the new 2.0 server and Refspec.

    ```
    root@ostree-host [ ~ ]# ostree remote add photon-2 http://10.197.103.204:8000/repo --no-gpg-verify
    root@ostree-host [ ~ ]# rpm-ostree rebase photon-2:photon/3.0/x86_64/minimal
    
    Rebasing to photon-2:photon/3.0/x86_64/minimal
    ⠉ Receiving objects: 99% (1541/1549) 478.3 kB/s 107.1 MB
    Receiving objects: 99% (1541/1549) 478.3 kB/s 107.1 MB... done
    Staging deployment... done
    Upgraded:
      docker 18.06.2-3.ph3 -> 18.06.2-4.ph3
      gmp 6.1.2-2.ph3 -> 6.1.2-3.ph3
      gobject-introspection 1.58.0-2.ph3 -> 1.58.0-3.ph3
      gzip 1.9-1.ph3 -> 1.9-2.ph3
      linux 4.19.65-3.ph3 -> 4.19.69-1.ph3
      mpfr 4.0.1-1.ph3 -> 4.0.1-2.ph3
      ostree 2019.2-1.ph3 -> 2019.2-2.ph3
      ostree-grub2 2019.2-1.ph3 -> 2019.2-2.ph3
      ostree-libs 2019.2-1.ph3 -> 2019.2-2.ph3
      zlib 1.2.11-1.ph3 -> 1.2.11-2.ph3
    Added:
      efibootmgr-15-1.ph3.x86_64
      efivar-36-1.ph3.x86_64
      tar-1.30-3.ph3.x86_64
    Run "systemctl reboot" to start a reboot
    ```
1. Check the status

    ```
    root@ostree-host [ ~ ]# rpm-ostree status
    State: idle
    AutomaticUpdates: disabled
    Deployments:
    * ostree://photon-1:photon/3.0/x86_64/minimal
                   Version: 3.0_minimal.2 (2019-09-18T08:22:15Z)
                BaseCommit: c8f2b116b067d7695f9033bf2a99505198269354e157c0f2d5b78266cb874239
           LayeredPackages: createrepo_c rpm wget

      ostree://photon:photon/1.0/x86_64/minimal
                   Version: 1.0_minimal.1 (2017-01-11T02:18:42)
                BaseCommit: 28dc49ecb4604c0bc349e4445adc659491a1874c01198e6253a261f4d59708b7
           LayeredPackages: createrepo_c rpm wget
    ```

You may now reboot to the new Photon OS 3.0 image.

## Creating a host raw image
It is now possible to run at server a script that is part of RPM-OStree package, to create a host raw mage.