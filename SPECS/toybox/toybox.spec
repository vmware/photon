Name:           toybox
Version:        0.8.2
Release:        5%{?dist}
License:        BSD
Summary:        Common Linux command line utilities in a single executable
Url:            http://landley.net/toybox/
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        http://landley.net/toybox/downloads/%{name}-%{version}.tar.gz
%define sha1 toybox=0477740759f5132397fdfdbf8aea88e811869173
Patch0:         toybox.patch
Source1:        config-toybox
Source2:        toybox-toys
BuildRequires:  openssl-devel zlib-devel
Requires:       openssl zlib
%description
Toybox combines common Linux command line utilities together into a single
BSD-licensed executable that's simple, small, fast, reasonably
standards-compliant, and powerful enough to turn Android into a development
environment.

%prep
%setup -q -n toybox-%{version}
%patch0 -p1
%build
# Move sed to /bin
sed -i 's#TOYFLAG_USR|TOYFLAG_BIN#TOYFLAG_BIN#' toys/posix/sed.c
cp %{SOURCE1} .config
NOSTRIP=1 make CFLAGS="-Wall -Wundef -Wno-char-subscripts -Werror=implicit-function-declaration -g"

%install
install -d %{buildroot}/bin
PREFIX=%{buildroot} make install
chmod 755 %{buildroot}/bin/toybox
install -m 0755 %{SOURCE2} %{buildroot}/bin/toybox-toys

%check
# Do not run all tests, skip losetup
# make tests
sed -i "s/^  if \[ \$# -ne 0 \]/  if false; /" scripts/test.sh
pushd tests
tests_to_run=`ls *.test | sed 's/.test//;/losetup/d'`
popd
tests_to_run=`echo  $tests_to_run | sed -e 's/pkill//g'`
./scripts/test.sh $tests_to_run

%define mktoy() /bin/toybox ln -sf /bin/toybox %1

%posttrans
/bin/toybox-toys --install

%preun
/bin/toybox-toys --uninstall

%triggerpostun -- bzip2
[ $2 -eq 0 ] || exit 0
%mktoy /usr/bin/bunzip2
%mktoy /usr/bin/bzcat

%triggerpostun -- coreutils
[ $2 -eq 0 ] || exit 0
%mktoy /bin/cat
%mktoy /bin/chgrp
%mktoy /bin/chmod
%mktoy /bin/chown
%mktoy /bin/cksum
%mktoy /bin/cp
%mktoy /bin/date
%mktoy /bin/df
%mktoy /bin/echo
%mktoy /bin/false
%mktoy /bin/ln
%mktoy /bin/ls
%mktoy /bin/mkdir
%mktoy /bin/mknod
%mktoy /bin/mktemp
%mktoy /bin/mv
%mktoy /bin/nice
%mktoy /bin/printenv
%mktoy /bin/pwd
%mktoy /bin/rm
%mktoy /bin/rmdir
%mktoy /bin/sleep
%mktoy /bin/stat
%mktoy /bin/stty
%mktoy /bin/sync
%mktoy /bin/touch
%mktoy /bin/true
%mktoy /bin/uname
%mktoy /usr/bin/base64
%mktoy /usr/bin/basename
%mktoy /usr/bin/comm
%mktoy /usr/bin/cut
%mktoy /usr/bin/dirname
%mktoy /usr/bin/du
%mktoy /usr/bin/env
%mktoy /usr/bin/expand
%mktoy /usr/bin/factor
%mktoy /usr/bin/groups
%mktoy /usr/bin/head
%mktoy /usr/bin/id
%mktoy /usr/bin/install
%mktoy /usr/bin/link
%mktoy /usr/bin/logname
%mktoy /usr/bin/md5sum
%mktoy /usr/bin/mkfifo
%mktoy /usr/bin/nl
%mktoy /usr/bin/nohup
%mktoy /usr/bin/nproc
%mktoy /usr/bin/od
%mktoy /usr/bin/paste
%mktoy /usr/bin/printf
%mktoy /usr/bin/readlink
%mktoy /usr/bin/realpath
%mktoy /usr/bin/seq
%mktoy /usr/bin/sha1sum
%mktoy /usr/bin/sha224sum
%mktoy /usr/bin/sha256sum
%mktoy /usr/bin/sha384sum
%mktoy /usr/bin/sha512sum
%mktoy /usr/bin/shred
%mktoy /usr/bin/sort
%mktoy /usr/bin/split
%mktoy /usr/bin/tac
%mktoy /usr/bin/tail
%mktoy /usr/bin/tee
%mktoy /usr/bin/test
%mktoy /usr/bin/timeout
%mktoy /usr/bin/truncate
%mktoy /usr/bin/tty
%mktoy /usr/bin/uniq
%mktoy /usr/bin/unlink
%mktoy /usr/bin/wc
%mktoy /usr/bin/who
%mktoy /usr/bin/whoami
%mktoy /usr/bin/yes
%mktoy /usr/sbin/chroot

