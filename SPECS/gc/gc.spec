Summary:    A garbage collector for C and C++
Name:       gc
Version:    8.0.4
Release:    2%{?dist}
License:    BSD
Url:        http://www.hboehm.info/gc
Group:      System Environment/Base
Vendor:     VMware, Inc.
Distribution:   Photon

Source0: http://www.hboehm.info/gc/gc_source/%{name}-%{version}.tar.gz
%define sha512 %{name}=57ccca15c6e50048d306a30de06c1a844f36103a84c2d1c17cbccbbc0001e17915488baec79737449982da99ce5d14ce527176afae9ae153cbbb5a19d986366e

BuildRequires: libatomic_ops-devel

Requires: libatomic_ops

%description
The Boehm-Demers-Weiser conservative garbage collector can be
used as a garbage collecting replacement for C malloc or C++ new.

%package devel
Summary:    Development libraries and header files for gc
Requires:   %{name} = %{version}-%{release}

%description devel
The package contains libraries and header files for
developing applications that use gc.

%prep
%autosetup -p1

%build
%configure --enable-cplusplus
%make_build

%install
%make_install %{?_smp_mflags}
rm -f %{buildroot}%{_libdir}/*.la

%check
make %{?_smp_mflags} check

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_libdir}/*.so.*
%{_docdir}/gc/*
%{_mandir}/man3/*

%files devel
%defattr(-,root,root)
%{_includedir}/*.h
%{_includedir}/gc/*.h
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc

%changelog
* Fri Feb 24 2023 Shreenidhi Shedi <sshedi@vmware.com> 8.0.4-2
- Fix the missed version bump
* Thu Oct 17 2019 Shreenidhi Shedi <sshedi@vmware.com> 8.0.4-1
- Upgrade to version 8.0.4
* Mon Sep 17 2018 Sujay G <gsujay@vmware.com> 8.0.0-1
- Bump to version 8.0.0
* Wed Apr 05 2017 Danut Moraru <dmoraru@vmware.com> 7.6.0-1
- Upgrade gc to 7.6.0, libatomic_ops to 7.4.4
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 7.4.2-2
- GA - Bump release of all rpms
* Thu Jun 18 2015 Divya Thaluru <dthaluru@vmware.com> 7.4.2-1
- Initial build. First version
