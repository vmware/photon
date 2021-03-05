---
title:  Querying For Commit File and Package Metadata
weight: 4
---

There are several ostree and rpm-ostree commands that list file or package data based on either the Commit ID, or Refspec. If Refspec is passed as a parameter, it's the same as passing the most recent commit ID (head) for that branch.

## Commit history

For a host that is freshly installed, there is only one commit in the history for the only branch.

```
root@photon-host [ ~ ]# ostree log photon/3.0/x86_64/minimal
commit a31a843985e314a9e70bcf09afe8d59f7351817d9fb743c2b6dab84f20833650
ContentChecksum:  e91261daf8d60074f334a7ebf81d3b930c3fc88c765f994f79ab2445296f03c5
Date:  2019-08-29 11:20:19 +0000
Version: 3.0_minimal
```

This commit has no parent; if there was an older commit, it would have been listed too. We can get the same listing (either nicely formatted or raw variant data) by passing the Commit ID. Just the first several hex digits will suffice to identify the commit ID. We can either request to be displayed in a pretty format, or raw - the actual C struct.

```
root@photon-host [ ~ ]# ostree log a31a
commit a31a843985e314a9e70bcf09afe8d59f7351817d9fb743c2b6dab84f20833650
ContentChecksum:  e91261daf8d60074f334a7ebf81d3b930c3fc88c765f994f79ab2445296f03c5
Date:  2019-08-29 11:20:19 +0000
Version: 3.0_minimal
```