%triggerpostun -- cpio
[ $2 -eq 0 ] || exit 0
%mktoy /bin/cpio

%triggerpostun -- diffutils
[ $2 -eq 0 ] || exit 0
%mktoy /usr/bin/cmp

%triggerpostun -- elixir
[ $2 -eq 0 ] || exit 0
%mktoy /usr/bin/mix

%triggerpostun -- expect
[ $2 -eq 0 ] || exit 0
%mktoy /usr/bin/mkpasswd

%triggerpostun -- e2fsprogs
[ $2 -eq 0 ] || exit 0
%mktoy /bin/chattr
%mktoy /bin/lsattr

%triggerpostun -- file
[ $2 -eq 0 ] || exit 0
%mktoy /usr/bin/file

%triggerpostun -- findutils
[ $2 -eq 0 ] || exit 0
%mktoy /usr/bin/find
%mktoy /usr/bin/xargs

%triggerpostun -- grep
[ $2 -eq 0 ] || exit 0
%mktoy /bin/egrep
%mktoy /bin/fgrep
%mktoy /bin/grep

%triggerpostun -- gzip
[ $2 -eq 0 ] || exit 0
%mktoy /usr/bin/gunzip
%mktoy /usr/bin/gzip
%mktoy /usr/bin/zcat

%triggerpostun -- iotop
[ $2 -eq 0 ] || exit 0
%mktoy /usr/sbin/iotop

%triggerpostun -- iputils
[ $2 -eq 0 ] || exit 0
%mktoy /usr/bin/ping
%mktoy /usr/bin/ping6

%triggerpostun -- kbd
[ $2 -eq 0 ] || exit 0
%mktoy /usr/bin/chvt

%triggerpostun -- kmod
[ $2 -eq 0 ] || exit 0
%mktoy /sbin/insmod
%mktoy /sbin/lsmod
%mktoy /sbin/modinfo
%mktoy /sbin/rmmod

%triggerpostun -- netcat
[ $2 -eq 0 ] || exit 0
%mktoy /bin/netcat
%mktoy /usr/bin/nc

%triggerpostun -- net-tools
[ $2 -eq 0 ] || exit 0
%mktoy /bin/hostname
%mktoy /bin/netstat
%mktoy /sbin/ifconfig

%triggerpostun -- parted
[ $2 -eq 0 ] || exit 0
%mktoy /sbin/partprobe

%triggerpostun -- patch
[ $2 -eq 0 ] || exit 0
%mktoy /usr/bin/patch

%triggerpostun -- pciutils
[ $2 -eq 0 ] || exit 0
%mktoy /usr/sbin/lspci

%triggerpostun -- procps-ng
[ $2 -eq 0 ] || exit 0
%mktoy /bin/pidof
%mktoy /bin/ps
%mktoy /bin/vmstat
%mktoy /sbin/sysctl
%mktoy /usr/bin/free
%mktoy /usr/bin/pgrep
%mktoy /usr/bin/pkill
%mktoy /usr/bin/pmap
%mktoy /usr/bin/pwdx
%mktoy /usr/bin/top
%mktoy /usr/bin/uptime
%mktoy /usr/bin/w

%triggerpostun -- psmisc
[ $2 -eq 0 ] || exit 0
%mktoy /usr/bin/killall

%triggerpostun -- sed
[ $2 -eq 0 ] || exit 0
%mktoy /bin/sed

%triggerpostun -- shadow-tools
[ $2 -eq 0 ] || exit 0
%mktoy /bin/login
%mktoy /bin/su
%mktoy /usr/bin/passwd

%triggerpostun -- tar
[ $2 -eq 0 ] || exit 0
%mktoy /usr/bin/tar

%triggerpostun -- usbutils
[ $2 -eq 0 ] || exit 0
%mktoy /usr/bin/lsusb

%triggerpostun -- util-linux
[ $2 -eq 0 ] || exit 0
%mktoy /bin/dmesg
%mktoy /bin/kill
%mktoy /bin/mount
%mktoy /bin/mountpoint
%mktoy /bin/umount
%mktoy /sbin/blkid
%mktoy /sbin/blockdev
%mktoy /sbin/hwclock
%mktoy /sbin/losetup
%mktoy /sbin/mkswap
%mktoy /sbin/pivot_root
%mktoy /sbin/swapoff
%mktoy /sbin/swapon
%mktoy /sbin/switch_root
%mktoy /usr/bin/cal
%mktoy /usr/bin/eject
%mktoy /usr/bin/fallocate
%mktoy /usr/bin/flock
%mktoy /usr/bin/ionice
%mktoy /usr/bin/renice
%mktoy /usr/bin/rev
%mktoy /usr/bin/setsid
%mktoy /usr/bin/taskset
%mktoy /usr/sbin/fsfreeze
%mktoy /usr/sbin/rfkill

