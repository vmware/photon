Name:            drpm
Summary:         A library for making, reading and applying deltarpm packages
Version:         0.5.2
Release:         1%{?dist}
License:         LGPLv2+ and BSD
URL:             https://github.com/rpm-software-management/%{name}
Vendor:          VMware, Inc.
Distribution:    Photon
Group:           System Environment/Base

Source0: https://github.com/rpm-software-management/drpm/releases/download/%{version}/drpm-%{version}.tar.bz2
%define sha512 %{name}=bda395d9dd34d67351cab2758a14a7fe358ee2a4b86b7b020338ef868c04f248d63cf599295087222a658710f80c80f832c5c347c5803fa3afb869249853204f

BuildRequires:   cmake
BuildRequires:   gcc
BuildRequires:   rpm-devel
BuildRequires:   openssl-devel
BuildRequires:   zlib-devel
BuildRequires:   bzip2-devel
BuildRequires:   xz-devel
BuildRequires:   cmocka-devel
BuildRequires:   pkg-config

%description
The drpm package provides a library for making, reading and applying deltarpms,
compatible with the original deltarpm packages.

%package         devel
Summary:         C interface for the drpm library
Requires:        %{name} = %{version}-%{release}

%description     devel
The drpm-devel package provides a C interface (drpm.h) for the drpm library.

%prep
%autosetup -p1

%build
%{cmake} \
    -DWITH_ZSTD:BOOL=yes \
    -DHAVE_LZLIB_DEVEL:BOOL=0 \
    -DCMAKE_INSTALL_LIBDIR=%{_libdir} \
    -DCMAKE_BUILD_TYPE=Debug

%{cmake_build}

%install
%{cmake_install}

%check
cd %{__cmake_builddir}
%{ctest}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%{_libdir}/lib%{name}.so.*
%license COPYING LICENSE.BSD

%files devel
%defattr(-,root,root)
%{_libdir}/lib%{name}.so
%{_includedir}/%{name}.h
%{_libdir}/pkgconfig/%{name}.pc

%changelog
* Sat Nov 04 2023 Shreenidhi Shedi <sshedi@vmware.com> 0.5.2-1
- Upgrade to v0.5.2
* Fri Apr 14 2023 Shreenidhi Shedi <sshedi@vmware.com> 0.5.1-6
- Bump version as a part of zlib upgrade
* Fri Jan 06 2023 Oliver Kurth <okurth@vmware.com> 0.5.1-5
- bump version as a part of xz upgrade
* Tue Jan 03 2023 Shreenidhi Shedi <sshedi@vmware.com> 0.5.1-4
- Bump version as a part of rpm upgrade
* Thu Jul 07 2022 Shreenidhi Shedi <sshedi@vmware.com> 0.5.1-3
- Bump version as a part of rpm upgrade
* Mon Jun 20 2022 Shreenidhi Shedi <sshedi@vmware.com> 0.5.1-2
- Use cmake macros for build and install
* Mon Apr 18 2022 Gerrit Photon <photon-checkins@vmware.com> 0.5.1-1
- Automatic Version Bump
* Wed Aug 04 2021 Satya Naga Vasamsetty <svasamsetty@vmware.com> 0.5.0-4
- Bump up release for openssl
* Fri Nov 13 2020 Prashant S Chauhan <psinghchauha@vmware.com> 0.5.0-3
- make drpm build with zstd
* Tue Sep 29 2020 Satya Naga Vasamsetty <svasamsetty@vmware.com> 0.5.0-2
- openssl 1.1.1
* Fri Jun 26 2020 Keerthana K <keerthanak@vmware.com> 0.5.0-1
- Initial package for PhotonOS.
