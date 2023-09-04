Summary:        Google RPC
Name:           grpc
Version:        1.15.1
Release:        3%{?dist}
License:        Apache License, Version 2.0
URL:            https://grpc.io
Group:          Development/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://github.com/grpc/grpc/archive/%{name}-%{version}.tar.gz
%define sha512  grpc=c34313abede4993119e69e8aacaf7d700cc54d2a1844ade75a087848ea78777a530628328c198ab06c8a0247afa322092f21fcc7eeddf86f599687950cb3f8dd
Patch0:         grpc-CVE-2020-7768.patch
BuildRequires:  build-essential
BuildRequires:  which
BuildRequires:  c-ares-devel
BuildRequires:  zlib-devel
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
%autosetup -p1

%build
make  %{_smp_mflags} prefix=%{_prefix} libdir=%{_libdir}

%install
make install prefix=%{buildroot}%{_prefix} libdir=%{buildroot}%{_libdir} %{_smp_mflags}
ln -sf libgrpc++.so.6 %{buildroot}%{_libdir}/libgrpc++.so.1
ln -sf libgrpc++_reflection.so.6 %{buildroot}%{_libdir}/libgrpc++_reflection.so.1
ln -sf libgrpc++_unsecure.so.6 %{buildroot}%{_libdir}/libgrpc++_unsecure.so.1
ln -sf libgrpc++_error_details.so.6 %{buildroot}%{_libdir}/libgrpc++_error_details.so.1

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%{_bindir}/*
%{_libdir}/lib*
%{_datarootdir}/%{name}

%files devel
%{_includedir}/*
%{_libdir}/pkgconfig/*

%changelog
* Mon Sep 11 2023 Harinadh D <hdommaraju@vmware.com> 1.15.1-3
- Version bump to use updated c-ares
* Tue Dec 08 2020 Dweep Advani <dadvani@vmware.com> 1.15.1-2
- Consuming fix of CVE-2020-7768 in grpc-node
* Thu Oct 04 2018 Siju Maliakkal <smaliakkal@vmware.com> 1.15.1-1
- Updated to latest version
* Tue Mar 27 2018 Dheeraj Shetty <dheerajs@vmware.com> 1.10.0-1
- initial version
