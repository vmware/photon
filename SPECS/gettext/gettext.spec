Summary:	Utilities for internationalization and localization
Name:		gettext
Version:	0.19.8.1
Release:	5%{?dist}
License:	GPLv3
URL:		http://www.gnu.org/software/gettext
Group:		Applications/System
Vendor:		VMware, Inc.
Distribution:	Photon
Source0:	http://ftp.gnu.org/gnu/gettext/%{name}-%{version}.tar.xz
%define sha512  gettext=3553227b62f2a7d9b67c881ef889c030a6a21d5ecd210c4bf3d649df0b37193a99a68cf8fd5f2c69b6a87e847035dd9576f9bcb9363422866e26b04f4f6dd431
Patch0:         gettext-0.19.8.1-CVE-2018-18751.patch
Patch1:		libcroco-CVE-2020-12825.patch
Patch2:         libxml2-CVE-2022-40304.patch

BuildRequires:  bison

%description
These allow programs to be compiled with NLS
(Native Language Support), enabling them to output
messages in the user's native language.

%prep
%autosetup -p1

%build
%configure \
	--docdir=%{_defaultdocdir}/%{name}-%{version} \
	--disable-silent-rules
%make_build

%install
%make_install
find %{buildroot}%{_libdir} -name '*.la' -delete
rm -rf %{buildroot}/usr/share/doc/gettext-%{version}/examples
rm -rf %{buildroot}%{_infodir}
%find_lang %{name} --all-name

%check
sed -i 's/test-term-ostream-xterm//1' ./gettext-tools/gnulib-tests/Makefile
make %{?_smp_mflags} check

%post	-p /sbin/ldconfig

%postun	-p /sbin/ldconfig

%files -f %{name}.lang
%defattr(-,root,root)
%{_bindir}/*
%{_includedir}/*
%{_libdir}/gettext/*
%{_libdir}/*.so.*
%{_libdir}/*.so
%{_libdir}/*.a
%{_datarootdir}/aclocal/*
%{_datadir}/*
%{_defaultdocdir}/%{name}-%{version}/*
%{_datarootdir}/%{name}/*
%{_mandir}/*

%changelog
*       Wed Dec 21 2022 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 0.19.8.1-5
-       Fix CVE-2022-40304
*	Tue Oct 13 2020 Siju Maliakkal <smaliakkal@vmware.com> 0.19.8.1-4
-	Fix CVE-2020-12825 in blundled libcroco source
*       Thu Jun 18 2020 Ashwin H <ashwinh@vmware.com> 0.19.8.1-3
-       Fix CVE-2018-18751
*       Mon Sep 09 2019 Prashant Singh Chauhan <psinghchauha@vmware.com> 0.19.8.1-2
-       Fix for make check
*       Fri Sep 14 2018 Keerthana K <keerthanak@vmware.com> 0.19.8.1-1
-       Update to version 0.19.8.1
*	Wed Apr 05 2017 Danut Moraru <dmoraru@vmware.com> 0.19.8-1
-	Upgrade to 0.19.8
*	Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 0.19.5.1-2
-	GA - Bump release of all rpms
* 	Tue Jan 12 2016 Xiaolin Li <xiaolinl@vmware.com> 0.19.5.1-1
- 	Updated to version 0.19.5.1
*	Tue Nov 10 2015 Xiaolin Li <xiaolinl@vmware.com> 0.18.3.2-2
-	Handled locale files with macro find_lang
*	Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 0.18.3.2-1
-	Initial build. First version
