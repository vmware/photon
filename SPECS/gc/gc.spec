Summary:	A garbage collector for C and C++
Name:		gc
Version:	8.0.0
Release:	1%{?dist}
License:	BSD
URL:		http://www.hboehm.info/gc/
Source0:	http://www.hboehm.info/gc/gc_source/%{name}-%{version}.tar.gz
%define sha1 gc=bfb22367b95c796f2248b41405d37388027fe382
Source1:       http://www.ivmaisoft.com/_bin/atomic_ops/libatomic_ops-7.6.6.tar.gz
%define sha1 libatomic_ops=89a320bc94860fc63069615a0a7ee6f38eee9b70
Group:		System Environment/Base
Vendor:		VMware, Inc.
Distribution:	Photon

%description
The Boehm-Demers-Weiser conservative garbage collector can be
used as a garbage collecting replacement for C malloc or C++ new.

%package devel
Summary:	Development libraries and header files for gc
Requires:	gc

%description devel
The package contains libraries and header files for
developing applications that use gc.

%prep
%setup -q
%setup -q -T -D -a 1
ln -sfv libatomic_ops-7.6.6 libatomic_ops

%build
%configure \
	--datadir=%{_docdir} \
        --enable-cplusplus
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install

%check
make %{?_smp_mflags} check

%post	-p /sbin/ldconfig

%postun	-p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_libdir}/*.so.*
%{_docdir}/gc/*
%{_libdir}/*.la
%{_mandir}/man3/*

%files devel
%defattr(-,root,root)
%{_includedir}/*.h
%{_includedir}/gc/*.h
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc

%changelog
*   Mon Sep 17 2018 Sujay G <gsujay@vmware.com> 8.0.0-1
-   Bump to version 8.0.0
*   Wed Apr 05 2017 Danut Moraru <dmoraru@vmware.com> 7.6.0-1
-   Upgrade gc to 7.6.0, libatomic_ops to 7.4.4
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 7.4.2-2
-   GA - Bump release of all rpms
*   Thu Jun 18 2015 Divya Thaluru <dthaluru@vmware.com> 7.4.2-1
-   Initial build. First version

