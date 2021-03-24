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

```console
root@photon-host-def [ ~ ]# rpm-ostree upgrade
Updating from: photon:photon/4.0/x86_64/minimal

No upgrade available.
```

It is good idea to check periodically for updates.

To check if there are any new updates without actually applying them, we will pass the --check-diff flag, that would list the different packages as added, modified or deleted - if such operations were to happen.

```console
root@photon-host [ ~ ]# rpm-ostree upgrade --check-diff
Updating from: photon:photon/4.0/x86_64/minimal

8 metadata, 13 content objects fetched; 1026 KiB transferred in 0 seconds
+gawk-4.1.3-2.ph1.x86_64
+sudo-1.8.15-3.ph1.x86_64
+wget-1.17.1-2.ph1.x86_64
```

We like what we see and now let's upgrade for real. This command will deploy a new bootable filetree.

```console
root@photon-7c2d910d79e9 [ ~ ]# rpm-ostree upgrade --allow-downgrade
⠂ Receiving metadata objects: 0/(estimating) -/s 0 bytes... 
Receiving metadata objects: 0/(estimating) -/s 0 bytes... done
Staging deployment... done
Downgraded:
  audit 2.8.5-6.ph4 -> 2.8.5-3.ph4
  cloud-init 20.4.1-1.ph4 -> 20.3-2.ph4
  cpio 2.13-3.ph4 -> 2.13-1.ph4
  curl 7.74.0-1.ph4 -> 7.72.0-2.ph4
  curl-libs 7.74.0-1.ph4 -> 7.72.0-2.ph4
  cyrus-sasl 2.1.27-4.ph4 -> 2.1.27-3.ph4
  dhcp-client 4.4.2-2.ph4 -> 4.4.2-1.ph4
  dhcp-libs 4.4.2-2.ph4 -> 4.4.2-1.ph4
  dracut 050-7.ph4 -> 050-5.ph4
  dracut-tools 050-7.ph4 -> 050-5.ph4
  file 5.39-2.ph4 -> 5.39-1.ph4
  file-libs 5.39-2.ph4 -> 5.39-1.ph4
  gdbm 1.19-1.ph4 -> 1.18.1-1.ph4
  glibc 2.32-2.ph4 -> 2.32-1.ph4
  glibc-iconv 2.32-2.ph4 -> 2.32-1.ph4
  gobject-introspection 1.66.0-3.ph4 -> 1.66.0-1.ph4
  grub2-theme 4.0-2.ph4 -> 4.0-1.ph4
  grub2-theme-ostree 4.0-2.ph4 -> 4.0-1.ph4
  iproute2 5.10.0-1.ph4 -> 5.8.0-1.ph4
  iptables 1.8.7-1.ph4 -> 1.8.4-1.ph4
  json-c 0.15-3.ph4 -> 0.15-2.ph4
  libgcc 10.2.0-1.ph4 -> 8.4.0-1.ph4
  libmetalink 0.1.3-3.ph4 -> 0.1.3-2.ph4
  libmodulemd 2.11.0-1.ph4 -> 2.9.4-1.ph4
  librepo 1.12.1-4.ph4 -> 1.12.1-3.ph4
  libsepol 3.1-2.ph4 -> 3.1-1.ph4
  libsolv 0.6.35-7.ph4 -> 0.6.35-5.ph4
  libssh2 1.9.0-3.ph4 -> 1.9.0-2.ph4
  libstdc++ 10.2.0-1.ph4 -> 8.4.0-1.ph4
  libxml2 2.9.10-6.ph4 -> 2.9.10-3.ph4
  libxml2-devel 2.9.10-6.ph4 -> 2.9.10-3.ph4
  libxslt 1.1.34-2.ph4 -> 1.1.34-1.ph4
  linux 5.10.4-15.ph4 -> 5.9.0-3.ph4
  ncurses 6.2-3.ph4 -> 6.2-2.ph4
  ncurses-libs 6.2-3.ph4 -> 6.2-2.ph4
  ncurses-terminfo 6.2-3.ph4 -> 6.2-2.ph4
  nss 3.57-2.ph4 -> 3.57-1.ph4
  nss-libs 3.57-2.ph4 -> 3.57-1.ph4
  open-vm-tools 11.2.5-1.ph4 -> 11.1.5-4.ph4
  openldap 2.4.53-3.ph4 -> 2.4.53-2.ph4
  openssl 1.1.1i-2.ph4 -> 1.1.1g-3.ph4
  pcre 8.44-2.ph4 -> 8.44-1.ph4
  pcre-libs 8.44-2.ph4 -> 8.44-1.ph4
  python3 3.9.1-2.ph4 -> 3.8.6-1.ph4
  python3-PyYAML 5.4.1-1.ph4 -> 5.3.1-1.ph4
  python3-attrs 20.3.0-2.ph4 -> 20.2.0-2.ph4
  python3-cryptography 3.2.1-1.ph4 -> 3.1.1-2.ph4
  python3-gobject-introspection 1.66.0-3.ph4 -> 1.66.0-1.ph4
  python3-libs 3.9.1-2.ph4 -> 3.8.6-1.ph4
  python3-packaging 20.4-3.ph4 -> 20.4-2.ph4
  python3-pyrsistent 0.17.3-2.ph4 -> 0.17.3-1.ph4
  python3-setuptools 3.9.1-2.ph4 -> 3.8.6-1.ph4
  python3-urllib3 1.25.11-1.ph4 -> 1.25.10-2.ph4
  python3-xml 3.9.1-2.ph4 -> 3.8.6-1.ph4
  rpm 4.16.1.2-1.ph4 -> 4.14.2-11.ph4
  rpm-libs 4.16.1.2-1.ph4 -> 4.14.2-11.ph4
  rpm-ostree 2020.5-5.ph4 -> 2020.5-4.ph4
  shadow 4.8.1-3.ph4 -> 4.8.1-2.ph4
  shadow-tools 4.8.1-3.ph4 -> 4.8.1-2.ph4
  sudo 1.9.5-1.ph4 -> 1.8.30-2.ph4
  systemd 247.3-1.ph4 -> 245.5-3.ph4
  util-linux 2.36-2.ph4 -> 2.36-1.ph4
  util-linux-libs 2.36-2.ph4 -> 2.36-1.ph4
Removed:
  libpcap-1.10.0-1.ph4.x86_64
  python3-Pygments-2.7.2-2.ph4.noarch
  python3-alabaster-0.7.12-1.ph4.noarch
  python3-babel-2.8.0-3.ph4.noarch
  python3-docutils-0.16-1.ph4.noarch
  python3-imagesize-1.2.0-2.ph4.noarch
  python3-pytz-2020.4-2.ph4.noarch
  python3-snowballstemmer-2.0.0-1.ph4.noarch
  python3-sphinx-3.3.0-2.ph4.noarch
  python3-sphinxcontrib-applehelp-1.0.2-1.ph4.noarch
  python3-sphinxcontrib-devhelp-1.0.2-1.ph4.noarch
  python3-sphinxcontrib-htmlhelp-1.0.3-1.ph4.noarch
  python3-sphinxcontrib-jsmath-1.0.1-1.ph4.noarch
  python3-sphinxcontrib-qthelp-1.0.3-1.ph4.noarch
  python3-sphinxcontrib-serializinghtml-1.1.4-1.ph4.noarch
  python3-typing-3.7.4.3-1.ph4.noarch
  systemd-libs-247.3-1.ph4.x86_64
  systemd-pam-247.3-1.ph4.x86_64
  systemd-rpm-macros-247.3-1.ph4.noarch
  systemd-udev-247.3-1.ph4.x86_64
Run "systemctl reboot" to start a reboot
```

By looking at the commit history, notice that the new commit has the original commit as parent.

```console
root@photon-7c2d910d79e9 [ ~ ]# ostree log photon/4.0/x86_64/minimal
commit 820b584a6f90bf6b9b8cb6aad8c093064b88d0ab686be8130baa03d68917ad88
ContentChecksum:  c7956cedc5c1b8c07a06e10789c17364a5b7a4b970daab64f3398b7c42bd97d9
Date:  2020-11-04 02:21:47 +0000
Version: 4.0_minimal
(no subject)
```   


Notice that now we have a new reference, that corresponds to the newly deployed image.

```console
root@photon-7c2d910d79e9 [ ~ ]# ostree refs
ostree/0/1/1
photon:photon/4.0/x86_64/minimal
ostree/0/1/0
```


Let us look at the status. The new filetree version .1 has the expected Commit ID and a newer timestamp, that is actually the server date/time when the image has been generated, not the time/date when it was downloaded or installed at the host. The old image has a star next to it, showing that's the image the system is booted currently into. 

```console
root@photon-7c2d910d79e9 [ ~ ]# rpm-ostree status
State: idle
Deployments:
  ostree://photon:photon/4.0/x86_64/minimal
    Version: 4.0_minimal (2020-11-04T02:21:47Z)
Commit: 820b584a6f90bf6b9b8cb6aad8c093064b88d0ab686be8130baa03d68917ad88
  Diff: 63 downgraded, 20 removed

● ostree://photon:photon/4.0/x86_64/minimal
    Version: 4.0_minimal (2021-02-20T07:15:43Z)
Commit: 965c1abeb048e1a8ff77e9cd34ffccc5e3356176cda3332b4ff0e7a6c66b661f
```    

