---
title:  Querying For Commit File and Package Metadata
weight: 4
---

There are several ostree and rpm-ostree commands that list file or package data based on either the Commit ID, or Refspec. If Refspec is passed as a parameter, it's the same as passing the most recent commit ID (head) for that branch.

## Commit history

For a host that is freshly installed, there is only one commit in the history for the only branch.
    
```console
root@photon-7c2d910d79e9 [ ~ ]# ostree log photon/4.0/x86_64/minimal
commit 820b584a6f90bf6b9b8cb6aad8c093064b88d0ab686be8130baa03d68917ad88
ContentChecksum:  c7956cedc5c1b8c07a06e10789c17364a5b7a4b970daab64f3398b7c42bd97d9
Date:  2020-11-04 02:21:47 +0000
Version: 4.0_minimal
(no subject)
```


This commit has no parent; if there was an older commit, it would have been listed too. We can get the same listing (either nicely formatted or raw variant data) by passing the Commit ID. Just the first several hex digits will suffice to identify the commit ID. We can either request to be displayed in a pretty format, or raw - the actual C struct.

```console
root@photon-7c2d910d79e9 [ ~ ]# ostree log 820b
commit 820b584a6f90bf6b9b8cb6aad8c093064b88d0ab686be8130baa03d68917ad88
ContentChecksum:  c7956cedc5c1b8c07a06e10789c17364a5b7a4b970daab64f3398b7c42bd97d9
Date:  2020-11-04 02:21:47 +0000
Version: 4.0_minimal
(no subject)
```

