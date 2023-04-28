Summary:    nghttp2 is an implementation of HTTP/2 and its header compression algorithm, HPACK.
Name:       nghttp2
Version:    1.41.0
Release:    4%{?dist}
License:    MIT
URL:        https://nghttp2.org
Group:      Applications/System
Vendor:     VMware, Inc.
Distribution: Photon
Source0:    https://github.com/nghttp2/nghttp2/releases/download/v%{version}/%{name}-%{version}.tar.xz
%define sha512 nghttp2=c92e8022ccc876fa311f21bc5bf5af75feff8232efb56a4b2ab198031e974d15b67c16c046188cc76552f75a1b2e7115925d6ce1e42d6f94ae482fe69727466d
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
Requires: %{name} = %{version}-%{release}

%description devel
These are the header files of nghttp2.

%prep
%autosetup -p1

%build
%configure \
    --disable-static \
    --enable-lib-only \
    --disable-python-bindings

make %{?_smp_mflags}

%install
%make_install %{?_smp_mflags}

%files
%defattr(-,root,root)
%{_libdir}/*.so.*
%{_datadir}/nghttp2
%{_docdir}/%{name}/README.rst

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%{_mandir}/man1/*

%changelog
*   Wed Apr 12 2023 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 1.41.0-4
-   Bump version as a part of libevent upgrade
*   Wed Mar 15 2023 Anmol Jain <anmolja@vmware.com> 1.41.0-3
-   Version bump up to use c-ares
*   Tue Sep 29 2020 Satya Naga Vasamsetty <svasamsetty@vmware.com> 1.41.0-2
-   openssl 1.1.1
*   Tue Jul 07 2020 Gerrit Photon <photon-checkins@vmware.com> 1.41.0-1
-   Automatic Version Bump
*   Wed Jun 24 2020 Prashant S Chauhan <psinghchauha@vmware.com> 1.33.0-2
-   Used configure macro
*   Fri Sep 7 2018 Him Kalyan Bordoloi <bordoloih@vmware.com> 1.33.0-1
-   Upgrade to version 1.33.0
*   Tue Jun 13 2017 Dheeraj Shetty <dheerajs@vmware.com> 1.23.1-1
-   First version
