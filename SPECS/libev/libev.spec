Summary:	A full-featured and high-performance event loop
Name:		libev
Version:	4.24
Release:	1%{?dist}
License:	BSD-2-Clause
URL:		http://software.schmorp.de/pkg/libev.html
Source0:	http://dist.schmorp.de/libev/%{name}-%{version}.tar.gz
%define sha1 libev=436dd8eff00a45f8805b8cacfe4dd3bd993caedb
Group:		System/Library
Vendor:		VMware, Inc.
Distribution:	Photon
BuildRequires:  pkg-config
#BuildRequires:  openssl-devel
#Requires:       openssl

%description
A full-featured and high-performance event loop that is loosely modelled after libevent, but without its limitations and bugs.

%package        devel
Summary:        Development files for libev
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description    devel
The subpackage includes all development related headers and library for libev

%prep
%setup -q -n %{name}-%{version}

%build
%configure --disable-static
make %{?_smp_mflags}

%install
%makeinstall
find %{buildroot} -name '*.la' -delete

%check
make %{?_smp_mflags} -k check

%post -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_libdir}/*.so.*
%{_mandir}/*

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/*.so

%changelog
*	Mon Apr 03 2017 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 4.24-1
-       Initial Version.