Now let's type `reboot`. Grub will list the new filetree as the first image, marked with a star, as the default bootable image. If the keyboard is not touched and order is not changed, grub will timeout and will boot into that image.

![Grub-dual-boot-1-0](/docs/images/rpmostree-grub.png)

Let's look again at the status. It's identical, just that the star is next to the newer image, to show it's the current image it has booted from.

```console
root@photon-7c2d910d79e9 [ ~ ]# rpm-ostree status
State: idle
Deployments:
● ostree://photon:photon/4.0/x86_64/minimal
    Version: 4.0_minimal (2020-11-04T02:21:47Z)
Commit: 820b584a6f90bf6b9b8cb6aad8c093064b88d0ab686be8130baa03d68917ad88
  Diff: 63 downgraded, 20 removed

  ostree://photon:photon/4.0/x86_64/minimal
    Version: 4.0_minimal (2021-02-20T07:15:43Z)
Commit: 965c1abeb048e1a8ff77e9cd34ffccc5e3356176cda3332b4ff0e7a6c66b661f
```


Also, the current deployment directory is based on the new commit:

```console
root@photon-7c2d910d79e9 [ ~ ]# ostree admin config-diff --print-current-dir
/ostree/deploy/photon/deploy/820b584a6f90bf6b9b8cb6aad8c093064b88d0ab686be8130baa03d68917ad88.0
```

A fresh upgrade for a new version will delete the older, original image and bring a new one, that will become the new default image. The previous 'default' image will move down one position as the backup image.

## Listing file differences

Now we can look at what files have been **A**dded, **M**odified, **D**eleted due to the addition of those three packages and switching of the boot directories, by comparing the two commits.

