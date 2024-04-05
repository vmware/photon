Summary:    nghttp2 is an implementation of HTTP/2 and its header compression algorithm, HPACK.
Name:       nghttp2
Version:    1.57.0
Release:    2%{?dist}
License:    MIT
URL:        https://nghttp2.org
Group:      Applications/System
Vendor:     VMware, Inc.
Distribution: Photon
Source0:    https://github.com/nghttp2/nghttp2/releases/download/v%{version}/%{name}-%{version}.tar.xz
%define sha512 nghttp2=d914eb48afd1ea182c1b2a454bf5e7963a7e28165f1d6d29bb83dd61a1b611c8c469e72a7a22daf23b8037f6e5ae9d4e791150b7d135746c1a5ec71ceb777f92

Patch0: CVE-2024-28182.patch

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
%autosetup -p1

%build
autoreconf -i
%configure  \
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
*   Fri Apr 05 2024 Harinadh D <harinadh.dommaraju@broadcom.com> 1.57.0-2
-   Fix for CVE-2024-28182
*   Mon Oct 23 2023 Him Kalyan Bordoloi <bordoloih@vmware.com> 1.57.0-1
-   Upgrade to version 1.57.0
*   Mon Sep 11 2023 Harinadh D <hdommaraju@vmware.com> 1.41.0-5
-   Bump version as a part of c-ares upgrade
*   Wed Apr 12 2023 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 1.41.0-4
-   Bump version as a part of libevent upgrade
*   Tue Mar 14 2023 Anmol Jain <anmolja@vmware.com> 1.41.0-3
-   Version bump up to use c-ares
*   Wed Jun 24 2020 Tapas Kundu <tkundu@vmware.com> 1.41.0-2
-   Used configure macro and removed whitespaces
*   Thu Jun 11 2020 Ashwin H <ashwinh@vmware.com> 1.41.0-1
-   Upgrade to version 1.41.0
*   Fri Sep 7 2018 Him Kalyan Bordoloi <bordoloih@vmware.com> 1.33.0-1
-   Upgrade to version 1.33.0
*   Tue Jun 13 2017 Dheeraj Shetty <dheerajs@vmware.com> 1.23.1-1
-   First version
