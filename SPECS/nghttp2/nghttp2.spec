Summary:    nghttp2 is an implementation of HTTP/2 and its header compression algorithm, HPACK.
Name:       nghttp2
Version:    1.23.1
Release:    2%{?dist}
License:    MIT
URL:        https://nghttp2.org
Group:      Applications/System
Vendor:     VMware, Inc.
Distribution: Photon
Source0:        https://github.com/nghttp2/nghttp2/releases/download/v1.23.1/%{name}-%{version}.tar.xz
%define sha1 nghttp2=80758c07d20fcde717243c1a0baf99da78693fca

Patch0:        CVE-2018-1000168.patch

BuildRequires: c-ares-devel
BuildRequires: openssl-devel
BuildRequires: systemd
BuildRequires: zlib-devel
BuildRequires: libxml2-devel
BuildRequires: libevent-devel
BuildRequires: jansson-devel

%description
Implementation of the Hypertext Transfer Protocol version 2 in C.

%package devel
Summary: Header files for nghttp2
#Requires: %{name}
Requires: %{name} = %{version}-%{release}

%description devel
These are the header files of nghttp2.

%prep
%setup -q
%patch0 -p1

%build
./configure --prefix=%{_prefix}        \
            --disable-static           \
            --enable-lib-only          \
            --disable-python-bindings 

make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install
rm %{buildroot}/%{_libdir}/*.la

%files
%defattr(-,root,root)
%{_libdir}/*.so.*
%{_datadir}/nghttp2
%{_docdir}/%{name}/*
%{_mandir}/man1/*

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc

%changelog
*   Mon Jun 18 2018 Dweep Advani <dadvani@vmware.com> 1.23.1-2
-   Fix of CVE-2018-1000168.
*   Tue Jun 13 2017 Dheeraj Shetty <dheerajs@vmware.com> 1.23.1-1
-   First version
