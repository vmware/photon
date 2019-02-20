Summary:	Utilities for Linux CAN subsystem
Name:		can-utils
Version:	2018.02.0
Release:	1%{?dist}
License:	GPLv2
URL:		https://github.com/linux-can/can-utils
Group:		Utilities
Vendor:		VMware, Inc.
Distribution:	Photon
Source0:	https://github.com/linux-can/can-utils/archive/%{name}-%{version}.tar.gz
%define sha1 can-utils=daaccd3cf19b74bc9d257ac2aca4d0a590e01038

%description
This package provides a set of userspace utilities on top of 
Linux CAN (Controller Area Network) Protocol Family aka SocketCAN

%global debug_package %{nil}

%prep
%setup -q

%build
make %{?_smp_mflags}

%install
sed -i "s/PREFIX ?= \/usr\/local/PREFIX ?= \/usr/g" Makefile
make DESTDIR=%{buildroot} install

%files
%defattr(-,root,root)
%{_bindir}/*

%changelog
*    Thu Feb 14 2019 Him Kalyan Bordoloi <bordoloih@vmware.com> 0.8.6-1
-    Initial build added for Photon.
