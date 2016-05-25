Summary:	String handling essentials library
Name:		libestr
Version:	0.1.10
Release:	2%{?dist}
License:	LGPLv2+
URL:		http://libestr.adiscon.com/
Source0:	http://libestr.adiscon.com/files/download/%{name}-%{version}.tar.gz
%define sha1 libestr=35cc717f5ae737a28140dd1472e13ce2ec317c6c
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
%setup -q
%build
./configure \
	--prefix=%{_prefix}
make %{?_smp_mflags}
%install
make DESTDIR=%{buildroot} install
%check
make -k check |& tee %{_specdir}/%{name}-check-log || %{nocheck}
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
*	Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 0.1.10-2
-	GA - Bump release of all rpms
*	Wed Jun 17 2015 Divya Thaluru <dthaluru@vmware.com> 0.1.10-1
-	Initial build. First version

