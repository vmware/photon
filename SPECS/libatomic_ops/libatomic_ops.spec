Summary:       Atomic memory update operations portable implementation
Name:          libatomic_ops
Version:       7.6.14
Release:       1%{?dist}
License:       GPLv2 and MIT
URL:           https://github.com/ivmai/libatomic_ops
Group:         Development/Libraries
Vendor:        VMware, Inc.
Distribution:  Photon

Source0: http://www.ivmaisoft.com/_bin/atomic_ops/libatomic_ops-%{version}.tar.gz
%define sha512 %{name}=da83886b4d766da64b27672eede40bd5787523a4c308ac7bd3f03ac831ae1a141ba21e5f5ada27bfcf811b9fb04d8a519331ea2573af036f8791958668dad851

%description
This package provides semi-portable access to hardware-provided atomic memory update operations on a number of architectures.

%package       devel
Summary:       Development files for the libatomic_ops library
Group:         Development/Libraries
Requires:      %{name} = %{version}-%{release}

%description   devel
Libraries and header files for libatomic_ops library.

%prep
%autosetup -p1

%build
%configure \
    --bindir=%{_sbindir} \
    --enable-shared \
    --disable-silent-rules

%make_build

%install
%make_install %{?_smp_mflags}
find %{buildroot} -name '*.la' -delete

%if 0%{?with_check}
%check
make check %{?_smp_mflags}
%endif

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
* Thu Sep 29 2022 Shreenidhi Shedi <sshedi@vmware.com> 7.6.14-1
- Upgrade to v7.6.14
* Mon Apr 18 2022 Gerrit Photon <photon-checkins@vmware.com> 7.6.12-1
- Automatic Version Bump
* Mon Jun 22 2020 Gerrit Photon <photon-checkins@vmware.com> 7.6.10-1
- Automatic Version Bump
* Thu Sep 13 2018 Siju Maliakkal <smaliakkal@vmware.com> 7.6.6-1
- Updated to latest version
* Tue Jul 26 2016 Xiaolin Li <xiaolinl@vmware.com> 7.4.4-1
- Initial build. First version.
