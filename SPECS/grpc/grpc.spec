Summary:        Google RPC
Name:           grpc
Version:        1.32.0
Release:        1%{?dist}
License:        Apache License, Version 2.0
URL:            https://grpc.io
Group:          Development/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://github.com/grpc/grpc/archive/%{name}-%{version}.tar.gz
%define sha1    grpc=5c5821d40bd1c9e73992867c260421b7b539fa7d
Source1:        https://github.com/google/re2/archive/re2-2020-08-01.tar.gz
%define sha1    re2=ac4796e631461c27cd05629097a6931c1d5b13a4
Source2:        https://github.com/abseil/abseil-cpp/archive/abseil-cpp-20200225.2.tar.gz
%define sha1    abseil=f8207455be29fa9b0fc80393f63df49a85212084
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
%setup -q
%setup -q -T -D -a1 -a2
mkdir -p cmake/build

%build
cd cmake/build
cmake ../.. \
      -DCMAKE_INSTALL_PREFIX=%{_prefix} \
      -DBUILD_SHARED_LIBS=ON \
      -DgRPC_BUILD_TESTS=OFF \
      -DgRPC_ZLIB_PROVIDER=package \
      -DgRPC_SSL_PROVIDER=package \
      -DgRPC_PROTOBUF_PROVIDER=package \
      -DgRPC_CARES_PROVIDER=package \
      -DABSL_ROOT_DIR=%{_builddir}/%{name}-%{version}/abseil-cpp-20200225.2 \
      -DRE2_ROOT_DIR=%{_builddir}/%{name}-%{version}/re2-2020-08-01
make  %{_smp_mflags} prefix=%{_prefix} libdir=%{_libdir}

%install
cd cmake/build
make DESTDIR=%{buildroot} install
# remove libre2 duplicates.
rm -rf %{buildroot}/usr/lib64

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
