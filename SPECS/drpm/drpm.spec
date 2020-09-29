Name:            drpm
Summary:         A library for making, reading and applying deltarpm packages
Version:         0.5.0
Release:         2%{?dist}
License:         LGPLv2+ and BSD
URL:             https://github.com/rpm-software-management/%{name}
Source0:         https://github.com/rpm-software-management/drpm/releases/download/0.5.0/drpm-%{version}.tar.bz2
Vendor:          VMware, Inc.
Distribution:    Photon
Group:           System Environment/Base
%define sha1     %{name}=1bef47256b0aa658c1dd5e51e04f05be40b8b360
BuildRequires:   cmake
BuildRequires:   gcc
BuildRequires:   rpm-devel
BuildRequires:   openssl-devel
BuildRequires:   zlib-devel
BuildRequires:   bzip2-devel
BuildRequires:   xz-devel
BuildRequires:   cmocka
BuildRequires:   pkg-config

%description
The drpm package provides a library for making, reading and applying deltarpms,
compatible with the original deltarpm packages.

%package devel
Summary:        C interface for the drpm library
Requires:       %{name} = %{version}-%{release}

%description devel
The drpm-devel package provides a C interface (drpm.h) for the drpm library.

%prep
%setup -q -n %{name}-%{version}
mkdir build

%build
pushd build
cmake .. -DWITH_ZSTD:BOOL=no -DHAVE_LZLIB_DEVEL:BOOL=0 -DCMAKE_INSTALL_PREFIX=/usr
make %{?_smp_mflags}
popd

%install
pushd build
make install DESTDIR=%{?buildroot}
popd

%check
pushd build
ctest -VV
popd

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%{_lib64dir}/lib%{name}.so.*
%license COPYING LICENSE.BSD

%files devel
%{_lib64dir}/lib%{name}.so
%{_includedir}/%{name}.h
%{_lib64dir}/pkgconfig/%{name}.pc

%changelog
*   Tue Sep 29 2020 Satya Naga Vasamsetty <svasamsetty@vmware.com> 0.5.0-2
-   openssl 1.1.1
*   Fri Jun 26 2020 Keerthana K <keerthanak@vmware.com> 0.5.0-1
-   Initial package for PhotonOS.