```
root@photon-host [ ~ ]# ostree log a31a --raw
commit a31a843985e314a9e70bcf09afe8d59f7351817d9fb743c2b6dab84f20833650
({'rpmostree.inputhash': <'a3e8f3f6ef6e93c2ed6ce9edd1e9e80c93a36ecda0fed0d78f607e6ec3179d04'>, 'rpmostree.rpmmd-repos': <[{'id': <'photon'>, 'timestamp': <uint64 1567077533>}]>, 'version': <'3.0_minimal'>, 'rpmostree.rpmdb.pkglist': <[('Linux-PAM', '0', '1.3.0', '1.ph3', 'x86_64'), ('attr', '0', '2.4.48', '1.ph3', 'x86_64'), ('autogen-libopts', '0', '5.18.16', '1.ph3', 'x86_64'), ('bash', '0', '4.4.18', '1.ph3', 'x86_64'), ('bc', '0', '1.07.1', '1.ph3', 'x86_64'), ('binutils', '0', '2.31.1', '6.ph3', 'x86_64'), ('bridge-utils', '0', '1.6', '1.ph3', 'x86_64'), ('bubblewrap', '0', '0.3.0', '2.ph3', 'x86_64'), ('bzip2', '0', '1.0.6', '10.ph3', 'x86_64'), ('bzip2-libs', '0', '1.0.6', '10.ph3', 'x86_64'), ('ca-certificates', '0', '20190521', '1.ph3', 'x86_64'), ('ca-certificates-pki', '0', '20190521', '1.ph3', 'x86_64'), ('coreutils', '0', '8.30', '1.ph3', 'x86_64'), ('cpio', '0', '2.12', '4.ph3', 'x86_64'), ('cracklib', '0', '2.9.6', '8.ph3', 'x86_64'), ('cracklib-dicts', '0', '2.9.6', '8.ph3', 'x86_64'), ('curl', '0', '7.61.1', '4.ph3', 'x86_64'), ('curl-libs', '0', '7.61.1', '4.ph3', 'x86_64'), ('dbus', '0', '1.13.6', '1.ph3', 'x86_64'), ('device-mapper', '0', '2.02.181', '1.ph3', 'x86_64'), ('device-mapper-libs', '0', '2.02.181', '1.ph3', 'x86_64'), ('docker', '0', '18.06.2', '3.ph3', 'x86_64'), ('dracut', '0', '048', '1.ph3', 'x86_64'), ('dracut-tools', '0', '048', '1.ph3', 'x86_64'), ('e2fsprogs-libs', '0', '1.44.3', '2.ph3', 'x86_64'), ('elfutils', '0', '0.176', '1.ph3', 'x86_64'), ('elfutils-libelf', '0', '0.176', '1.ph3', 'x86_64'), ('expat', '0', '2.2.6', '2.ph3', 'x86_64'), ('expat-libs', '0', '2.2.6', '2.ph3', 'x86_64'), ('file', '0', '5.34', '1.ph3', 'x86_64'), ('file-libs', '0', '5.34', '1.ph3', 'x86_64'), ('filesystem', '0', '1.1', '4.ph3', 'x86_64'), ('findutils', '0', '4.6.0', '5.ph3', 'x86_64'), ('flex', '0', '2.6.4', '2.ph3', 'x86_64'), ('fuse', '0', '2.9.7', '5.ph3', 'x86_64'), ('gc', '0', '8.0.0', '1.ph3', 'x86_64'), ('glib', '0', '2.58.0', '4.ph3', 'x86_64'), ('glib-networking', '0', '2.59.1', '2.ph3', 'x86_64'), ('glibc', '0', '2.28', '4.ph3', 'x86_64'), ('glibc-iconv', '0', '2.28', '4.ph3', 'x86_64'), ('gmp', '0', '6.1.2', '2.ph3', 'x86_64'), ('gnupg', '0', '2.2.17', '1.ph3', 'x86_64'), ('gnutls', '0', '3.6.3', '3.ph3', 'x86_64'), ('gobject-introspection', '0', '1.58.0', '2.ph3', 'x86_64'), ('gpgme', '0', '1.11.1', '2.ph3', 'x86_64'), ('grep', '0', '3.1', '1.ph3', 'x86_64'), ('grub2', '0', '2.02', '13.ph3', 'x86_64'), ('grub2-efi', '0', '2.02', '13.ph3', 'x86_64'), ('grub2-pc', '0', '2.02', '13.ph3', 'x86_64'), ('guile', '0', '2.0.13', '2.ph3', 'x86_64'), ('gzip', '0', '1.9', '1.ph3', 'x86_64'), ('iana-etc', '0', '2.30', '2.ph3', 'noarch'), ('icu', '0', '61.1', '1.ph3', 'x86_64'), ('iproute2', '0', '4.18.0', '2.ph3', 'x86_64'), ('iptables', '0', '1.8.3', '1.ph3', 'x86_64'), ('js', '0', '1.8.5', '2.ph3', 'x86_64'), ('json-c', '0', '0.13.1', '1.ph3', 'x86_64'), ('json-glib', '0', '1.4.4', '1.ph3', 'x86_64'), ('kmod', '0', '25', '1.ph3', 'x86_64'), ('krb5', '0', '1.17', '1.ph3', 'x86_64'), ('libapparmor', '0', '2.13', '7.ph3', 'x86_64'), ('libarchive', '0', '3.3.3', '3.ph3', 'x86_64'), ('libassuan', '0', '2.5.1', '1.ph3', 'x86_64'), ('libcap', '0', '2.25', '8.ph3', 'x86_64'), ('libdb', '0', '5.3.28', '2.ph3', 'x86_64'), ('libffi', '0', '3.2.1', '6.ph3', 'x86_64'), ('libgcc', '0', '7.3.0', '4.ph3', 'x86_64'), ('libgcrypt', '0', '1.8.3', '2.ph3', 'x86_64'), ('libgomp', '0', '7.3.0', '4.ph3', 'x86_64'), ('libgpg-error', '0', '1.32', '1.ph3', 'x86_64'), ('libgsystem', '0', '2015.2', '2.ph3', 'x86_64'), ('libksba', '0', '1.3.5', '1.ph3', 'x86_64'), ('libltdl', '0', '2.4.6', '3.ph3', 'x86_64'), ('libmodulemd', '0', '2.4.0', '1.ph3', 'x86_64'), ('libpsl', '0', '0.20.2', '1.ph3', 'x86_64'), ('librepo', '0', '1.10.2', '1.ph3', 'x86_64'), ('libseccomp', '0', '2.4.0', '1.ph3', 'x86_64'), ('libselinux', '0', '2.8', '1.ph3', 'x86_64'), ('libsepol', '0', '2.8', '1.ph3', 'x86_64'), ('libsolv', '0', '0.6.35', '1.ph3', 'x86_64'), ('libsoup', '0', '2.64.0', '2.ph3', 'x86_64'), ('libssh2', '0', '1.9.0', '1.ph3', 'x86_64'), ('libstdc++', '0', '7.3.0', '4.ph3', 'x86_64'), ('libtasn1', '0', '4.13', '1.ph3', 'x86_64'), ('libtool', '0', '2.4.6', '3.ph3', 'x86_64'), ('libunistring', '0', '0.9.10', '1.ph3', 'x86_64'), ('libxml2', '0', '2.9.9', '1.ph3', 'x86_64'), ('libyaml', '0', '0.2.1', '2.ph3', 'x86_64'), ('linux', '0', '4.19.65', '3.ph3', 'x86_64'), ('m4', '0', '1.4.18', '2.ph3', 'x86_64'), ('mpfr', '0', '4.0.1', '1.ph3', 'x86_64'), ('ncurses', '0', '6.1', '1.ph3', 'x86_64'), ('ncurses-libs', '0', '6.1', '1.ph3', 'x86_64'), ('ncurses-terminfo', '0', '6.1', '1.ph3', 'x86_64'), ('net-tools', '0', '1.60', '11.ph3', 'x86_64'), ('nettle', '0', '3.4', '1.ph3', 'x86_64'), ('npth', '0', '1.6', '1.ph3', 'x86_64'), ('nspr', '0', '4.21', '1.ph3', 'x86_64'), ('nss-altfiles', '0', '2.23.0', '1.ph3', 'x86_64'), ('nss-libs', '0', '3.44', '2.ph3', 'x86_64'), ('openssh', '0', '7.8p1', '5.ph3', 'x86_64'), ('openssh-clients', '0', '7.8p1', '5.ph3', 'x86_64'), ('openssh-server', '0', '7.8p1', '5.ph3', 'x86_64'), ('openssl', '0', '1.0.2s', '1.ph3', 'x86_64'), ('ostree', '0', '2019.2', '1.ph3', 'x86_64'), ('ostree-grub2', '0', '2019.2', '1.ph3', 'x86_64'), ('ostree-libs', '0', '2019.2', '1.ph3', 'x86_64'), ('pcre', '0', '8.42', '1.ph3', 'x86_64'), ('pcre-libs', '0', '8.42', '1.ph3', 'x86_64'), ('photon-release', '0', '3.0', '3.ph3', 'noarch'), ('photon-repos', '0', '3.0', '3.ph3', 'noarch'), ('pinentry', '0', '1.1.0', '1.ph3', 'x86_64'), ('pkg-config', '0', '0.29.2', '2.ph3', 'x86_64'), ('polkit', '0', '0.113', '5.ph3', 'x86_64'), ('popt', '0', '1.16', '5.ph3', 'x86_64'), ('procps-ng', '0', '3.3.15', '1.ph3', 'x86_64'), ('python3', '0', '3.7.3', '2.ph3', 'x86_64'), ('python3-libs', '0', '3.7.3', '2.ph3', 'x86_64'), ('readline', '0', '7.0', '2.ph3', 'x86_64'), ('rpm-libs', '0', '4.14.2', '4.ph3', 'x86_64'), ('rpm-ostree', '0', '2019.3', '1.ph3', 'x86_64'), ('sed', '0', '4.5', '1.ph3', 'x86_64'), ('shadow', '0', '4.6', '3.ph3', 'x86_64'), ('shadow-tools', '0', '4.6', '3.ph3', 'x86_64'), ('sqlite-libs', '0', '3.27.2', '3.ph3', 'x86_64'), ('systemd', '0', '239', '13.ph3', 'x86_64'), ('util-linux', '0', '2.32', '1.ph3', 'x86_64'), ('util-linux-libs', '0', '2.32', '1.ph3', 'x86_64'), ('vim', '0', '8.1.0388', '4.ph3', 'x86_64'), ('which', '0', '2.21', '5.ph3', 'x86_64'), ('xz', '0', '5.2.4', '1.ph3', 'x86_64'), ('xz-libs', '0', '5.2.4', '1.ph3', 'x86_64'), ('zchunk', '0', '1.1.1', '1.ph3', 'x86_64'), ('zchunk-libs', '0', '1.1.1', '1.ph3', 'x86_64'), ('zlib', '0', '1.2.11', '1.ph3', 'x86_64')]>}, @ay [], @a(say) [], '', '', uint64 1567077619, [byte 0x1e, 0x0a, 0x85, 0x20, 0xa8, 0xe0, 0x18, 0x6a, 0x88, 0x15, 0xc0, 0xd9, 0xb0, 0xab, 0xc9, 0x98, 0x94, 0xa1, 0xfb, 0x0a, 0x48, 0xdf, 0xa0, 0x73, 0x32, 0x02, 0x9a, 0xdf, 0x49, 0xed, 0x13, 0x8d], [byte 0x44, 0x6a, 0x0e, 0xf1, 0x1b, 0x7c, 0xc1, 0x67, 0xf3, 0xb6, 0x03, 0xe5, 0x85, 0xc7, 0xee, 0xee, 0xb6, 0x75, 0xfa, 0xa4, 0x12, 0xd5, 0xec, 0x73, 0xf6, 0x29, 0x88, 0xeb, 0x0b, 0x6c, 0x54, 0x88])
```