```console
root@photon-7c2d910d79e9 [ ~ ]# ostree log 820b --raw
commit 820b584a6f90bf6b9b8cb6aad8c093064b88d0ab686be8130baa03d68917ad88
({'rpmostree.inputhash': <'1ce3f6d518ec2cbaebc2de2ccb01888e59fc7efb482caba590bc96a604e54f82'>, 'rpmostree.rpmmd-repos': <[{'id': <'photon'>, 'timestamp': <uint64 1604456423>}]>, 'version': <'4.0_minimal'>, 'rpmostree.rpmdb.pkglist': <[('Linux-PAM', '0', '1.4.0', '2.ph4', 'x86_64'), ('attr', '0', '2.4.48', '1.ph4', 'x86_64'), ('audit', '0', '2.8.5', '3.ph4', 'x86_64'), ('autogen-libopts', '0', '5.18.16', '3.ph4', 'x86_64'), ('bash', '0', '5.0', '1.ph4', 'x86_64'), ('bc', '0', '1.07.1', '4.ph4', 'x86_64'), ('bridge-utils', '0', '1.6', '1.ph4', 'x86_64'), ('bubblewrap', '0', '0.4.1', '1.ph4', 'x86_64'), ('bzip2', '0', '1.0.8', '3.ph4', 'x86_64'), ('bzip2-libs', '0', '1.0.8', '3.ph4', 'x86_64'), ('ca-certificates', '0', '20201001', '1.ph4', 'x86_64'), ('ca-certificates-pki', '0', '20201001', '1.ph4', 'x86_64'), ('cloud-init', '0', '20.3', '2.ph4', 'noarch'), ('coreutils-selinux', '0', '8.32', '2.ph4', 'x86_64'), ('cpio', '0', '2.13', '1.ph4', 'x86_64'), ('cracklib', '0', '2.9.7', '1.ph4', 'x86_64'), ('cracklib-dicts', '0', '2.9.7', '1.ph4', 'x86_64'), ('curl', '0', '7.72.0', '2.ph4', 'x86_64'), ('curl-libs', '0', '7.72.0', '2.ph4', 'x86_64'), ('cyrus-sasl', '0', '2.1.27', '3.ph4', 'x86_64'), ('dbus', '0', '1.13.18', '1.ph4', 'x86_64'), ('device-mapper', '0', '2.03.10', '2.ph4', 'x86_64'), ('device-mapper-libs', '0', '2.03.10', '2.ph4', 'x86_64'), ('dhcp-client', '0', '4.4.2', '1.ph4', 'x86_64'), ('dhcp-libs', '0', '4.4.2', '1.ph4', 'x86_64'), ('dracut', '0', '050', '5.ph4', 'x86_64'), ('dracut-tools', '0', '050', '5.ph4', 'x86_64'), ('e2fsprogs', '0', '1.45.6', '2.ph4', 'x86_64'), ('e2fsprogs-libs', '0', '1.45.6', '2.ph4', 'x86_64'), ('elfutils', '0', '0.181', '2.ph4', 'x86_64'), ('elfutils-libelf', '0', '0.181', '2.ph4', 'x86_64'), ('expat', '0', '2.2.9', '2.ph4', 'x86_64'), ('expat-libs', '0', '2.2.9', '2.ph4', 'x86_64'), ('file', '0', '5.39', '1.ph4', 'x86_64'), ('file-libs', '0', '5.39', '1.ph4', 'x86_64'), ('filesystem', '0', '1.1', '4.ph4', 'x86_64'), ('findutils', '0', '4.7.0', '1.ph4', 'x86_64'), ('finger', '0', '0.17', '3.ph4', 'x86_64'), ('flex', '0', '2.6.4', '3.ph4', 'x86_64'), ('fuse', '0', '2.9.9', '1.ph4', 'x86_64'), ('gawk', '0', '5.1.0', '1.ph4', 'x86_64'), ('gc', '0', '8.0.4', '1.ph4', 'x86_64'), ('gdbm', '0', '1.18.1', '1.ph4', 'x86_64'), ('glib', '0', '2.66.1', '1.ph4', 'x86_64'), ('glib-networking', '0', '2.66.0', '1.ph4', 'x86_64'), ('glibc', '0', '2.32', '1.ph4', 'x86_64'), ('glibc-iconv', '0', '2.32', '1.ph4', 'x86_64'), ('gmp', '0', '6.2.0', '1.ph4', 'x86_64'), ('gnupg', '0', '2.2.23', '1.ph4', 'x86_64'), ('gnutls', '0', '3.6.15', '3.ph4', 'x86_64'), ('gobject-introspection', '0', '1.66.0', '1.ph4', 'x86_64'), ('gpgme', '0', '1.14.0', '1.ph4', 'x86_64'), ('grep', '0', '3.4', '1.ph4', 'x86_64'), ('grub2', '0', '2.04', '2.ph4', 'x86_64'), ('grub2-efi', '0', '2.04', '2.ph4', 'x86_64'), ('grub2-efi-image', '0', '2.04', '2.ph4', 'x86_64'), ('grub2-pc', '0', '2.04', '2.ph4', 'x86_64'), ('grub2-theme', '0', '4.0', '1.ph4', 'noarch'), ('grub2-theme-ostree', '0', '4.0', '1.ph4', 'noarch'), ('guile', '0', '2.0.13', '3.ph4', 'x86_64'), ('gzip', '0', '1.10', '1.ph4', 'x86_64'), ('iana-etc', '0', '2.30', '2.ph4', 'noarch'), ('icu', '0', '67.1', '1.ph4', 'x86_64'), ('iproute2', '0', '5.8.0', '1.ph4', 'x86_64'), ('iptables', '0', '1.8.4', '1.ph4', 'x86_64'), ('iputils', '0', '20200821', '1.ph4', 'x86_64'), ('json-c', '0', '0.15', '2.ph4', 'x86_64'), ('json-glib', '0', '1.6.0', '1.ph4', 'x86_64'), ('kmod', '0', '27', '1.ph4', 'x86_64'), ('krb5', '0', '1.17', '4.ph4', 'x86_64'), ('libacl', '0', '2.2.53', '1.ph4', 'x86_64'), ('libarchive', '0', '3.4.3', '3.ph4', 'x86_64'), ('libassuan', '0', '2.5.3', '1.ph4', 'x86_64'), ('libcap', '0', '2.43', '1.ph4', 'x86_64'), ('libcap-ng', '0', '0.8', '1.ph4', 'x86_64'), ('libdb', '0', '5.3.28', '2.ph4', 'x86_64'), ('libdnet', '0', '1.11', '7.ph4', 'x86_64'), ('libffi', '0', '3.3', '1.ph4', 'x86_64'), ('libgcc', '0', '8.4.0', '1.ph4', 'x86_64'), ('libgcrypt', '0', '1.8.6', '2.ph4', 'x86_64'), ('libgpg-error', '0', '1.39', '1.ph4', 'x86_64'), ('libgpg-error-devel', '0', '1.39', '1.ph4', 'x86_64'), ('libksba', '0', '1.4.0', '1.ph4', 'x86_64'), ('libltdl', '0', '2.4.6', '3.ph4', 'x86_64'), ('libmetalink', '0', '0.1.3', '2.ph4', 'x86_64'), ('libmicrohttpd', '0', '0.9.71', '2.ph4', 'x86_64'), ('libmodulemd', '0', '2.9.4', '1.ph4', 'x86_64'), ('libmspack', '0', '0.10.1alpha', '1.ph4', 'x86_64'), ('libnsl', '0', '1.3.0', '1.ph4', 'x86_64'), ('libpsl', '0', '0.21.1', '1.ph4', 'x86_64'), ('libpwquality', '0', '1.4.2', '1.ph4', 'x86_64'), ('librepo', '0', '1.12.1', '3.ph4', 'x86_64'), ('libseccomp', '0', '2.5.0', '2.ph4', 'x86_64'), ('libselinux', '0', '3.1', '1.ph4', 'x86_64'), ('libsemanage', '0', '3.1', '1.ph4', 'x86_64'), ('libsepol', '0', '3.1', '1.ph4', 'x86_64'), ('libsolv', '0', '0.6.35', '5.ph4', 'x86_64'), ('libsoup', '0', '2.72.0', '1.ph4', 'x86_64'), ('libssh2', '0', '1.9.0', '2.ph4', 'x86_64'), ('libstdc++', '0', '8.4.0', '1.ph4', 'x86_64'), ('libtasn1', '0', '4.14', '1.ph4', 'x86_64'), ('libtirpc', '0', '1.2.6', '1.ph4', 'x86_64'), ('libtool', '0', '2.4.6', '3.ph4', 'x86_64'), ('libunistring', '0', '0.9.10', '1.ph4', 'x86_64'), ('libxml2', '0', '2.9.10', '3.ph4', 'x86_64'), ('libxml2-devel', '0', '2.9.10', '3.ph4', 'x86_64'), ('libxslt', '0', '1.1.34', '1.ph4', 'x86_64'), ('libyaml', '0', '0.2.5', '1.ph4', 'x86_64'), ('linux', '0', '5.9.0', '3.ph4', 'x86_64'), ('lua', '0', '5.3.5', '1.ph4', 'x86_64'), ('lz4', '0', '1.9.2', '1.ph4', 'x86_64'), ('m4', '0', '1.4.18', '3.ph4', 'x86_64'), ('motd', '0', '0.1.3', '6.ph4', 'noarch'), ('mozjs', '0', '78.3.1', '1.ph4', 'x86_64'), ('mpfr', '0', '4.1.0', '1.ph4', 'x86_64'), ('ncurses', '0', '6.2', '2.ph4', 'x86_64'), ('ncurses-libs', '0', '6.2', '2.ph4', 'x86_64'), ('ncurses-terminfo', '0', '6.2', '2.ph4', 'x86_64'), ('net-tools', '0', '1.60', '12.ph4', 'x86_64'), ('nettle', '0', '3.6', '1.ph4', 'x86_64'), ('npth', '0', '1.6', '1.ph4', 'x86_64'), ('nspr', '0', '4.29', '1.ph4', 'x86_64'), ('nss', '0', '3.57', '1.ph4', 'x86_64'), ('nss-altfiles', '0', '2.23.0', '1.ph4', 'x86_64'), ('nss-libs', '0', '3.57', '1.ph4', 'x86_64'), ('open-vm-tools', '0', '11.1.5', '4.ph4', 'x86_64'), ('openldap', '0', '2.4.53', '2.ph4', 'x86_64'), ('openssh', '0', '8.4p1', '2.ph4', 'x86_64'), ('openssh-clients', '0', '8.4p1', '2.ph4', 'x86_64'), ('openssh-server', '0', '8.4p1', '2.ph4', 'x86_64'), ('openssl', '0', '1.1.1g', '3.ph4', 'x86_64'), ('ostree', '0', '2020.6', '1.ph4', 'x86_64'), ('ostree-grub2', '0', '2020.6', '1.ph4', 'x86_64'), ('ostree-libs', '0', '2020.6', '1.ph4', 'x86_64'), ('pcre', '0', '8.44', '1.ph4', 'x86_64'), ('pcre-libs', '0', '8.44', '1.ph4', 'x86_64'), ('photon-release', '0', '4.0', '1.ph4', 'noarch'), ('photon-repos', '0', '4.0', '1.ph4', 'noarch'), ('pinentry', '0', '1.1.0', '1.ph4', 'x86_64'), ('pkg-config', '0', '0.29.2', '3.ph4', 'x86_64'), ('policycoreutils', '0', '3.1', '1.ph4', 'x86_64'), ('polkit', '0', '0.118', '1.ph4', 'x86_64'), ('popt', '0', '1.16', '5.ph4', 'x86_64'), ('procps-ng', '0', '3.3.16', '1.ph4', 'x86_64'), ('python3', '0', '3.8.6', '1.ph4', 'x86_64'), ('python3-PyYAML', '0', '5.3.1', '1.ph4', 'x86_64'), ('python3-asn1crypto', '0', '1.4.0', '1.ph4', 'noarch'), ('python3-attrs', '0', '20.2.0', '2.ph4', 'noarch'), ('python3-certifi', '0', '2020.6.20', '1.ph4', 'noarch'), ('python3-cffi', '0', '1.14.3', '2.ph4', 'x86_64'), ('python3-chardet', '0', '3.0.4', '2.ph4', 'noarch'), ('python3-configobj', '0', '5.0.6', '5.ph4', 'noarch'), ('python3-cryptography', '0', '3.1.1', '2.ph4', 'x86_64'), ('python3-gobject-introspection', '0', '1.66.0', '1.ph4', 'x86_64'), ('python3-idna', '0', '2.10', '1.ph4', 'noarch'), ('python3-jinja2', '0', '2.11.2', '1.ph4', 'noarch'), ('python3-jsonpatch', '0', '1.26', '1.ph4', 'noarch'), ('python3-jsonpointer', '0', '2.0', '2.ph4', 'noarch'), ('python3-jsonschema', '0', '3.2.0', '1.ph4', 'noarch'), ('python3-libs', '0', '3.8.6', '1.ph4', 'x86_64'), ('python3-markupsafe', '0', '1.1.1', '1.ph4', 'x86_64'), ('python3-netifaces', '0', '0.10.9', '2.ph4', 'x86_64'), ('python3-oauthlib', '0', '3.1.0', '1.ph4', 'noarch'), ('python3-packaging', '0', '20.4', '2.ph4', 'noarch'), ('python3-prettytable', '0', '0.7.2', '7.ph4', 'noarch'), ('python3-pyOpenSSL', '0', '19.1.0', '2.ph4', 'noarch'), ('python3-pyasn1', '0', '0.4.8', '1.ph4', 'noarch'), ('python3-pycparser', '0', '2.20', '1.ph4', 'noarch'), ('python3-pyparsing', '0', '2.4.7', '1.ph4', 'noarch'), ('python3-pyrsistent', '0', '0.17.3', '1.ph4', 'x86_64'), ('python3-requests', '0', '2.24.0', '1.ph4', 'noarch'), ('python3-setuptools', '0', '3.8.6', '1.ph4', 'noarch'), ('python3-six', '0', '1.15.0', '2.ph4', 'noarch'), ('python3-urllib3', '0', '1.25.10', '2.ph4', 'noarch'), ('python3-xml', '0', '3.8.6', '1.ph4', 'x86_64'), ('readline', '0', '7.0', '3.ph4', 'x86_64'), ('rpcsvc-proto', '0', '1.4.2', '1.ph4', 'x86_64'), ('rpm', '0', '4.14.2', '11.ph4', 'x86_64'), ('rpm-libs', '0', '4.14.2', '11.ph4', 'x86_64'), ('rpm-ostree', '0', '2020.5', '4.ph4', 'x86_64'), ('sed', '0', '4.8', '1.ph4', 'x86_64'), ('selinux-policy', '0', '3.14.7', '1.ph4', 'noarch'), ('shadow', '0', '4.8.1', '2.ph4', 'x86_64'), ('shadow-tools', '0', '4.8.1', '2.ph4', 'x86_64'), ('shim-signed', '0', '15', '1.ph4', 'x86_64'), ('sqlite-libs', '0', '3.33.0', '1.ph4', 'x86_64'), ('sudo', '0', '1.8.30', '2.ph4', 'x86_64'), ('systemd', '0', '245.5', '3.ph4', 'x86_64'), ('tcp_wrappers', '0', '7.6', '7.ph4', 'x86_64'), ('tzdata', '0', '2020a', '1.ph4', 'noarch'), ('util-linux', '0', '2.36', '1.ph4', 'x86_64'), ('util-linux-libs', '0', '2.36', '1.ph4', 'x86_64'), ('vim', '0', '8.2.1361', '1.ph4', 'x86_64'), ('which', '0', '2.21', '6.ph4', 'x86_64'), ('xmlsec1', '0', '1.2.30', '3.ph4', 'x86_64'), ('xz', '0', '5.2.5', '1.ph4', 'x86_64'), ('xz-libs', '0', '5.2.5', '1.ph4', 'x86_64'), ('zchunk', '0', '1.1.7', '1.ph4', 'x86_64'), ('zchunk-libs', '0', '1.1.7', '1.ph4', 'x86_64'), ('zlib', '0', '1.2.11', '2.ph4', 'x86_64'), ('zstd', '0', '1.4.5', '2.ph4', 'x86_64'), ('zstd-libs', '0', '1.4.5', '2.ph4', 'x86_64')]>}, @ay [], @a(say) [], '', '', uint64 1604456507, [byte 0xca, 0x99, 0x35, 0xe5, 0xaa, 0xc6, 0xbd, 0xb3, 0x52, 0xb4, 0x81, 0x62, 0xbb, 0x3f, 0xba, 0x44, 0x0e, 0x3c, 0xa0, 0x00, 0xc8, 0x6f, 0x7c, 0x32, 0xa0, 0xa0, 0x8b, 0xc6, 0xf0, 0xd5, 0x06, 0x0e], [byte 0x44, 0x6a, 0x0e, 0xf1, 0x1b, 0x7c, 0xc1, 0x67, 0xf3, 0xb6, 0x03, 0xe5, 0x85, 0xc7, 0xee, 0xee, 0xb6, 0x75, 0xfa, 0xa4, 0x12, 0xd5, 0xec, 0x73, 0xf6, 0x29, 0x88, 0xeb, 0x0b, 0x6c, 0x54, 0x88])
```


