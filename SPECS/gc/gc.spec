Summary:	A garbage collector for C and C++
Name:		gc
Version:	7.4.2
Release:	1%{?dist}
License:	BSD
Url:		http://www.hboehm.info/gc/
Source0:	http://www.hboehm.info/gc/gc_source/%{name}-%{version}.tar.gz
Source1:	http://www.ivmaisoft.com/_bin/atomic_ops/libatomic_ops-7.4.2.tar.gz
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
ln -sfv libatomic_ops-7.4.2 libatomic_ops
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
%files devel
%defattr(-,root,root)
%{_includedir}/*.h
%{_includedir}/gc/*.h
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%changelog
*	Thu Jun 18 2015 Divya Thaluru <dthaluru@vmware.com> 7.4.2-1
-	Initial build. First version

