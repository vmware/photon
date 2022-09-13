%define re2_ver 2020-08-01
%define abseil_ver 20200225.2

Summary:        Google RPC
Name:           grpc
Version:        1.32.0
Release:        4%{?dist}
License:        Apache License, Version 2.0
URL:            https://grpc.io
Group:          Development/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        https://github.com/grpc/grpc/archive/%{name}-%{version}.tar.gz
%define sha512 %{name}=90136042327cea4e3680e19484f23cc00322914a7aae7987bf00b6e0901721d14c487555fdd94888192d6beb950172361ac57fbd02d43b40552f7ff5cac442ed

Source1:        https://github.com/google/re2/archive/re2-%{re2_ver}.tar.gz
%define sha512 re2=1ae261155a1eb96606788eb736faa4dc3240d85f47e3b4c412a4f85f7e4cc69f7c7cbab98397aaf725def1cbc9c5da2c679cfb5573a442d60897740766ae2967

Source2:        https://github.com/abseil/abseil-cpp/archive/abseil-cpp-%{abseil_ver}.tar.gz
%define sha512 abseil=75a607dee825e83c10dcd5e509515461f1b12c4aca861e4739ac4d41357b8e893dbfbe33873aa5c05463dde0891dedd7535af2ec59f173de29488e1b1321b335

BuildRequires:  build-essential
BuildRequires:  which
BuildRequires:  c-ares-devel
BuildRequires:  zlib-devel
BuildRequires:  cmake
BuildRequires:  gperftools-devel
BuildRequires:  protobuf-devel >= 3.6.0

Requires:       protobuf >= 3.6.0
Requires:       protobuf-c
Requires:       c-ares-devel
Requires:       zlib-devel
Requires:       openssl-devel

%description
Remote Procedure Calls (RPCs) provide a useful abstraction for building
distributed applications and services. The libraries in this repository
provide a concrete implementation of the gRPC protocol, layered over HTTP/2.
These libraries enable communication between clients and servers using and
combination of the supported languages.

%package        devel
Summary:        Development files for grpc
Group:          Development/Libraries
Requires:       grpc = %{version}-%{release}
Requires:       protobuf-devel >= 3.6.0

%description    devel
The grpc-devel package contains libraries and header files for
developing applications that use grpc.

%prep
# Using autosetup is not feasible
%setup -q
# Using autosetup is not feasible
%setup -q -T -D -a1 -a2

%build
%cmake \
      -DBUILD_SHARED_LIBS=ON \
      -DgRPC_BUILD_TESTS=OFF \
      -DgRPC_ZLIB_PROVIDER=package \
      -DgRPC_SSL_PROVIDER=package \
      -DgRPC_PROTOBUF_PROVIDER=package \
      -DgRPC_CARES_PROVIDER=package \
      -DABSL_ROOT_DIR=%{_builddir}/%{name}-%{version}/abseil-cpp-%{abseil_ver} \
      -DRE2_ROOT_DIR=%{_builddir}/%{name}-%{version}/re2-%{re2_ver} \
      -DCMAKE_INSTALL_LIBDIR=%{_libdir} \
      -DCMAKE_BUILD_TYPE=Debug

%cmake_build

%install
%cmake_install
# remove libre2 duplicates.
rm -rf %{buildroot}%{_lib64dir}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%{_bindir}/*
%{_libdir}/*.so.*
%{_datarootdir}/%{name}

%files devel
%defattr(-,root,root,-)
%{_includedir}/*
%{_libdir}/pkgconfig/*.pc
%{_libdir}/cmake/*
%{_libdir}/*.so

%changelog
* Wed Aug 04 2021 Satya Naga Vasamsetty <svasamsetty@vmware.com> 1.32.0-4
- Bump up release for openssl
* Fri Feb 19 2021 Harinadh D <hdommaraju@vmware.com> 1.32.0-3
- Version bump up to build with latest protobuf
* Tue Sep 29 2020 Satya Naga Vasamsetty <svasamsetty@vmware.com> 1.32.0-2
- openssl 1.1.1
* Wed Jul 22 2020 Gerrit Photon <photon-checkins@vmware.com> 1.32.0-1
- Automatic Version Bump
* Thu Apr 02 2020 Alexey Makhalov <amakhalov@vmware.com> 1.15.1-3
- Fix compilation issue with gcc-8.4.0
* Wed Mar 25 2020 Alexey Makhalov <amakhalov@vmware.com> 1.15.1-2
- Fix compilation issue with glibc >= 2.30.
* Thu Oct 04 2018 Siju Maliakkal <smaliakkal@vmware.com> 1.15.1-1
- Updated to latest version
* Tue Mar 27 2018 Dheeraj Shetty <dheerajs@vmware.com> 1.10.0-1
- initial version
