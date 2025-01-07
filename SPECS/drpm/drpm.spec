Name:            drpm
Summary:         A library for making, reading and applying deltarpm packages
Version:         0.5.0
Release:         7%{?dist}
License:         LGPLv2+ and BSD
URL:             https://github.com/rpm-software-management/%{name}
Vendor:          VMware, Inc.
Distribution:    Photon
Group:           System Environment/Base

Source0: https://github.com/rpm-software-management/drpm/releases/download/0.5.0/drpm-%{version}.tar.bz2
%define sha512 %{name}=9b622de94067e18e5238b67678f746632751ac03a29dd584e7cab3d024a9b9e8f7f1ee80503147614493cf4928eba183bbdc1086c71d4433996b2b9475341cdb

BuildRequires:   cmake
BuildRequires:   gcc
BuildRequires:   rpm-devel
BuildRequires:   openssl-devel
BuildRequires:   zlib-devel
BuildRequires:   bzip2-devel
BuildRequires:   xz-devel
BuildRequires:   cmocka-devel
BuildRequires:   pkg-config

Requires: rpm-libs
Requires: cmocka
Requires: openssl

%description
The drpm package provides a library for making, reading and applying deltarpms,
compatible with the original deltarpm packages.

%package devel
Summary:        C interface for the drpm library
Requires:       %{name} = %{version}-%{release}

%description devel
The drpm-devel package provides a C interface (drpm.h) for the drpm library.

%prep
%autosetup -p1 -n %{name}-%{version}

%build
%cmake \
    -DWITH_ZSTD:BOOL=yes \
    -DHAVE_LZLIB_DEVEL:BOOL=0 \
    -DCMAKE_INSTALL_LIBDIR=%{_libdir} \
    -DCMAKE_BUILD_TYPE=Debug

%cmake_build

%install
%cmake_install

%if 0%{?with_check}
%check
cd %{__cmake_builddir}
%ctest
%endif

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_libdir}/lib%{name}.so.*
%license COPYING LICENSE.BSD

%files devel
%defattr(-,root,root)
%{_libdir}/lib%{name}.so
%{_includedir}/%{name}.h
%{_libdir}/pkgconfig/%{name}.pc

%changelog
* Tue Jan 07 2025 Tapas Kundu <tapas.kundu@broadcom.com> 0.5.0-7
- Release bump for SRP
* Tue Aug 16 2022 Harinadh D <hdommaraju@vmware.com> 0.5.0-6
- Version bump to use latest zstd
* Mon Aug 01 2022 Shreenidhi Shedi <sshedi@vmware.com> 0.5.0-5
- Fix cmocka dependecy
* Wed Aug 04 2021 Satya Naga Vasamsetty <svasamsetty@vmware.com> 0.5.0-4
- Bump up release for openssl
* Fri Nov 13 2020 Prashant S Chauhan <psinghchauha@vmware.com> 0.5.0-3
- make drpm build with zstd
* Tue Sep 29 2020 Satya Naga Vasamsetty <svasamsetty@vmware.com> 0.5.0-2
- openssl 1.1.1
* Fri Jun 26 2020 Keerthana K <keerthanak@vmware.com> 0.5.0-1
- Initial package for PhotonOS.
