# also defined in coreutils.spec and coreutils-selinux.spec
%define coreutils_present           %{_sharedstatedir}/rpm-state/coreutils
%define coreutils_selinux_present   %{_sharedstatedir}/rpm-state/coreutils-selinux

Name:           toybox
Version:        0.8.9
Release:        6%{?dist}
License:        BSD
Summary:        Common Linux command line utilities in a single executable
Url:            http://landley.net/toybox
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: http://landley.net/toybox/downloads/%{name}-%{version}.tar.gz
%define sha512 %{name}=73a3ec2a0d69b1566e1663e94b2bc7764b9f93e53978725f036f066837ab2769033e8bf17d5550e565656781cacf27d93960dd611ffed5425fa006d1d3104351

Patch0: %{name}-change-toys-path.patch

Source1: config-%{name}
Source2: %{name}-toys

BuildRequires:  openssl-devel
BuildRequires:  zlib-devel

Requires:       openssl-libs
Requires:       zlib

Provides:       /bin/grep

%description
Toybox combines common Linux command line utilities together into a single
BSD-licensed executable that's simple, small, fast, reasonably
standards-compliant, and powerful enough to turn Android into a development
environment.

%package docs
Summary:    %{name} docs
Group:      Documentation
Requires:   %{name} = %{version}-%{release}

%description docs
The package contains %{name} doc files.

%prep
%autosetup -p1

%build
cp %{SOURCE1} .config
# If we make NOSTRIP=0, toybox debuginfo rpm will be useless
NOSTRIP=1 make CFLAGS="-Wall -Wundef -Wno-char-subscripts -Werror=implicit-function-declaration -g" %{?_smp_mflags}

