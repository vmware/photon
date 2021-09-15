Name:           toybox
Version:        0.7.3
Release:        7%{?dist}
License:        BSD
Summary:        Common Linux command line utilities in a single executable
Url:            http://landley.net/toybox
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        http://landley.net/toybox/downloads/%{name}-%{version}.tar.gz
%define sha1 %{name}=f3d9f5396a210fb2ad7d6309acb237751c50812f
Source1:        config-%{version}
Source2:        toybox-toys

Patch0:         config2help_use_after_free_fix.patch

%description
Toybox combines common Linux command line utilities together into a single
BSD-licensed executable that's simple, small, fast, reasonably
standards-compliant, and powerful enough to turn Android into a development
environment.

%prep
%autosetup -p1 -n toybox-%{version}

%build
# Move sed to /bin
sed -i 's#TOYFLAG_USR|TOYFLAG_BIN#TOYFLAG_BIN#' toys/posix/sed.c
cp %{SOURCE1} .config
NOSTRIP=1 make %{?_smp_mflags} CFLAGS="-Wall -Wundef -Wno-char-subscripts -Werror=implicit-function-declaration -g"

%install
PREFIX=%{buildroot} make install %{?_smp_mflags}
chmod 755 %{buildroot}/bin/toybox
install -m 0755 %{SOURCE2} %{buildroot}/bin/toybox-toys

%check
# Do not run all tests, skip losetup
# make tests
sed -i "s/^  if \[ \$# -ne 0 \]/  if false; /" scripts/test.sh
pushd tests
tests_to_run=$(ls *.test | sed 's/.test//;/losetup/d')
popd
tests_to_run=$(echo  $tests_to_run | sed -e 's/pkill//g')
./scripts/test.sh $tests_to_run

%define mktoy() /bin/toybox ln -sf /bin/toybox %1

%posttrans
/bin/toybox-toys --install

%preun
/bin/toybox-toys --uninstall

%triggerpostun -- bzip2
[ $2 -eq 0 ] || exit 0
%mktoy %{_bindir}/bunzip2
%mktoy %{_bindir}/bzcat

%triggerpostun -- coreutils
[ $2 -eq 0 ] || exit 0
%mktoy /bin/cat
%mktoy /bin/chgrp
%mktoy /bin/chmod
%mktoy /bin/chown
%mktoy /bin/cksum
%mktoy /bin/cp
%mktoy /bin/date
%mktoy /bin/echo
%mktoy /bin/false
%mktoy /bin/ln
%mktoy /bin/ls
%mktoy /bin/mkdir
%mktoy /bin/mknod
%mktoy /bin/mktemp
%mktoy /bin/mv
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
%mktoy /bin/nl
%mktoy /bin/paste
%mktoy /bin/timeout
%mktoy /bin/truncate
%mktoy /sbin/df
%mktoy %{_bindir}/nice
%mktoy %{_bindir}/printenv
%mktoy %{_bindir}/base64
%mktoy %{_bindir}/basename
%mktoy %{_bindir}/comm
%mktoy %{_bindir}/cut
%mktoy %{_bindir}/dirname
%mktoy %{_bindir}/du
%mktoy %{_bindir}/env
%mktoy %{_bindir}/expand
%mktoy %{_bindir}/factor
%mktoy %{_bindir}/groups
%mktoy %{_bindir}/head
%mktoy %{_bindir}/id
%mktoy %{_bindir}/install
%mktoy %{_bindir}/link
%mktoy %{_bindir}/logname
%mktoy %{_bindir}/md5sum
%mktoy %{_bindir}/mkfifo
%mktoy %{_bindir}/nohup
%mktoy %{_bindir}/nproc
%mktoy %{_bindir}/od
%mktoy %{_bindir}/printf
%mktoy %{_bindir}/readlink
%mktoy %{_bindir}/realpath
%mktoy %{_bindir}/seq
%mktoy %{_bindir}/sha1sum
%mktoy %{_bindir}/sha224sum
%mktoy %{_bindir}/sha256sum
%mktoy %{_bindir}/sha384sum
%mktoy %{_bindir}/sha512sum
%mktoy %{_bindir}/shred
%mktoy %{_bindir}/sort
%mktoy %{_bindir}/split
%mktoy %{_bindir}/tac
%mktoy %{_bindir}/tail
%mktoy %{_bindir}/tee
%mktoy %{_bindir}/test
%mktoy %{_bindir}/tty
%mktoy %{_bindir}/uniq
%mktoy %{_bindir}/unlink
%mktoy %{_bindir}/wc
%mktoy %{_bindir}/who
%mktoy %{_bindir}/whoami
%mktoy %{_bindir}/yes
%mktoy %{_sbindir}/chroot

