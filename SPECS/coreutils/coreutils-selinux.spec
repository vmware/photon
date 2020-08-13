Summary:        Basic system utilities (SELinux enabled)
Name:           coreutils-selinux
Version:        8.32
Release:        2%{?dist}
License:        GPLv3
URL:            http://www.gnu.org/software/coreutils
Group:          System Environment/Base
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        http://ftp.gnu.org/gnu/coreutils/coreutils-%{version}.tar.xz
%define sha1    coreutils=b2b12195e276c64c8e850cf40ea2cff9b3aa53f6
# make this package to own serial console profile since it utilizes stty tool
Source1:        serial-console.sh
Patch0:         http://www.linuxfromscratch.org/patches/downloads/coreutils/coreutils-8.32-i18n-1.patch
%if %{with_check}
# Commented out one symlink test because device node and '.' are mounted on different folder
Patch1:         make-check-failure.patch
%endif
%ifarch aarch64
Patch2:         coreutils-8.32-aarch64-build-fix.patch
Patch3:         0001-ls-improve-removed-directory-test.patch
%endif
BuildRequires:  libselinux-devel
Requires:       gmp
Provides:       sh-utils
Provides:       coreutils = %{version}-%{release}
Obsoletes:      coreutils
%description
SELinux enabled coreutils package.

%prep
%setup -qn coreutils-%{version}
%patch0 -p1
%if %{with_check}
%patch1 -p1
%endif
%ifarch aarch64
%patch2 -p1
%patch3 -p1
%endif

%build
autoreconf -fiv
export FORCE_UNSAFE_CONFIGURE=1
%configure \
	--enable-no-install-program=kill,uptime \
	--with-selinux \
	--disable-silent-rules
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install
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
sed -i '/tests\/misc\/sort.pl/d' Makefile
sed -i 's/test-getlogin$(EXEEXT)//' gnulib-tests/Makefile
sed -i 's/PET/-05/g' tests/misc/date-debug.sh
sed -i 's/2>err\/merge-/2>\&1 > err\/merge-/g' tests/misc/sort-merge-fdlimit.sh
sed -i 's/)\" = \"10x0/| head -n 1)\" = \"10x0/g' tests/split/r-chunk.sh
sed  -i '/mb.sh/d' Makefile
chown -Rv nobody .
env PATH="$PATH" NON_ROOT_USERNAME=nobody make -k check-root
make NON_ROOT_USERNAME=nobody check

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(-,root,root)
/bin/*
%{_sysconfdir}/profile.d/serial-console.sh
%{_libexecdir}/*
%{_bindir}/*
%{_sbindir}/*
%{_mandir}/*/*

%changelog
* Thu Aug 13 2020 Shreenidhi Shedi <sshedi@vmware.com> 8.32-2
- Fixed aarch64 build issue
* Wed Jul 08 2020 Gerrit Photon <photon-checkins@vmware.com> 8.32-1
- Automatic Version Bump
* Sat Apr 18 2020 Alexey Makhalov <amakhalov@vmware.com> 8.30-3
- coreutils-selinux: new package, cloned from coreutils.
- keep version-release in sync with coreutils.