%install
install -d %{buildroot}{%{_bindir},%{_sbindir}}
PREFIX=%{buildroot} make install %{?_smp_mflags}
mv %{buildroot}/bin/* %{buildroot}%{_bindir}
mv %{buildroot}/sbin/* %{buildroot}%{_sbindir}
mv %{buildroot}%{_sbindir}/{ifconfig,lspci} %{buildroot}%{_bindir}
mv %{buildroot}%{_bindir}/httpd %{buildroot}%{_sbindir}
chmod 755 %{buildroot}%{_bindir}/%{name}
install -m 0755 %{SOURCE2} %{buildroot}%{_bindir}/%{name}-toys

%if 0%{?with_check}
%check
# Do not run all tests, skip losetup make tests
sed -i "s/^  if \[ \$# -ne 0 \]/  if false; /" scripts/test.sh
pushd tests
tests_to_run=$(ls *.test | sed 's/.test//;/losetup/d')
popd
tests_to_run=$(echo $tests_to_run | sed -e 's/pkill//g')
./scripts/test.sh $tests_to_run
%endif

%global _mktoy_() \
mktoy() { \
  local arg='' \
  for arg in $@; do \
    %{_bindir}/toybox ln -sf %{_bindir}/toybox "${arg}" \
  done \
}

%posttrans
%{_bindir}/%{name}-toys --install

%preun
%{_bindir}/%{name}-toys --uninstall

%triggerpostun -- dos2unix
[ $2 -eq 0 ] || exit 0
%{_mktoy_}
mktoy %{_bindir}/dos2unix %{_bindir}/unix2dos

%triggerpostun -- bzip2
[ $2 -eq 0 ] || exit 0
%{_mktoy_}
mktoy %{_bindir}/bunzip2 %{_bindir}/bzcat

%triggerpostun -- coreutils
[ $2 -eq 0 ] || exit 0
[ -f %{coreutils_selinux_present} ] && exit 0
%{_mktoy_}
mktoy %{_bindir}/cat \
    %{_bindir}/chgrp \
    %{_bindir}/chmod \
    %{_bindir}/chown \
    %{_bindir}/cksum \
    %{_bindir}/cp \
    %{_bindir}/date \
    %{_bindir}/df \
    %{_bindir}/echo \
    %{_bindir}/false \
    %{_bindir}/ln \
    %{_bindir}/ls \
    %{_bindir}/mkdir \
    %{_bindir}/mknod \
    %{_bindir}/mktemp \
    %{_bindir}/mv \
    %{_bindir}/nice \
    %{_bindir}/printenv \
    %{_bindir}/pwd \
    %{_bindir}/rm \
    %{_bindir}/rmdir \
    %{_bindir}/sleep \
    %{_bindir}/stat \
    %{_bindir}/stty \
    %{_bindir}/sync \
    %{_bindir}/touch \
    %{_bindir}/true \
    %{_bindir}/uname \
    %{_bindir}/[ \
    %{_bindir}/base64 \
    %{_bindir}/basename \
    %{_bindir}/comm \
    %{_bindir}/cut \
    %{_bindir}/dirname \
    %{_bindir}/du \
    %{_bindir}/env \
    %{_bindir}/expand \
    %{_bindir}/factor \
    %{_bindir}/groups \
    %{_bindir}/head \
    %{_bindir}/id \
    %{_bindir}/install \
    %{_bindir}/link \
    %{_bindir}/logname \
    %{_bindir}/md5sum \
    %{_bindir}/mkfifo \
    %{_bindir}/nl \
    %{_bindir}/nohup \
    %{_bindir}/nproc \
    %{_bindir}/od \
    %{_bindir}/paste \
    %{_bindir}/printf \
    %{_bindir}/readlink \
    %{_bindir}/realpath \
    %{_bindir}/seq \
    %{_bindir}/sha1sum \
    %{_bindir}/sha224sum \
    %{_bindir}/sha256sum \
    %{_bindir}/sha384sum \
    %{_bindir}/sha512sum \
    %{_bindir}/shred \
    %{_bindir}/sort \
    %{_bindir}/split \
    %{_bindir}/tac \
    %{_bindir}/tail \
    %{_bindir}/tee \
    %{_bindir}/test \
    %{_bindir}/timeout \
    %{_bindir}/truncate \
    %{_bindir}/tty \
    %{_bindir}/uniq \
    %{_bindir}/unlink \
    %{_bindir}/wc \
    %{_bindir}/who \
    %{_bindir}/whoami \
    %{_bindir}/yes \
    %{_sbindir}/chroot

%triggerpostun -- coreutils-selinux
[ $2 -eq 0 ] || exit 0
[ -f %{coreutils_present} ] && exit 0
%{_mktoy_}
mktoy %{_bindir}/cat \
    %{_bindir}/chgrp \
    %{_bindir}/chmod \
    %{_bindir}/chown \
    %{_bindir}/cksum \
    %{_bindir}/cp \
    %{_bindir}/date \
    %{_bindir}/df \
    %{_bindir}/echo \
    %{_bindir}/false \
    %{_bindir}/ln \
    %{_bindir}/ls \
    %{_bindir}/mkdir \
    %{_bindir}/mknod \
    %{_bindir}/mktemp \
    %{_bindir}/mv \
    %{_bindir}/nice \
    %{_bindir}/printenv \
    %{_bindir}/pwd \
    %{_bindir}/rm \
    %{_bindir}/rmdir \
    %{_bindir}/sleep \
    %{_bindir}/stat \
    %{_bindir}/stty \
    %{_bindir}/sync \
    %{_bindir}/touch \
    %{_bindir}/true \
    %{_bindir}/uname \
    %{_bindir}/[ \
    %{_bindir}/base64 \
    %{_bindir}/basename \
    %{_bindir}/comm \
    %{_bindir}/cut \
    %{_bindir}/dirname \
    %{_bindir}/du \
    %{_bindir}/env \
    %{_bindir}/expand \
    %{_bindir}/factor \
    %{_bindir}/groups \
    %{_bindir}/head \
    %{_bindir}/id \
    %{_bindir}/install \
    %{_bindir}/link \
    %{_bindir}/logname \
    %{_bindir}/md5sum \
    %{_bindir}/mkfifo \
    %{_bindir}/nl \
    %{_bindir}/nohup \
    %{_bindir}/nproc \
    %{_bindir}/od \
    %{_bindir}/paste \
    %{_bindir}/printf \
    %{_bindir}/readlink \
    %{_bindir}/realpath \
    %{_bindir}/seq \
    %{_bindir}/sha1sum \
    %{_bindir}/sha224sum \
    %{_bindir}/sha256sum \
    %{_bindir}/sha384sum \
    %{_bindir}/sha512sum \
    %{_bindir}/shred \
    %{_bindir}/sort \
    %{_bindir}/split \
    %{_bindir}/tac \
    %{_bindir}/tail \
    %{_bindir}/tee \
    %{_bindir}/test \
    %{_bindir}/timeout \
    %{_bindir}/truncate \
    %{_bindir}/tty \
    %{_bindir}/uniq \
    %{_bindir}/unlink \
    %{_bindir}/wc \
    %{_bindir}/who \
    %{_bindir}/whoami \
    %{_bindir}/yes \
    %{_sbindir}/chroot

%triggerpostun -- cpio
[ $2 -eq 0 ] || exit 0
%{_mktoy_}
mktoy %{_bindir}/cpio

%triggerpostun -- diffutils
[ $2 -eq 0 ] || exit 0
%{_mktoy_}
mktoy %{_bindir}/cmp

%triggerpostun -- elixir
[ $2 -eq 0 ] || exit 0
%{_mktoy_}
mktoy %{_bindir}/mix

%triggerpostun -- expect
[ $2 -eq 0 ] || exit 0
%{_mktoy_}
mktoy %{_bindir}/mkpasswd

%triggerpostun -- mkpasswd
[ $2 -eq 0 ] || exit 0
%{_mktoy_}
mktoy /usr/bin/mkpasswd

%triggerpostun -- e2fsprogs
[ $2 -eq 0 ] || exit 0
%{_mktoy_}
mktoy %{_bindir}/chattr %{_bindir}/lsattr

%triggerpostun -- file
[ $2 -eq 0 ] || exit 0
%{_mktoy_}
mktoy %{_bindir}/file

%triggerpostun -- findutils
[ $2 -eq 0 ] || exit 0
%{_mktoy_}
mktoy %{_bindir}/find %{_bindir}/xargs

%triggerpostun -- grep
[ $2 -eq 0 ] || exit 0
%{_mktoy_}
mktoy %{_bindir}/egrep \
      %{_bindir}/fgrep \
      %{_bindir}/grep

%triggerpostun -- gzip
[ $2 -eq 0 ] || exit 0
%{_mktoy_}
mktoy %{_bindir}/gunzip \
      %{_bindir}/gzip \
      %{_bindir}/zcat

%triggerpostun -- httpd
[ $2 -eq 0 ] || exit 0
%{_mktoy_}
mktoy %{_sbindir}/httpd

%triggerpostun -- iotop
[ $2 -eq 0 ] || exit 0
%{_mktoy_}
mktoy %{_sbindir}/iotop

%triggerpostun -- iputils
[ $2 -eq 0 ] || exit 0
%{_mktoy_}
mktoy %{_bindir}/ping %{_bindir}/ping6

%triggerpostun -- kbd
[ $2 -eq 0 ] || exit 0
%{_mktoy_}
mktoy %{_bindir}/chvt

%triggerpostun -- kmod
[ $2 -eq 0 ] || exit 0
%{_mktoy_}
mktoy %{_sbindir}/insmod \
      %{_sbindir}/lsmod \
      %{_sbindir}/modinfo \
      %{_sbindir}/rmmod

%triggerpostun -- netcat
[ $2 -eq 0 ] || exit 0
%{_mktoy_}
mktoy %{_bindir}/netcat %{_bindir}/nc

%triggerpostun -- net-tools
[ $2 -eq 0 ] || exit 0
%{_mktoy_}
mktoy %{_bindir}/hostname \
      %{_bindir}/netstat \
      %{_bindir}/ifconfig

%triggerpostun -- parted
[ $2 -eq 0 ] || exit 0
%{_mktoy_}
mktoy %{_sbindir}/partprobe

%triggerpostun -- patch
[ $2 -eq 0 ] || exit 0
%{_mktoy_}
mktoy %{_bindir}/patch

%triggerpostun -- pciutils
[ $2 -eq 0 ] || exit 0
%{_mktoy_}
mktoy %{_bindir}/lspci

%triggerpostun -- procps-ng
[ $2 -eq 0 ] || exit 0
%{_mktoy_}
mktoy %{_bindir}/ps \
      %{_bindir}/pidof \
      %{_bindir}/free \
      %{_bindir}/w \
      %{_bindir}/pgrep \
      %{_bindir}/uptime \
      %{_bindir}/vmstat \
      %{_bindir}/pmap \
      %{_bindir}/pwdx \
      %{_bindir}/top \
      %{_bindir}/pkill \
      %{_sbindir}/sysctl

%triggerpostun -- psmisc
[ $2 -eq 0 ] || exit 0
%{_mktoy_}
mktoy %{_bindir}/killall

%triggerpostun -- sed
[ $2 -eq 0 ] || exit 0
%{_mktoy_}
mktoy %{_bindir}/sed

%triggerpostun -- shadow-tools
[ $2 -eq 0 ] || exit 0
%{_mktoy_}
mktoy %{_bindir}/login \
      %{_bindir}/su \
      %{_bindir}/passwd

%triggerpostun -- tar
[ $2 -eq 0 ] || exit 0
%{_mktoy_}
mktoy %{_bindir}/tar

%triggerpostun -- usbutils
[ $2 -eq 0 ] || exit 0
%{_mktoy_}
mktoy %{_bindir}/lsusb

%triggerpostun -- util-linux
[ $2 -eq 0 ] || exit 0
%{_mktoy_}
mktoy %{_bindir}/dmesg \
      %{_bindir}/kill \
      %{_bindir}/mount \
      %{_bindir}/mountpoint \
      %{_bindir}/umount \
      %{_sbindir}/blkid \
      %{_sbindir}/blockdev \
      %{_sbindir}/hwclock \
      %{_sbindir}/losetup \
      %{_sbindir}/mkswap \
      %{_sbindir}/pivot_root \
      %{_sbindir}/swapoff \
      %{_sbindir}/swapon \
      %{_sbindir}/switch_root \
      %{_bindir}/cal \
      %{_bindir}/eject \
      %{_bindir}/fallocate \
      %{_bindir}/flock \
      %{_bindir}/ionice \
      %{_bindir}/nsenter \
      %{_bindir}/renice \
      %{_bindir}/rev \
      %{_bindir}/setsid \
      %{_bindir}/taskset \
      %{_sbindir}/fsfreeze \
      %{_sbindir}/rfkill

%triggerpostun -- vim-extra
[ $2 -eq 0 ] || exit 0
%{_mktoy_}
mktoy %{_bindir}/xxd

%triggerpostun -- wget
[ $2 -eq 0 ] || exit 0
%{_mktoy_}
mktoy %{_bindir}/wget

%triggerpostun -- which
[ $2 -eq 0 ] || exit 0
%{_mktoy_}
mktoy %{_bindir}/which

%files
%defattr(-,root,root)
%{_bindir}/%{name}
%{_bindir}/%{name}-toys

# bzip2
%ghost %{_bindir}/bunzip2
%ghost %{_bindir}/bzcat

# coreutils
%ghost %{_bindir}/cat
%ghost %{_bindir}/chgrp
%ghost %{_bindir}/chmod
%ghost %{_bindir}/chown
%ghost %{_bindir}/cksum
%ghost %{_bindir}/cp
%ghost %{_bindir}/date
%ghost %{_bindir}/df
%ghost %{_bindir}/echo
%ghost %{_bindir}/false
%ghost %{_bindir}/ln
%ghost %{_bindir}/ls
%ghost %{_bindir}/mkdir
%ghost %{_bindir}/mknod
%ghost %{_bindir}/mktemp
%ghost %{_bindir}/mv
%ghost %{_bindir}/nice
%ghost %{_bindir}/printenv
%ghost %{_bindir}/pwd
%ghost %{_bindir}/rm
%ghost %{_bindir}/rmdir
%ghost %{_bindir}/sleep
%ghost %{_bindir}/stat
%ghost %{_bindir}/stty
%ghost %{_bindir}/sync
%ghost %{_bindir}/touch
%ghost %{_bindir}/true
%ghost %{_bindir}/uname
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
%ghost %{_bindir}/cpio

# diffutils
%ghost %{_bindir}/cmp

# elixir
%ghost %{_bindir}/mix

# expect & mkpasswd
%ghost %{_bindir}/mkpasswd

# e2fsprogs
%ghost %{_bindir}/chattr
%ghost %{_bindir}/lsattr

# file
%ghost %{_bindir}/file

# findutils
%ghost %{_bindir}/find
%ghost %{_bindir}/xargs

# grep
%ghost %{_bindir}/egrep
%ghost %{_bindir}/fgrep
%ghost %{_bindir}/grep

# gzip
%ghost %{_bindir}/gunzip
%ghost %{_bindir}/gzip
%ghost %{_bindir}/zcat

# httpd
%ghost %{_sbindir}/httpd

# iotop
%ghost %{_sbindir}/iotop

# iputils
%ghost %{_bindir}/ping
%ghost %{_bindir}/ping6

# kbd
%ghost %{_bindir}/chvt

# kmod
%ghost %{_sbindir}/insmod
%ghost %{_sbindir}/lsmod
%ghost %{_sbindir}/modinfo
%ghost %{_sbindir}/rmmod

# netcat
%ghost %{_bindir}/netcat
%ghost %{_bindir}/nc

# net-tools
%ghost %{_bindir}/hostname
%ghost %{_bindir}/netstat
%ghost %{_bindir}/ifconfig

# parted
%ghost %{_sbindir}/partprobe

# patch
%ghost %{_bindir}/patch

# pciutils
%ghost %{_bindir}/lspci

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
%ghost %{_bindir}/sed

# shadow-tools
%ghost %{_bindir}/login
%ghost %{_bindir}/su
%ghost %{_bindir}/passwd

# tar
%ghost %{_bindir}/tar

# usbutils
%ghost %{_bindir}/lsusb

# util-linux
%ghost %{_bindir}/dmesg
%ghost %{_bindir}/kill
%ghost %{_bindir}/mount
%ghost %{_bindir}/mountpoint
%ghost %{_bindir}/umount
%ghost %{_sbindir}/blkid
%ghost %{_sbindir}/blockdev
%ghost %{_sbindir}/hwclock
%ghost %{_sbindir}/losetup
%ghost %{_sbindir}/mkswap
%ghost %{_sbindir}/pivot_root
%ghost %{_sbindir}/swapoff
%ghost %{_sbindir}/swapon
%ghost %{_sbindir}/switch_root
%ghost %{_bindir}/cal
%ghost %{_bindir}/eject
%ghost %{_bindir}/fallocate
%ghost %{_bindir}/flock
%ghost %{_bindir}/ionice
%ghost %{_bindir}/nsenter
%ghost %{_bindir}/renice
%ghost %{_bindir}/rev
%ghost %{_bindir}/setsid
%ghost %{_bindir}/taskset
%ghost %{_sbindir}/fsfreeze
%ghost %{_sbindir}/rfkill

# vim-extra
%ghost %{_bindir}/xxd

# wget
%ghost %{_bindir}/wget

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
* Sun Nov 19 2023 Shreenidhi Shedi <sshedi@vmware.com> 0.8.9-6
- Bump version as a part of openssl upgrade
* Fri Jul 28 2023 Oliver Kurth <okurth@vmware.com> 0.8.9-5
- enable httpd
* Fri Apr 14 2023 Shreenidhi Shedi <sshedi@vmware.com> 0.8.9-4
- Bump version as a part of zlib upgrade
* Tue Mar 28 2023 Shreenidhi Shedi <sshedi@vmware.com> 0.8.9-3
- Fix iputils provided binary path
* Thu Mar 09 2023 Shreenidhi Shedi <sshedi@vmware.com> 0.8.9-2
- Require openssl-libs
* Mon Mar 06 2023 Harinadh D <hdommaraju@vmware.com> 0.8.9-1
- version upgrade
- fix copy_file_range() issue when copying to another filesystem
* Fri Feb 17 2023 Shreenidhi Shedi <sshedi@vmware.com> 0.8.8-3
- Add rules for mkpasswd
* Fri Jan 27 2023 Shreenidhi Shedi <sshedi@vmware.com> 0.8.8-2
- Fix triggers
* Sun Aug 21 2022 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 0.8.8-1
- Upgrade to 0.8.8
- catv is removed, use 'cat -v' instead
* Sun May 29 2022 Shreenidhi Shedi <sshedi@vmware.com> 0.8.6-3
- Fix binary path
* Sat Apr 02 2022 Prashant S Chauhan <psinghchauha@vmware.com> 0.8.6-2
- Enable nsenter utility in toybox
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
