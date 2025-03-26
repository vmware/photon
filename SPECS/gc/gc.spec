Summary:    A garbage collector for C and C++
Name:       gc
Version:    8.2.2
Release:    3%{?dist}
Url:        http://www.hboehm.info/gc
Group:      System Environment/Base
Vendor:     VMware, Inc.
Distribution:   Photon

Source0: http://www.hboehm.info/gc/gc_source/%{name}-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}

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

%if 0%{?with_check}
%check
make %{?_smp_mflags} check
%endif

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_libdir}/*.so.*
%{_docdir}/%{name}/*
%{_mandir}/man3/*

%files devel
%defattr(-,root,root)
%{_includedir}/*.h
%{_includedir}/%{name}/*.h
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc

%changelog
* Thu Dec 12 2024 Guruswamy Basavaiah <guruswamy.basavaiah@broadcom.com> 8.2.2-3
- Release bump for SRP compliance
* Tue Nov 05 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 8.2.2-2
- Release bump for SRP compliance
* Thu Sep 29 2022 Shreenidhi Shedi <sshedi@vmware.com> 8.2.2-1
- Upgrade to v8.2.2
* Sun Aug 07 2022 Shreenidhi Shedi <sshedi@vmware.com> 8.0.4-2
- Remove .la files
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