## Listing file mappings

This command lists the file relations between the original source Linux Photon filetree and the deployed filetree. The normal columns include file type type (regular file, directory, link), permissions in chmod octal format, userID, groupID, file size, file name. 
```
root@photon-host [ ~ ]# ostree ls photon/3.0/x86_64/minimal
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
root@photon-host [ /usr/share/man/man1 ]# ostree ls photon/3.0/x86_64/minimal -C
d00755 0 0      0 1e0a8520a8e0186a8815c0d9b0abc99894a1fb0a48dfa07332029adf49ed138d 446a0ef11b7cc167f3b603e585c7eeeeb675faa412d5ec73f62988eb0b6c5488 /
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
d00755 0 0      0 6e340b9cffb37a989ca544e6bb780a2c78901d3fb33738768511a30617afa01d 446a0ef11b7cc167f3b603e585c7eeeeb675faa412d5ec73f62988eb0b6c5488 /boot
d00755 0 0      0 6e340b9cffb37a989ca544e6bb780a2c78901d3fb33738768511a30617afa01d 446a0ef11b7cc167f3b603e585c7eeeeb675faa412d5ec73f62988eb0b6c5488 /dev
d00755 0 0      0 6e340b9cffb37a989ca544e6bb780a2c78901d3fb33738768511a30617afa01d 446a0ef11b7cc167f3b603e585c7eeeeb675faa412d5ec73f62988eb0b6c5488 /proc
d00755 0 0      0 6e340b9cffb37a989ca544e6bb780a2c78901d3fb33738768511a30617afa01d 446a0ef11b7cc167f3b603e585c7eeeeb675faa412d5ec73f62988eb0b6c5488 /run
d00755 0 0      0 6e340b9cffb37a989ca544e6bb780a2c78901d3fb33738768511a30617afa01d 446a0ef11b7cc167f3b603e585c7eeeeb675faa412d5ec73f62988eb0b6c5488 /sys
d00755 0 0      0 6e340b9cffb37a989ca544e6bb780a2c78901d3fb33738768511a30617afa01d 446a0ef11b7cc167f3b603e585c7eeeeb675faa412d5ec73f62988eb0b6c5488 /sysroot
d00755 0 0      0 ef1c0980e0d77f64e7f250a3e48f0b24e9285fc0716b80520dac6f98c148324a 446a0ef11b7cc167f3b603e585c7eeeeb675faa412d5ec73f62988eb0b6c5488 /usr
d00755 0 0      0 a3a987e053ea5a116f1e75a31cd7557fc6e57a3ae09e64171d7fea17ef71ec3e 446a0ef11b7cc167f3b603e585c7eeeeb675faa412d5ec73f62988eb0b6c5488 /var
```

