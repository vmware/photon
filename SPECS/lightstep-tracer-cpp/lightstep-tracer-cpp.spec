Summary:        LightStep distributed tracing library for C++
Name:           lightstep-tracer-cpp
Version:        0.19
Release:        2%{?dist}
License:        MIT
URL:            https://github.com/lightstep/lightstep-tracer-cpp
Source0:        https://github.com/lightstep/lightstep-tracer-cpp/releases/download/v0_19/%{name}-%{version}.tar.gz
%define sha1    lightstep-tracer-cpp=ed536c8954ad7a47d9023b9bff8070361b44d06d
Group:          Development/Tools
Vendor:         VMware, Inc.
Distribution:   Photon
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  clang
BuildRequires:  c-ares
BuildRequires:  c-ares-devel
BuildRequires:  gcc
BuildRequires:  protobuf
BuildRequires:  protobuf-devel
Requires:       protobuf

Patch0:         0001-lightstep-tracer-cpp-Fix-build-issues-with-gcc-7.3.patch

%description
LightStep distributed tracing library for C++.

%prep
%setup -q
%patch0 -p1

%build
./configure                     \
        --disable-silent-rules  \
        --prefix=%{_prefix}     \
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
make DESTDIR=%{buildroot} install
find %{buildroot} -name '*.la' -delete

%files
%defattr(-,root,root)
%{_includedir}/lightstep/*.h
%{_includedir}/mapbox_variant/*.hpp
%{_libdir}/liblightstep_*

%changelog
*    Fri Aug 31 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 0.19-2
-    Fix build issues with gcc 7.3
*    Wed Jul 05 2017 Vinay Kulkarni <kulkarniv@vmware.com> 0.19-1
-    Initial version of lightstep-tracer-cpp package for Photon.
