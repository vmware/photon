There are several ostree and rpm-ostree commands that list file or package data based on either the Commit ID, or Refspec. If Refspec is passed as a parameter, it's the same as passing the most recent commit ID (head) for that branch.

### 4.1 Commit history
For a host that is freshly installed, there is only one commit in the history for the only branch.
```
root@photon-host [ ~ ]# ostree log photon/1.0/x86_64/minimal
commit 56ef687f1319604b7900a232715718d26ca407de7e1dc89251b206f8e255dcb4
Date:  2016-06-07 14:06:17 +0000
Version: 1.0_minimal
```
This commit has no parent; if there was an older commit, it would have been listed too. We can get the same listing (either nicely formatted or raw variant data) by passing the Commit ID. Just the first several hex digits will suffice to identify the commit ID. We can either request to be displayed in a pretty format, or raw - the actual C struct.
```
root@photon-host [ ~ ]# ostree log 56ef
commit 56ef687f1319604b7900a232715718d26ca407de7e1dc89251b206f8e255dcb4
Date:  2016-06-07 14:06:17 +0000
Version: 1.0_minimal
```
```
root@photon-host [ ~ ]# ostree log 56ef --raw
commit 56ef687f1319604b7900a232715718d26ca407de7e1dc89251b206f8e255dcb4
({'version': <'1.0_minimal'>, 'rpmostree.inputhash': <'40ae75453cf7f00b163848676c4b5716511e7515b95fb7b9168004aa97f05dd9'>}, @ay [], @a(say) [], '', '', uint64 1465308377, [byte 0x3c, 0x6b, 0x71, 0x44, 0x07, 0xd0, 0x5e, 0xd5, 0x9d, 0xfc, 0x4a, 0x1c, 0x33, 0x74, 0x96, 0x1d, 0x50, 0xa3, 0x53, 0xd5, 0xf1, 0x20, 0xb4, 0x40, 0xd0, 0x60, 0x35, 0xf2, 0xf8, 0x29, 0xcf, 0x5f], [byte 0x44, 0x6a, 0x0e, 0xf1, 0x1b, 0x7c, 0xc1, 0x67, 0xf3, 0xb6, 0x03, 0xe5, 0x85, 0xc7, 0xee, 0xee, 0xb6, 0x75, 0xfa, 0xa4, 0x12, 0xd5, 0xec, 0x73, 0xf6, 0x29, 0x88, 0xeb, 0x0b, 0x6c, 0x54, 0x88])
```