%triggerpostun -- vim-extra
[ $2 -eq 0 ] || exit 0
%mktoy /usr/bin/xxd

%triggerpostun -- which
[ $2 -eq 0 ] || exit 0
%mktoy /usr/bin/which

%files
%defattr(-,root,root)
%doc README LICENSE
/bin/toybox
/bin/toybox-toys

# bzip2
%ghost /usr/bin/bunzip2
%ghost /usr/bin/bzcat

# coreutils
%ghost /bin/cat
%ghost /bin/chgrp
%ghost /bin/chmod
%ghost /bin/chown
%ghost /bin/cksum
%ghost /bin/cp
%ghost /bin/date
%ghost /bin/df
%ghost /bin/echo
%ghost /bin/false
%ghost /bin/ln
%ghost /bin/ls
%ghost /bin/mkdir
%ghost /bin/mknod
%ghost /bin/mktemp
%ghost /bin/mv
%ghost /bin/nice
%ghost /bin/printenv
%ghost /bin/pwd
%ghost /bin/rm
%ghost /bin/rmdir
%ghost /bin/sleep
%ghost /bin/stat
%ghost /bin/stty
%ghost /bin/sync
%ghost /bin/touch
%ghost /bin/true
%ghost /bin/uname
%ghost /usr/bin/base64
%ghost /usr/bin/basename
%ghost /usr/bin/comm
%ghost /usr/bin/cut
%ghost /usr/bin/dirname
%ghost /usr/bin/du
%ghost /usr/bin/env
%ghost /usr/bin/expand
%ghost /usr/bin/factor
%ghost /usr/bin/groups
%ghost /usr/bin/head
%ghost /usr/bin/id
%ghost /usr/bin/install
%ghost /usr/bin/link
%ghost /usr/bin/logname
%ghost /usr/bin/md5sum
%ghost /usr/bin/mkfifo
%ghost /usr/bin/nl
%ghost /usr/bin/nohup
%ghost /usr/bin/nproc
%ghost /usr/bin/od
%ghost /usr/bin/paste
%ghost /usr/bin/printf
%ghost /usr/bin/readlink
%ghost /usr/bin/realpath
%ghost /usr/bin/seq
%ghost /usr/bin/sha1sum
%ghost /usr/bin/sha224sum
%ghost /usr/bin/sha256sum
%ghost /usr/bin/sha384sum
%ghost /usr/bin/sha512sum
%ghost /usr/bin/shred
%ghost /usr/bin/sort
%ghost /usr/bin/split
%ghost /usr/bin/tac
%ghost /usr/bin/tail
%ghost /usr/bin/tee
%ghost /usr/bin/test
%ghost /usr/bin/timeout
%ghost /usr/bin/truncate
%ghost /usr/bin/tty
%ghost /usr/bin/uniq
%ghost /usr/bin/unlink
%ghost /usr/bin/wc
%ghost /usr/bin/who
%ghost /usr/bin/whoami
%ghost /usr/bin/yes
%ghost /usr/sbin/chroot

# cpio
%ghost /bin/cpio

# diffutils
%ghost /usr/bin/cmp

# elixir
%ghost /usr/bin/mix

# expect
%ghost /usr/bin/mkpasswd

# e2fsprogs
%ghost /bin/chattr
%ghost /bin/lsattr

# file
%ghost /usr/bin/file

# findutils
%ghost /usr/bin/find
%ghost /usr/bin/xargs

# grep
%ghost /bin/egrep
%ghost /bin/fgrep
%ghost /bin/grep

# gzip
%ghost /usr/bin/gunzip
%ghost /usr/bin/gzip
%ghost /usr/bin/zcat

# iotop
%ghost /usr/sbin/iotop

# iputils
%ghost /usr/bin/ping
%ghost /usr/bin/ping6

# kbd
%ghost /usr/bin/chvt

# kmod
%ghost /sbin/insmod
%ghost /sbin/lsmod
%ghost /sbin/modinfo
%ghost /sbin/rmmod

# netcat
%ghost /bin/netcat
%ghost /usr/bin/nc

# net-tools
%ghost /bin/hostname
%ghost /bin/netstat
%ghost /sbin/ifconfig