%triggerpostun -- cpio
[ $2 -eq 0 ] || exit 0
%mktoy /bin/cpio

%triggerpostun -- diffutils
[ $2 -eq 0 ] || exit 0
%mktoy %{_bindir}/cmp

%triggerpostun -- elixir
[ $2 -eq 0 ] || exit 0
%mktoy %{_bindir}/mix

%triggerpostun -- expect
[ $2 -eq 0 ] || exit 0
%mktoy %{_bindir}/mkpasswd

%triggerpostun -- e2fsprogs
[ $2 -eq 0 ] || exit 0
%mktoy /bin/chattr
%mktoy /bin/lsattr

%triggerpostun -- file
[ $2 -eq 0 ] || exit 0
%mktoy %{_bindir}/file

%triggerpostun -- findutils
[ $2 -eq 0 ] || exit 0
%mktoy %{_bindir}/find
%mktoy %{_bindir}/xargs

%triggerpostun -- grep
[ $2 -eq 0 ] || exit 0
%mktoy /bin/egrep
%mktoy /bin/fgrep
%mktoy /bin/grep

%triggerpostun -- gzip
[ $2 -eq 0 ] || exit 0
%mktoy %{_bindir}/gunzip
%mktoy %{_bindir}/gzip
%mktoy %{_bindir}/zcat

%triggerpostun -- iotop
[ $2 -eq 0 ] || exit 0
%mktoy %{_bindir}/iotop

%triggerpostun -- iputils
[ $2 -eq 0 ] || exit 0
%mktoy %{_bindir}/ping
%mktoy %{_bindir}/ping6

%triggerpostun -- kbd
[ $2 -eq 0 ] || exit 0
%mktoy %{_bindir}/chvt

%triggerpostun -- kmod
[ $2 -eq 0 ] || exit 0
%mktoy /sbin/insmod
%mktoy /sbin/lsmod
%mktoy /sbin/modinfo
%mktoy /sbin/rmmod

%triggerpostun -- netcat
[ $2 -eq 0 ] || exit 0
%mktoy /bin/netcat
%mktoy %{_bindir}/nc

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
%mktoy %{_bindir}/patch

%triggerpostun -- pciutils
[ $2 -eq 0 ] || exit 0
%mktoy %{_bindir}/lspci

%triggerpostun -- procps-ng
[ $2 -eq 0 ] || exit 0
%mktoy /bin/pidof
%mktoy /bin/vmstat
%mktoy /bin/pmap
%mktoy /sbin/sysctl
%mktoy %{_bindir}/ps
%mktoy %{_bindir}/free
%mktoy %{_bindir}/pgrep
%mktoy %{_bindir}/pkill
%mktoy %{_bindir}/pwdx
%mktoy %{_bindir}/top
%mktoy %{_bindir}/uptime
%mktoy %{_bindir}/w

%triggerpostun -- psmisc
[ $2 -eq 0 ] || exit 0
%mktoy %{_bindir}/killall

%triggerpostun -- sed
[ $2 -eq 0 ] || exit 0
%mktoy /bin/sed

%triggerpostun -- shadow-tools
[ $2 -eq 0 ] || exit 0
%mktoy /bin/login
%mktoy /bin/su
%mktoy %{_bindir}/passwd

%triggerpostun -- tar
[ $2 -eq 0 ] || exit 0
%mktoy %{_bindir}/tar

%triggerpostun -- usbutils
[ $2 -eq 0 ] || exit 0
%mktoy %{_bindir}/lsusb