## Listing file mappings

This command lists the file relations between the original source Linux Photon filetree and the deployed filetree. The normal columns include file type type (regular file, directory, link), permissions in chmod octal format, userID, groupID, file size, file name. 

```console
root@photon-7c2d910d79e9 [ ~ ]# ostree ls photon/4.0/x86_64/minimal
d00755 0 0  0 /
l00777 0 0  0 /bin -> usr/bin
l00777 0 0  0 /home -> var/home
l00777 0 0  0 /lib -> usr/lib
l00777 0 0  0 /lib64 -> usr/lib
l00777 0 0  0 /media -> run/media
l00777 0 0  0 /mnt -> var/mnt
l00777 0 0  0 /opt -> var/opt
l00777 0 0  0 /ostree -> sysroot/ostree
l00777 0 0  0 /root -> var/roothome
l00777 0 0  0 /sbin -> usr/sbin
l00777 0 0  0 /srv -> var/srv
l00777 0 0  0 /tmp -> sysroot/tmp
d00755 0 0  0 /boot
d00755 0 0  0 /dev
d00755 0 0  0 /proc
d00755 0 0  0 /run
d00755 0 0  0 /sys
d00755 0 0  0 /sysroot
d00755 0 0  0 /usr
d00755 0 0  0 /var
```