### 4.2 Listing file mappings
This command lists the file relations between the original source Linux Photon filetree and the deployed filetree. The normal columns include file type type (regular file, directory, link), permissions in chmod octal format, userID, groupID, file size, file name. 
```
root@photon-host [ ~ ]# ostree ls photon/1.0/x86_64/minimal
d00755 0 0      0 /
l00777 0 0      0 /bin -> usr/bin
l00777 0 0      0 /home -> var/home
l00777 0 0      0 /lib -> usr/lib
l00777 0 0      0 /lib64 -> usr/lib
l00777 0 0      0 /media -> run/media
l00777 0 0      0 /mnt -> var/mnt
l00777 0 0      0 /opt -> var/opt
l00777 0 0      0 /ostree -> sysroot/ostree
l00777 0 0      0 /root -> var/roothome
l00777 0 0      0 /sbin -> usr/sbin
l00777 0 0      0 /srv -> var/srv
l00777 0 0      0 /tmp -> sysroot/tmp
d00755 0 0      0 /boot
d00755 0 0      0 /dev
d00755 0 0      0 /proc
d00755 0 0      0 /run
d00755 0 0      0 /sys
d00755 0 0      0 /sysroot
d00755 0 0      0 /usr
d00755 0 0      0 /var
```
Extra columns can be added like checksum (-C) and extended attributes (-X). 
```
root@photon-host [ /usr/share/man/man1 ]# ostree ls photon/1.0/x86_64/minimal -C
d00755 0 0      0 3c6b714407d05ed59dfc4a1c3374961d50a353d5f120b440d06035f2f829cf5f 446a0ef11b7cc167f3b603e585c7eeeeb675faa412d5ec73f62988eb0b6c5488 /
l00777 0 0      0 389846c2702216e1367c8dfb68326a6b93ccf5703c89c93979052a9bf359608e /bin -> usr/bin
l00777 0 0      0 4344c10bf4931483f918496534f12ed9b50dc6a2cead35e3cd9dd898d6ac9414 /home -> var/home
l00777 0 0      0 f11902ca9d69a80df33918534a3e443251fd0aa7f94b76301e1f55e52aed29dd /lib -> usr/lib
l00777 0 0      0 f11902ca9d69a80df33918534a3e443251fd0aa7f94b76301e1f55e52aed29dd /lib64 -> usr/lib
l00777 0 0      0 75317a3df11447c470ffdd63dde045450ca97dfb2a97a0f3f6a21a5da66f737c /media -> run/media
l00777 0 0      0 97c55dbe24e8f3aecfd3f3e5b3f44646fccbb39799807d37a217e9c871da108b /mnt -> var/mnt
l00777 0 0      0 46b1abbd27a846a9257a8d8c9fc4b384ac0888bdb8ac0d6a2d5de72715bd5092 /opt -> var/opt
l00777 0 0      0 d37269e3f46023fd0275212473e07011894cdf4148cbf3fb5758a7e9471dad8e /ostree -> sysroot/ostree
l00777 0 0      0 6f800e74eed172661278d1e1f09e389a6504dcd3358618e1c1618f91f9d33601 /root -> var/roothome
l00777 0 0      0 e0bead7be9323b06bea05cb9b66eb151839989e3a4e5d1a93e09a36919e91818 /sbin -> usr/sbin
l00777 0 0      0 5d4250bba1ed300f793fa9769474351ee5cebd71e8339078af7ebfbe6256d9b5 /srv -> var/srv
l00777 0 0      0 364fbd62f91ca1e06eb7dbd50c93de8976f2cea633658e2dbe803ce6f7490c09 /tmp -> sysroot/tmp
d00755 0 0      0 1e4f98d92b35c453d8f61e668aea9fae7ca1863f6609db787374b4ad5caf3b2f 446a0ef11b7cc167f3b603e585c7eeeeb675faa412d5ec73f62988eb0b6c5488 /boot
d00755 0 0      0 6e340b9cffb37a989ca544e6bb780a2c78901d3fb33738768511a30617afa01d 446a0ef11b7cc167f3b603e585c7eeeeb675faa412d5ec73f62988eb0b6c5488 /dev
d00755 0 0      0 6e340b9cffb37a989ca544e6bb780a2c78901d3fb33738768511a30617afa01d 446a0ef11b7cc167f3b603e585c7eeeeb675faa412d5ec73f62988eb0b6c5488 /proc
d00755 0 0      0 6e340b9cffb37a989ca544e6bb780a2c78901d3fb33738768511a30617afa01d 446a0ef11b7cc167f3b603e585c7eeeeb675faa412d5ec73f62988eb0b6c5488 /run
d00755 0 0      0 6e340b9cffb37a989ca544e6bb780a2c78901d3fb33738768511a30617afa01d 446a0ef11b7cc167f3b603e585c7eeeeb675faa412d5ec73f62988eb0b6c5488 /sys
d00755 0 0      0 6e340b9cffb37a989ca544e6bb780a2c78901d3fb33738768511a30617afa01d 446a0ef11b7cc167f3b603e585c7eeeeb675faa412d5ec73f62988eb0b6c5488 /sysroot
d00755 0 0      0 b072f4b3e995a491c04d88636401ca156e80f103b002d724ae76c07174ee4c74 446a0ef11b7cc167f3b603e585c7eeeeb675faa412d5ec73f62988eb0b6c5488 /usr
d00755 0 0      0 6e340b9cffb37a989ca544e6bb780a2c78901d3fb33738768511a30617afa01d 446a0ef11b7cc167f3b603e585c7eeeeb675faa412d5ec73f62988eb0b6c5488 /var
```

By default, only the top folders are listed, but -R will list recursively. Instead of listing over 10,000 files, let's filter to just all files that contain 'rpm-ostree', 'rpmostree' or 'RpmOstree', that must belong to **rpm-ostree** package itself.
```
root@photon-host [ /usr/share/rpm-ostree ]# ostree ls photon/1.0/x86_64/minimal -R | grep -e '[Rr]pm-\?[Oo]stree'
l00777 0 0      0 /usr/bin/atomic -> rpm-ostree
-00755 0 0 131104 /usr/bin/rpm-ostree
l00777 0 0      0 /usr/lib/librpmostree-1.so.1 -> librpmostree-1.so.1.0.0
-00755 0 0 104272 /usr/lib/librpmostree-1.so.1.0.0
-00644 0 0   1296 /usr/lib/girepository-1.0/RpmOstree-1.0.typelib
d00755 0 0      0 /usr/lib/rpm-ostree
-00644 0 0    622 /usr/lib/rpm-ostree/tmpfiles-ostree-integration.conf
-00644 0 0    717 /usr/lib/tmpfiles.d/rpm-ostree-autovar.conf
d00755 0 0      0 /usr/share/rpm-ostree
-00644 0 0   1132 /usr/share/rpm-ostree/treefile.json
```