```console
root@photon-7c2d910d79e9 [ ~ ]# ostree diff 820b 965c
M    /usr/bin/VGAuthService
M    /usr/bin/[
M    /usr/bin/asn1Coding
M    /usr/bin/asn1Decoding
M    /usr/bin/asn1Parser
M    /usr/bin/attr
M    /usr/bin/aulast
M    /usr/bin/aulastlog
M    /usr/bin/ausyscall
M    /usr/bin/auvirt
M    /usr/bin/b2sum
M    /usr/bin/base32
M    /usr/bin/base64
M    /usr/bin/basename
M    /usr/bin/basenc
M    /usr/bin/bash
M    /usr/bin/bc
M    /usr/bin/bootctl
M    /usr/bin/bsdcat
M    /usr/bin/bsdcpio
M    /usr/bin/bsdtar
M    /usr/bin/busctl
M    /usr/bin/bwrap
M    /usr/bin/bzip2
M    /usr/bin/bzip2recover
M    /usr/bin/cal
M    /usr/bin/captest
M    /usr/bin/cat
M    /usr/bin/certtool
M    /usr/bin/certutil
M    /usr/bin/chage
M    /usr/bin/chattr
M    /usr/bin/chcon
M    /usr/bin/chfn
M    /usr/bin/chgrp
M    /usr/bin/chmem
M    /usr/bin/chmod
M    /usr/bin/choom
M    /usr/bin/chown
M    /usr/bin/chrt
M    /usr/bin/chsh
M    /usr/bin/cksum
M    /usr/bin/clear
M    /usr/bin/cloud-id
M    /usr/bin/cloud-init
M    /usr/bin/col
M    /usr/bin/colcrt
M    /usr/bin/colrm
M    /usr/bin/column
M    /usr/bin/comm
M    /usr/bin/coredumpctl
M    /usr/bin/cp
M    /usr/bin/cpio
M    /usr/bin/csplit
M    /usr/bin/curl
M    /usr/bin/curl-config
M    /usr/bin/cut
M    /usr/bin/cvtsudoers
M    /usr/bin/date
M    /usr/bin/dbus-cleanup-sockets
M    /usr/bin/dbus-daemon
M    /usr/bin/dbus-launch
M    /usr/bin/dbus-monitor
M    /usr/bin/dbus-run-session
M    /usr/bin/dbus-send
M    /usr/bin/dbus-test-tool
M    /usr/bin/dbus-update-activation-environment
M    /usr/bin/dbus-uuidgen
M    /usr/bin/dc
M    /usr/bin/dd
M    /usr/bin/debuginfod
M    /usr/bin/debuginfod-find
M    /usr/bin/deltainfoxml2solv
M    /usr/bin/derb
M    /usr/bin/df
M    /usr/bin/dir
M    /usr/bin/dircolors
M    /usr/bin/dirmngr
M    /usr/bin/dirmngr-client
M    /usr/bin/dirname
M    /usr/bin/dmesg
M    /usr/bin/du
M    /usr/bin/dumpsexp
M    /usr/bin/dumpsolv
M    /usr/bin/echo
M    /usr/bin/eject
M    /usr/bin/env
M    /usr/bin/eu-addr2line
M    /usr/bin/eu-ar
M    /usr/bin/eu-elfclassify
M    /usr/bin/eu-elfcmp
M    /usr/bin/eu-elfcompress
M    /usr/bin/eu-elflint
M    /usr/bin/eu-findtextrel
M    /usr/bin/eu-nm
M    /usr/bin/eu-objdump
M    /usr/bin/eu-ranlib
M    /usr/bin/eu-readelf
M    /usr/bin/eu-size
M    /usr/bin/eu-stack
M    /usr/bin/eu-strings
M    /usr/bin/eu-strip
M    /usr/bin/eu-unstrip
M    /usr/bin/expand
M    /usr/bin/expiry
M    /usr/bin/expr
M    /usr/bin/factor
M    /usr/bin/faillog
M    /usr/bin/fallocate
M    /usr/bin/false
M    /usr/bin/file
M    /usr/bin/filecap
M    /usr/bin/fincore
M    /usr/bin/find
M    /usr/bin/findmnt
M    /usr/bin/finger
M    /usr/bin/flex
M    /usr/bin/flock
M    /usr/bin/fmt
M    /usr/bin/fold
M    /usr/bin/free
M    /usr/bin/fusermount
M    /usr/bin/gawk
M    /usr/bin/gawk-5.1.0
M    /usr/bin/gdbm_dump
M    /usr/bin/gdbm_load
M    /usr/bin/gdbmtool
M    /usr/bin/genbrk
M    /usr/bin/gencat
M    /usr/bin/gencfu
M    /usr/bin/gencnval
M    /usr/bin/gendict
M    /usr/bin/gendiff
M    /usr/bin/genrb
M    /usr/bin/getconf
M    /usr/bin/getent
M    /usr/bin/getfattr
M    /usr/bin/getopt
M    /usr/bin/gnutls-cli
M    /usr/bin/gnutls-cli-debug
M    /usr/bin/gnutls-serv
M    /usr/bin/gpasswd
M    /usr/bin/gpg
M    /usr/bin/gpg-agent
M    /usr/bin/gpg-connect-agent
M    /usr/bin/gpg-error
M    /usr/bin/gpg-wks-server
M    /usr/bin/gpgconf
M    /usr/bin/gpgparsemail
M    /usr/bin/gpgscm
M    /usr/bin/gpgsm
M    /usr/bin/gpgsplit
M    /usr/bin/gpgtar
M    /usr/bin/gpgv
M    /usr/bin/grep
M    /usr/bin/groups
M    /usr/bin/grub2-editenv
M    /usr/bin/grub2-file
M    /usr/bin/grub2-fstest
M    /usr/bin/grub2-glue-efi
M    /usr/bin/grub2-menulst2cfg
M    /usr/bin/grub2-mkimage
M    /usr/bin/grub2-mklayout
M    /usr/bin/grub2-mknetdir
M    /usr/bin/grub2-mkpasswd-pbkdf2
M    /usr/bin/grub2-mkrelpath
M    /usr/bin/grub2-mkrescue
M    /usr/bin/grub2-mkstandalone
M    /usr/bin/grub2-render-label
M    /usr/bin/grub2-script-check
M    /usr/bin/grub2-syslinux2cfg
M    /usr/bin/gss-client
M    /usr/bin/guile
M    /usr/bin/gzip
M    /usr/bin/hardlink
M    /usr/bin/head
M    /usr/bin/hexdump
M    /usr/bin/hmac256
M    /usr/bin/hostid
M    /usr/bin/hostname
M    /usr/bin/hostnamectl
M    /usr/bin/iconv
M    /usr/bin/icuinfo
M    /usr/bin/id
M    /usr/bin/infocmp
M    /usr/bin/install
M    /usr/bin/installcheck
M    /usr/bin/ionice
M    /usr/bin/ipcmk
M    /usr/bin/ipcrm
M    /usr/bin/ipcs
M    /usr/bin/irqtop
M    /usr/bin/isosize
M    /usr/bin/join
M    /usr/bin/journalctl
M    /usr/bin/js78
M    /usr/bin/json-glib-format
M    /usr/bin/json-glib-validate
M    /usr/bin/kadmin
M    /usr/bin/kbxutil
M    /usr/bin/kdestroy
M    /usr/bin/kernel-install
M    /usr/bin/kill
M    /usr/bin/kinit
M    /usr/bin/klist
M    /usr/bin/kmod
M    /usr/bin/kpasswd
M    /usr/bin/kswitch
M    /usr/bin/ktutil
M    /usr/bin/kvno
M    /usr/bin/last
M    /usr/bin/lastlog
M    /usr/bin/ldapcompare
M    /usr/bin/ldapdelete
M    /usr/bin/ldapexop
M    /usr/bin/ldapmodify
M    /usr/bin/ldapmodrdn
M    /usr/bin/ldappasswd
M    /usr/bin/ldapsearch
M    /usr/bin/ldapurl
M    /usr/bin/ldapwhoami
M    /usr/bin/libtool
M    /usr/bin/link
M    /usr/bin/ln
M    /usr/bin/locale
M    /usr/bin/localectl
M    /usr/bin/localedef
M    /usr/bin/locate
M    /usr/bin/logger
M    /usr/bin/login
M    /usr/bin/loginctl
M    /usr/bin/logname
M    /usr/bin/look
M    /usr/bin/ls
M    /usr/bin/lsattr
M    /usr/bin/lsblk
M    /usr/bin/lscpu
M    /usr/bin/lsipc
M    /usr/bin/lsirq
M    /usr/bin/lslocks
M    /usr/bin/lslogins
M    /usr/bin/lsmem
M    /usr/bin/lsns
M    /usr/bin/lua
M    /usr/bin/luac
M    /usr/bin/lz4
M    /usr/bin/lzmadec
M    /usr/bin/lzmainfo
M    /usr/bin/m4
M    /usr/bin/makeconv
M    /usr/bin/makedb
M    /usr/bin/mcookie
M    /usr/bin/md5sum
M    /usr/bin/mergesolv
M    /usr/bin/mesg
M    /usr/bin/mkdir
M    /usr/bin/mkfifo
M    /usr/bin/mkinitrd
M    /usr/bin/mknod
M    /usr/bin/mktemp
M    /usr/bin/modulemd-validator
M    /usr/bin/more
M    /usr/bin/mount
M    /usr/bin/mountpoint
M    /usr/bin/mpicalc
M    /usr/bin/mt
M    /usr/bin/mv
M    /usr/bin/namei
M    /usr/bin/netcap
M    /usr/bin/netstat
M    /usr/bin/nettle-hash
M    /usr/bin/nettle-lfib-stream
M    /usr/bin/nettle-pbkdf2
M    /usr/bin/networkctl
M    /usr/bin/newgidmap
M    /usr/bin/newgrp
M    /usr/bin/newrole
M    /usr/bin/newuidmap
M    /usr/bin/nice
M    /usr/bin/nl
M    /usr/bin/nohup
M    /usr/bin/nproc
M    /usr/bin/nsenter
M    /usr/bin/numfmt
M    /usr/bin/ocsptool
M    /usr/bin/od
M    /usr/bin/openssl
M    /usr/bin/ostree
M    /usr/bin/passwd
M    /usr/bin/paste
M    /usr/bin/pathchk
M    /usr/bin/pcregrep
M    /usr/bin/pcretest
M    /usr/bin/pgrep
M    /usr/bin/pidof
M    /usr/bin/pinentry-curses
M    /usr/bin/pinentry-tty
M    /usr/bin/ping
M    /usr/bin/pinky
M    /usr/bin/pk-example-frobnicate
M    /usr/bin/pk12util
M    /usr/bin/pkaction
M    /usr/bin/pkcheck
M    /usr/bin/pkcs1-conv
M    /usr/bin/pkexec
M    /usr/bin/pkg-config
M    /usr/bin/pkgdata
M    /usr/bin/pkill
M    /usr/bin/pkttyagent
M    /usr/bin/pmap
M    /usr/bin/portablectl
M    /usr/bin/pr
M    /usr/bin/printenv
M    /usr/bin/printf
M    /usr/bin/prlimit
M    /usr/bin/ps
M    /usr/bin/pscap
M    /usr/bin/psktool
M    /usr/bin/ptx
M    /usr/bin/pwd
M    /usr/bin/pwdx
M    /usr/bin/pwmake
M    /usr/bin/pwscore
M    /usr/bin/pydoc3
M    /usr/bin/python3
M    /usr/bin/readlink
M    /usr/bin/realpath
M    /usr/bin/rename
M    /usr/bin/renice
M    /usr/bin/repo2solv
M    /usr/bin/repomdxml2solv
M    /usr/bin/resolvectl
M    /usr/bin/rev
M    /usr/bin/rm
M    /usr/bin/rmdir
M    /usr/bin/rofiles-fuse
M    /usr/bin/rpcgen
M    /usr/bin/rpm
M    /usr/bin/rpm-ostree
M    /usr/bin/rpm2archive
M    /usr/bin/rpm2cpio
M    /usr/bin/rpmdb
M    /usr/bin/rpmdb2solv
M    /usr/bin/rpmgraph
M    /usr/bin/rpmkeys
M    /usr/bin/rpmmd2solv
M    /usr/bin/rpms2solv
M    /usr/bin/runcon
M    /usr/bin/sclient
M    /usr/bin/scp
M    /usr/bin/script
M    /usr/bin/scriptlive
M    /usr/bin/scriptreplay
M    /usr/bin/secon
M    /usr/bin/sed
M    /usr/bin/seq
M    /usr/bin/setarch
M    /usr/bin/setfattr
M    /usr/bin/setsid
M    /usr/bin/setterm
M    /usr/bin/sexp-conv
M    /usr/bin/sftp
M    /usr/bin/sha1sum
M    /usr/bin/sha224sum
M    /usr/bin/sha256sum
M    /usr/bin/sha384sum
M    /usr/bin/sha512sum
M    /usr/bin/shred
M    /usr/bin/shuf
M    /usr/bin/sim_client
M    /usr/bin/slabtop
M    /usr/bin/sleep
M    /usr/bin/sort
M    /usr/bin/split
M    /usr/bin/srptool
M    /usr/bin/ssh
M    /usr/bin/ssh-add
M    /usr/bin/ssh-agent
M    /usr/bin/ssh-keygen
M    /usr/bin/ssh-keyscan
M    /usr/bin/stat
M    /usr/bin/stdbuf
M    /usr/bin/stty
M    /usr/bin/su
M    /usr/bin/sudo
M    /usr/bin/sudoreplay
M    /usr/bin/sum
M    /usr/bin/sync
M    /usr/bin/systemctl
M    /usr/bin/systemd-analyze
M    /usr/bin/systemd-ask-password
M    /usr/bin/systemd-cat
M    /usr/bin/systemd-cgls
M    /usr/bin/systemd-cgtop
M    /usr/bin/systemd-delta
M    /usr/bin/systemd-detect-virt
M    /usr/bin/systemd-escape
M    /usr/bin/systemd-hwdb
M    /usr/bin/systemd-id128
M    /usr/bin/systemd-inhibit
M    /usr/bin/systemd-machine-id-setup
M    /usr/bin/systemd-mount
M    /usr/bin/systemd-notify
M    /usr/bin/systemd-path
M    /usr/bin/systemd-repart
M    /usr/bin/systemd-run
M    /usr/bin/systemd-socket-activate
M    /usr/bin/systemd-stdio-bridge
M    /usr/bin/systemd-tmpfiles
M    /usr/bin/systemd-tty-ask-password-agent
M    /usr/bin/tabs
M    /usr/bin/tac
M    /usr/bin/tail
M    /usr/bin/taskset
M    /usr/bin/tee
M    /usr/bin/test
M    /usr/bin/testsolv
M    /usr/bin/tic
M    /usr/bin/timedatectl
M    /usr/bin/timeout
M    /usr/bin/tload
M    /usr/bin/toe
M    /usr/bin/top
M    /usr/bin/touch
M    /usr/bin/tput
M    /usr/bin/tr
M    /usr/bin/tracepath
M    /usr/bin/traceroute6
M    /usr/bin/true
M    /usr/bin/truncate
M    /usr/bin/tset
M    /usr/bin/tsort
M    /usr/bin/tty
M    /usr/bin/uconv
M    /usr/bin/udevadm
M    /usr/bin/ul
M    /usr/bin/ulockmgr_server
M    /usr/bin/umount
M    /usr/bin/uname
M    /usr/bin/unexpand
M    /usr/bin/uniq
M    /usr/bin/unlink
M    /usr/bin/unshare
M    /usr/bin/unzck
M    /usr/bin/updateinfoxml2solv
M    /usr/bin/uptime
M    /usr/bin/userdbctl
M    /usr/bin/users
M    /usr/bin/utmpdump
M    /usr/bin/uuclient
M    /usr/bin/uuidgen
M    /usr/bin/uuidparse
M    /usr/bin/vdir
M    /usr/bin/vim
M    /usr/bin/vmhgfs-fuse
M    /usr/bin/vmstat
M    /usr/bin/vmtoolsd
M    /usr/bin/vmware-checkvm
M    /usr/bin/vmware-hgfsclient
M    /usr/bin/vmware-namespace-cmd
M    /usr/bin/vmware-rpctool
M    /usr/bin/vmware-toolbox-cmd
M    /usr/bin/vmware-vgauth-cmd
M    /usr/bin/vmware-vgauth-smoketest
M    /usr/bin/vmware-vmblock-fuse
M    /usr/bin/vmware-xferlogs
M    /usr/bin/w
M    /usr/bin/wall
M    /usr/bin/watch
M    /usr/bin/watchgnupg
M    /usr/bin/wc
M    /usr/bin/wdctl
M    /usr/bin/whereis
M    /usr/bin/which
M    /usr/bin/who
M    /usr/bin/whoami
M    /usr/bin/xargs
M    /usr/bin/xmlcatalog
M    /usr/bin/xmllint
M    /usr/bin/xmlsec1
M    /usr/bin/xmlwf
M    /usr/bin/xsltproc
M    /usr/bin/xz
M    /usr/bin/xzdec
M    /usr/bin/yat2m
M    /usr/bin/yes
M    /usr/bin/zck
M    /usr/bin/zck_delta_size
M    /usr/bin/zck_gen_zdict
M    /usr/bin/zck_read_header
M    /usr/bin/zckdl
M    /usr/bin/zstd
M    /usr/bin/rpm-ostree-server/mkostreerepo
M    /usr/etc/ld.so.cache
M    /usr/etc/photon-release
M    /usr/etc/shadow
M    /usr/etc/sudoers
M    /usr/etc/cloud/cloud.cfg
M    /usr/etc/iproute2/rt_protos
M    /usr/etc/pam.d/vmtoolsd
M    /usr/etc/systemd/journald.conf
M    /usr/etc/systemd/logind.conf
M    /usr/etc/systemd/networkd.conf
M    /usr/etc/systemd/resolved.conf
M    /usr/etc/systemd/system.conf
M    /usr/etc/systemd/user.conf
M    /usr/etc/udev/hwdb.bin
M    /usr/etc/udev/udev.conf
M    /usr/etc/udev/rules.d/99-vmware-hotplug.rules
M    /usr/etc/vmware-tools/tools.conf.example
M    /usr/etc/vmware-tools/vgauth.conf
M    /usr/include/sudo_plugin.h
M    /usr/lib/e2initrd_helper
M    /usr/lib/ld-2.32.so
M    /usr/lib/libBrokenLocale-2.32.so
M    /usr/lib/libDeployPkg.so.0.0.0
M    /usr/lib/libSegFault.so
M    /usr/lib/libacl.so.1.1.2253
M    /usr/lib/libanl-2.32.so
M    /usr/lib/libarchive.so.13.4.3
M    /usr/lib/libasm-0.181.so
M    /usr/lib/libassuan.so.0.8.3
M    /usr/lib/libattr.so.1.1.2448
M    /usr/lib/libaudit.so.1.0.0
M    /usr/lib/libauparse.so.0.0.0
M    /usr/lib/libblkid.so.1.1.0
M    /usr/lib/libbz2.so.1.0.8
M    /usr/lib/libc-2.32.so
M    /usr/lib/libcap-ng.so.0.0.0
M    /usr/lib/libcap.so.2.43
M    /usr/lib/libcom_err.so.2.1
M    /usr/lib/libcord.so.1.4.0
M    /usr/lib/libcrack.so.2.9.0
M    /usr/lib/libcrypt-2.32.so
M    /usr/lib/libcrypto.so.1.1
M    /usr/lib/libcurl.so.4
M    /usr/lib/libdb-5.3.so
M    /usr/lib/libdbus-1.so.3.29.0
M    /usr/lib/libdebuginfod-0.181.so
M    /usr/lib/libdevmapper.so.1.02
M    /usr/lib/libdhcp.a
M    /usr/lib/libdhcpctl.a
M    /usr/lib/libdl-2.32.so
M    /usr/lib/libdnet.1.0.1
M    /usr/lib/libdw-0.181.so
M    /usr/lib/libe2p.so.2.3
M    /usr/lib/libelf-0.181.so
M    /usr/lib/libexpat.so.1.6.11
M    /usr/lib/libexslt.so.0.8.20
M    /usr/lib/libext2fs.so.2.4
M    /usr/lib/libfdisk.so.1.1.0
M    /usr/lib/libffi.so.7.1.0
M    /usr/lib/libfl.so.2.0.0
M    /usr/lib/libformw.so.6.2
M    /usr/lib/libfreebl3.chk
M    /usr/lib/libfreebl3.so
M    /usr/lib/libfreeblpriv3.chk
M    /usr/lib/libfreeblpriv3.so
M    /usr/lib/libfuse.so.2.9.9
M    /usr/lib/libgc.so.1.4.3
M    /usr/lib/libgcc_s.so.1
M    /usr/lib/libgccpp.so.1.4.0
M    /usr/lib/libgcrypt.so.20.2.6
M    /usr/lib/libgdbm.so.6.0.0
M    /usr/lib/libgdbm_compat.so.4.0.0
M    /usr/lib/libgio-2.0.so.0.6600.1
M    /usr/lib/libgirepository-1.0.so.1.0.0
M    /usr/lib/libglib-2.0.so.0.6600.1
M    /usr/lib/libgmodule-2.0.so.0.6600.1
M    /usr/lib/libgmp.so.10.4.0
M    /usr/lib/libgnutls.so.30.28.1
M    /usr/lib/libgnutlsxx.so.28.1.0
M    /usr/lib/libgobject-2.0.so.0.6600.1
M    /usr/lib/libgpg-error.so.0.30.0
M    /usr/lib/libgpgme.so.11.23.0
M    /usr/lib/libgssapi_krb5.so.2.2
M    /usr/lib/libgssrpc.so.4.2
M    /usr/lib/libgthread-2.0.so.0.6600.1
M    /usr/lib/libguestlib.so.0.0.0
M    /usr/lib/libguile-2.0.so.22.8.1
M    /usr/lib/libguilereadline-v-18.so.18.0.0
M    /usr/lib/libhgfs.so.0.0.0
M    /usr/lib/libhistory.so.7.0
M    /usr/lib/libhogweed.so.6.0
M    /usr/lib/libicui18n.so.67.1
M    /usr/lib/libicuio.so.67.1
M    /usr/lib/libicutest.so.67.1
M    /usr/lib/libicutu.so.67.1
M    /usr/lib/libicuuc.so.67.1
M    /usr/lib/libip4tc.so.2.0.0
M    /usr/lib/libip6tc.so.2.0.0
M    /usr/lib/libipq.so.0.0.0
M    /usr/lib/libjson-c.so.5.1.0
M    /usr/lib/libjson-glib-1.0.so.0.600.0
M    /usr/lib/libk5crypto.so.3.1
M    /usr/lib/libkadm5clnt_mit.so.11.0
M    /usr/lib/libkadm5srv_mit.so.11.0
M    /usr/lib/libkdb5.so.9.0
M    /usr/lib/libkmod.so.2.3.5
M    /usr/lib/libkrad.so.0.0
M    /usr/lib/libkrb5.so.3.3
M    /usr/lib/libkrb5support.so.0.1
M    /usr/lib/libksba.so.8.12.0
M    /usr/lib/liblber-2.4.so.2.11.1
M    /usr/lib/libldap-2.4.so.2.11.1
M    /usr/lib/libldap_r-2.4.so.2.11.1
M    /usr/lib/libltdl.so.7.3.1
M    /usr/lib/liblua.so.5.3.4
M    /usr/lib/liblz4.so.1.9.2
M    /usr/lib/liblzma.so.5.2.5
M    /usr/lib/libm-2.32.so
M    /usr/lib/libmagic.so.1.0.0
M    /usr/lib/libmemusage.so
M    /usr/lib/libmenuw.so.6.2
M    /usr/lib/libmetalink.so.3.1.0
M    /usr/lib/libmicrohttpd.so.12.56.0
M    /usr/lib/libmodulemd.so.2
M    /usr/lib/libmount.so.1.1.0
M    /usr/lib/libmozjs-78.so
M    /usr/lib/libmpfr.so.6.1.0
M    /usr/lib/libmspack.so.0.1.0
M    /usr/lib/libmvec-2.32.so
M    /usr/lib/libncursesw.so.6.2
M    /usr/lib/libnettle.so.8.0
M    /usr/lib/libnpth.so.0.1.2
M    /usr/lib/libnsl-2.32.so
M    /usr/lib/libnsl.so.2.0.1
M    /usr/lib/libnspr4.so
M    /usr/lib/libnss3.so
M    /usr/lib/libnss_altfiles.so.2
M    /usr/lib/libnss_compat-2.32.so
M    /usr/lib/libnss_db-2.32.so
M    /usr/lib/libnss_dns-2.32.so
M    /usr/lib/libnss_files-2.32.so
M    /usr/lib/libnss_hesiod-2.32.so
M    /usr/lib/libnss_myhostname.so.2
M    /usr/lib/libnss_mymachines.so.2
M    /usr/lib/libnss_resolve.so.2
M    /usr/lib/libnss_systemd.so.2
M    /usr/lib/libnssckbi-testlib.so
M    /usr/lib/libnssckbi.so
M    /usr/lib/libnssdbm3.chk
M    /usr/lib/libnssdbm3.so
M    /usr/lib/libnsssysinit.so
M    /usr/lib/libnssutil3.so
M    /usr/lib/libomapi.a
M    /usr/lib/libopts.so.25.17.1
M    /usr/lib/libostree-1.so.1.0.0
M    /usr/lib/libpam.so.0.85.1
M    /usr/lib/libpam_misc.so.0.82.1
M    /usr/lib/libpamc.so.0.82.1
M    /usr/lib/libpanelw.so.6.2
M    /usr/lib/libpcre.so.1.2.12
M    /usr/lib/libpcre16.so.0.2.12
M    /usr/lib/libpcre32.so.0.0.12
M    /usr/lib/libpcrecpp.so.0.0.2
M    /usr/lib/libpcreposix.so.0.0.7
M    /usr/lib/libpkcs11testmodule.so
M    /usr/lib/libplc4.so
M    /usr/lib/libplds4.so
M    /usr/lib/libpolkit-agent-1.so.0.0.0
M    /usr/lib/libpolkit-gobject-1.so.0.0.0
M    /usr/lib/libpopt.so.0.0.0
M    /usr/lib/libprocps.so.8.0.2
M    /usr/lib/libpsl.so.5.3.3
M    /usr/lib/libpthread-2.32.so
M    /usr/lib/libpwquality.so.1.0.2
M    /usr/lib/libpython3.so
M    /usr/lib/libreadline.so.7.0
M    /usr/lib/librepo.so.0
M    /usr/lib/libresolv-2.32.so
M    /usr/lib/librpmostree-1.so.1.0.0
M    /usr/lib/librt-2.32.so
M    /usr/lib/libsasl2.so.3.0.0
M    /usr/lib/libseccomp.so.2.5.0
M    /usr/lib/libselinux.so.1
M    /usr/lib/libsemanage.so.1
M    /usr/lib/libsepol.so.1
M    /usr/lib/libsmartcols.so.1.1.0
M    /usr/lib/libsmime3.so
M    /usr/lib/libsoftokn3.chk
M    /usr/lib/libsoftokn3.so
M    /usr/lib/libsolv.so.0
M    /usr/lib/libsolvext.so.0
M    /usr/lib/libsoup-2.4.so.1.11.0
M    /usr/lib/libsoup-gnome-2.4.so.1.11.0
M    /usr/lib/libsqlite3.so.0.8.6
M    /usr/lib/libss.so.2.0
M    /usr/lib/libssh2.so.1.0.1
M    /usr/lib/libssl.so.1.1
M    /usr/lib/libssl3.so
M    /usr/lib/libstdc++.so.6
M    /usr/lib/libsystemd.so.0
M    /usr/lib/libtasn1.so.6.5.6
M    /usr/lib/libthread_db-1.0.so
M    /usr/lib/libtirpc.so.3.0.0
M    /usr/lib/libudev.so.1
M    /usr/lib/libulockmgr.so.1.0.1
M    /usr/lib/libunistring.a
M    /usr/lib/libunistring.so.2.1.0
M    /usr/lib/libutil-2.32.so
M    /usr/lib/libuuid.so.1.3.0
M    /usr/lib/libverto.so.0.0
M    /usr/lib/libvgauth.so.0.0.0
M    /usr/lib/libvmtools.so.0.0.0
M    /usr/lib/libwrap.a
M    /usr/lib/libwrap.so.0.7.6
M    /usr/lib/libxml2.so.2.9.10
M    /usr/lib/libxmlsec1-nss.so.1.2.30
M    /usr/lib/libxmlsec1-openssl.so.1.2.30
M    /usr/lib/libxmlsec1.so.1.2.30
M    /usr/lib/libxslt.so.1.1.34
M    /usr/lib/libxtables.so.12
M    /usr/lib/libyaml-0.so.2.0.9
M    /usr/lib/libz.so.1.2.11
M    /usr/lib/libzck.so.1.1.7
M    /usr/lib/libzstd.so.1.4.5
M    /usr/lib/bash/basename
M    /usr/lib/bash/dirname
M    /usr/lib/bash/fdflags
M    /usr/lib/bash/finfo
M    /usr/lib/bash/head
M    /usr/lib/bash/id
M    /usr/lib/bash/ln
M    /usr/lib/bash/logname
M    /usr/lib/bash/mkdir
M    /usr/lib/bash/mypid
M    /usr/lib/bash/pathchk
M    /usr/lib/bash/print
M    /usr/lib/bash/printenv
M    /usr/lib/bash/push
M    /usr/lib/bash/realpath
M    /usr/lib/bash/rmdir
M    /usr/lib/bash/seq
M    /usr/lib/bash/setpgid
M    /usr/lib/bash/sleep
M    /usr/lib/bash/strftime
M    /usr/lib/bash/sync
M    /usr/lib/bash/tee
M    /usr/lib/bash/truefalse
M    /usr/lib/bash/tty
M    /usr/lib/bash/uname
M    /usr/lib/bash/unlink
M    /usr/lib/bash/whoami
M    /usr/lib/cloud-init/ds-identify
M    /usr/lib/dracut/dracut-install
M    /usr/lib/dracut/dracut-version.sh
M    /usr/lib/dracut/skipcpio
M    /usr/lib/engines-1.1/afalg.so
M    /usr/lib/engines-1.1/capi.so
M    /usr/lib/engines-1.1/padlock.so
M    /usr/lib/gawk/filefuncs.so
M    /usr/lib/gawk/fnmatch.so
M    /usr/lib/gawk/fork.so
M    /usr/lib/gawk/inplace.so
M    /usr/lib/gawk/intdiv.so
M    /usr/lib/gawk/ordchr.so
M    /usr/lib/gawk/readdir.so
M    /usr/lib/gawk/readfile.so
M    /usr/lib/gawk/revoutput.so
M    /usr/lib/gawk/revtwoway.so
M    /usr/lib/gawk/rwarray.so
M    /usr/lib/gawk/time.so
M    /usr/lib/gconv/ANSI_X3.110.so
M    /usr/lib/gconv/ARMSCII-8.so
M    /usr/lib/gconv/ASMO_449.so
M    /usr/lib/gconv/BIG5.so
M    /usr/lib/gconv/BIG5HKSCS.so
M    /usr/lib/gconv/BRF.so
M    /usr/lib/gconv/CP10007.so
M    /usr/lib/gconv/CP1125.so
M    /usr/lib/gconv/CP1250.so
M    /usr/lib/gconv/CP1251.so
M    /usr/lib/gconv/CP1252.so
M    /usr/lib/gconv/CP1253.so
M    /usr/lib/gconv/CP1254.so
M    /usr/lib/gconv/CP1255.so
M    /usr/lib/gconv/CP1256.so
M    /usr/lib/gconv/CP1257.so
M    /usr/lib/gconv/CP1258.so
M    /usr/lib/gconv/CP737.so
M    /usr/lib/gconv/CP770.so
M    /usr/lib/gconv/CP771.so
M    /usr/lib/gconv/CP772.so
M    /usr/lib/gconv/CP773.so
M    /usr/lib/gconv/CP774.so
M    /usr/lib/gconv/CP775.so
M    /usr/lib/gconv/CP932.so
M    /usr/lib/gconv/CSN_369103.so
M    /usr/lib/gconv/CWI.so
M    /usr/lib/gconv/DEC-MCS.so
M    /usr/lib/gconv/EBCDIC-AT-DE-A.so
M    /usr/lib/gconv/EBCDIC-AT-DE.so
M    /usr/lib/gconv/EBCDIC-CA-FR.so
M    /usr/lib/gconv/EBCDIC-DK-NO-A.so
M    /usr/lib/gconv/EBCDIC-DK-NO.so
M    /usr/lib/gconv/EBCDIC-ES-A.so
M    /usr/lib/gconv/EBCDIC-ES-S.so
M    /usr/lib/gconv/EBCDIC-ES.so
M    /usr/lib/gconv/EBCDIC-FI-SE-A.so
M    /usr/lib/gconv/EBCDIC-FI-SE.so
M    /usr/lib/gconv/EBCDIC-FR.so
M    /usr/lib/gconv/EBCDIC-IS-FRISS.so
M    /usr/lib/gconv/EBCDIC-IT.so
M    /usr/lib/gconv/EBCDIC-PT.so
M    /usr/lib/gconv/EBCDIC-UK.so
M    /usr/lib/gconv/EBCDIC-US.so
M    /usr/lib/gconv/ECMA-CYRILLIC.so
M    /usr/lib/gconv/EUC-CN.so
M    /usr/lib/gconv/EUC-JISX0213.so
M    /usr/lib/gconv/EUC-JP-MS.so
M    /usr/lib/gconv/EUC-JP.so
M    /usr/lib/gconv/EUC-KR.so
M    /usr/lib/gconv/EUC-TW.so
M    /usr/lib/gconv/GB18030.so
M    /usr/lib/gconv/GBBIG5.so
M    /usr/lib/gconv/GBGBK.so
M    /usr/lib/gconv/GBK.so
M    /usr/lib/gconv/GEORGIAN-ACADEMY.so
M    /usr/lib/gconv/GEORGIAN-PS.so
M    /usr/lib/gconv/GOST_19768-74.so
M    /usr/lib/gconv/GREEK-CCITT.so
M    /usr/lib/gconv/GREEK7-OLD.so
M    /usr/lib/gconv/GREEK7.so
M    /usr/lib/gconv/HP-GREEK8.so
M    /usr/lib/gconv/HP-ROMAN8.so
M    /usr/lib/gconv/HP-ROMAN9.so
M    /usr/lib/gconv/HP-THAI8.so
M    /usr/lib/gconv/HP-TURKISH8.so
M    /usr/lib/gconv/IBM037.so
M    /usr/lib/gconv/IBM038.so
M    /usr/lib/gconv/IBM1004.so
M    /usr/lib/gconv/IBM1008.so
M    /usr/lib/gconv/IBM1008_420.so
M    /usr/lib/gconv/IBM1025.so
M    /usr/lib/gconv/IBM1026.so
M    /usr/lib/gconv/IBM1046.so
M    /usr/lib/gconv/IBM1047.so
M    /usr/lib/gconv/IBM1097.so
M    /usr/lib/gconv/IBM1112.so
M    /usr/lib/gconv/IBM1122.so
M    /usr/lib/gconv/IBM1123.so
M    /usr/lib/gconv/IBM1124.so
M    /usr/lib/gconv/IBM1129.so
M    /usr/lib/gconv/IBM1130.so
M    /usr/lib/gconv/IBM1132.so
M    /usr/lib/gconv/IBM1133.so
M    /usr/lib/gconv/IBM1137.so
M    /usr/lib/gconv/IBM1140.so
M    /usr/lib/gconv/IBM1141.so
M    /usr/lib/gconv/IBM1142.so
M    /usr/lib/gconv/IBM1143.so
M    /usr/lib/gconv/IBM1144.so
M    /usr/lib/gconv/IBM1145.so
M    /usr/lib/gconv/IBM1146.so
M    /usr/lib/gconv/IBM1147.so
M    /usr/lib/gconv/IBM1148.so
M    /usr/lib/gconv/IBM1149.so
M    /usr/lib/gconv/IBM1153.so
M    /usr/lib/gconv/IBM1154.so
M    /usr/lib/gconv/IBM1155.so
M    /usr/lib/gconv/IBM1156.so
M    /usr/lib/gconv/IBM1157.so
M    /usr/lib/gconv/IBM1158.so
M    /usr/lib/gconv/IBM1160.so
M    /usr/lib/gconv/IBM1161.so
M    /usr/lib/gconv/IBM1162.so
M    /usr/lib/gconv/IBM1163.so
M    /usr/lib/gconv/IBM1164.so
M    /usr/lib/gconv/IBM1166.so
M    /usr/lib/gconv/IBM1167.so
M    /usr/lib/gconv/IBM12712.so
M    /usr/lib/gconv/IBM1364.so
M    /usr/lib/gconv/IBM1371.so
M    /usr/lib/gconv/IBM1388.so
M    /usr/lib/gconv/IBM1390.so
M    /usr/lib/gconv/IBM1399.so
M    /usr/lib/gconv/IBM16804.so
M    /usr/lib/gconv/IBM256.so
M    /usr/lib/gconv/IBM273.so
M    /usr/lib/gconv/IBM274.so
M    /usr/lib/gconv/IBM275.so
M    /usr/lib/gconv/IBM277.so
M    /usr/lib/gconv/IBM278.so
M    /usr/lib/gconv/IBM280.so
M    /usr/lib/gconv/IBM281.so
M    /usr/lib/gconv/IBM284.so
M    /usr/lib/gconv/IBM285.so
M    /usr/lib/gconv/IBM290.so
M    /usr/lib/gconv/IBM297.so
M    /usr/lib/gconv/IBM420.so
M    /usr/lib/gconv/IBM423.so
M    /usr/lib/gconv/IBM424.so
M    /usr/lib/gconv/IBM437.so
M    /usr/lib/gconv/IBM4517.so
M    /usr/lib/gconv/IBM4899.so
M    /usr/lib/gconv/IBM4909.so
M    /usr/lib/gconv/IBM4971.so
M    /usr/lib/gconv/IBM500.so
M    /usr/lib/gconv/IBM5347.so
M    /usr/lib/gconv/IBM803.so
M    /usr/lib/gconv/IBM850.so
M    /usr/lib/gconv/IBM851.so
M    /usr/lib/gconv/IBM852.so
M    /usr/lib/gconv/IBM855.so
M    /usr/lib/gconv/IBM856.so
M    /usr/lib/gconv/IBM857.so
M    /usr/lib/gconv/IBM858.so
M    /usr/lib/gconv/IBM860.so
M    /usr/lib/gconv/IBM861.so
M    /usr/lib/gconv/IBM862.so
M    /usr/lib/gconv/IBM863.so
M    /usr/lib/gconv/IBM864.so
M    /usr/lib/gconv/IBM865.so
M    /usr/lib/gconv/IBM866.so
M    /usr/lib/gconv/IBM866NAV.so
M    /usr/lib/gconv/IBM868.so
M    /usr/lib/gconv/IBM869.so
M    /usr/lib/gconv/IBM870.so
M    /usr/lib/gconv/IBM871.so
M    /usr/lib/gconv/IBM874.so
M    /usr/lib/gconv/IBM875.so
M    /usr/lib/gconv/IBM880.so
M    /usr/lib/gconv/IBM891.so
M    /usr/lib/gconv/IBM901.so
M    /usr/lib/gconv/IBM902.so
M    /usr/lib/gconv/IBM903.so
M    /usr/lib/gconv/IBM9030.so
M    /usr/lib/gconv/IBM904.so
M    /usr/lib/gconv/IBM905.so
M    /usr/lib/gconv/IBM9066.so
M    /usr/lib/gconv/IBM918.so
M    /usr/lib/gconv/IBM921.so
M    /usr/lib/gconv/IBM922.so
M    /usr/lib/gconv/IBM930.so
M    /usr/lib/gconv/IBM932.so
M    /usr/lib/gconv/IBM933.so
M    /usr/lib/gconv/IBM935.so
M    /usr/lib/gconv/IBM937.so
M    /usr/lib/gconv/IBM939.so
M    /usr/lib/gconv/IBM943.so
M    /usr/lib/gconv/IBM9448.so
M    /usr/lib/gconv/IEC_P27-1.so
```