Extra columns can be added like checksum (-C) and extended attributes (-X). 

```console
root@photon-7c2d910d79e9 [ ~ ]# ostree ls photon/4.0/x86_64/minimal -C
d00755 0 0  0 ca9935e5aac6bdb352b48162bb3fba440e3ca000c86f7c32a0a08bc6f0d5060e 446a0ef11b7cc167f3b603e585c7eeeeb675faa412d5ec73f62988eb0b6c5488 /
l00777 0 0  0 389846c2702216e1367c8dfb68326a6b93ccf5703c89c93979052a9bf359608e /bin -> usr/bin
l00777 0 0  0 4344c10bf4931483f918496534f12ed9b50dc6a2cead35e3cd9dd898d6ac9414 /home -> var/home
l00777 0 0  0 f11902ca9d69a80df33918534a3e443251fd0aa7f94b76301e1f55e52aed29dd /lib -> usr/lib
l00777 0 0  0 f11902ca9d69a80df33918534a3e443251fd0aa7f94b76301e1f55e52aed29dd /lib64 -> usr/lib
l00777 0 0  0 75317a3df11447c470ffdd63dde045450ca97dfb2a97a0f3f6a21a5da66f737c /media -> run/media
l00777 0 0  0 97c55dbe24e8f3aecfd3f3e5b3f44646fccbb39799807d37a217e9c871da108b /mnt -> var/mnt
l00777 0 0  0 46b1abbd27a846a9257a8d8c9fc4b384ac0888bdb8ac0d6a2d5de72715bd5092 /opt -> var/opt
l00777 0 0  0 d37269e3f46023fd0275212473e07011894cdf4148cbf3fb5758a7e9471dad8e /ostree -> sysroot/ostree
l00777 0 0  0 6f800e74eed172661278d1e1f09e389a6504dcd3358618e1c1618f91f9d33601 /root -> var/roothome
l00777 0 0  0 e0bead7be9323b06bea05cb9b66eb151839989e3a4e5d1a93e09a36919e91818 /sbin -> usr/sbin
l00777 0 0  0 5d4250bba1ed300f793fa9769474351ee5cebd71e8339078af7ebfbe6256d9b5 /srv -> var/srv
l00777 0 0  0 364fbd62f91ca1e06eb7dbd50c93de8976f2cea633658e2dbe803ce6f7490c09 /tmp -> sysroot/tmp
d00755 0 0  0 6e340b9cffb37a989ca544e6bb780a2c78901d3fb33738768511a30617afa01d 446a0ef11b7cc167f3b603e585c7eeeeb675faa412d5ec73f62988eb0b6c5488 /boot
d00755 0 0  0 6e340b9cffb37a989ca544e6bb780a2c78901d3fb33738768511a30617afa01d 446a0ef11b7cc167f3b603e585c7eeeeb675faa412d5ec73f62988eb0b6c5488 /dev
d00755 0 0  0 6e340b9cffb37a989ca544e6bb780a2c78901d3fb33738768511a30617afa01d 446a0ef11b7cc167f3b603e585c7eeeeb675faa412d5ec73f62988eb0b6c5488 /proc
d00755 0 0  0 6e340b9cffb37a989ca544e6bb780a2c78901d3fb33738768511a30617afa01d 446a0ef11b7cc167f3b603e585c7eeeeb675faa412d5ec73f62988eb0b6c5488 /run
d00755 0 0  0 6e340b9cffb37a989ca544e6bb780a2c78901d3fb33738768511a30617afa01d 446a0ef11b7cc167f3b603e585c7eeeeb675faa412d5ec73f62988eb0b6c5488 /sys
d00755 0 0  0 6e340b9cffb37a989ca544e6bb780a2c78901d3fb33738768511a30617afa01d 446a0ef11b7cc167f3b603e585c7eeeeb675faa412d5ec73f62988eb0b6c5488 /sysroot
d00755 0 0  0 83902b1171980665a74c9ea4d3817add50e9fd3279d3ee92381fb2c0098f7ab0 446a0ef11b7cc167f3b603e585c7eeeeb675faa412d5ec73f62988eb0b6c5488 /usr
d00755 0 0  0 a3a987e053ea5a116f1e75a31cd7557fc6e57a3ae09e64171d7fea17ef71ec3e 446a0ef11b7cc167f3b603e585c7eeeeb675faa412d5ec73f62988eb0b6c5488 /var
```    

