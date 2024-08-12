%define abseil_ver 20220623.1
%define envoy_api_commit 9c42588c956220b48eb3099d186487c2f04d32ec
%define opencensus_proto_version 0.3.0
%define googleapis_commit 2f9af297c84c55c8b871ba4495e01ade42476c92
%define xds_commit cb28da3451f158a947dfc45090fe92b07b243bc1

Summary:        Google RPC
Name:           grpc
Version:        1.59.5
Release:        1%{?dist}
License:        Apache License, Version 2.0
URL:            https://grpc.io
Group:          Development/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://github.com/grpc/grpc/archive/%{name}-%{version}.tar.gz
%define sha512 %{name}=9f35ee3185c4cbb4140b86380e97d62dc6ecd886df3ec3aa3e917dc3f1e3acf518e2a28ed143f430869508f3c853b3f3f21226d74bab42f70b99a7096e0e18af

Source1: https://github.com/envoyproxy/data-plane-api/archive/%{envoy_api_commit}/data-plane-api-%{envoy_api_commit}.tar.gz
%define sha512 data-plane-api=9b1ceff5d018e70b36e02aa1b583f5495b0eb92506055bf6913d2e7ef401d3602cba8723efbc178ee31fdef9aba510fc2284612ebe22a24b5b4a703f07099897

Source2: https://github.com/googleapis/googleapis/archive/%{googleapis_commit}/googleapis-%{googleapis_commit}.tar.gz
%define sha512 googleapis=cdeefae807df7097174b4bb28c0900b06a68d424c00ebba4ff5add260c9c651351d5e429bfc5de42f95ebb75dadec313f7bd3991c2fa476c9104f9ea656acad4

Source3: https://github.com/census-instrumentation/opencensus-proto/archive/v%{opencensus_proto_version}/opencensus-proto-%{opencensus_proto_version}.tar.gz
%define sha512 opencensus-proto=39231a495dfdccfc8267d1e6af2ac624feea611a8691c10ec570de2194b352e4a9c3b0ce1606414fb98e5d77c66873bed4a9e56512efa12b267b8a91e0c5851e

Source4: https://github.com/cncf/xds/archive/%{xds_commit}/xds-%{xds_commit}.tar.gz
%define sha512 xds=eb5878764503872c18b8750b20e2c2e2224e73d9601197752cea7e1e4171899474ad4f39aacc80d6c1b57a50b2161d39f219df64ffb250d045af482dae01ea79

BuildRequires:  build-essential
BuildRequires:  which
BuildRequires:  c-ares-devel
BuildRequires:  zlib-devel
BuildRequires:  cmake
BuildRequires:  gperftools-devel
BuildRequires:  protobuf-devel
BuildRequires:  re2-devel
BuildRequires:  abseil-cpp-devel

Requires:       protobuf >= 3.6.0
Requires:       protobuf-c
Requires:       c-ares-devel
Requires:       zlib-devel
Requires:       openssl-devel
Requires:       re2
Requires:       abseil-cpp

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
Requires:       re2-devel
Requires:       abseil-cpp-devel

%description    devel
The grpc-devel package contains libraries and header files for
developing applications that use grpc.

%prep
%autosetup -p1
# Using autosetup is not feasible
%setup -q -T -D -b 1 -b 2 -b 3 -b 4
# Overwrite third party sources
rm -r %{_builddir}/%{name}-%{version}/third_party/{envoy-api,googleapis,opencensus-proto,xds}
mv %{_builddir}/data-plane-api-%{envoy_api_commit} %{_builddir}/%{name}-%{version}/third_party/envoy-api
mv %{_builddir}/googleapis-%{googleapis_commit} %{_builddir}/%{name}-%{version}/third_party/googleapis
mv %{_builddir}/opencensus-proto-%{opencensus_proto_version} %{_builddir}/%{name}-%{version}/third_party/opencensus-proto
mv %{_builddir}/xds-%{xds_commit} %{_builddir}/%{name}-%{version}/third_party/xds

%build
%{cmake} \
      -DBUILD_SHARED_LIBS=ON \
      -DABSL_PROPAGATE_CXX_STD=ON \
      -DgRPC_BUILD_TESTS=OFF \
      -DgRPC_ZLIB_PROVIDER=package \
      -DgRPC_SSL_PROVIDER=package \
      -DgRPC_PROTOBUF_PROVIDER=package \
      -DgRPC_CARES_PROVIDER=package \
      -DgRPC_RE2_PROVIDER=package \
      -DCMAKE_INSTALL_LIBDIR=%{_libdir} \
      -DCMAKE_BUILD_TYPE=Debug

%{cmake_build}

%install
%{cmake_install}
# remove libre2 duplicates.
rm -rf %{buildroot}%{_lib64dir}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%{_bindir}/*
%{_libdir}/*.so.*
%{_datadir}/%{name}

%files devel
%defattr(-,root,root,-)
%{_includedir}/*
%{_libdir}/pkgconfig/*.pc
%{_libdir}/cmake/*
%{_libdir}/*.so

%changelog
* Mon Aug 12 2024 Mukul Sikka <mukul.sikka@broadcom.com> 1.59.5-1
- Upgrade to v1.59.5
* Wed Nov 29 2023 Shreenidhi Shedi <sshedi@vmware.com> 1.59.3-1
- Upgrade to v1.59.3
* Wed Aug 23 2023 Mukul Sikka <msikka@vmware.com> 1.54.3-1
- Updated to 1.54.3 to fix CVE-2023-33953
* Wed Jul 26 2023 Mukul Sikka <msikka@vmware.com> 1.54.2-1
- Updated to latest version
* Sat Jun 17 2023 Shreenidhi Shedi <sshedi@vmware.com> 1.48.1-4
- Bump version as a part of protobuf upgrade
* Tue Jun 06 2023 Mukul Sikka <msikka@vmware.com> 1.48.1-3
- Bump version as a part of protobuf-c
* Fri Apr 14 2023 Shreenidhi Shedi <sshedi@vmware.com> 1.48.1-2
- Bump version as a part of zlib upgrade
* Tue Aug 30 2022 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 1.48.1-1
- Updated to latest version
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