## Listing package differences

We can also look at package differences, as you expect, using the right tool for the job.

```console
root@photon-7c2d910d79e9 [ ~ ]# rpm-ostree db diff 820b 965c
ostree diff commit from: 820b (820b584a6f90bf6b9b8cb6aad8c093064b88d0ab686be8130baa03d68917ad88)
ostree diff commit to:   965c (965c1abeb048e1a8ff77e9cd34ffccc5e3356176cda3332b4ff0e7a6c66b661f)
Upgraded:
audit 2.8.5-3.ph4 -> 2.8.5-6.ph4
cloud-init 20.3-2.ph4 -> 20.4.1-1.ph4
cpio 2.13-1.ph4 -> 2.13-3.ph4
curl 7.72.0-2.ph4 -> 7.74.0-1.ph4
curl-libs 7.72.0-2.ph4 -> 7.74.0-1.ph4
cyrus-sasl 2.1.27-3.ph4 -> 2.1.27-4.ph4
dhcp-client 4.4.2-1.ph4 -> 4.4.2-2.ph4
dhcp-libs 4.4.2-1.ph4 -> 4.4.2-2.ph4
dracut 050-5.ph4 -> 050-7.ph4
dracut-tools 050-5.ph4 -> 050-7.ph4
file 5.39-1.ph4 -> 5.39-2.ph4
file-libs 5.39-1.ph4 -> 5.39-2.ph4
gdbm 1.18.1-1.ph4 -> 1.19-1.ph4
glibc 2.32-1.ph4 -> 2.32-2.ph4
glibc-iconv 2.32-1.ph4 -> 2.32-2.ph4
gobject-introspection 1.66.0-1.ph4 -> 1.66.0-3.ph4
grub2-theme 4.0-1.ph4 -> 4.0-2.ph4
grub2-theme-ostree 4.0-1.ph4 -> 4.0-2.ph4
iproute2 5.8.0-1.ph4 -> 5.10.0-1.ph4
iptables 1.8.4-1.ph4 -> 1.8.7-1.ph4
json-c 0.15-2.ph4 -> 0.15-3.ph4
libgcc 8.4.0-1.ph4 -> 10.2.0-1.ph4
libmetalink 0.1.3-2.ph4 -> 0.1.3-3.ph4
libmodulemd 2.9.4-1.ph4 -> 2.11.0-1.ph4
librepo 1.12.1-3.ph4 -> 1.12.1-4.ph4
libsepol 3.1-1.ph4 -> 3.1-2.ph4
libsolv 0.6.35-5.ph4 -> 0.6.35-7.ph4
libssh2 1.9.0-2.ph4 -> 1.9.0-3.ph4
libstdc++ 8.4.0-1.ph4 -> 10.2.0-1.ph4
libxml2 2.9.10-3.ph4 -> 2.9.10-6.ph4
libxml2-devel 2.9.10-3.ph4 -> 2.9.10-6.ph4
libxslt 1.1.34-1.ph4 -> 1.1.34-2.ph4
linux 5.9.0-3.ph4 -> 5.10.4-15.ph4
ncurses 6.2-2.ph4 -> 6.2-3.ph4
ncurses-libs 6.2-2.ph4 -> 6.2-3.ph4
ncurses-terminfo 6.2-2.ph4 -> 6.2-3.ph4
nss 3.57-1.ph4 -> 3.57-2.ph4
nss-libs 3.57-1.ph4 -> 3.57-2.ph4
open-vm-tools 11.1.5-4.ph4 -> 11.2.5-1.ph4
openldap 2.4.53-2.ph4 -> 2.4.53-3.ph4
openssl 1.1.1g-3.ph4 -> 1.1.1i-2.ph4
pcre 8.44-1.ph4 -> 8.44-2.ph4
pcre-libs 8.44-1.ph4 -> 8.44-2.ph4
python3 3.8.6-1.ph4 -> 3.9.1-2.ph4
python3-PyYAML 5.3.1-1.ph4 -> 5.4.1-1.ph4
python3-attrs 20.2.0-2.ph4 -> 20.3.0-2.ph4
python3-cryptography 3.1.1-2.ph4 -> 3.2.1-1.ph4
python3-gobject-introspection 1.66.0-1.ph4 -> 1.66.0-3.ph4
python3-libs 3.8.6-1.ph4 -> 3.9.1-2.ph4
python3-packaging 20.4-2.ph4 -> 20.4-3.ph4
python3-pyrsistent 0.17.3-1.ph4 -> 0.17.3-2.ph4
python3-setuptools 3.8.6-1.ph4 -> 3.9.1-2.ph4
python3-urllib3 1.25.10-2.ph4 -> 1.25.11-1.ph4
python3-xml 3.8.6-1.ph4 -> 3.9.1-2.ph4
rpm 4.14.2-11.ph4 -> 4.16.1.2-1.ph4
rpm-libs 4.14.2-11.ph4 -> 4.16.1.2-1.ph4
rpm-ostree 2020.5-4.ph4 -> 2020.5-5.ph4
shadow 4.8.1-2.ph4 -> 4.8.1-3.ph4
shadow-tools 4.8.1-2.ph4 -> 4.8.1-3.ph4
sudo 1.8.30-2.ph4 -> 1.9.5-1.ph4
systemd 245.5-3.ph4 -> 247.3-1.ph4
util-linux 2.36-1.ph4 -> 2.36-2.ph4
util-linux-libs 2.36-1.ph4 -> 2.36-2.ph4
Added:
libpcap-1.10.0-1.ph4.x86_64
python3-Pygments-2.7.2-2.ph4.noarch
python3-alabaster-0.7.12-1.ph4.noarch
python3-babel-2.8.0-3.ph4.noarch
python3-docutils-0.16-1.ph4.noarch
python3-imagesize-1.2.0-2.ph4.noarch
python3-pytz-2020.4-2.ph4.noarch
python3-snowballstemmer-2.0.0-1.ph4.noarch
python3-sphinx-3.3.0-2.ph4.noarch
python3-sphinxcontrib-applehelp-1.0.2-1.ph4.noarch
python3-sphinxcontrib-devhelp-1.0.2-1.ph4.noarch
python3-sphinxcontrib-htmlhelp-1.0.3-1.ph4.noarch
python3-sphinxcontrib-jsmath-1.0.1-1.ph4.noarch
python3-sphinxcontrib-qthelp-1.0.3-1.ph4.noarch
python3-sphinxcontrib-serializinghtml-1.1.4-1.ph4.noarch
python3-typing-3.7.4.3-1.ph4.noarch
systemd-libs-247.3-1.ph4.x86_64
systemd-pam-247.3-1.ph4.x86_64
systemd-rpm-macros-247.3-1.ph4.noarch
systemd-udev-247.3-1.ph4.x86_64
```