By default, only the top folders are listed, but -R will list recursively. Instead of listing over 10,000 files, let's filter to just all files that contain 'rpm-ostree', 'rpmostree' or 'RpmOstree', that must belong to **rpm-ostree** package itself.

```console
root@photon-7c2d910d79e9 [ ~ ]# ostree ls photon/4.0/x86_64/minimal -R | grep -e '[Rr]pm-\?[Oo]stree'
-00755 0 0 787208 /usr/bin/rpm-ostree
d00755 0 0  0 /usr/bin/rpm-ostree-host
-00644 0 0   1069 /usr/bin/rpm-ostree-host/function.inc
-00755 0 0  10507 /usr/bin/rpm-ostree-host/mk-ostree-host.sh
d00755 0 0  0 /usr/bin/rpm-ostree-server
-00755 0 0   6452 /usr/bin/rpm-ostree-server/mkostreerepo
-00644 0 0209 /usr/etc/rpm-ostreed.conf
l00777 0 0  0 /usr/lib/librpmostree-1.so.1 -> librpmostree-1.so.1.0.0
-00755 0 0 9878248 /usr/lib/librpmostree-1.so.1.0.0
-00644 0 0   2312 /usr/lib/girepository-1.0/RpmOstree-1.0.typelib
-00755 0 0 22 /usr/lib/kernel/install.d/00-rpmostree-skip.install
d00755 0 0  0 /usr/lib/rpm-ostree
-00755 0 0 1846216 /usr/lib/rpm-ostree/libdnf.so.2
-00644 0 0622 /usr/lib/rpm-ostree/rpm-ostree-0-integration.conf
d00755 0 0  0 /usr/lib/sysimage/rpm-ostree-base-db
-00644 0 0 1069056 /usr/lib/sysimage/rpm-ostree-base-db/Basenames
-00644 0 0   8192 /usr/lib/sysimage/rpm-ostree-base-db/Conflictname
-00644 0 0 159744 /usr/lib/sysimage/rpm-ostree-base-db/Dirnames
-00644 0 0   8192 /usr/lib/sysimage/rpm-ostree-base-db/Enhancename
-00644 0 0   8192 /usr/lib/sysimage/rpm-ostree-base-db/Filetriggername
-00644 0 0   8192 /usr/lib/sysimage/rpm-ostree-base-db/Group
-00644 0 0  12288 /usr/lib/sysimage/rpm-ostree-base-db/Installtid
-00644 0 0  16384 /usr/lib/sysimage/rpm-ostree-base-db/Name
-00644 0 0   8192 /usr/lib/sysimage/rpm-ostree-base-db/Obsoletename
-00644 0 0 4313088 /usr/lib/sysimage/rpm-ostree-base-db/Packages
-00644 0 0 102400 /usr/lib/sysimage/rpm-ostree-base-db/Providename
-00644 0 0   8192 /usr/lib/sysimage/rpm-ostree-base-db/Recommendname
-00644 0 0 106496 /usr/lib/sysimage/rpm-ostree-base-db/Requirename
-00644 0 0  24576 /usr/lib/sysimage/rpm-ostree-base-db/Sha1header
-00644 0 0  16384 /usr/lib/sysimage/rpm-ostree-base-db/Sigmd5
-00644 0 0   8192 /usr/lib/sysimage/rpm-ostree-base-db/Suggestname
-00644 0 0   8192 /usr/lib/sysimage/rpm-ostree-base-db/Supplementname
-00644 0 0   8192 /usr/lib/sysimage/rpm-ostree-base-db/Transfiletriggername
-00644 0 0   8192 /usr/lib/sysimage/rpm-ostree-base-db/Triggername
-00644 0 0263 /usr/lib/systemd/system/rpm-ostree-bootstatus.service
-00644 0 0257 /usr/lib/systemd/system/rpm-ostreed-automatic.service
-00644 0 0227 /usr/lib/systemd/system/rpm-ostreed-automatic.timer
-00644 0 0325 /usr/lib/systemd/system/rpm-ostreed.service
-00644 0 0102 /usr/lib/systemd/system-preset/40-rpm-ostree-auto.preset
-00644 0 0622 /usr/lib/tmpfiles.d/rpm-ostree-0-integration.conf
-00644 0 0   1572 /usr/lib/tmpfiles.d/rpm-ostree-1-autovar.conf
-00755 0 0 53 /usr/libexec/rpm-ostreed
-00644 0 0   3049 /usr/share/bash-completion/completions/rpm-ostree
-00644 0 0  17210 /usr/share/dbus-1/interfaces/org.projectatomic.rpmostree1.xml
-00644 0 0133 /usr/share/dbus-1/system-services/org.projectatomic.rpmostree1.service
-00644 0 0   1530 /usr/share/dbus-1/system.d/org.projectatomic.rpmostree1.conf
-00644 0 0   6593 /usr/share/polkit-1/actions/org.projectatomic.rpmostree1.policy
d00755 0 0  0 /usr/share/rpm-ostree
-00644 0 0   1199 /usr/share/rpm-ostree/treefile.json
```

