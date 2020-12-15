Summary:	String handling essentials library
Name:		libestr
Version:	0.1.11
Release:	1%{?dist}
License:	LGPLv2+
URL:		http://libestr.adiscon.com/
Source0:	http://libestr.adiscon.com/files/download/%{name}-%{version}.tar.gz
%define sha1 libestr=3acdf7dae0c3e0fa3dabf43267a1fb5f625c0606
Group:		System Environment/Base
Vendor:		VMware, Inc.
Distribution:	Photon
%description
This package compiles the string handling essentials library
used by the Rsyslog daemon.

%package devel
Summary:	Development libraries for string handling
Requires:	libestr

%description devel
The package contains libraries and header files for
developing applications that use libestr.

%prep
%autosetup -p1

%build
%configure
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_libdir}/*.so.*
%{_libdir}/*.a
%{_libdir}/*.la

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc

%changelog
*	Mon Dec 14 2020 Gerrit Photon <photon-checkins@vmware.com> 0.1.11-1
-	Automatic Version Bump
*	Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 0.1.10-2
-	GA - Bump release of all rpms
*	Wed Jun 17 2015 Divya Thaluru <dthaluru@vmware.com> 0.1.10-1
-	Initial build. First version
