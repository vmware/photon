Summary:        LightStep distributed tracing library for C++
Name:           lightstep-tracer-cpp
Version:        0.19
Release:        1%{?dist}
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
BuildRequires:  protobuf3
BuildRequires:  protobuf3-devel
Requires:       protobuf3

%description
LightStep distributed tracing library for C++.

%package devel
Summary:        lightstep-tracer-cpp devel
Group:          Development/Tools
Requires:       %{name} = %{version}
%description devel
This contains development tools and libraries for lightstep-tracer.

%prep
%setup -q

%build
./configure                     \
        --disable-silent-rules  \
        --prefix=%{_prefix}     \
        --disable-static        \
        --enable-shared         \
        --disable-grpc

%install
make DESTDIR=%{buildroot} install
find %{buildroot} -name '*.la' -delete

%files
%defattr(-,root,root)
%{_libdir}/liblightstep_core_cxx11.so.*

%files devel
%defattr(-,root,root)
%{_includedir}/lightstep/*.h
%{_includedir}/mapbox_variant/*.hpp
%{_libdir}/liblightstep_core_cxx11.so

%changelog
*    Wed Jun 14 2017 Vinay Kulkarni <kulkarniv@vmware.com> 0.19-1
-    Initial version of lightstep-tracer-cpp package for Photon.