**atomic** is really an alias for rpm-ostree command. The last file **treefile.json** is not installed by the rpm-ostree package, it is actually downloaded from the server, as we will see in the next chapter. For now, let us notice **"osname" : "photon",  "ref" : "photon/1.0/x86_64/minimal",  "automatic_version_prefix" : "1.0_minimal"**, that matches what we have known so far, and also the **"documentation" : false** setting, that explains why there are no manual files installed for rpm-ostree, and in fact for any package.

```console
root@photon-host [ /usr/share/rpm-ostree ]# ls -l /usr/share/man/man1 
total 0
```

## Listing configuration changes

To diff the current /etc configuration versus default /etc (from the base image), this command will show the **M**odified, **A**dded and **D**eleted files:

```console
root@photon-7c2d910d79e9 [ ~ ]# ostree admin config-diff
M  ssh/sshd_config
M  udev/hwdb.bin
M  fstab
M  machine-id
M  gshadow
M  hosts
M  shadow
A  ssh/ssh_host_rsa_key
A  ssh/ssh_host_rsa_key.pub
A  ssh/ssh_host_dsa_key
A  ssh/ssh_host_dsa_key.pub
A  ssh/ssh_host_ecdsa_key
A  ssh/ssh_host_ecdsa_key.pub
A  ssh/ssh_host_ed25519_key
A  ssh/ssh_host_ed25519_key.pub
A  hostname
A  group-
A  locale.conf
A  .pwd.lock
A  gshadow-
A  shadow-
A  resolv.conf
A  .updated
```

## Listing packages

The following is the rpm-ostree command that lists all the packages for that branch, extracted from RPM database.   

