Summary:    String handling essentials library
Name:       libestr
Version:    0.1.11
Release:    2%{?dist}
License:    LGPLv2+
URL:        http://libestr.adiscon.com/
Source0:    http://libestr.adiscon.com/files/download/%{name}-%{version}.tar.gz
%define sha512 libestr=0ab98c2fa4b58cf6fee89c88602725b8b5e8e5a171a6976cdd8cff4dfc1cd3e5b747868da74fccd1bca66b9fa524ceae1c4f1ad5ee653a44ff81df6916ab5328
Group:      System Environment/Base
Vendor:     VMware, Inc.
Distribution:   Photon
%description
This package compiles the string handling essentials library
used by the Rsyslog daemon.

%package devel
Summary:    Development libraries for string handling
Requires:   %{name} = %{version}-%{release}

%description devel
The package contains libraries and header files for
developing applications that use libestr.

%prep
%autosetup -p1

%build
%configure
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install %{?_smp_mflags}

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/*.a
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc

%changelog
* Mon Oct 03 2022 Shreenidhi Shedi <sshedi@vmware.com> 0.1.11-2
- Remove .la files
* Mon Dec 14 2020 Gerrit Photon <photon-checkins@vmware.com> 0.1.11-1
- Automatic Version Bump
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 0.1.10-2
- GA - Bump release of all rpms
* Wed Jun 17 2015 Divya Thaluru <dthaluru@vmware.com> 0.1.10-1
- Initial build. First version
