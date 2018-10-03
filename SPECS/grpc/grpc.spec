Summary:        Google RPC
Name:           grpc
Version:        1.15.1
Release:        1%{?dist}
License:        Apache License, Version 2.0
URL:            https://grpc.io
Group:          Development/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://github.com/grpc/grpc/archive/%{name}-%{version}.tar.gz
%define sha1 grpc=0c5ab74d3f64800dbf6005ec337e4291f04df438
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
%setup -q

%build
make  %{_smp_mflags} prefix=%{_prefix} libdir=%{_libdir}

%install
make install prefix=%{buildroot}%{_prefix} libdir=%{buildroot}%{_libdir}
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
* Thu Oct 04 2018 Siju Maliakkal <smaliakkal@vmware.com> 1.15.1-1
- Updated to latest version
* Tue Mar 27 2018 Dheeraj Shetty <dheerajs@vmware.com> 1.10.0-1
- initial version
