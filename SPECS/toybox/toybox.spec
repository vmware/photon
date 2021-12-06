Name:           toybox
Version:        0.8.6
Release:        1%{?dist}
License:        BSD
Summary:        Common Linux command line utilities in a single executable
Url:            http://landley.net/toybox
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        http://landley.net/toybox/downloads/%{name}-%{version}.tar.gz
%define sha1 %{name}=7198960aa13ce5c79c7c057beb0823703cac69ec

Patch0:         toybox-change-toys-path.patch

Source1:        config-toybox
Source2:        toybox-toys

BuildRequires:  openssl-devel
BuildRequires:  zlib-devel

Requires:       openssl
Requires:       zlib

%description
Toybox combines common Linux command line utilities together into a single
BSD-licensed executable that's simple, small, fast, reasonably
standards-compliant, and powerful enough to turn Android into a development
environment.

%package docs
Summary:    toybox docs
Group:      Documentation
Requires:   %{name} = %{version}-%{release}

%description docs
The package contains toybox doc files.

%prep
%autosetup -p1 -n toybox-%{version}

%build
cp %{SOURCE1} .config
# If we make NOSTRIP=0, toybox debuginfo rpm will be useless
NOSTRIP=1 make CFLAGS="-Wall -Wundef -Wno-char-subscripts -Werror=implicit-function-declaration -g" %{?_smp_mflags}

%install
install -d %{buildroot}%{_bindir}
PREFIX=%{buildroot} make install %{?_smp_mflags}
mv %{buildroot}/bin/%{name} %{buildroot}%{_bindir}/toybox
chmod 755 %{buildroot}%{_bindir}/toybox
install -m 0755 %{SOURCE2} %{buildroot}%{_bindir}/toybox-toys

%check
# Do not run all tests, skip losetup
# make tests
sed -i "s/^  if \[ \$# -ne 0 \]/  if false; /" scripts/test.sh
pushd tests
tests_to_run=`ls *.test | sed 's/.test//;/losetup/d'`
popd
tests_to_run=`echo  $tests_to_run | sed -e 's/pkill//g'`
./scripts/test.sh $tests_to_run

%define mktoy() %{_bindir}/toybox ln -sf %{_bindir}/toybox %1

%posttrans
%{_bindir}/toybox-toys --install

%preun
%{_bindir}/toybox-toys --uninstall

%triggerpostun -- dos2unix
[ $2 -eq 0 ] || exit 0
%mktoy /usr/bin/dos2unix
%mktoy /usr/bin/unix2dos

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
%mktoy /usr/bin/[
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
%mktoy /usr/bin/ps
%mktoy /usr/bin/pidof
%mktoy /usr/bin/free
%mktoy /usr/bin/w
%mktoy /usr/bin/pgrep
%mktoy /usr/bin/uptime
%mktoy /usr/bin/vmstat
%mktoy /usr/bin/pmap
%mktoy /usr/bin/pwdx
%mktoy /usr/bin/top
%mktoy /usr/bin/pkill
%mktoy /usr/sbin/sysctl

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
%{_bindir}/toybox
%{_bindir}/toybox-toys

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
%ghost %{_bindir}/[
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
%ghost %{_bindir}/nl
%ghost %{_bindir}/nohup
%ghost %{_bindir}/nproc
%ghost %{_bindir}/od
%ghost %{_bindir}/paste
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
%ghost %{_bindir}/timeout
%ghost %{_bindir}/truncate
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
%ghost %{_sbindir}/iotop

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
%ghost %{_sbindir}/lspci

# procps-ng
%ghost %{_bindir}/ps
%ghost %{_bindir}/pidof
%ghost %{_bindir}/free
%ghost %{_bindir}/w
%ghost %{_bindir}/pgrep
%ghost %{_bindir}/uptime
%ghost %{_bindir}/vmstat
%ghost %{_bindir}/pmap
%ghost %{_bindir}/pwdx
%ghost %{_bindir}/top
%ghost %{_bindir}/pkill
%ghost %{_sbindir}/sysctl

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
%ghost /sbin/blkid
%ghost /sbin/blockdev
%ghost /sbin/hwclock
%ghost /sbin/losetup
%ghost /sbin/mkswap
%ghost /sbin/pivot_root
%ghost /sbin/swapoff
%ghost /sbin/swapon
%ghost /sbin/switch_root
%ghost %{_bindir}/cal
%ghost %{_bindir}/eject
%ghost %{_bindir}/fallocate
%ghost %{_bindir}/flock
%ghost %{_bindir}/ionice
%ghost %{_bindir}/renice
%ghost %{_bindir}/rev
%ghost %{_bindir}/setsid
%ghost %{_bindir}/taskset
%ghost %{_sbindir}/fsfreeze
%ghost %{_sbindir}/rfkill

# vim-extra
%ghost %{_bindir}/xxd

# which
%ghost %{_bindir}/which

# dos2unix
%ghost %{_bindir}/dos2unix
%ghost %{_bindir}/unix2dos

# Non conflicting toybox toys
%{_bindir}/fstype
%{_bindir}/fsync
%{_bindir}/help
%{_bindir}/readahead
%{_sbindir}/freeramdisk
%{_sbindir}/killall5
%{_sbindir}/oneit
%{_sbindir}/vconfig
%{_bindir}/acpi
%{_bindir}/catv
%{_bindir}/count
%{_bindir}/ftpget
%{_bindir}/ftpput
%{_bindir}/hexedit
%{_bindir}/inotifyd
%{_bindir}/iorenice
%{_bindir}/makedevs
%{_bindir}/microcom
%{_bindir}/nbd-client
%{_bindir}/time
%{_bindir}/tunctl
%{_bindir}/uudecode
%{_bindir}/uuencode

%files docs
%defattr(-,root,root)
%doc README LICENSE

%changelog
* Tue Dec 07 2021 Shreenidhi Shedi <sshedi@vmware.com> 0.8.6-1
- Upgrade to 0.8.6
* Wed Aug 04 2021 Satya Naga Vasamsetty <svasamsetty@vmware.com> 0.8.3-3
- Bump up release for openssl
* Fri Feb 19 2021 Satya Naga Vasamsetty <svasamsetty@vmware.com> 0.8.3-2
- Move documents to docs sub-package
* Wed Oct 14 2020 Prashant S Chauhan <psinghchauha@vmware.com> 0.8.3-1
- Version update to 0.8.3
* Tue Sep 29 2020 Satya Naga Vasamsetty <svasamsetty@vmware.com> 0.8.2-5
- openssl 1.1.1
* Fri Aug 21 2020 Prashant S Chauhan <psinghchauha@vmware.com> 0.8.2-4
- Fixed path for the utilities df,iotop,lspci,blkid
* Tue Jun 30 2020 Prashant S Chauhan <psinghchauhan@vmware.com> 0.8.2-3
- Avoid conflicts with other packages by not packaging (%ghost-ing) symlinks
- Added elixir
* Wed Apr 15 2020 Alexey Makhalov <amakhalov@vmware.com> 0.8.2-2
- Avoid conflicts with other packages by not packaging (%ghost-ing) symlinks
- Use system zlib as it is installed by tdnf
- Added gzip, iputils, kmod, tar toys
* Wed Oct 30 2019 Alexey Makhalov <amakhalov@vmware.com> 0.8.2-1
- Version update. Use system libcrypto.
* Mon Oct 01 2018 Alexey Makhalov <amakhalov@vmware.com> 0.7.7-1
- Version update
* Mon Oct 02 2017 Alexey Makhalov <amakhalov@vmware.com> 0.7.3-6
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