By default, only the top folders are listed, but -R will list recursively. Instead of listing over 10,000 files, let's filter to just all files that contain 'rpm-ostree', 'rpmostree' or 'RpmOstree', that must belong to **rpm-ostree** package itself.

```
root@photon-host [ /usr/share/rpm-ostree ]# ostree ls photon/3.0/x86_64/minimal -R | grep -e '[Rr]pm-\?[Oo]stree'
-00755 0 0 749000 /usr/bin/rpm-ostree
d00755 0 0      0 /usr/bin/rpm-ostree-host
-00644 0 0   1069 /usr/bin/rpm-ostree-host/function.inc
-00755 0 0  10507 /usr/bin/rpm-ostree-host/mk-ostree-host.sh
-00644 0 0    209 /usr/etc/rpm-ostreed.conf
-00644 0 0   1530 /usr/etc/dbus-1/system.d/org.projectatomic.rpmostree1.conf
l00777 0 0      0 /usr/lib/librpmostree-1.so.1 -> librpmostree-1.so.1.0.0
-00755 0 0 5278496 /usr/lib/librpmostree-1.so.1.0.0
-00644 0 0   2312 /usr/lib/girepository-1.0/RpmOstree-1.0.typelib
-00755 0 0     22 /usr/lib/kernel/install.d/00-rpmostree-skip.install
d00755 0 0      0 /usr/lib/rpm-ostree
-00755 0 0 1640704 /usr/lib/rpm-ostree/libdnf.so.2
-00644 0 0    622 /usr/lib/rpm-ostree/rpm-ostree-0-integration.conf
d00755 0 0      0 /usr/lib/sysimage/rpm-ostree-base-db
-00644 0 0 544768 /usr/lib/sysimage/rpm-ostree-base-db/Basenames
-00644 0 0   8192 /usr/lib/sysimage/rpm-ostree-base-db/Conflictname
-00644 0 0 110592 /usr/lib/sysimage/rpm-ostree-base-db/Dirnames
-00644 0 0   8192 /usr/lib/sysimage/rpm-ostree-base-db/Enhancename
-00644 0 0   8192 /usr/lib/sysimage/rpm-ostree-base-db/Filetriggername
-00644 0 0   8192 /usr/lib/sysimage/rpm-ostree-base-db/Group
-00644 0 0  12288 /usr/lib/sysimage/rpm-ostree-base-db/Installtid
-00644 0 0   8192 /usr/lib/sysimage/rpm-ostree-base-db/Name
-00644 0 0   8192 /usr/lib/sysimage/rpm-ostree-base-db/Obsoletename
-00644 0 0 2625536 /usr/lib/sysimage/rpm-ostree-base-db/Packages
-00644 0 0  86016 /usr/lib/sysimage/rpm-ostree-base-db/Providename
-00644 0 0   8192 /usr/lib/sysimage/rpm-ostree-base-db/Recommendname
-00644 0 0  69632 /usr/lib/sysimage/rpm-ostree-base-db/Requirename
-00644 0 0  20480 /usr/lib/sysimage/rpm-ostree-base-db/Sha1header
-00644 0 0  16384 /usr/lib/sysimage/rpm-ostree-base-db/Sigmd5
-00644 0 0   8192 /usr/lib/sysimage/rpm-ostree-base-db/Suggestname
-00644 0 0   8192 /usr/lib/sysimage/rpm-ostree-base-db/Supplementname
-00644 0 0   8192 /usr/lib/sysimage/rpm-ostree-base-db/Transfiletriggername
-00644 0 0   8192 /usr/lib/sysimage/rpm-ostree-base-db/Triggername
-00644 0 0    263 /usr/lib/systemd/system/rpm-ostree-bootstatus.service
-00644 0 0    257 /usr/lib/systemd/system/rpm-ostreed-automatic.service
-00644 0 0    227 /usr/lib/systemd/system/rpm-ostreed-automatic.timer
-00644 0 0    272 /usr/lib/systemd/system/rpm-ostreed.service
-00644 0 0    102 /usr/lib/systemd/system-preset/40-rpm-ostree-auto.preset
-00644 0 0    622 /usr/lib/tmpfiles.d/rpm-ostree-0-integration.conf
-00644 0 0   1082 /usr/lib/tmpfiles.d/rpm-ostree-1-autovar.conf
-00755 0 0     53 /usr/libexec/rpm-ostreed
-00644 0 0   3049 /usr/share/bash-completion/completions/rpm-ostree
-00644 0 0  15997 /usr/share/dbus-1/interfaces/org.projectatomic.rpmostree1.xml
-00644 0 0    133 /usr/share/dbus-1/system-services/org.projectatomic.rpmostree1.service
-00644 0 0   6160 /usr/share/polkit-1/actions/org.projectatomic.rpmostree1.policy
d00755 0 0      0 /usr/share/rpm-ostree
-00644 0 0   1169 /usr/share/rpm-ostree/treefile.json
```

