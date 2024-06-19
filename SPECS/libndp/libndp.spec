Summary:    Library for Neighbor Discovery Protocol
Name:       libndp
Version:    1.7
Release:    3%{?dist}
License:    LGPLv2+
URL:        http://www.libndp.org/
Group:      System Environment/Libraries
Vendor:     VMware, Inc.
Distribution:   Photon

Source:     http://www.libndp.org/files/%{name}-%{version}.tar.gz
%define sha512 libndp=a9a4b4cb0a9e23384fbb37b7315129d891559bb4203ddd50348d9cddbd03c7d38bd62697d7c17db52568cf06ad631fb59612fc85b8a987309de65b270bca68cd

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
%make_install %{?_smp_mflags}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_bindir}/ndptool
%{_libdir}/*.so.*
%{_mandir}/man8/ndptool.8*

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc

%changelog
* Wed Jun 19 2024 Brennan Lamoreaux <brennan.lamoreaux@broadcom.com> 1.7-3
- Fix CVE-2024-5564
* Sun Oct 02 2022 Shreenidhi Shedi <sshedi@vmware.com> 1.7-2
- Remove .la files
* Thu Sep 13 2018 Bo Gan <ganb@vmware.com> 1.7-1
- Update to 1.7
* Mon Nov 28 2016 Alexey Makhalov <amakhalov@vmware.com> 1.6-1
- Update to 1.6 to fix CVE-2016-3698
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.5-2
- GA - Bump release of all rpms
* Tue Jun 23 2015 Divya Thaluru <dthaluru@vmware.com> 1.5-1
- Initial build.
