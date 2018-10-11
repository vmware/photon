# Install or rebase to Photon OS 2.0

Photon OS 2.0 release has a different focus and while it provides full RPM-OSTree functionality (updated to 2017), it lets the user drive it, rather than provide a pre-defined solution as part of the installation.  

The number of packages included in the RPMS repo in Photon OS 2.0 increased significantly, compared to 1.0. To keep the ISO at reasonable size, Photon OS 2.0 no longer includes the compressed ostree.repo file, that helped optimize both the server and host install in 1.0 or 1.0 Rev2. That decision affected the OSTree features we ship out of the box. Customer could achieve the same results by several additional simple steps, that will be explained in this chapter. In addition, there is a new way to create a host raw image at server.

## 12.1 Installing an RPM-OSTree server
Photon OS 2.0 installer contains an option to install an OSTree server, just like Photon 1.0 OS does. It will not run, however, the server 'compose tree' as part of installation, as most users will want to start from scratch to create their own image anyway, using different package set and customized settings.
In addition to starter photon-base.json, we provide photon-minimal.json and photon-full.json, updated with a 2.0 Refspec. We still fire up an Apache web server, that will point to an empty site initially at the repo directory. Assuming you've customized photon-base.json to you liking, all you need to do is to run the commands you are already familiar with from [Chapter 9](Photon-RPM-OSTree-9-Package-oriented-server-operations.md).
```
root [ /srv/rpm-ostree ]# ostree --repo=repo init --mode=archive-z2
root [ /srv/rpm-ostree ]# rpm-ostree compose tree --repo=repo photon-base.json
```
Now if you point a browser to http://<server_IP_address>, you should see the familiar directory structure of an OSTree repo.