**atomic** is really an alias for rpm-ostree command. The last file **treefile.json** is not installed by the rpm-ostree package, it is actually downloaded from the server, as we will see in the next chapter. For now, let us notice **"osname" : "photon",  "ref" : "photon/1.0/x86_64/minimal",  "automatic_version_prefix" : "1.0_minimal"**, that matches what we have known so far, and also the **"documentation" : false** setting, that explains why there are no manual files installed for rpm-ostree, and in fact for any package.

```
root@photon-host [ /usr/share/rpm-ostree ]# ls -l /usr/share/man/man1 
total 0
```

## Listing configuration changes

To diff the current /etc configuration versus default /etc (from the base image), this command will show the **M**odified, **A**dded and **D**eleted files:
```
root@photon-host [ ~ ]# ostree admin config-diff
M    ssh/sshd_config
M    machine-id
M    fstab
M    hosts
M    mtab
M    shadow
A    ssh/ssh_host_rsa_key
A    ssh/ssh_host_rsa_key.pub
A    ssh/ssh_host_dsa_key
A    ssh/ssh_host_dsa_key.pub
A    ssh/ssh_host_ecdsa_key
A    ssh/ssh_host_ecdsa_key.pub
A    ssh/ssh_host_ed25519_key
A    ssh/ssh_host_ed25519_key.pub
A    udev/hwdb.bin
A    resolv.conf
A    hostname
A    localtime
A    .pwd.lock
A    .updated
```

