Summary:        LightStep distributed tracing library for C++
Name:           lightstep-tracer-cpp
Version:        0.19
Release:        4%{?dist}
License:        MIT
URL:            https://github.com/lightstep/lightstep-tracer-cpp
Source0:        https://github.com/lightstep/lightstep-tracer-cpp/releases/download/v0_19/%{name}-%{version}.tar.gz
%define sha512  lightstep-tracer-cpp=a9f0e86843e5997e8c5d1aa05b58e7df59beea832531c78d1a42ab37087f1de4036762af03a2d3f6f461eea52503000e6822f355abcabdca04608ba99fb9a9db
Group:          Development/Tools
Vendor:         VMware, Inc.
Distribution:   Photon
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  clang-devel
BuildRequires:  c-ares
BuildRequires:  c-ares-devel
BuildRequires:  gcc
BuildRequires:  protobuf
BuildRequires:  protobuf-devel
Requires:       protobuf
Requires:       clang
Patch0:         0001-lightstep-tracer-cpp-Fix-build-issues-with-gcc-7.3.patch

%description
LightStep distributed tracing library for C++.

%prep
%autosetup -p1

%build
%configure                     \
        --disable-silent-rules  \
        --disable-static        \
        --enable-shared         \
        --disable-grpc
pushd src/c++11/envoy
protoc --cpp_out=. envoy_carrier.proto
mv envoy_carrier.pb.h ../lightstep/
mv envoy_carrier.pb.cc ../proto/
popd
pushd lightstep-tracer-common
protoc --cpp_out=. collector.proto
mv collector.pb.h ../src/c++11/lightstep/
mv collector.pb.cc ../src/c++11/proto/
popd

%install
%make_install

%files
%defattr(-,root,root)
%{_includedir}/lightstep/*.h
%{_includedir}/mapbox_variant/*.hpp
%{_libdir}/liblightstep_*

%changelog
*    Mon Sep 11 2023 Harinadh D <hdommaraju@vmware.com> 0.19-4
-    Version bump to use updated c-ares
*    Tue Jul 27 2021 Tapas Kundu <tkundu@vmware.com> 0.19-3
-    Rebuild with updated clang
*    Fri Aug 31 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 0.19-2
-    Fix build issues with gcc 7.3
*    Wed Jul 05 2017 Vinay Kulkarni <kulkarniv@vmware.com> 0.19-1
-    Initial version of lightstep-tracer-cpp package for Photon.
