Now that we have a Photon RPM-OSTree server up and running (if not, see how to [[install|Photon-RPM-OSTree:-6-Installing-a-server]] one), we will learn how to provide the desired set of packages as input and instruct rpm-ostree to compose a filetree, that will result in creation (or update) of an OSTree repo.   
The simplest way to explain is to take a look at the files installed by the Photon RPM-OSTree server during setup.  
```  
root [ ~ ]# cd /srv/rpm-ostree/
root [ /srv/rpm-ostree ]# ls -l
total 16
lrwxrwxrwx 1 root root   31 Aug 28 19:06 lightwave-ostree.repo -> /etc/yum.repos.d/lightwave.repo
-rw-r--r-- 1 root root 7356 Aug 28 19:06 ostree-httpd.conf
-rw-r--r-- 1 root root 1085 Aug 28 19:06 photon-base.json
lrwxrwxrwx 1 root root   35 Aug 28 19:06 photon-extras-ostree.repo -> /etc/yum.repos.d/photon-extras.repo
lrwxrwxrwx 1 root root   32 Aug 28 19:06 photon-iso-ostree.repo -> /etc/yum.repos.d/photon-iso.repo
lrwxrwxrwx 1 root root   28 Aug 28 19:06 photon-ostree.repo -> /etc/yum.repos.d/photon.repo
lrwxrwxrwx 1 root root   36 Aug 28 19:06 photon-updates-ostree.repo -> /etc/yum.repos.d/photon-updates.repo
drwxr-xr-x 7 root root 4096 Aug 20 22:27 repo
```
### 9.1 JSON configuration file
How can we tell rpm-ostree what packages we want to include, where to get them from and how to compose the filetree? There is JSON file for that. Let's take a look at photon-base.json used by the Photon OS team.  
```
root [ /srv/rpm-ostree ]# cat photon-base.json 
{
    "comment": "Photon Minimal OSTree",

    "osname": "photon",

    "ref": "photon/1.0/x86_64/minimal",

    "automatic_version_prefix": "1.0_minimal",

    "repos": ["photon"],

    "selinux": false,

    "initramfs-args": ["--no-hostonly"],

    "bootstrap_packages": ["filesystem"],

    "packages": ["glibc", "zlib", "binutils", "gmp", "mpfr", "libgcc", "libstdc++","libgomp",
                "pkg-config", "ncurses", "bash", "bzip2", "cracklib", "cracklib-dicts", "shadow",
                "procps-ng", "iana-etc", "readline", "coreutils", "bc", "libtool", "inetutils",
                "findutils", "xz", "grub2", "iproute2", "util-linux", "linux",
                "attr", "libcap", "kmod", "expat", "dbus", "file",
                "sed", "grep", "cpio", "gzip",
                "openssl", "ca-certificates", "curl",
                "systemd",
                "openssh", "iptables",
                "photon-release",
                "vim", "tdnf",
                "docker","bridge-utils",
                "dracut", "dracut-tools", "rpm-ostree", "nss-altfiles", "which"]
}
``` 
There are some mandatory settings, some optional. I'm only going to explain the most important ones for our use case.  
**osname** and **ref** should be familiar, they have been explained in previous sections [[OSname|Photon-RPM-OStree:-3-Concepts-in-action#34-osname]] and [[Refspec|Photon-RPM-OStree:-3-Concepts-in-action#35-refspec]]. Basicaly, we are asking `rpm-ostree` to compose a tree for photon OS and photon/1.0/x86_64/minimal branch.

### 9.2 Package addition, removal, upgrade 
**packages** is the list of packages that are to be added, in this case, in the "minimal" installation profile, on top of the packages already included by default. This is not quite the identical set of RPMS you get when you select the minimal profile in the ISO installer, but it's pretty close and that's why it's been named the same. 
Let's add to the list three new packages: gawk, sudo and wget using `vim photon-base.json`

**!!!Warning: do not remove any packages from the default list, even an "innocent" one, as it may bring the system to an unstable condition.  During my testing, I've removed "which"; it turns out it was used to figure out the grub booting roots: on reboot, the system was left hanging at grub prompt.**

### 9.3 RPMS repository
But where are these packages located? RPM-OStree uses the same standard RPMS repositories, that yum installs from.
``` 
root [ /srv/rpm-ostree ]# ls /etc/yum.repos.d/
lightwave.repo  photon-iso.repo  photon-updates.repo  photon.repo
```
Going back to our JSON file, **repos** is a multi-value setting that tells RPM-OSTree in what RPMS repositories to look for packages. In this case, it looks in the current directory for a "photon" repo configuration file, that is a .repo file starting with a [photon] section. There is such a file: **photon-ostree.repo**, that is in fact a link to **photon.repo** in /etc/yum.repos.d directory.
``` 
root [ /srv/rpm-ostree ]# cat /etc/yum.repos.d/photon.repo 
[photon]
name=VMware Photon Linux 1.0(x86_64)
baseurl=https://dl.bintray.com/vmware/photon_release_1.0_x86_64
gpgkey=file:///etc/pki/rpm-gpg/VMWARE-RPM-GPG-KEY
gpgcheck=1
enabled=1
skip_if_unavailable=True
```
In this case, `rpm-ostree` is instructed to download its packages in RPM format from the bintray URL, that is the location of an online RPMS repo maintained by the WMware Photon OS team. To make sure those packages are genuine, signed by VMware, the signature is checked against the official VMware public key.

So what's in an RPMS repository? If we point the browser to https://dl.bintray.com/vmware/photon_release_1.0_x86_64, we can see there are three top directories:
* noarch - where all packages that don't depend on the architecture reside. Those may contain scripts, platform neutral source files, configuration.
* x86_64 - platform dependent packages for Intel 32 and 64 bits CPUs.
* repodata - internal repo management data, like a catalog of all packages, and for every package its name, id, version, architecture and full path file/directory list. There is also a compressed XML file containing the history of changelogs extracted from github, as packages in RPM format were built by Photon OS team members from sources.

Fortunately, in order to compose a tree, you don't need to download the packages from the online repository (which is time consuming - in the order of minutes), unless there are some new ones or updated versions of them, added by the Photon team after shipping 1.0 version or the 1.0 Refresh. A copy of the starter RPMS repository (as of 1.0 shipping date) has been included on the CD-ROM and you can access it.
```
root [ /srv/rpm-ostree ]# mount /dev/cdrom
root [ /srv/rpm-ostree ]# ls /mnt/cdrom/RPMS
noarch  repodata  x86_64
```
All you have to do now is to replace the `"repos": ["photon"]` entry by `"repos": ["photon-iso"]`, which will point to the RPMS repo on CD-ROM, rather than the online repo. This way, composing saves time, bandwidth and reduces to zero the risk of failure because of a networking issue. 

_**Note**_: Check from time to time if the [[known issue|Photon-RPM-OSTree:-Appendix-A:-Known-issues#error-composing-when-photon-iso-repo-is-selected]] has been fixed.
```
root [ /srv/rpm-ostree ]# cat /etc/yum.repos.d/photon-iso.repo 
[photon-iso]
name=VMWare Photon Linux 1.0(x86_64)
baseurl=file:///mnt/cdrom/RPMS
gpgkey=file:///etc/pki/rpm-gpg/VMWARE-RPM-GPG-KEY
gpgcheck=1
enabled=0
skip_if_unavailable=True
```

There are already in current directory links created to all repositories in /etc/yum.repos.d, so they are found when tree compose command is invoked. You may add any other repo to the list and include packages found in that repo to be part of the image. 


### 9.4 Composing a tree
After so much preparation, it's time to execute a tree compose. We've only added 3 new packages and changed the RPMS repo source. Assuming you've already edited the JSON file, let's do it.
```
root [ /srv/rpm-ostree ]# rpm-ostree compose tree --repo=repo photon-base.json
Previous commit: 2940e10c4d90ce6da572cbaeeff7b511cab4a64c280bd5969333dd2fca57cfa8

Downloading metadata [=========================================================================] 100%

Transaction: 117 packages
  Linux-PAM-1.1.8-2.ph1.x86_64
  attr-2.4.47-1.ph1.x86_64
  ...
  gawk-4.1.0-2.ph1.x86_64
  ...
  sudo-1.8.11p1-4.ph1.x86_64
  ...
  wget-1.15-1.ph1.x86_64
  which-2.20-1.ph1.x86_64
  xz-5.0.5-2.ph1.x86_64
  zlib-1.2.8-2.ph1.x86_64
Installing packages [==========================================================================] 100%
Writing '/var/tmp/rpm-ostree.TVO089/rootfs.tmp/usr/share/rpm-ostree/treefile.json'
Preparing kernel
Creating empty machine-id
Executing: /usr/bin/dracut -v --tmpdir=/tmp -f /var/tmp/initramfs.img 4.0.9 --no-hostonly
...
*** Including module: bash ***
*** Including module: kernel-modules ***
*** Including module: resume ***
*** Including module: rootfs-block ***
*** Including module: terminfo ***
*** Including module: udev-rules ***
Skipping udev rule: 91-permissions.rules
Skipping udev rule: 80-drivers-modprobe.rules
*** Including module: ostree ***
*** Including module: systemd ***
*** Including module: usrmount ***
*** Including module: base ***
/etc/os-release: line 1: Photon: command not found
*** Including module: fs-lib ***
*** Including module: shutdown ***
*** Including modules done ***
*** Installing kernel module dependencies and firmware ***
*** Installing kernel module dependencies and firmware done ***
*** Resolving executable dependencies ***
*** Resolving executable dependencies done***
*** Stripping files ***
*** Stripping files done ***
*** Store current command line parameters ***
*** Creating image file ***
*** Creating image file done ***
Image: /var/tmp/initramfs.img: 11M
========================================================================
Version: dracut-041-1.ph1

Arguments: -v --tmpdir '/tmp' -f --no-hostonly

dracut modules:
bash
kernel-modules
resume
rootfs-block
terminfo
udev-rules
ostree
systemd
usrmount
base
fs-lib
shutdown
========================================================================
drwxr-xr-x  12 root     root            0 Sep  1 00:52 .
crw-r--r--   1 root     root       5,   1 Sep  1 00:52 dev/console
crw-r--r--   1 root     root       1,  11 Sep  1 00:52 dev/kmsg
...   (long list of files removed)
========================================================================
Initializing rootfs
Migrating /etc/passwd to /usr/lib/
Migrating /etc/group to /usr/lib/
Moving /usr to target
Linking /usr/local -> ../var/usrlocal
Moving /etc to /usr/etc
Placing RPM db in /usr/share/rpm
Ignoring non-directory/non-symlink '/var/tmp/rpm-ostree.TVO089/rootfs.tmp/var/lib/nss_db/Makefile'
Ignoring non-directory/non-symlink '/var/tmp/rpm-ostree.TVO089/rootfs.tmp/var/cache/ldconfig/aux-cache'
Ignoring non-directory/non-symlink '/var/tmp/rpm-ostree.TVO089/rootfs.tmp/var/log/btmp'
Ignoring non-directory/non-symlink '/var/tmp/rpm-ostree.TVO089/rootfs.tmp/var/log/lastlog'
Ignoring non-directory/non-symlink '/var/tmp/rpm-ostree.TVO089/rootfs.tmp/var/log/wtmp'
Moving /boot
Using boot location: both
Copying toplevel compat symlinks
Adding tmpfiles-ostree-integration.conf
Committing '/var/tmp/rpm-ostree.TVO089/rootfs.tmp' ...
photon/1.0/x86_64/minimal => c505f4bddb4381e8b5213682465f1e5bb150a18228aa207d763cea45c6a81bbe
```
I've cut a big part of logging, but as you can see, the new filetree adds to the top of the previous (initial) commit 2940e10c4d and produces a new commit c505f4bddb. Our packages gawk-4.1.0-2.ph1.x86_64, sudo-1.8.11p1-4.ph1.x86_64 and wget-1.15-1.ph1.x86_64 have been added.  

During compose, `rpm-ostree` checks out the file tree into its uncompressed form, applies the package changes, places the updated RPM repo into /usr/share/rpm  and calls `ostree` to commit its changes back into the OSTree repo. If we were to look at the temp directory during this time:
```
root [ /srv/rpm-ostree ]# ls /var/tmp/rpm-ostree.TVO089/rootfs.tmp
bin   dev   lib    media  opt     proc  run   srv  sysroot  usr
boot  home  lib64  mnt    ostree  root  sbin  sys  tmp      var
```
If we repeat the command, and there is no change in the JSON file settings and no change in metadata, rpm-ostree will figure out that nothing has changed and stop. You can force however to redo the whole composition.
```
root [ /srv/rpm-ostree ]# rpm-ostree compose tree --repo=repo photon-base.json
Previous commit: c505f4bddb4381e8b5213682465f1e5bb150a18228aa207d763cea45c6a81bbe

Downloading metadata [=========================================================================] 100%


No apparent changes since previous commit; use --force-nocache to override
```

This takes several minutes. Then why is the RPM-OSTree server installing so fast, in 45 seconds on my SSD? The server doesn't compose the tree, it uses a pre-created OSTree repo that is stored on the CD-ROM. It comes of course at the expense of larger CD-ROM size. This OSTree repo is created from the same set of RPMS on the CD-ROM, so if you compose fresh, you will get the same exact tree, with same commit ID for the "minimal" ref. 


### 9.5 Automatic version prefix
If you recall the filetree version explained earlier, this is where it comes into play. When a tree is composed from scratch, the first version (0) associated to the initial commit is going to get that human readable value. Any subsequent compose operation will auto-increment to .1, .2, .3 and so on.  
It's a good idea to start a versionning scheme of your own, so that your customized Photon builds that may get different packages of your choice don't get the same version numbers as the official Photon team builds, coming from VMware's bintray OSTree repository. There is no conflict, it's just confusing to have same name for different commits coming from different repos!  
So if you work for a company named Big Data Inc., you may want to switch to a new versioning scheme `"automatic_version_prefix": "1.0_bigdata"`.


### 9.6 Installing package updates
If you want to provide hosts with the package updates that VMware periodically releases, all that you need to do is to add the photon-updates.repo to the list of repos in photon-base.json and then re-compose the usual way. 
```
"repos": ["photon", "photon-updates"],
```

Even though you may have not modified the "packages" section in the json file, the newer versions of existing packages will be included in the new image and then downloaded by the host the usual way. Note that upgrading a package shows differently than adding (+) or removing (-). You may still see packages added (or removed) though because they are new dependencies (or no longer dependencies) for the newer versions of other packages, as libssh2 in the example below.
```
root [ ~ ]# rpm-ostree upgrade --check-diff
Updating from: photon:photon/1.0/x86_64/minimal

8 metadata, 13 content objects fetched; 1002 KiB transferred in 0 seconds
!bridge-utils-1.5-2.ph1.x86_64
=bridge-utils-1.5-3.ph1.x86_64
!bzip2-1.0.6-5.ph1.x86_64
=bzip2-1.0.6-6.ph1.x86_64
!curl-7.47.1-2.ph1.x86_64
=curl-7.51.0-2.ph1.x86_64
!docker-1.11.0-5.ph1.x86_64
=docker-1.12.1-1.ph1.x86_64
...
+libssh2-1.8.0-1.ph1.x86_64
...

root [ ~ ]# rpm-ostree upgrade             
Updating from: photon:photon/1.0/x86_64/minimal

258 metadata, 1165 content objects fetched; 76893 KiB transferred in 8 seconds
Copying /etc changes: 6 modified, 0 removed, 14 added
Transaction complete; bootconfig swap: yes deployment count change: 1
Changed:
  bridge-utils 1.5-2.ph1 -> 1.5-3.ph1
  bzip2 1.0.6-5.ph1 -> 1.0.6-6.ph1
  curl 7.47.1-2.ph1 -> 7.51.0-2.ph1
  docker 1.11.0-5.ph1 -> 1.12.1-1.ph1
  ...
Added:
  libssh2-1.8.0-1.ph1.x86_64
Upgrade prepared for next boot; run "systemctl reboot" to start a reboot
```

Now if we want to see what packages have been updated and what issues have been fixed, just run at the host the command that we learned about in chapter 5.4.

```
root [ ~ ]# rpm-ostree db diff 56ef 396e
ostree diff commit old: 56e (56ef687f1319604b7900a232715718d26ca407de7e1dc89251b206f8e255dcb4)
ostree diff commit new: 396 (396e1116ad94692b8c105edaee4fa12447ec3d8f73c7b3ade4e955163d517497)
Upgraded:
 bridge-utils-1.5-3.ph1.x86_64
* Mon Sep 12 2016 Alexey Makhalov <amakhalov@vmware.com> 1.5-3
-	Update patch to fix-2.

 bzip2-1.0.6-6.ph1.x86_64
* Fri Oct 21 2016 Kumar Kaushik <kaushikk@vmware.com> 1.0.6-6
-       Fixing security bug CVE-2016-3189.

 curl-7.51.0-2.ph1.x86_64
* Wed Nov 30 2016 Xiaolin Li <xiaolinl@vmware.com> 7.51.0-2
-   Enable sftp support.

* Wed Nov 02 2016 Anish Swaminathan <anishs@vmware.com> 7.51.0-1
-   	Upgrade curl to 7.51.0

* Thu Oct 27 2016 Anish Swaminathan <anishs@vmware.com> 7.47.1-4
-   	Patch for CVE-2016-5421

* Mon Sep 19 2016 Xiaolin Li <xiaolinl@vmware.com> 7.47.1-3
-   	Applied CVE-2016-7167.patch.

 docker-1.12.1-1.ph1.x86_64
* Wed Sep 21 2016 Xiaolin Li <xiaolinl@vmware.com> 1.12.1-1
-   Upgraded to version 1.12.1

* Mon Aug 22 2016 Alexey Makhalov <amakhalov@vmware.com> 1.12.0-2
-   Added bash completion file

* Tue Aug 09 2016 Anish Swaminathan <anishs@vmware.com> 1.12.0-1
-   Upgraded to version 1.12.0

* Tue Jun 28 2016 Anish Swaminathan <anishs@vmware.com> 1.11.2-1
-   Upgraded to version 1.11.2
...
Added:
 libssh2-1.8.0-1.ph1.x86_64
``` 

### 9.7 Composing for a different branch
RPM-OSTree makes it very easy to create and update new branches, by composing using json config files that include the Refspec as the new branch name, the list of packages and the other settings we are now familiar with.  Photon OS 2.0 RPM-OSTRee Server installer adds two extra files photon-minimal.json and photon-full.json in addition to photon-base.json, that correspond almost identically to the minimal and full profiles installed via tdnf. It also makes 'photon-base' a smaller set of starter branch.  
Of course, you can create your own config files for your branches with desired lists of packages. You may compose on top of the existing tree, or you can [[start fresh your own OSTRee repo|Photon-RPM-OSTree:-8-File-oriented-server-operations#81-starting-a-fresh-ostree-repo]], using your own customized versioning.


[[Back to main page|Photon-RPM-OSTree:-a-simple-guide]] | [[Previous page|Photon-RPM-OSTree:-8-File-oriented-server-operations]]  | [[Next page >|Photon RPM-OSTree:-10-Remotes]]