%triggerpostun -- util-linux
[ $2 -eq 0 ] || exit 0
%mktoy /bin/dmesg
%mktoy /bin/kill
%mktoy /bin/mount
%mktoy /bin/mountpoint
%mktoy /bin/umount
%mktoy /bin/taskset
%mktoy /sbin/blkid
%mktoy /sbin/losetup
%mktoy /sbin/mkswap
%mktoy /sbin/pivot_root
%mktoy /sbin/swapoff
%mktoy /sbin/swapon
%mktoy /sbin/switch_root
%mktoy %{_bindir}/blockdev
%mktoy %{_bindir}/hwclock
%mktoy %{_bindir}/cal
%mktoy %{_bindir}/eject
%mktoy %{_bindir}/fallocate
%mktoy %{_bindir}/flock
%mktoy %{_bindir}/ionice
%mktoy %{_bindir}/renice
%mktoy %{_bindir}/rev
%mktoy %{_bindir}/setsid
%mktoy %{_sbindir}/fsfreeze
%mktoy %{_sbindir}/rfkill

%triggerpostun -- vim-extra
[ $2 -eq 0 ] || exit 0
%mktoy %{_bindir}/xxd

%triggerpostun -- which
[ $2 -eq 0 ] || exit 0
%mktoy %{_bindir}/which

%files
%defattr(-,root,root)
%doc README LICENSE
/bin/toybox
/bin/toybox-toys

# bzip2
%ghost %{_bindir}/bunzip2
%ghost %{_bindir}/bzcat

# coreutils
%ghost /bin/cat
%ghost /bin/chgrp
%ghost /bin/chmod
%ghost /bin/chown
%ghost /bin/cksum
%ghost /bin/cp
%ghost /bin/date
%ghost /bin/echo
%ghost /bin/false
%ghost /bin/ln
%ghost /bin/ls
%ghost /bin/mkdir
%ghost /bin/mknod
%ghost /bin/mktemp
%ghost /bin/mv
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
%ghost /bin/nl
%ghost /bin/paste
%ghost /bin/timeout
%ghost /bin/truncate
%ghost /sbin/df
%ghost %{_bindir}/nice
%ghost %{_bindir}/printenv
%ghost %{_bindir}/base64
%ghost %{_bindir}/basename
%ghost %{_bindir}/comm
%ghost %{_bindir}/cut
%ghost %{_bindir}/dirname
%ghost %{_bindir}/du
%ghost %{_bindir}/env
%ghost %{_bindir}/expand
%ghost %{_bindir}/factor
%ghost %{_bindir}/groups
%ghost %{_bindir}/head
%ghost %{_bindir}/id
%ghost %{_bindir}/install
%ghost %{_bindir}/link
%ghost %{_bindir}/logname
%ghost %{_bindir}/md5sum
%ghost %{_bindir}/mkfifo
%ghost %{_bindir}/nohup
%ghost %{_bindir}/nproc
%ghost %{_bindir}/od
%ghost %{_bindir}/printf
%ghost %{_bindir}/readlink
%ghost %{_bindir}/realpath
%ghost %{_bindir}/seq
%ghost %{_bindir}/sha1sum
%ghost %{_bindir}/sha224sum
%ghost %{_bindir}/sha256sum
%ghost %{_bindir}/sha384sum
%ghost %{_bindir}/sha512sum
%ghost %{_bindir}/shred
%ghost %{_bindir}/sort
%ghost %{_bindir}/split
%ghost %{_bindir}/tac
%ghost %{_bindir}/tail
%ghost %{_bindir}/tee
%ghost %{_bindir}/test
%ghost %{_bindir}/tty
%ghost %{_bindir}/uniq
%ghost %{_bindir}/unlink
%ghost %{_bindir}/wc
%ghost %{_bindir}/who
%ghost %{_bindir}/whoami
%ghost %{_bindir}/yes
%ghost %{_sbindir}/chroot

# cpio
%ghost /bin/cpio

# diffutils
%ghost %{_bindir}/cmp

# elixir
%ghost %{_bindir}/mix

# expect
%ghost %{_bindir}/mkpasswd

# e2fsprogs
%ghost /bin/chattr
%ghost /bin/lsattr

# file
%ghost %{_bindir}/file

# findutils
%ghost %{_bindir}/find
%ghost %{_bindir}/xargs

# grep
%ghost /bin/egrep
%ghost /bin/fgrep
%ghost /bin/grep

# gzip
%ghost %{_bindir}/gunzip
%ghost %{_bindir}/gzip
%ghost %{_bindir}/zcat

