%define re2_ver 2022-06-01
%define abseil_ver 20220623.1
%define envoy_api_commit 9c42588c956220b48eb3099d186487c2f04d32ec
%define opencensus_proto_version 0.3.0
%define googleapis_commit 2f9af297c84c55c8b871ba4495e01ade42476c92
%define xds_commit cb28da3451f158a947dfc45090fe92b07b243bc1

Summary:        Google RPC
Name:           grpc
Version:        1.48.1
Release:        2%{?dist}
License:        Apache License, Version 2.0
URL:            https://grpc.io
Group:          Development/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        https://github.com/grpc/grpc/archive/%{name}-%{version}.tar.gz
%define sha512  %{name}=593bff5b264023733d3bd5050a8b8d4e4258ea84b27bca31f271e139da24a2af5bb261e187208606b91227c8b602a329c66fb3c13bc05b0ad31cd9c48face948

Source1:        https://github.com/google/re2/archive/re2-%{re2_ver}.tar.gz
%define sha512  re2=f3d5f2a3aa5eda74bc8f434d7b000eed8e107c894307a889466a4cb16a15b352a0332e10d80ed603c9e2e38bbcbdf11f15b6953cbdf461cc9fb0560e89a8ceb8

Source2:        https://github.com/abseil/abseil-cpp/archive/abseil-cpp-%{abseil_ver}.tar.gz
%define sha512  abseil=ab4fccd9a2bfa0c5ad4b56c8e8f8b7ec7a8eca8b6cc6959802acadd1da785e1feb078c6ac621808cd699c82717a9e637dc426d94b70a8db7f2a807059d41cbc2

Source3:        https://github.com/envoyproxy/data-plane-api/archive/%{envoy_api_commit}/data-plane-api-%{envoy_api_commit}.tar.gz
%define sha512  data-plane-api=9b1ceff5d018e70b36e02aa1b583f5495b0eb92506055bf6913d2e7ef401d3602cba8723efbc178ee31fdef9aba510fc2284612ebe22a24b5b4a703f07099897

Source4:        https://github.com/googleapis/googleapis/archive/%{googleapis_commit}/googleapis-%{googleapis_commit}.tar.gz
%define sha512  googleapis=cdeefae807df7097174b4bb28c0900b06a68d424c00ebba4ff5add260c9c651351d5e429bfc5de42f95ebb75dadec313f7bd3991c2fa476c9104f9ea656acad4

Source5:        https://github.com/census-instrumentation/opencensus-proto/archive/v%{opencensus_proto_version}/opencensus-proto-%{opencensus_proto_version}.tar.gz
%define sha512  opencensus-proto=39231a495dfdccfc8267d1e6af2ac624feea611a8691c10ec570de2194b352e4a9c3b0ce1606414fb98e5d77c66873bed4a9e56512efa12b267b8a91e0c5851e

Source6:        https://github.com/cncf/xds/archive/%{xds_commit}/xds-%{xds_commit}.tar.gz
%define sha512  xds=eb5878764503872c18b8750b20e2c2e2224e73d9601197752cea7e1e4171899474ad4f39aacc80d6c1b57a50b2161d39f219df64ffb250d045af482dae01ea79

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
%setup -q -T -D -b 1 -b 2 -b 3 -b 4 -b 5 -b 6
# Overwrite third party sources
rm -r %{_builddir}/%{name}-%{version}/third_party/{envoy-api,googleapis,opencensus-proto,xds}
mv %{_builddir}/data-plane-api-%{envoy_api_commit} %{_builddir}/%{name}-%{version}/third_party/envoy-api
mv %{_builddir}/googleapis-%{googleapis_commit} %{_builddir}/%{name}-%{version}/third_party/googleapis
mv %{_builddir}/opencensus-proto-%{opencensus_proto_version} %{_builddir}/%{name}-%{version}/third_party/opencensus-proto
mv %{_builddir}/xds-%{xds_commit} %{_builddir}/%{name}-%{version}/third_party/xds

%build
%cmake \
      -DBUILD_SHARED_LIBS=ON \
      -DABSL_PROPAGATE_CXX_STD=ON \
      -DgRPC_BUILD_TESTS=OFF \
      -DgRPC_ZLIB_PROVIDER=package \
      -DgRPC_SSL_PROVIDER=package \
      -DgRPC_PROTOBUF_PROVIDER=package \
      -DgRPC_CARES_PROVIDER=package \
      -DABSL_ROOT_DIR=%{_builddir}/abseil-cpp-%{abseil_ver} \
      -DRE2_ROOT_DIR=%{_builddir}/re2-%{re2_ver} \
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
