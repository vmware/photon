Summary:    Atomic memory update operations portable implementation
Name:       libatomic_ops
Version:    7.4.4
Release:    1%{?dist}
License:    GPLv2 and MIT
URL:        https://github.com/ivmai/libatomic_ops
Group:      Development/Libraries
Source0:    http://www.ivmaisoft.com/_bin/atomic_ops/libatomic_ops-%{version}.tar.gz
%define sha1 libatomic_ops=426af02f1bb8b91979fa8794e9e0b29e2be1e47e
Vendor:     VMware, Inc.
Distribution:   Photon

%description
This package provides semi-portable access to hardware-provided atomic memory update operations on a number of architectures.

%package devel
Summary:    Development files for the libatomic_ops library
Group:      Development/Libraries
Requires:   libatomic_ops
Provides:   libatomic_ops-devel
Provides:   libatomic_ops-devel(x86-64)

%description devel
Libraries and header files for libatomic_ops library.


%prep
%setup -q
%build
./configure --prefix=%{_prefix}      \
            --bindir=%{_sbindir}     \
            --enable-shared \
            --disable-silent-rules

make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install
find %{buildroot} -name '*.la' -delete

%check
make check

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%{_datadir}/libatomic_ops/COPYING
%{_datadir}/libatomic_ops/LICENSING.txt
%{_libdir}/libatomic_ops.so.*
%{_libdir}/libatomic_ops_gpl.so.*

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_datadir}/libatomic_ops/README*
%{_libdir}/libatomic_ops.a
%{_libdir}/libatomic_ops_gpl.a
%{_libdir}/libatomic_ops.so
%{_libdir}/libatomic_ops_gpl.so
%{_libdir}/pkgconfig/atomic_ops.pc

%changelog
*   Tue Jul 26 2016 Xiaolin Li <xiaolinl@vmware.com> 7.4.4-1
-   Initial build. First version