## Rollback

If we want to go back to the previous image, we can rollback. The order of the images will be changed, so the old filetree will become the default bootable image. If -r option is passed, the rollback will continue with a reboot.

```console
root@photon-7c2d910d79e9 [ ~ ]# rpm-ostree rollback
Moving '965c1abeb048e1a8ff77e9cd34ffccc5e3356176cda3332b4ff0e7a6c66b661f.0' to be first deployment
Transaction complete; bootconfig swap: yes; deployment count change: 0
Upgraded:
  audit 2.8.5-3.ph4 -> 2.8.5-6.ph4
  cloud-init 20.3-2.ph4 -> 20.4.1-1.ph4
  cpio 2.13-1.ph4 -> 2.13-3.ph4
  curl 7.72.0-2.ph4 -> 7.74.0-1.ph4
  curl-libs 7.72.0-2.ph4 -> 7.74.0-1.ph4
  cyrus-sasl 2.1.27-3.ph4 -> 2.1.27-4.ph4
  dhcp-client 4.4.2-1.ph4 -> 4.4.2-2.ph4
  dhcp-libs 4.4.2-1.ph4 -> 4.4.2-2.ph4
  dracut 050-5.ph4 -> 050-7.ph4
  dracut-tools 050-5.ph4 -> 050-7.ph4
  file 5.39-1.ph4 -> 5.39-2.ph4
  file-libs 5.39-1.ph4 -> 5.39-2.ph4
  gdbm 1.18.1-1.ph4 -> 1.19-1.ph4
  glibc 2.32-1.ph4 -> 2.32-2.ph4
  glibc-iconv 2.32-1.ph4 -> 2.32-2.ph4
  gobject-introspection 1.66.0-1.ph4 -> 1.66.0-3.ph4
  grub2-theme 4.0-1.ph4 -> 4.0-2.ph4
  grub2-theme-ostree 4.0-1.ph4 -> 4.0-2.ph4
  iproute2 5.8.0-1.ph4 -> 5.10.0-1.ph4
  iptables 1.8.4-1.ph4 -> 1.8.7-1.ph4
  json-c 0.15-2.ph4 -> 0.15-3.ph4
  libgcc 8.4.0-1.ph4 -> 10.2.0-1.ph4
  libmetalink 0.1.3-2.ph4 -> 0.1.3-3.ph4
  libmodulemd 2.9.4-1.ph4 -> 2.11.0-1.ph4
  librepo 1.12.1-3.ph4 -> 1.12.1-4.ph4
  libsepol 3.1-1.ph4 -> 3.1-2.ph4
  libsolv 0.6.35-5.ph4 -> 0.6.35-7.ph4
  libssh2 1.9.0-2.ph4 -> 1.9.0-3.ph4
  libstdc++ 8.4.0-1.ph4 -> 10.2.0-1.ph4
  libxml2 2.9.10-3.ph4 -> 2.9.10-6.ph4
  libxml2-devel 2.9.10-3.ph4 -> 2.9.10-6.ph4
  libxslt 1.1.34-1.ph4 -> 1.1.34-2.ph4
  linux 5.9.0-3.ph4 -> 5.10.4-15.ph4
  ncurses 6.2-2.ph4 -> 6.2-3.ph4
  ncurses-libs 6.2-2.ph4 -> 6.2-3.ph4
  ncurses-terminfo 6.2-2.ph4 -> 6.2-3.ph4
  nss 3.57-1.ph4 -> 3.57-2.ph4
  nss-libs 3.57-1.ph4 -> 3.57-2.ph4
  open-vm-tools 11.1.5-4.ph4 -> 11.2.5-1.ph4
  openldap 2.4.53-2.ph4 -> 2.4.53-3.ph4
  openssl 1.1.1g-3.ph4 -> 1.1.1i-2.ph4
  pcre 8.44-1.ph4 -> 8.44-2.ph4
  pcre-libs 8.44-1.ph4 -> 8.44-2.ph4
  python3 3.8.6-1.ph4 -> 3.9.1-2.ph4
  python3-PyYAML 5.3.1-1.ph4 -> 5.4.1-1.ph4
  python3-attrs 20.2.0-2.ph4 -> 20.3.0-2.ph4
  python3-cryptography 3.1.1-2.ph4 -> 3.2.1-1.ph4
  python3-gobject-introspection 1.66.0-1.ph4 -> 1.66.0-3.ph4
  python3-libs 3.8.6-1.ph4 -> 3.9.1-2.ph4
  python3-packaging 20.4-2.ph4 -> 20.4-3.ph4
  python3-pyrsistent 0.17.3-1.ph4 -> 0.17.3-2.ph4
  python3-setuptools 3.8.6-1.ph4 -> 3.9.1-2.ph4
  python3-urllib3 1.25.10-2.ph4 -> 1.25.11-1.ph4
  python3-xml 3.8.6-1.ph4 -> 3.9.1-2.ph4
  rpm 4.14.2-11.ph4 -> 4.16.1.2-1.ph4
  rpm-libs 4.14.2-11.ph4 -> 4.16.1.2-1.ph4
  rpm-ostree 2020.5-4.ph4 -> 2020.5-5.ph4
  shadow 4.8.1-2.ph4 -> 4.8.1-3.ph4
  shadow-tools 4.8.1-2.ph4 -> 4.8.1-3.ph4
  sudo 1.8.30-2.ph4 -> 1.9.5-1.ph4
  systemd 245.5-3.ph4 -> 247.3-1.ph4
  util-linux 2.36-1.ph4 -> 2.36-2.ph4
  util-linux-libs 2.36-1.ph4 -> 2.36-2.ph4
Added:
  libpcap-1.10.0-1.ph4.x86_64
  python3-Pygments-2.7.2-2.ph4.noarch
  python3-alabaster-0.7.12-1.ph4.noarch
  python3-babel-2.8.0-3.ph4.noarch
  python3-docutils-0.16-1.ph4.noarch
  python3-imagesize-1.2.0-2.ph4.noarch
  python3-pytz-2020.4-2.ph4.noarch
  python3-snowballstemmer-2.0.0-1.ph4.noarch
  python3-sphinx-3.3.0-2.ph4.noarch
  python3-sphinxcontrib-applehelp-1.0.2-1.ph4.noarch
  python3-sphinxcontrib-devhelp-1.0.2-1.ph4.noarch
  python3-sphinxcontrib-htmlhelp-1.0.3-1.ph4.noarch
  python3-sphinxcontrib-jsmath-1.0.1-1.ph4.noarch
  python3-sphinxcontrib-qthelp-1.0.3-1.ph4.noarch
  python3-sphinxcontrib-serializinghtml-1.1.4-1.ph4.noarch
  python3-typing-3.7.4.3-1.ph4.noarch
  systemd-libs-247.3-1.ph4.x86_64
  systemd-pam-247.3-1.ph4.x86_64
  systemd-rpm-macros-247.3-1.ph4.noarch
  systemd-udev-247.3-1.ph4.x86_64
  Run "systemctl reboot" to start a reboot
```