## 12.2 Installing an RPM-OSTree host
Photon OS 2.0 installer no longer includes a UI option to deploy a host manually - either against a default or a custom server repo, and also there is no official online Photon OS 2.0 OSTree repo published. This is now completely customer driven.  
Automated host install is supported, as explained in [Chapter 7.2 Automated install of a custom host via kickstart](Photon-RPM-OSTree-7-Installing-a-host-against-a-custom-server-repository.md#72-automated-install-of-a-custom-host-via-kickstart).  

## 12.3 Rebasing a host from Photon 1.0 to 2.0
If kickstart sounds too complicated and we still want to go the UI way like in 1.0, fortunately, there is a workaround that requires an extra step. Also, if you have an installed Photon 1.0 or 1.0 Rev2 that you want to carry to 2.0, you need to rebase it. Notice that I didn't say "upgrade".   

Basically the OSTree repo will switch to a different branch on a different server, following the new server's branch versioning scheme. The net result is that the lots of packages will get changed to newer versions from newer OSTree repo, that has been composed from a newer Photon OS 2.0 RPMS repo. Again, I didn't say "upgraded", neither the rebase command output, that lists "changed" packages. Some obsolete packages will be removed, new packages will be added, either because they didn't exist in 1.0 repo, or because the new config file includes them.  
The OS name is the same (Photon), so the content in /var and /etc will be transferred over.  

1. To install fresh, deploy a Photon 1.0 Rev2 host default, as described in [Chapter 2](Photon-RPM-OSTree-2-Installing-a-host-against-default-server-repository.md). Of course, if you already have an existing Photon OS 1.0 host that you want to move to 2.0, skip this step.
2. Edit /ostree/repo/config and substitute the url, providing the IP address for the Photon OS 2.0 RPM-OSTree server installed above. This was explained in [Chapter 10](Photon-RPM-OSTree-10-Remotes.md#102-switching-repositories).  
ostree should confirm that is the updated server IP for the "photon" remote.
```
root@ostree-host [ ~ ]# ostree remote show-url photon
http://10.118.101.180
```
3. Rebase your host to the new 2.0 server and Refspec.
```
root@ostree-host [ ~ ]# rpm-ostree rebase photon/2.0/x86_64/minimal

549 metadata, 2654 content objects fetched; 119853 KiB transferred in 17 seconds
Copying /etc changes: 6 modified, 0 removed, 14 added
Transaction complete; bootconfig swap: yes deployment count change: 1
Deleting ref 'photon:photon/1.0/x86_64/minimal'
Changed:
  Linux-PAM 1.2.1-3.ph1 -> 1.3.0-1.ph2
  attr 2.4.47-3.ph1 -> 2.4.47-4.ph2
  autogen-libopts 5.18.7-2.ph1 -> 5.18.12-2.ph2
  bash 4.3.30-4.ph1 -> 4.4-5.ph2
  bc 1.06.95-3.ph1 -> 1.06.95-3.ph2
  binutils 2.25.1-2.ph1 -> 2.29-3.ph2
  bridge-utils 1.5-3.ph1 -> 1.6-1.ph2
  bzip2 1.0.6-6.ph1 -> 1.0.6-8.ph2
  ca-certificates 20160109-5.ph1 -> 20170406-3.ph2
  coreutils 8.25-2.ph1 -> 8.27-2.ph2
  cpio 2.12-2.ph1 -> 2.12-3.ph2
  cracklib 2.9.6-2.ph1 -> 2.9.6-8.ph2
  cracklib-dicts 2.9.6-2.ph1 -> 2.9.6-8.ph2
  curl 7.51.0-2.ph1 -> 7.54.1-1.ph2
  dbus 1.8.8-5.ph1 -> 1.11.12-1.ph2
  device-mapper 2.02.141-5.ph1 -> 2.02.171-3.ph2
  device-mapper-libs 2.02.141-5.ph1 -> 2.02.171-3.ph2
  docker 1.12.1-1.ph1 -> 17.06.0-1.ph2
  dracut 044-3.ph1 -> 045-4.ph2
  dracut-tools 044-3.ph1 -> 045-4.ph2
  elfutils-libelf 0.165-2.ph1 -> 0.169-1.ph2
  expat 2.2.0-1.ph1 -> 2.2.0-2.ph2
  file 5.24-2.ph1 -> 5.30-2.ph2
  filesystem 1.0-8.ph1 -> 1.0-13.ph2
  findutils 4.6.0-2.ph1 -> 4.6.0-3.ph2
  flex 2.5.39-3.ph1 -> 2.6.4-2.ph2
  glib 2.47.6-2.ph1 -> 2.52.1-2.ph2
  glib-networking 2.46.1-2.ph1 -> 2.50.0-1.ph2
  glibc 2.22-9.ph1 -> 2.26-1.ph2
  gmp 6.0.0a-3.ph1 -> 6.1.2-2.ph2
  gnutls 3.4.11-2.ph1 -> 3.5.10-1.ph2
  gobject-introspection 1.46.0-2.ph1 -> 1.52.1-4.ph2
  gpgme 1.6.0-2.ph1 -> 1.9.0-2.ph2
  grep 2.21-2.ph1 -> 3.0-3.ph2
  grub2 2.02-5.ph1 -> 2.02-9.ph2
  gzip 1.6-2.ph1 -> 1.8-1.ph2
  iana-etc 2.30-2.ph1 -> 2.30-2.ph2
  iproute2 4.2.0-2.ph1 -> 4.10.0-3.ph2
  iptables 1.6.0-5.ph1 -> 1.6.1-4.ph2
  json-glib 1.0.4-2.ph1 -> 1.2.8-1.ph2
  kmod 21-4.ph1 -> 24-3.ph2
  krb5 1.14-4.ph1 -> 1.15.1-2.ph2
  libarchive 3.1.2-7.ph1 -> 3.3.1-1.ph2
  libassuan 2.4.2-2.ph1 -> 2.4.3-1.ph2
  libcap 2.25-2.ph1 -> 2.25-7.ph2
  libffi 3.2.1-2.ph1 -> 3.2.1-5.ph2
  libgcc 5.3.0-3.ph1 -> 6.3.0-3.ph2
  libgcrypt 1.6.5-2.ph1 -> 1.7.6-1.ph2
  libgomp 5.3.0-3.ph1 -> 6.3.0-3.ph2
  libgpg-error 1.21-2.ph1 -> 1.27-1.ph2
  libgsystem 2015.1-2.ph1 -> 2015.2-1.ph2
  librepo 1.7.17-2.ph1 -> 1.7.20-2.ph2
  libselinux 2.5-2.ph1 -> 2.6-4.ph2
  libsepol 2.5-2.ph1 -> 2.6-1.ph2
  libsolv 0.6.19-2.ph1 -> 0.6.26-3.ph2
  libsoup 2.53.90-2.ph1 -> 2.57.1-2.ph2
  libssh2 1.8.0-1.ph1 -> 1.8.0-1.ph2
  libstdc++ 5.3.0-3.ph1 -> 6.3.0-3.ph2
  libtasn1 4.7-3.ph1 -> 4.10-1.ph2
  libtool 2.4.6-2.ph1 -> 2.4.6-3.ph2
  libxml2 2.9.4-3.ph1 -> 2.9.4-11.ph2
  linux 4.4.41-1.ph1 -> 4.9.43-2.ph2
  m4 1.4.17-2.ph1 -> 1.4.18-1.ph2
  mkinitcpio 19-2.ph1 -> 23-3.ph2
  mpfr 3.1.3-2.ph1 -> 3.1.5-1.ph2
  ncurses 6.0-2.ph1 -> 6.0-10.ph2
  net-tools 1.60-7.ph1 -> 1.60-10.ph2
  nettle 3.2-2.ph1 -> 3.3-1.ph2
  nspr 4.12-2.ph1 -> 4.15-1.ph2
  nss-altfiles 2.19.1-2.ph1 -> 2.23.0-1.ph2
  openssh 7.4p1-1.ph1 -> 7.5p1-4.ph2
  openssl 1.0.2j-1.ph1 -> 1.0.2l-1.ph2
  ostree 2015.7-5.ph1 -> 2017.5-1.ph2
  pcre 8.39-1.ph1 -> 8.40-4.ph2
  photon-release 1.0-6.ph1 -> 2.0-1.ph2
  pkg-config 0.28-2.ph1 -> 0.29.2-1.ph2
  popt 1.16-2.ph1 -> 1.16-4.ph2
  procps-ng 3.3.11-3.ph1 -> 3.3.12-2.ph2
  readline 6.3-4.ph1 -> 7.0-2.ph2
  rpm-ostree 2015.7-2.ph1 -> 2017.5-1.ph2
  sed 4.2.2-2.ph1 -> 4.4-2.ph2
  shadow 4.2.1-8.ph1 -> 4.2.1-13.ph2
  systemd 228-32.ph1 -> 233-7.ph2
  util-linux 2.27.1-2.ph1 -> 2.29.2-3.ph2
  vim 7.4-6.ph1 -> 8.0.0533-3.ph2
  which 2.21-2.ph1 -> 2.21-3.ph2
  xz 5.2.2-2.ph1 -> 5.2.3-2.ph2
  zlib 1.2.8-3.ph1 -> 1.2.11-1.ph2
Removed:
  db-6.1.26-2.ph1.x86_64
  e2fsprogs-1.42.13-2.ph1.x86_64
  gdbm-1.11-2.ph1.x86_64
  hawkey-2014.1-4.ph1.x86_64
  iputils-20151218-3.ph1.x86_64
  libhif-0.2.2-2.ph1.x86_64
  lua-5.3.2-2.ph1.x86_64
  nss-3.25-1.ph1.x86_64
  python2-2.7.11-8.ph1.x86_64
  python2-libs-2.7.11-8.ph1.x86_64
  rpm-4.11.2-11.ph1.x86_64
  sqlite-autoconf-3.11.0-2.ph1.x86_64
  tcsh-6.19.00-4.ph1.x86_64
Added:
  bubblewrap-0.1.8-1.ph2.x86_64
  bzip2-libs-1.0.6-8.ph2.x86_64
  ca-certificates-pki-20170406-3.ph2.x86_64
  curl-libs-7.54.1-1.ph2.x86_64
  e2fsprogs-libs-1.43.4-2.ph2.x86_64
  expat-libs-2.2.0-2.ph2.x86_64
  fuse-2.9.7-2.ph2.x86_64
  gnupg-2.1.20-2.ph2.x86_64
  libdb-5.3.28-1.ph2.x86_64
  libksba-1.3.5-1.ph2.x86_64
  libltdl-2.4.6-3.ph2.x86_64
  libseccomp-2.3.2-1.ph2.x86_64
  ncurses-libs-6.0-10.ph2.x86_64
  ncurses-terminfo-6.0-10.ph2.x86_64
  npth-1.3-1.ph2.x86_64
  nss-libs-3.31-2.ph2.x86_64
  openssh-clients-7.5p1-4.ph2.x86_64
  openssh-server-7.5p1-4.ph2.x86_64
  pcre-libs-8.40-4.ph2.x86_64
  pinentry-1.0.0-2.ph2.x86_64
  rpm-libs-4.13.0.1-5.ph2.x86_64
  sqlite-libs-3.19.3-1.ph2.x86_64
  util-linux-libs-2.29.2-3.ph2.x86_64
  xz-libs-5.2.3-2.ph2.x86_64

root@ostree-host [ ~ ]# rpm-ostree status
  TIMESTAMP (UTC)         VERSION           ID             OSNAME     REFSPEC                              
  2017-08-31 18:19:36     2.0_minimal       f4497b1948     photon     photon:photon/2.0/x86_64/minimal
* 2017-01-11 02:18:42     1.0_minimal.1     4a21972b29     photon     photon:photon/1.0/x86_64/minimal
```
That's it! You may now reboot to the new Photon OS 2.0 image. The updated ostree and rpm-ostree packages have a slightly changed output format:
```
root@ph2-ostree-host [ ~ ]# rpm-ostree status
State: idle
Deployments:
* photon:photon/2.0/x86_64/minimal
             Version: 2.0_minimal (2017-08-31 18:19:36)
              Commit: f4497b194826adb0db6e17a6867df04edd1dc1ebe796a73db9f19b973b5658df

  photon:photon/1.0/x86_64/minimal
             Version: 1.0_minimal.1 (2017-01-11 02:18:42)
              Commit: 4a21972b293978d39777017ccb33dde45713dd435b3cb77ee42161e7e849e5e4
```

There are some side effects of installing Photon OS 2.0 based on the skeleton of a 1.0. For one, the custom disk partitioning is not available in 1.0. There could be others, I cannot think of now.

## 12.4 Creating a host raw image
It is now possible to run at server a script that is part of RPM-OStree package, to create a host raw mage.