# parted
%ghost /sbin/partprobe

# patch
%ghost /usr/bin/patch

# pciutils
%ghost /usr/sbin/lspci

# procps-ng
%ghost /bin/pidof
%ghost /bin/ps
%ghost /bin/vmstat
%ghost /sbin/sysctl
%ghost /usr/bin/free
%ghost /usr/bin/pgrep
%ghost /usr/bin/pkill
%ghost /usr/bin/pmap
%ghost /usr/bin/pwdx
%ghost /usr/bin/top
%ghost /usr/bin/uptime
%ghost /usr/bin/w

# psmisc
%ghost /usr/bin/killall

# sed
%ghost /bin/sed

# shadow-tools
%ghost /bin/login
%ghost /bin/su
%ghost /usr/bin/passwd

# tar
%ghost /usr/bin/tar

# usbutils
%ghost /usr/bin/lsusb

# util-linux
%ghost /bin/dmesg
%ghost /bin/kill
%ghost /bin/mount
%ghost /bin/mountpoint
%ghost /bin/umount
%ghost /sbin/blkid
%ghost /sbin/blockdev
%ghost /sbin/hwclock
%ghost /sbin/losetup
%ghost /sbin/mkswap
%ghost /sbin/pivot_root
%ghost /sbin/swapoff
%ghost /sbin/swapon
%ghost /sbin/switch_root
%ghost /usr/bin/cal
%ghost /usr/bin/eject
%ghost /usr/bin/fallocate
%ghost /usr/bin/flock
%ghost /usr/bin/ionice
%ghost /usr/bin/renice
%ghost /usr/bin/rev
%ghost /usr/bin/setsid
%ghost /usr/bin/taskset
%ghost /usr/sbin/fsfreeze
%ghost /usr/sbin/rfkill

# vim-extra
%ghost /usr/bin/xxd

# which
%ghost /usr/bin/which

# Non conflicting toybox toys
/bin/dos2unix
/bin/fstype
/bin/fsync
/bin/help
/bin/readahead
/bin/unix2dos
/sbin/freeramdisk
/sbin/killall5
/sbin/oneit
/sbin/vconfig
/usr/bin/acpi
/usr/bin/catv
/usr/bin/count
/usr/bin/ftpget
/usr/bin/ftpput
/usr/bin/hexedit
/usr/bin/inotifyd
/usr/bin/iorenice
/usr/bin/makedevs
/usr/bin/microcom
/usr/bin/nbd-client
/usr/bin/time
/usr/bin/tunctl
/usr/bin/uudecode
/usr/bin/uuencode

%changelog
*   Tue Sep 29 2020 Satya Naga Vasamsetty <svasamsetty@vmware.com> 0.8.2-5
-   openssl 1.1.1
*   Fri Aug 21 2020 Prashant S Chauhan <psinghchauha@vmware.com> 0.8.2-4
-   Fixed path for the utilities df,iotop,lspci,blkid
*   Tue Jun 30 2020 Prashant S Chauhan <psinghchauhan@vmware.com> 0.8.2-3
-   Avoid conflicts with other packages by not packaging (%ghost-ing) symlinks
-   Added elixir
*   Wed Apr 15 2020 Alexey Makhalov <amakhalov@vmware.com> 0.8.2-2
-   Avoid conflicts with other packages by not packaging (%ghost-ing) symlinks
-   Use system zlib as it is installed by tdnf
-   Added gzip, iputils, kmod, tar toys
*   Wed Oct 30 2019 Alexey Makhalov <amakhalov@vmware.com> 0.8.2-1
-   Version update. Use system libcrypto.
*   Mon Oct 01 2018 Alexey Makhalov <amakhalov@vmware.com> 0.7.7-1
-   Version update
*   Mon Oct 02 2017 Alexey Makhalov <amakhalov@vmware.com> 0.7.3-6
-   remove strings and usleep to avoid conflict with binutils and initscripts
*   Mon Sep 25 2017 Alexey Makhalov <amakhalov@vmware.com> 0.7.3-5
-   Move sed to /bin
-   Remove kmod and systemd toys due to incomplete
*   Thu Aug 24 2017 Alexey Makhalov <amakhalov@vmware.com> 0.7.3-4
-   Fix compilation issue for glibc-2.26
*   Thu Jun 01 2017 Chang Lee <changlee@vmware.com> 0.7.3-3
-   Remove pkill test in %check
*   Thu Apr 27 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 0.7.3-2
-   Ensure debuginfo
*   Thu Apr 20 2017 Fabio Rapposelli <fabio@vmware.com> 0.7.3-1
-   Initial build.  First version
