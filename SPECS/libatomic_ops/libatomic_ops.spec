Summary:    Atomic memory update operations portable implementation
Name:       libatomic_ops
Version:    7.6.10
Release:    2%{?dist}
License:    GPLv2 and MIT
URL:        https://github.com/ivmai/libatomic_ops
Group:      Development/Libraries
Vendor:     VMware, Inc.
Distribution:   Photon

Source0: http://www.ivmaisoft.com/_bin/atomic_ops/%{name}-%{version}.tar.gz
%define sha512 %{name}=4661445503ef4303e873559af319ad799a7eddad3df45ad602cf338c594a642ad4333a36fa91722f0d8c48acd38bbf45c60a468c7375d14824520a83c1109ec9

%description
This package provides semi-portable access to hardware-provided atomic memory update operations on a number of architectures.

%package devel
Summary:    Development files for the libatomic_ops library
Group:      Development/Libraries
Requires:   %{name} = %{version}-%{release}

%description devel
Libraries and header files for libatomic_ops library.

%prep
%autosetup -p1

%build
%configure \
    --enable-shared \
    --disable-silent-rules

make %{?_smp_mflags}

%install
%make_install %{?_smp_mflags}
find %{buildroot} -name '*.la' -delete

%check
make check %{?_smp_mflags}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%{_docdir}/libatomic_ops/COPYING
%{_docdir}/libatomic_ops/LICENSING.txt
%{_libdir}/libatomic_ops.so.*
%{_libdir}/libatomic_ops_gpl.so.*

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_docdir}/libatomic_ops/README*
%{_libdir}/libatomic_ops.a
%{_libdir}/libatomic_ops_gpl.a
%{_libdir}/libatomic_ops.so
%{_libdir}/libatomic_ops_gpl.so
%{_libdir}/pkgconfig/atomic_ops.pc

%changelog
* Sun Oct 02 2022 Shreenidhi Shedi <sshedi@vmware.com> 7.6.10-2
- Spec fixes
* Mon Jun 22 2020 Gerrit Photon <photon-checkins@vmware.com> 7.6.10-1
- Automatic Version Bump
* Thu Sep 13 2018 Siju Maliakkal <smaliakkal@vmware.com> 7.6.6-1
- Updated to latest version
* Tue Jul 26 2016 Xiaolin Li <xiaolinl@vmware.com> 7.4.4-1
- Initial build. First version