## Listing packages

The following is the rpm-ostree command that lists all the packages for that branch, extracted from RPM database.   
```
root@photon-host [ ~ ]# rpm-ostree db list photon/3.0/x86_64/minimal
ostree commit: photon/3.0/x86_64/minimal (a31a843985e314a9e70bcf09afe8d59f7351817d9fb743c2b6dab84f20833650)
 Linux-PAM-1.3.0-1.ph3.x86_64
 attr-2.4.48-1.ph3.x86_64
 autogen-libopts-5.18.16-1.ph3.x86_64
 bash-4.4.18-1.ph3.x86_64
 bc-1.07.1-1.ph3.x86_64
 binutils-2.31.1-6.ph3.x86_64
 bridge-utils-1.6-1.ph3.x86_64
 bubblewrap-0.3.0-2.ph3.x86_64
 bzip2-1.0.6-10.ph3.x86_64
 bzip2-libs-1.0.6-10.ph3.x86_64
 ca-certificates-20190521-1.ph3.x86_64
 ca-certificates-pki-20190521-1.ph3.x86_64
 coreutils-8.30-1.ph3.x86_64
 cpio-2.12-4.ph3.x86_64
 cracklib-2.9.6-8.ph3.x86_64
 cracklib-dicts-2.9.6-8.ph3.x86_64
 curl-7.61.1-4.ph3.x86_64
 curl-libs-7.61.1-4.ph3.x86_64
 dbus-1.13.6-1.ph3.x86_64
 device-mapper-2.02.181-1.ph3.x86_64
 device-mapper-libs-2.02.181-1.ph3.x86_64
 docker-18.06.2-3.ph3.x86_64
 dracut-048-1.ph3.x86_64
 dracut-tools-048-1.ph3.x86_64
 e2fsprogs-libs-1.44.3-2.ph3.x86_64
 elfutils-0.176-1.ph3.x86_64
 elfutils-libelf-0.176-1.ph3.x86_64
 expat-2.2.6-2.ph3.x86_64
 expat-libs-2.2.6-2.ph3.x86_64
 file-5.34-1.ph3.x86_64
 file-libs-5.34-1.ph3.x86_64
 filesystem-1.1-4.ph3.x86_64
 findutils-4.6.0-5.ph3.x86_64
 flex-2.6.4-2.ph3.x86_64
 fuse-2.9.7-5.ph3.x86_64
 gc-8.0.0-1.ph3.x86_64
 glib-2.58.0-4.ph3.x86_64
 glib-networking-2.59.1-2.ph3.x86_64
 glibc-2.28-4.ph3.x86_64
 glibc-iconv-2.28-4.ph3.x86_64
 gmp-6.1.2-2.ph3.x86_64
 gnupg-2.2.17-1.ph3.x86_64
 gnutls-3.6.3-3.ph3.x86_64
 gobject-introspection-1.58.0-2.ph3.x86_64
 gpgme-1.11.1-2.ph3.x86_64
 grep-3.1-1.ph3.x86_64
 grub2-2.02-13.ph3.x86_64
 grub2-efi-2.02-13.ph3.x86_64
 grub2-pc-2.02-13.ph3.x86_64
 guile-2.0.13-2.ph3.x86_64
 gzip-1.9-1.ph3.x86_64
 iana-etc-2.30-2.ph3.noarch
 icu-61.1-1.ph3.x86_64
 iproute2-4.18.0-2.ph3.x86_64
 iptables-1.8.3-1.ph3.x86_64
 js-1.8.5-2.ph3.x86_64
 json-c-0.13.1-1.ph3.x86_64
 json-glib-1.4.4-1.ph3.x86_64
 kmod-25-1.ph3.x86_64
 krb5-1.17-1.ph3.x86_64
 libapparmor-2.13-7.ph3.x86_64
 libarchive-3.3.3-3.ph3.x86_64
 libassuan-2.5.1-1.ph3.x86_64
 libcap-2.25-8.ph3.x86_64
 libdb-5.3.28-2.ph3.x86_64
 libffi-3.2.1-6.ph3.x86_64
 libgcc-7.3.0-4.ph3.x86_64
 libgcrypt-1.8.3-2.ph3.x86_64
 libgomp-7.3.0-4.ph3.x86_64
 libgpg-error-1.32-1.ph3.x86_64
 libgsystem-2015.2-2.ph3.x86_64
 libksba-1.3.5-1.ph3.x86_64
 libltdl-2.4.6-3.ph3.x86_64
 libmodulemd-2.4.0-1.ph3.x86_64
 libpsl-0.20.2-1.ph3.x86_64
 librepo-1.10.2-1.ph3.x86_64
 libseccomp-2.4.0-1.ph3.x86_64
 libselinux-2.8-1.ph3.x86_64
 libsepol-2.8-1.ph3.x86_64
 libsolv-0.6.35-1.ph3.x86_64
 libsoup-2.64.0-2.ph3.x86_64
 libssh2-1.9.0-1.ph3.x86_64
 libstdc++-7.3.0-4.ph3.x86_64
 libtasn1-4.13-1.ph3.x86_64
 libtool-2.4.6-3.ph3.x86_64
 libunistring-0.9.10-1.ph3.x86_64
 libxml2-2.9.9-1.ph3.x86_64
 libyaml-0.2.1-2.ph3.x86_64
 linux-4.19.65-3.ph3.x86_64
 m4-1.4.18-2.ph3.x86_64
 mpfr-4.0.1-1.ph3.x86_64
 ncurses-6.1-1.ph3.x86_64
 ncurses-libs-6.1-1.ph3.x86_64
 ncurses-terminfo-6.1-1.ph3.x86_64
 net-tools-1.60-11.ph3.x86_64
 nettle-3.4-1.ph3.x86_64
 npth-1.6-1.ph3.x86_64
 nspr-4.21-1.ph3.x86_64
 nss-altfiles-2.23.0-1.ph3.x86_64
 nss-libs-3.44-2.ph3.x86_64
 openssh-7.8p1-5.ph3.x86_64
 openssh-clients-7.8p1-5.ph3.x86_64
 openssh-server-7.8p1-5.ph3.x86_64
 openssl-1.0.2s-1.ph3.x86_64
 ostree-2019.2-1.ph3.x86_64
 ostree-grub2-2019.2-1.ph3.x86_64
 ostree-libs-2019.2-1.ph3.x86_64
 pcre-8.42-1.ph3.x86_64
 pcre-libs-8.42-1.ph3.x86_64
 photon-release-3.0-3.ph3.noarch
 photon-repos-3.0-3.ph3.noarch
 pinentry-1.1.0-1.ph3.x86_64
 pkg-config-0.29.2-2.ph3.x86_64
 polkit-0.113-5.ph3.x86_64
 popt-1.16-5.ph3.x86_64
 procps-ng-3.3.15-1.ph3.x86_64
 python3-3.7.3-2.ph3.x86_64
 python3-libs-3.7.3-2.ph3.x86_64
 readline-7.0-2.ph3.x86_64
 rpm-libs-4.14.2-4.ph3.x86_64
 rpm-ostree-2019.3-1.ph3.x86_64
 sed-4.5-1.ph3.x86_64
 shadow-4.6-3.ph3.x86_64
 shadow-tools-4.6-3.ph3.x86_64
 sqlite-libs-3.27.2-3.ph3.x86_64
 systemd-239-13.ph3.x86_64
 util-linux-2.32-1.ph3.x86_64
 util-linux-libs-2.32-1.ph3.x86_64
 vim-8.1.0388-4.ph3.x86_64
 which-2.21-5.ph3.x86_64
 xz-5.2.4-1.ph3.x86_64
 xz-libs-5.2.4-1.ph3.x86_64
 zchunk-1.1.1-1.ph3.x86_64
 zchunk-libs-1.1.1-1.ph3.x86_64
 zlib-1.2.11-1.ph3.x86_64
```

## Querying for package details

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

## Why am I unable to install, upgrade or uninstall packages?

The OSTree host installer needs the server URL or the server repository. 

When you perform the installation using the repo, the install packages are located under the layer package.  When you install with the URL, the packages are located under the local packages.

You can use the `rpm-ostree uninstall` command to uninstall only the layered and local packages but not the base packages. To modify the base packages, you can use the `rpm-ostree override` command. 

When you run `rpm-ostree upgrade`, the command will only upgrade packages based on the commit available in the server.