In fact, we can repeat the rollback operation as many times as we want before reboot. On each execution, it's going to change the order. It will not delete any image.  
However, an upgrade will keep the current default image and will eliminate the other image, whichever that is. So if Photon installation rolled back to an older build, an upgrade will keep that, eliminate the newer version and will replace it with an even newer version at the next upgrade.  

The boot order moved back to original:

```console
root@photon-7c2d910d79e9 [ ~ ]# rpm-ostree status
State: idle
Deployments:
  ostree://photon:photon/4.0/x86_64/minimal
    Version: 4.0_minimal (2021-02-20T07:15:43Z)
Commit: 965c1abeb048e1a8ff77e9cd34ffccc5e3356176cda3332b4ff0e7a6c66b661f
  Diff: 63 upgraded, 20 added

● ostree://photon:photon/4.0/x86_64/minimal
    Version: 4.0_minimal (2020-11-04T02:21:47Z)
Commit: 820b584a6f90bf6b9b8cb6aad8c093064b88d0ab686be8130baa03d68917ad88
```

The current bootable image path moved also back to the original value:

```console
root@photon-host-def [ ~ ]# ostree admin config-diff --print-current-dir
/ostree/deploy/photon/deploy/47899767bdd4276266383fce13c4a26a51ca0304ae754609283d75f7d8aad36e.0
```