**atomic** is really an alias for rpm-ostree command. The last file **treefile.json** is not installed by the rpm-ostree package, it's actually downloaded from the server, as we will see in the next chapter. For now, let's notice **"osname" : "photon",  "ref" : "photon/1.0/x86_64/minimal",  "automatic_version_prefix" : "1.0_minimal"**, that matches what we've known so far, and also the **"documentation" : false** setting, that explains why there are no manual files installed for rpm-ostree, and in fact for any package.
```
root@photon-host [ /usr/share/rpm-ostree ]# ls -l /usr/share/man/man1 
total 0
```


### 4.3 Listing configuration changes

To diff the current /etc configuration versus default /etc (from the base image), this command will show the **M**odified, **A**dded and **D**eleted files:
```
root@photon-host [ ~ ]# ostree admin config-diff
M    mtab
M    ssh/sshd_config
M    shadow
M    hosts
M    fstab
M    machine-id
A    ssh/ssh_host_rsa_key
A    ssh/ssh_host_rsa_key.pub
A    ssh/ssh_host_dsa_key
A    ssh/ssh_host_dsa_key.pub
A    ssh/ssh_host_ecdsa_key
A    ssh/ssh_host_ecdsa_key.pub
A    ssh/ssh_host_ed25519_key
A    ssh/ssh_host_ed25519_key.pub
A    ssh/sshd.pid
A    tmpfiles.d/postinstall.sh
A    udev/hwdb.bin
A    resolv.conf
A    hostname
A    postinstall
A    localtime
A    .updated
```

### 4.4 Listing packages
As expected, there is an rpm-ostree command that lists all the packages for that branch, extracted from RPM database.   
```
root@photon-host [ ~ ]# rpm-ostree db list photon/1.0/x86_64/minimal
ostree commit: photon/1.0/x86_64/minimal (56ef687f1319604b7900a232715718d26ca407de7e1dc89251b206f8e255dcb4)
 Linux-PAM-1.2.1-3.ph1.x86_64
 attr-2.4.47-3.ph1.x86_64
 autogen-libopts-5.18.7-2.ph1.x86_64
 bash-4.3.30-4.ph1.x86_64
 bc-1.06.95-3.ph1.x86_64
 binutils-2.25.1-2.ph1.x86_64
 bridge-utils-1.5-2.ph1.x86_64
 bzip2-1.0.6-5.ph1.x86_64
 ca-certificates-20160109-5.ph1.x86_64
 coreutils-8.25-2.ph1.x86_64
 cpio-2.12-2.ph1.x86_64
 cracklib-2.9.6-2.ph1.x86_64
 cracklib-dicts-2.9.6-2.ph1.x86_64
 curl-7.47.1-2.ph1.x86_64
 db-6.1.26-2.ph1.x86_64
 dbus-1.8.8-5.ph1.x86_64
 device-mapper-2.02.141-5.ph1.x86_64
 device-mapper-libs-2.02.141-5.ph1.x86_64
 docker-1.11.0-5.ph1.x86_64
 dracut-044-3.ph1.x86_64
 dracut-tools-044-3.ph1.x86_64
 e2fsprogs-1.42.13-2.ph1.x86_64
 elfutils-libelf-0.165-2.ph1.x86_64
 expat-2.1.0-2.ph1.x86_64
 file-5.24-2.ph1.x86_64
 filesystem-1.0-7.ph1.x86_64
 findutils-4.6.0-2.ph1.x86_64
 flex-2.5.39-2.ph1.x86_64
 gdbm-1.11-2.ph1.x86_64
 glib-2.47.6-2.ph1.x86_64
 glib-networking-2.46.1-2.ph1.x86_64
 glibc-2.22-8.ph1.x86_64
 gmp-6.0.0a-3.ph1.x86_64
 gnutls-3.4.11-2.ph1.x86_64
 gobject-introspection-1.46.0-2.ph1.x86_64
 gpgme-1.6.0-2.ph1.x86_64
 grep-2.21-2.ph1.x86_64
 grub2-2.02-4.ph1.x86_64
 gzip-1.6-2.ph1.x86_64
 hawkey-2014.1-4.ph1.x86_64
 iana-etc-2.30-2.ph1.noarch
 iproute2-4.2.0-2.ph1.x86_64
 iptables-1.6.0-4.ph1.x86_64
 iputils-20151218-3.ph1.x86_64
 json-glib-1.0.4-2.ph1.x86_64
 kmod-21-4.ph1.x86_64
 krb5-1.14-4.ph1.x86_64
 libarchive-3.1.2-6.ph1.x86_64
 libassuan-2.4.2-2.ph1.x86_64
 libcap-2.25-2.ph1.x86_64
 libffi-3.2.1-2.ph1.x86_64
 libgcc-5.3.0-3.ph1.x86_64
 libgcrypt-1.6.5-2.ph1.x86_64
 libgomp-5.3.0-3.ph1.x86_64
 libgpg-error-1.21-2.ph1.x86_64
 libgsystem-2015.1-2.ph1.x86_64
 libhif-0.2.2-2.ph1.x86_64
 librepo-1.7.17-2.ph1.x86_64
 libselinux-2.5-2.ph1.x86_64
 libsepol-2.5-2.ph1.x86_64
 libsolv-0.6.19-2.ph1.x86_64
 libsoup-2.53.90-2.ph1.x86_64
 libstdc++-5.3.0-3.ph1.x86_64
 libtasn1-4.7-2.ph1.x86_64
 libtool-2.4.6-2.ph1.x86_64
 libxml2-2.9.4-1.ph1.x86_64
 linux-4.4.8-6.ph1.x86_64
 lua-5.3.2-2.ph1.x86_64
 m4-1.4.17-2.ph1.x86_64
 mkinitcpio-19-2.ph1.x86_64
 mpfr-3.1.3-2.ph1.x86_64
 ncurses-6.0-2.ph1.x86_64
 net-tools-1.60-7.ph1.x86_64
 nettle-3.2-2.ph1.x86_64
 nspr-4.12-2.ph1.x86_64
 nss-3.21-2.ph1.x86_64
 nss-altfiles-2.19.1-2.ph1.x86_64
 openssh-7.1p2-3.ph1.x86_64
 openssl-1.0.2h-2.ph1.x86_64
 ostree-2015.7-5.ph1.x86_64
 pcre-8.38-3.ph1.x86_64
 photon-release-1.0-5.ph1.noarch
 pkg-config-0.28-2.ph1.x86_64
 popt-1.16-2.ph1.x86_64
 procps-ng-3.3.11-2.ph1.x86_64
 python2-2.7.11-4.ph1.x86_64
 python2-libs-2.7.11-4.ph1.x86_64
 readline-6.3-4.ph1.x86_64
 rpm-4.11.2-10.ph1.x86_64
 rpm-ostree-2015.7-2.ph1.x86_64
 sed-4.2.2-2.ph1.x86_64
 shadow-4.2.1-7.ph1.x86_64
 sqlite-autoconf-3.11.0-2.ph1.x86_64
 systemd-228-21.ph1.x86_64
 tcsh-6.19.00-4.ph1.x86_64
 util-linux-2.27.1-2.ph1.x86_64
 vim-7.4-5.ph1.x86_64
 which-2.21-2.ph1.x86_64
 xz-5.2.2-2.ph1.x86_64
 zlib-1.2.8-3.ph1.x86_64
```

