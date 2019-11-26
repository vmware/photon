Summary:	A garbage collector for C and C++
Name:		gc
Version:	7.4.18
Release:	1%{?dist}
License:	BSD
Url:		http://www.hboehm.info/gc/
Source0:	http://www.hboehm.info/gc/gc_source/%{name}-%{version}.tar.gz
%define sha1 gc=7d02be902a25f42db54ef79cad1f6adb48660f2b
Source1:	http://www.ivmaisoft.com/_bin/atomic_ops/libatomic_ops-7.4.14.tar.gz
%define sha1 libatomic_ops=c8b29003f4a7169dde25f8e47b277b3bb589d0a1
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
ln -sfv libatomic_ops-7.4.14 libatomic_ops
%build
./configure \
	--prefix=%{_prefix} \
	--datadir=%{_docdir} \
        --enable-cplusplus
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
%{_docdir}/gc/*
%{_libdir}/*.a
%{_libdir}/*.la
%{_mandir}/man3/*
%files devel
%defattr(-,root,root)
%{_includedir}/*.h
%{_includedir}/gc/*.h
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%changelog
*       Tue Nov 26 2019 Satya Naga Vasamsetty <svasamsetty@vmware.com> 7.4.18-1
-       Upgrade gc to 7.4.18, libatomic_ops to 7.4.14
*	Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 7.4.2-2
-	GA - Bump release of all rpms
*	Thu Jun 18 2015 Divya Thaluru <dthaluru@vmware.com> 7.4.2-1
-	Initial build. First version