## Installing Packages

You can add more packages onto the system that are not part of the commit composed on the server.

```console
rpm-ostree install <packages>
```

**Example**:

```console
rpm-ostree install https://kojipkgs.fedoraproject.org//packages/wget/1.19.5/5.fc29/x86_64/wget-1.19.5-5.fc29.x86_64.rpm
```

## Uninstalling Packages

To remove layered packages installed from a repository, use

```console
rpm-ostree uninstall <pkg>
```

To remove layered packages installed from a local package, you must specify the full NEVRA of the package. 

For example:

```console
rpm-ostree uninstall ltrace-0.7.91-16.fc22.x86_64
```

To uninstall a package that is a part of the base layer, use 

```console
rpm-ostree override remove <pkg>
```

For example: 

```console
rpm-ostree override remove firefox
```

## Deleting a deployed filetree

It is possible to delete a deployed tree. You won't need to do that normally, as upgrading to a new image will delete the old one, but if for some reason deploying failed (loss of power, networking issues), you'll want to delete the partially deployed image.  
The only supported index is 1. (If multiple bootable images will be supported in the future, a larger than one, zero-based index of the image to delete will be supported).  
You cannot delete the default bootable filetree, so passing 0 will result in an error. 

```console
root@photon-host-def [ ~ ]# ostree admin undeploy -v 1
OT: Using bootloader: OstreeBootloaderGrub2
Transaction complete; bootconfig swap: yes deployment count change: -1
Deleted deployment a31a843985e314a9e70bcf09afe8d59f7351817d9fb743c2b6dab84f20833650

root@photon-host-cus1 [ ~ ]# ostree admin undeploy -v 0
OT: Deployment cf357c0f376decb3bae42326737db7e36bcf3568ab901c33dc57800c3718f07b.0 unlocked=0
error: Cannot undeploy currently booted deployment 0
```