# iotop
%ghost %{_bindir}/iotop

# iputils
%ghost %{_bindir}/ping
%ghost %{_bindir}/ping6

# kbd
%ghost %{_bindir}/chvt

# kmod
%ghost /sbin/insmod
%ghost /sbin/lsmod
%ghost /sbin/modinfo
%ghost /sbin/rmmod

# netcat
%ghost /bin/netcat
%ghost %{_bindir}/nc

# net-tools
%ghost /bin/hostname
%ghost /bin/netstat
%ghost /sbin/ifconfig

# parted
%ghost /sbin/partprobe

# patch
%ghost %{_bindir}/patch

# pciutils
%ghost %{_bindir}/lspci

# procps-ng
%ghost /bin/pidof
%ghost /bin/vmstat
%ghost /bin/pmap
%ghost /sbin/sysctl
%ghost %{_bindir}/ps
%ghost %{_bindir}/free
%ghost %{_bindir}/pgrep
%ghost %{_bindir}/pkill
%ghost %{_bindir}/pwdx
%ghost %{_bindir}/top
%ghost %{_bindir}/uptime
%ghost %{_bindir}/w

# psmisc
%ghost %{_bindir}/killall

# sed
%ghost /bin/sed

# shadow-tools
%ghost /bin/login
%ghost /bin/su
%ghost %{_bindir}/passwd

# tar
%ghost %{_bindir}/tar

# usbutils
%ghost %{_bindir}/lsusb

# util-linux
%ghost /bin/dmesg
%ghost /bin/kill
%ghost /bin/mount
%ghost /bin/mountpoint
%ghost /bin/umount
%ghost /bin/blkid
%ghost /bin/taskset
%ghost /sbin/losetup
%ghost /sbin/mkswap
%ghost /sbin/pivot_root
%ghost /sbin/swapoff
%ghost /sbin/swapon
%ghost /sbin/switch_root
%ghost %{_bindir}/blockdev
%ghost %{_bindir}/hwclock
%ghost %{_bindir}/cal
%ghost %{_bindir}/eject
%ghost %{_bindir}/fallocate
%ghost %{_bindir}/flock
%ghost %{_bindir}/ionice
%ghost %{_bindir}/renice
%ghost %{_bindir}/rev
%ghost %{_bindir}/setsid
%ghost %{_sbindir}/fsfreeze
%ghost %{_sbindir}/rfkill

# vim-extra
%ghost %{_bindir}/xxd

# which
%ghost %{_bindir}/which

# Non conflicting toybox toys
/bin/dos2unix
/bin/fstype
/bin/fsync
/bin/help
/bin/readahead
/bin/unix2dos
/bin/microcom
/sbin/freeramdisk
/sbin/killall5
/sbin/oneit
/sbin/vconfig
%{_bindir}/acpi
%{_bindir}/catv
%{_bindir}/count
%{_bindir}/ftpget
%{_bindir}/ftpput
%{_bindir}/hexedit
%{_bindir}/inotifyd
%{_bindir}/iorenice
%{_bindir}/makedevs
%{_bindir}/nbd-client
%{_bindir}/time
%{_bindir}/tunctl
%{_bindir}/uudecode
%{_bindir}/uuencode

%changelog
* Mon Sep 13 2021 Shreenidhi Shedi <sshedi@vmware.com> 0.7.3-7
- Avoid conflicts with other packages by ghosting symlinks
* Sun Oct 01 2017 Alexey Makhalov <amakhalov@vmware.com> 0.7.3-6
- remove strings and usleep to avoid conflict with binutils and initscripts
* Mon Sep 25 2017 Alexey Makhalov <amakhalov@vmware.com> 0.7.3-5
- Move sed to /bin
- Remove kmod and systemd toys due to incomplete
* Thu Aug 24 2017 Alexey Makhalov <amakhalov@vmware.com> 0.7.3-4
- Fix compilation issue for glibc-2.26
* Thu Jun 01 2017 Chang Lee <changlee@vmware.com> 0.7.3-3
- Remove pkill test in %check
* Thu Apr 27 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 0.7.3-2
- Ensure debuginfo
* Thu Apr 20 2017 Fabio Rapposelli <fabio@vmware.com> 0.7.3-1
- Initial build.  First version