```console
root@photon-7c2d910d79e9 [ ~ ]# rpm-ostree db list photon/4.0/x86_64/minimal
    ostree commit: photon/4.0/x86_64/minimal (820b584a6f90bf6b9b8cb6aad8c093064b88d0ab686be8130baa03d68917ad88)
     Linux-PAM-1.4.0-2.ph4.x86_64
     attr-2.4.48-1.ph4.x86_64
     audit-2.8.5-3.ph4.x86_64
     autogen-libopts-5.18.16-3.ph4.x86_64
     bash-5.0-1.ph4.x86_64
     bc-1.07.1-4.ph4.x86_64
     bridge-utils-1.6-1.ph4.x86_64
     bubblewrap-0.4.1-1.ph4.x86_64
     bzip2-1.0.8-3.ph4.x86_64
     bzip2-libs-1.0.8-3.ph4.x86_64
     ca-certificates-20201001-1.ph4.x86_64
     ca-certificates-pki-20201001-1.ph4.x86_64
     cloud-init-20.3-2.ph4.noarch
     coreutils-selinux-8.32-2.ph4.x86_64
     cpio-2.13-1.ph4.x86_64
     cracklib-2.9.7-1.ph4.x86_64
     cracklib-dicts-2.9.7-1.ph4.x86_64
     curl-7.72.0-2.ph4.x86_64
     curl-libs-7.72.0-2.ph4.x86_64
     cyrus-sasl-2.1.27-3.ph4.x86_64
     dbus-1.13.18-1.ph4.x86_64
     device-mapper-2.03.10-2.ph4.x86_64
     device-mapper-libs-2.03.10-2.ph4.x86_64
     dhcp-client-4.4.2-1.ph4.x86_64
     dhcp-libs-4.4.2-1.ph4.x86_64
     dracut-050-5.ph4.x86_64
     dracut-tools-050-5.ph4.x86_64
     e2fsprogs-1.45.6-2.ph4.x86_64
     e2fsprogs-libs-1.45.6-2.ph4.x86_64
     elfutils-0.181-2.ph4.x86_64
     elfutils-libelf-0.181-2.ph4.x86_64
     expat-2.2.9-2.ph4.x86_64
     expat-libs-2.2.9-2.ph4.x86_64
     file-5.39-1.ph4.x86_64
     file-libs-5.39-1.ph4.x86_64
     filesystem-1.1-4.ph4.x86_64
     findutils-4.7.0-1.ph4.x86_64
     finger-0.17-3.ph4.x86_64
     flex-2.6.4-3.ph4.x86_64
     fuse-2.9.9-1.ph4.x86_64
     gawk-5.1.0-1.ph4.x86_64
     gc-8.0.4-1.ph4.x86_64
     gdbm-1.18.1-1.ph4.x86_64
     glib-2.66.1-1.ph4.x86_64
     glib-networking-2.66.0-1.ph4.x86_64
     glibc-2.32-1.ph4.x86_64
     glibc-iconv-2.32-1.ph4.x86_64
     gmp-6.2.0-1.ph4.x86_64
     gnupg-2.2.23-1.ph4.x86_64
     gnutls-3.6.15-3.ph4.x86_64
     gobject-introspection-1.66.0-1.ph4.x86_64
     gpgme-1.14.0-1.ph4.x86_64
     grep-3.4-1.ph4.x86_64
     grub2-2.04-2.ph4.x86_64
     grub2-efi-2.04-2.ph4.x86_64
     grub2-efi-image-2.04-2.ph4.x86_64
     grub2-pc-2.04-2.ph4.x86_64
     grub2-theme-4.0-1.ph4.noarch
     grub2-theme-ostree-4.0-1.ph4.noarch
     guile-2.0.13-3.ph4.x86_64
     gzip-1.10-1.ph4.x86_64
     iana-etc-2.30-2.ph4.noarch
     icu-67.1-1.ph4.x86_64
     iproute2-5.8.0-1.ph4.x86_64
     iptables-1.8.4-1.ph4.x86_64
     iputils-20200821-1.ph4.x86_64
     json-c-0.15-2.ph4.x86_64
     json-glib-1.6.0-1.ph4.x86_64
     kmod-27-1.ph4.x86_64
     krb5-1.17-4.ph4.x86_64
     libacl-2.2.53-1.ph4.x86_64
     libarchive-3.4.3-3.ph4.x86_64
     libassuan-2.5.3-1.ph4.x86_64
     libcap-2.43-1.ph4.x86_64
     libcap-ng-0.8-1.ph4.x86_64
     libdb-5.3.28-2.ph4.x86_64
     libdnet-1.11-7.ph4.x86_64
     libffi-3.3-1.ph4.x86_64
     libgcc-8.4.0-1.ph4.x86_64
     libgcrypt-1.8.6-2.ph4.x86_64
     libgpg-error-1.39-1.ph4.x86_64
     libgpg-error-devel-1.39-1.ph4.x86_64
     libksba-1.4.0-1.ph4.x86_64
     libltdl-2.4.6-3.ph4.x86_64
     libmetalink-0.1.3-2.ph4.x86_64
     libmicrohttpd-0.9.71-2.ph4.x86_64
     libmodulemd-2.9.4-1.ph4.x86_64
     libmspack-0.10.1alpha-1.ph4.x86_64
     libnsl-1.3.0-1.ph4.x86_64
     libpsl-0.21.1-1.ph4.x86_64
     libpwquality-1.4.2-1.ph4.x86_64
     librepo-1.12.1-3.ph4.x86_64
     libseccomp-2.5.0-2.ph4.x86_64
     libselinux-3.1-1.ph4.x86_64
     libsemanage-3.1-1.ph4.x86_64
     libsepol-3.1-1.ph4.x86_64
     libsolv-0.6.35-5.ph4.x86_64
     libsoup-2.72.0-1.ph4.x86_64
     libssh2-1.9.0-2.ph4.x86_64
     libstdc++-8.4.0-1.ph4.x86_64
     libtasn1-4.14-1.ph4.x86_64
     libtirpc-1.2.6-1.ph4.x86_64
     libtool-2.4.6-3.ph4.x86_64
     libunistring-0.9.10-1.ph4.x86_64
     libxml2-2.9.10-3.ph4.x86_64
     libxml2-devel-2.9.10-3.ph4.x86_64
     libxslt-1.1.34-1.ph4.x86_64
     libyaml-0.2.5-1.ph4.x86_64
     linux-5.9.0-3.ph4.x86_64
     lua-5.3.5-1.ph4.x86_64
     lz4-1.9.2-1.ph4.x86_64
     m4-1.4.18-3.ph4.x86_64
     motd-0.1.3-6.ph4.noarch
     mozjs-78.3.1-1.ph4.x86_64
     mpfr-4.1.0-1.ph4.x86_64
     ncurses-6.2-2.ph4.x86_64
     ncurses-libs-6.2-2.ph4.x86_64
     ncurses-terminfo-6.2-2.ph4.x86_64
     net-tools-1.60-12.ph4.x86_64
     nettle-3.6-1.ph4.x86_64
     npth-1.6-1.ph4.x86_64
     nspr-4.29-1.ph4.x86_64
     nss-3.57-1.ph4.x86_64
     nss-altfiles-2.23.0-1.ph4.x86_64
     nss-libs-3.57-1.ph4.x86_64
     open-vm-tools-11.1.5-4.ph4.x86_64
     openldap-2.4.53-2.ph4.x86_64
     openssh-8.4p1-2.ph4.x86_64
     openssh-clients-8.4p1-2.ph4.x86_64
     openssh-server-8.4p1-2.ph4.x86_64
     openssl-1.1.1g-3.ph4.x86_64
     ostree-2020.6-1.ph4.x86_64
     ostree-grub2-2020.6-1.ph4.x86_64
     ostree-libs-2020.6-1.ph4.x86_64
     pcre-8.44-1.ph4.x86_64
     pcre-libs-8.44-1.ph4.x86_64
     photon-release-4.0-1.ph4.noarch
     photon-repos-4.0-1.ph4.noarch
     pinentry-1.1.0-1.ph4.x86_64
     pkg-config-0.29.2-3.ph4.x86_64
     policycoreutils-3.1-1.ph4.x86_64
     polkit-0.118-1.ph4.x86_64
     popt-1.16-5.ph4.x86_64
     procps-ng-3.3.16-1.ph4.x86_64
     python3-3.8.6-1.ph4.x86_64
     python3-PyYAML-5.3.1-1.ph4.x86_64
     python3-asn1crypto-1.4.0-1.ph4.noarch
     python3-attrs-20.2.0-2.ph4.noarch
     python3-certifi-2020.6.20-1.ph4.noarch
     python3-cffi-1.14.3-2.ph4.x86_64
     python3-chardet-3.0.4-2.ph4.noarch
     python3-configobj-5.0.6-5.ph4.noarch
     python3-cryptography-3.1.1-2.ph4.x86_64
     python3-gobject-introspection-1.66.0-1.ph4.x86_64
     python3-idna-2.10-1.ph4.noarch
     python3-jinja2-2.11.2-1.ph4.noarch
     python3-jsonpatch-1.26-1.ph4.noarch
     python3-jsonpointer-2.0-2.ph4.noarch
     python3-jsonschema-3.2.0-1.ph4.noarch
     python3-libs-3.8.6-1.ph4.x86_64
     python3-markupsafe-1.1.1-1.ph4.x86_64
     python3-netifaces-0.10.9-2.ph4.x86_64
     python3-oauthlib-3.1.0-1.ph4.noarch
     python3-packaging-20.4-2.ph4.noarch
     python3-prettytable-0.7.2-7.ph4.noarch
     python3-pyOpenSSL-19.1.0-2.ph4.noarch
     python3-pyasn1-0.4.8-1.ph4.noarch
     python3-pycparser-2.20-1.ph4.noarch
     python3-pyparsing-2.4.7-1.ph4.noarch
     python3-pyrsistent-0.17.3-1.ph4.x86_64
     python3-requests-2.24.0-1.ph4.noarch
     python3-setuptools-3.8.6-1.ph4.noarch
     python3-six-1.15.0-2.ph4.noarch
     python3-urllib3-1.25.10-2.ph4.noarch
     python3-xml-3.8.6-1.ph4.x86_64
     readline-7.0-3.ph4.x86_64
     rpcsvc-proto-1.4.2-1.ph4.x86_64
     rpm-4.14.2-11.ph4.x86_64
     rpm-libs-4.14.2-11.ph4.x86_64
     rpm-ostree-2020.5-4.ph4.x86_64
     sed-4.8-1.ph4.x86_64
     selinux-policy-3.14.7-1.ph4.noarch
     shadow-4.8.1-2.ph4.x86_64
     shadow-tools-4.8.1-2.ph4.x86_64
     shim-signed-15-1.ph4.x86_64
     sqlite-libs-3.33.0-1.ph4.x86_64
     sudo-1.8.30-2.ph4.x86_64
     systemd-245.5-3.ph4.x86_64
     tcp_wrappers-7.6-7.ph4.x86_64
     tzdata-2020a-1.ph4.noarch
     util-linux-2.36-1.ph4.x86_64
     util-linux-libs-2.36-1.ph4.x86_64
     vim-8.2.1361-1.ph4.x86_64
     which-2.21-6.ph4.x86_64
     xmlsec1-1.2.30-3.ph4.x86_64
     xz-5.2.5-1.ph4.x86_64
     xz-libs-5.2.5-1.ph4.x86_64
     zchunk-1.1.7-1.ph4.x86_64
     zchunk-libs-1.1.7-1.ph4.x86_64
     zlib-1.2.11-2.ph4.x86_64
     zstd-1.4.5-2.ph4.x86_64
     zstd-libs-1.4.5-2.ph4.x86_64
```

