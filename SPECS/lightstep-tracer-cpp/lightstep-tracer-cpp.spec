Summary:        LightStep distributed tracing library for C++
Name:           lightstep-tracer-cpp
Version:        0.19
Release:        7%{?dist}
License:        MIT
URL:            https://github.com/lightstep/lightstep-tracer-cpp
Group:          Development/Tools
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://github.com/lightstep/lightstep-tracer-cpp/releases/download/v0_19/%{name}-%{version}.tar.gz
%define sha512 %{name}=a9f0e86843e5997e8c5d1aa05b58e7df59beea832531c78d1a42ab37087f1de4036762af03a2d3f6f461eea52503000e6822f355abcabdca04608ba99fb9a9db

BuildRequires:  clang
BuildRequires:  c-ares-devel
BuildRequires:  protobuf-devel

Requires:       protobuf

Patch0:         0001-lightstep-tracer-cpp-Fix-build-issues-with-gcc-7.3.patch

%description
LightStep distributed tracing library for C++.

%prep
%autosetup -p1

%build
%configure \
    --disable-silent-rules \
    --disable-static \
    --enable-shared \
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

%make_build

%install
%make_install %{?_smp_mflags}

%files
%defattr(-,root,root)
%{_includedir}/lightstep/*.h
%{_includedir}/mapbox_variant/*.hpp
%{_libdir}/liblightstep_*

%changelog
* Mon Feb 24 2025 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 0.19-7
- Bump to fix libprotobuf link issue
* Thu Jun 08 2023 Shreenidhi Shedi <sshedi@vmware.com> 0.19-6
- Bump version as a part of protobuf upgrade
* Tue Nov 22 2022 Shreenidhi Shedi <sshedi@vmware.com> 0.19-5
- Bump version as a part of llvm upgrade
* Mon Mar 28 2022 Harinadh D <hdommaraju@vmware.com> 0.19-4
- Version bump up to build with protobuf 3.19.4
* Fri Feb 19 2021 Harinadh D <hdommaraju@vmware.com> 0.19-3
- Version bump up to build with latest protobuf
* Fri Aug 31 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 0.19-2
- Fix build issues with gcc 7.3
* Wed Jul 05 2017 Vinay Kulkarni <kulkarniv@vmware.com> 0.19-1
- Initial version of lightstep-tracer-cpp package for Photon.
