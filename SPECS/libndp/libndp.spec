Summary:      Library for Neighbor Discovery Protocol
Name:         libndp
Version:      1.8
Release:      3%{?dist}
URL:          http://www.libndp.org/
Source0:       http://www.libndp.org/files/%{name}-%{version}.tar.gz
Group:        System Environment/Libraries
Vendor:       VMware, Inc.
Distribution: Photon

Source1: license.txt
%include %{SOURCE1}

Patch0: CVE-2024-5564.patch

%description
This package contains a library which provides a wrapper
for IPv6 Neighbor Discovery Protocol.  It also provides a tool
named ndptool for sending and receiving NDP messages.

%package devel
Summary:    Libraries and header files for libndp
Requires:   libndp

%description devel
Headers and libraries for the libndp.

%prep
%autosetup -p1

%build
./autogen.sh
%configure --disable-static
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install %{?_smp_mflags}
find %{buildroot} -name \*.la -delete

%ldconfig_scriptlets

%files
%{_bindir}/ndptool
%{_libdir}/*.so.*
%{_mandir}/man8/ndptool.8*

%files devel
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc

%changelog
*   Wed Dec 11 2024 Mukul Sikka <mukul.sikka@broadcom.com> 1.8-3
-   Release bump for SRP compliance
*   Wed Jun 19 2024 Brennan Lamoreaux <brennan.lamoreaux@broadcom.com> 1.8-2
-   Fix CVE-2024-5564
*   Wed Aug 04 2021 Susant Sahani <ssahani@vmware.com> 1.8-1
-   Update to 1.8
*   Thu Sep 13 2018 Bo Gan <ganb@vmware.com> 1.7-1
-   Update to 1.7
*   Mon Nov 28 2016 Alexey Makhalov <amakhalov@vmware.com> 1.6-1
-   Update to 1.6 to fix CVE-2016-3698
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.5-2
-   GA - Bump release of all rpms
*   Tue Jun 23 2015 Divya Thaluru <dthaluru@vmware.com> 1.5-1
-   Initial build.