Now, we can see that the newer image is gone, the deployment directory for commit a31a has been removed.

```console
root@photon-host-def [ ~ ]# rpm-ostree status
  State: idle
  AutomaticUpdates: disabled
  Deployments:
  * ostree://photon-2:photon/4.0/x86_64/minimal
      Version: 4.0_minimal (2019-09-18T12:48:03Z)
  Commit: cf357c0f376decb3bae42326737db7e36bcf3568ab901c33dc57800c3718f07b
  
  root@photon-host-cus1 [ ~ ]# ls /ostree/deploy/photon/deploy/
  cf357c0f376decb3bae42326737db7e36bcf3568ab901c33dc57800c3718f07b.0
  cf357c0f376decb3bae42326737db7e36bcf3568ab901c33dc57800c3718f07b.0.origin 
```

However the commit is still there in the OSTree repo.

```console
root@photon-7c2d910d79e9 [ ~ ]# ostree log 965c
  commit 965c1abeb048e1a8ff77e9cd34ffccc5e3356176cda3332b4ff0e7a6c66b661f
  ContentChecksum:  9bc85673bd8d5599d61a02a99accce9bc9b72612c7a3cebd35427875f6514288
  Date:  2021-02-20 07:15:43 +0000
  Version: 4.0_minimal
  (no subject)
```
    
But there is nothing to rollback to.

```console
root@photon-7c2d910d79e9 [ ~ ]# rpm-ostree rollback
Moving '820b584a6f90bf6b9b8cb6aad8c093064b88d0ab686be8130baa03d68917ad88.0' to be first deployment
Transaction complete; bootconfig swap: yes; deployment count change: 0
Run "systemctl reboot" to start a reboot
```
    
If we were to upgrade again, it would bring these packages back, but let's just check the differeneces.

```console
root@photon-7c2d910d79e9 [ ~ ]# rpm-ostree upgrade --check-diff
  ⠚ Receiving metadata objects: 0/(estimating) -/s 0 bytes... 
  Receiving metadata objects: 0/(estimating) -/s 0 bytes... done
  No updates available.
```

## Version skipping upgrade

Let's assume that after a while, VMware releases version 2 that removes **sudo** and adds **bison** and **tar**. Now, an upgrade will skip version 1 and go directly to 2. Let's first look at what packages are pulled (notice sudo missing, as expected), then upgrade with reboot option.

```console
root@photon-host-def [ ~ ]# rpm-ostree upgrade --check-diff
Updating from: photon:photon/4.0/x86_64/minimal

7 metadata, 13 content objects fetched; 1287 KiB transferred in 0 seconds
+bison-3.0.2-2.ph1.x86_64
+gawk-4.1.0-2.ph1.x86_64
+tar-1.27.1-1.ph1.x86_64
+wget-1.15-1.ph1.x86_64

root@photon-7c2d910d79e9 [ ~ ]# rpm-ostree upgrade -r
⠒ Receiving metadata objects: 0/(estimating) -/s 0 bytes... 
Receiving metadata objects: 0/(estimating) -/s 0 bytes... done
No upgrade available.
```

After reboot, let's check the booting filetrees, the current dir for the current filetree and look at commit differences:

```console
root@photon-7c2d910d79e9 [ ~ ]# rpm-ostree status
State: idle
Deployments:
● ostree://photon:photon/4.0/x86_64/minimal
    Version: 4.0_minimal (2020-11-04T02:21:47Z)
Commit: 820b584a6f90bf6b9b8cb6aad8c093064b88d0ab686be8130baa03d68917ad88

  ostree://photon:photon/4.0/x86_64/minimal
    Version: 4.0_minimal (2021-02-20T07:15:43Z)
Commit: 965c1abeb048e1a8ff77e9cd34ffccc5e3356176cda3332b4ff0e7a6c66b661f


root@photon-7c2d910d79e9 [ ~ ]# ostree admin config-diff --print-current-dir
/ostree/deploy/photon/deploy/820b584a6f90bf6b9b8cb6aad8c093064b88d0ab686be8130baa03d68917ad88.0


root@photon-host-cus1 [ ~ ]# rpm-ostree db diff  8b4b e663
ostree diff commit old: rollback deployment (8b4b9d4ec033d1eb816711bfdda595d1013fecbe5cd340f6a619cdc9d83a3bf2)
ostree diff commit new: booted deployment (e663b2872efa01d80e4c34c823431472beb653373af32de83c7d2480316b8a6a)

root@photon-host-cus1 [ ~ ]# rpm-ostree db diff  82bc 092e
error: Refspec '82bc' not found
Interesting fact: The metadata for commit 82bc has been removed from the local repo.
```

## Tracking parent commits

OSTree will display limited commit history - maximum 2 levels, so if you want to traverse the history even though it may not find a commitment by its ID, you can refer to its parent using '^' suffix, grandfather via '^^' and so on. We know that 82bc is the parent of 092e:

```console    
root@photon-host-def [ ~ ]# rpm-ostree db diff  092e^ 092e
  error: No such metadata object 82bca728eadb7292d568404484ad6889c3f6303600ca8c743a4336e0a10b3817.commit
  error: Refspec '82cb' not found
  root@photon-host-def [ ~ ]# rpm-ostree db diff  092e^^ 092e
  error: No such metadata object 82bca728eadb7292d568404484ad6889c3f6303600ca8c743a4336e0a10b3817.commit
```

So commit 092e knows who its parent is, but its metadata is no longer in the local repo, so it cannot traverse further to its parent to find an existing grandfather.

## Resetting a branch to a previous commit

We can reset the head of a branch in a local repo to a previous commit, for example corresponding to version 0 (3.0_minimal).

```console
root@photon-7c2d910d79e9 [ ~ ]# ostree reset photon:photon/4.0/x86_64/minimal 965c
```

Now if we look again at the branch commit history, the head is at version 0.

```console
root@photon-7c2d910d79e9 [ ~ ]# ostree log photon/4.0/x86_64/minimal
commit 965c1abeb048e1a8ff77e9cd34ffccc5e3356176cda3332b4ff0e7a6c66b661f
ContentChecksum:  9bc85673bd8d5599d61a02a99accce9bc9b72612c7a3cebd35427875f6514288
Date:  2021-02-20 07:15:43 +0000
Version: 4.0_minimal
(no subject)
```
    