### 4.5 Querying for package details
We are able to use the query option of rpm to make sure any package have been installed properly. The files list should match the previous file mappings in 4.2, so let's check package **rpm-ostree**. As we've seen, manual files listed here are actually missing, they were not installed.
```
root@photon-host [ /usr/share/man/man1 ]# rpm -ql  rpm-ostree
/usr/bin/atomic
/usr/bin/rpm-ostree
/usr/lib/girepository-1.0/RpmOstree-1.0.typelib
/usr/lib/librpmostree-1.so.1
/usr/lib/librpmostree-1.so.1.0.0
/usr/lib/rpm-ostree
/usr/lib/rpm-ostree/tmpfiles-ostree-integration.conf
/usr/share/man/man1/atomic.1.gz
/usr/share/man/man1/rpm-ostree.1.gz
```
### 4.6 Why am I unable to install, update or delete packages?

All the commands executed so far operated in read-only mode. But what if you want to erase or install a package using our old friend rpm?
The RPM database is not writable any longer and the file system itself is read-only (except for /var and /etc directories). The idea is that preparing the packages should be done via server tree composition and deployment at host should bring them installed into a new bootable tree that is read-only, recorded into the read-only RPM database. This will insure that all systems deployed are brought into a predictable state and no one could mess with them.
In fact, tdnf and yum commands are not even available to install new packages at the host. Even if you bring them over, adding a new package via **tdnf install** will return an error.
But don't get sad. Installing, updating and deleting files & packages the RPM-OSTree way - from the server - that's exactly the topic of next chapters.

[[Back to main page|Photon-RPM-OSTree:-a-simple-guide]] | [[Previous page|Photon-RPM-OStree:-3-Concepts-in-action]]  | [[Next page >|Photon-RPM-OSTree:-5-Host-updating-operations]] 

