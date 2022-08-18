Summary:        Contains programs for compressing and decompressing files
Name:           bzip2
Version:        1.0.8
Release:        5%{?dist}
License:        BSD
URL:            https://www.sourceware.org/bzip2
Group:          System Environment/Base
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://sourceware.org/pub/bzip2/%{name}-%{version}.tar.gz
%define sha512 %{name}=083f5e675d73f3233c7930ebe20425a533feedeaaa9d8cc86831312a6581cefbe6ed0d08d2fa89be81082f2a5abdabca8b3c080bf97218a1bd59dc118a30b9f3

# Downloaded from:
# https://www.linuxfromscratch.org/patches/lfs/9.1/bzip2-1.0.8-install_docs-1.patch
Patch0:         %{name}-%{version}-install_docs-1.patch

Requires:       %{name}-libs = %{version}-%{release}

Conflicts:      toybox < 0.8.2-2
Provides:       libbz2.so.1()(64bit)

%description
The Bzip2 package contains programs for compressing and
decompressing files.  Compressing text files with %{name} yields a much better
compression percentage than with the traditional gzip.

%package devel
Summary:        Header and development files for %{name}
Requires:       %{name} = %{version}-%{release}
%description    devel
It contains the libraries and header files to create applications

%package libs
Summary:        Libraries for %{name}
Group:          System Environment/Libraries
%description    libs
This package contains minimal set of shared %{name} libraries.

%prep
%autosetup -p1
sed -i 's@\(ln -s -f \)$(PREFIX)/bin/@\1@' Makefile
sed -i "s@(PREFIX)/man@(PREFIX)/share/man@g" Makefile

%build
if [ %{_host} != %{_build} ]; then
  MFLAGS="CC=%{_arch}-unknown-linux-gnu-gcc AR=%{_arch}-unknown-linux-gnu-ar RANLIB=%{_arch}-unknown-linux-gnu-ranlib"
  # deactivate buildtime testing
  sed -i 's/all: libbz2.a bzip2 bzip2recover test/all: libbz2.a bzip2 bzip2recover/' Makefile
else
  MFLAGS=
fi
make VERBOSE=1 %{?_smp_mflags} -f Makefile-libbz2_so $MFLAGS
make clean %{?_smp_mflags}
make VERBOSE=1 %{?_smp_mflags} $MFLAGS

%install
make PREFIX=%{buildroot}%{_usr} install %{?_smp_mflags}
install -vdm 0755 %{buildroot}%{_lib}
install -vdm 0755 %{buildroot}/bin
cp -av libbz2.so* %{buildroot}%{_lib}
install -vdm 755 %{buildroot}%{_libdir}
ln -sv libbz2.so.%{version} %{buildroot}%{_lib}/libbz2.so
ln -sv libbz2.so.%{version} %{buildroot}%{_lib}/libbz2.so.1
rm -v %{buildroot}%{_bindir}/{bunzip2,bzcat}
ln -sv %{name} %{buildroot}%{_bindir}/bunzip2
ln -sv %{name} %{buildroot}%{_bindir}/bzcat

find %{buildroot} -name '*.a' -delete

%check
make %{?_smp_mflags} check

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_bindir}/bzcat
%{_bindir}/bunzip2
%{_bindir}/bzless
%{_bindir}/bzgrep
%{_bindir}/%{name}
%{_bindir}/bzdiff
%{_bindir}/bzfgrep
%{_bindir}/bzcmp
%{_bindir}/bzip2recover
%{_bindir}/bzegrep
%{_bindir}/bzmore
%{_mandir}/man1/bzmore.1.gz
%{_mandir}/man1/bzfgrep.1.gz
%{_mandir}/man1/bzegrep.1.gz
%{_mandir}/man1/bzgrep.1.gz
%{_mandir}/man1/bzdiff.1.gz
%{_mandir}/man1/bzcmp.1.gz
%{_mandir}/man1/bzless.1.gz
%{_mandir}/man1/%{name}.1.gz

%files devel
%defattr(-,root,root)
%{_includedir}/bzlib.h
%{_libdir}/libbz2.so
%{_docdir}/*

%files libs
%defattr(-,root,root)
%{_lib}/libbz2.so.*

%changelog
* Wed Sep 07 2022 Shreenidhi Shedi <sshedi@vmware.com> 1.0.8-5
- Fix devel package Requires
* Thu Jun 17 2021 Shreenidhi Shedi <sshedi@vmware.com> 1.0.8-4
- Use 1.0.8 install_docs patch
* Thu Apr 16 2020 Alexey Makhalov <amakhalov@vmware.com> 1.0.8-3
- Do not conflict with toybox >= 0.8.2-2
* Tue Nov 26 2019 Alexey Makhalov <amakhalov@vmware.com> 1.0.8-2
- Cross compilation support
* Fri Oct 18 2019 Shreyas B <shreyasb@vmware.com> 1.0.8-1
- Upgrade to 1.0.8.
- Remove CVE-2016-3189.patch as the fix already available in the latest version.
* Tue Oct 2 2018 Michelle Wang <michellew@vmware.com> 1.0.6-9
- Add conflicts toybox.
* Sun Jun 04 2017 Bo Gan <ganb@vmware.com> 1.0.6-8
- Fix symlink.
* Fri Apr 14 2017 Alexey Makhalov <amakhalov@vmware.com> 1.0.6-7
- Added -libs subpackage.
* Fri Oct 21 2016 Kumar Kaushik <kaushikk@vmware.com> 1.0.6-6
- Fixing security bug CVE-2016-3189.
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.0.6-5
- GA - Bump release of all rpms.
* Tue Nov 10 2015 Mahmoud Bassiouny <mbassiouny@vmware.com> 1.0.6-4
- Providing libbz2.so.1, miror fix for devel provides.
* Fri Jun 5 2015 Divya Thaluru <dthaluru@vmware.com> 1.0.6-3
- Adding bzip2 package run time required package for bzip2-devel package.
* Mon May 18 2015 Touseef Liaqat <tliaqat@vmware.com> 1.0.6-2
- Update according to UsrMove.
* Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 1.0.6-1
- Initial build First version.
