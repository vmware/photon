Summary:        Basic system utilities (SELinux enabled)
Name:           coreutils-selinux
Version:        9.1
Release:        1%{?dist}
License:        GPLv3
URL:            http://www.gnu.org/software/coreutils
Group:          System Environment/Base
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        http://ftp.gnu.org/gnu/coreutils/coreutils-%{version}.tar.xz
%define sha512  coreutils=a6ee2c549140b189e8c1b35e119d4289ec27244ec0ed9da0ac55202f365a7e33778b1dc7c4e64d1669599ff81a8297fe4f5adbcc8a3a2f75c919a43cd4b9bdfa
# make this package to own serial console profile since it utilizes stty tool
Source1:        serial-console.sh

# Patches are taken from:
# www.linuxfromscratch.org/patches/downloads/coreutils/
Patch0: coreutils-%{version}-i18n-1.patch

BuildRequires: libselinux-devel

Requires: gmp

Provides: sh-utils
Provides: coreutils = %{version}-%{release}

Obsoletes: coreutils

%description
SELinux enabled coreutils package.

%prep
%autosetup -p1 -n coreutils-%{version}

%build
autoreconf -fiv
export FORCE_UNSAFE_CONFIGURE=1
%configure \
    --enable-no-install-program=kill,uptime \
    --with-selinux \
    --disable-silent-rules

make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install %{?_smp_mflags}
install -vdm 755 %{buildroot}/bin
install -vdm 755 %{buildroot}%{_sbindir}
install -vdm 755 %{buildroot}%{_mandir}/man8
mv -v %{buildroot}%{_bindir}/{cat,chgrp,chmod,chown,cp,date,dd,df,echo} %{buildroot}/bin
mv -v %{buildroot}%{_bindir}/{false,ln,ls,mkdir,mknod,mv,pwd,rm} %{buildroot}/bin
mv -v %{buildroot}%{_bindir}/{rmdir,stty,sync,true,uname,test,[} %{buildroot}/bin
mv -v %{buildroot}%{_bindir}/chroot %{buildroot}%{_sbindir}
mv -v %{buildroot}%{_mandir}/man1/chroot.1 %{buildroot}%{_mandir}/man8/chroot.8
sed -i 's/\"1\"/\"8\"/1' %{buildroot}%{_mandir}/man8/chroot.8
mv -v %{buildroot}%{_bindir}/{head,sleep,nice} %{buildroot}/bin
rm -rf %{buildroot}%{_infodir}
install -vdm755 %{buildroot}/etc/profile.d
install -m 0644 %{SOURCE1} %{buildroot}/etc/profile.d/
rm -rf %{buildroot}%{_datadir}/locale

%check
%if 0%{?with_check}
sed -i '/tests\/misc\/sort.pl/d' Makefile
sed -i 's/test-getlogin$(EXEEXT)//' gnulib-tests/Makefile
sed -i 's/PET/-05/g' tests/misc/date-debug.sh
sed -i 's/2>err\/merge-/2>\&1 > err\/merge-/g' tests/misc/sort-merge-fdlimit.sh
sed -i 's/)\" = \"10x0/| head -n 1)\" = \"10x0/g' tests/split/r-chunk.sh
sed  -i '/mb.sh/d' Makefile
chown -Rv nobody .
env PATH="$PATH" NON_ROOT_USERNAME=nobody make -k check-root
make NON_ROOT_USERNAME=nobody check %{?_smp_mflags}
%endif

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
/bin/*
%{_sysconfdir}/profile.d/serial-console.sh
%{_libexecdir}/*
%{_bindir}/*
%{_sbindir}/*
%{_mandir}/*/*

%changelog
* Mon Apr 25 2022 Shreenidhi Shedi <sshedi@vmware.com> 9.1-1
- Upgrade to v9.1
* Tue Nov 30 2021 Satya Naga Vasamsetty <svasamsetty@vmware.com> 8.32-3
- Increment version for openssl 3.0.0 compatibility
* Thu Aug 13 2020 Shreenidhi Shedi <sshedi@vmware.com> 8.32-2
- Fixed aarch64 build issue
* Wed Jul 08 2020 Gerrit Photon <photon-checkins@vmware.com> 8.32-1
- Automatic Version Bump
* Sat Apr 18 2020 Alexey Makhalov <amakhalov@vmware.com> 8.30-3
- coreutils-selinux: new package, cloned from coreutils.
- keep version-release in sync with coreutils.