## Querying for package details

We are able to use the query option of rpm to make sure any package have been installed properly. The files list should match the previous file mappings in 4.2, so let's check package **rpm-ostree**. As we've seen, manual files listed here are actually missing, they were not installed.

```console
root@photon-7c2d910d79e9 [ ~ ]# rpm -ql  rpm-ostree
    /etc/rpm-ostreed.conf
    /usr/bin/rpm-ostree
    /usr/bin/rpm-ostree-host
    /usr/bin/rpm-ostree-host/function.inc
    /usr/bin/rpm-ostree-host/mk-ostree-host.sh
    /usr/bin/rpm-ostree-server
    /usr/bin/rpm-ostree-server/mkostreerepo
    /usr/lib/girepository-1.0/RpmOstree-1.0.typelib
    /usr/lib/librpmostree-1.so.1
    /usr/lib/librpmostree-1.so.1.0.0
    /usr/lib/rpm-ostree
    /usr/lib/rpm-ostree/libdnf.so.2
    /usr/lib/rpm-ostree/rpm-ostree-0-integration.conf
    /usr/lib/systemd/system/rpm-ostree-bootstatus.service
    /usr/lib/systemd/system/rpm-ostreed-automatic.service
    /usr/lib/systemd/system/rpm-ostreed-automatic.timer
    /usr/lib/systemd/system/rpm-ostreed.service
    /usr/libexec/rpm-ostreed
    /usr/share/bash-completion/completions/rpm-ostree
    /usr/share/dbus-1/interfaces/org.projectatomic.rpmostree1.xml
    /usr/share/dbus-1/system-services/org.projectatomic.rpmostree1.service
    /usr/share/dbus-1/system.d/org.projectatomic.rpmostree1.conf
    /usr/share/man/man1/rpm-ostree.1.gz
    /usr/share/man/man5/rpm-ostreed.conf.5.gz
    /usr/share/man/man8/rpm-ostreed-automatic.service.8.gz
    /usr/share/man/man8/rpm-ostreed-automatic.timer.8.gz
    /usr/share/polkit-1/actions/org.projectatomic.rpmostree1.policy
```


## Why am I unable to install, upgrade or uninstall packages?

The OSTree host installer needs the server URL or the server repository. 

When you perform the installation using the repo, the install packages are located under the layer package.  When you install with the URL, the packages are located under the local packages.

You can use the `rpm-ostree uninstall` command to uninstall only the layered and local packages but not the base packages. To modify the base packages, you can use the `rpm-ostree override` command. 

When you run `rpm-ostree upgrade`, the command will only upgrade packages based on the commit available in the server.


