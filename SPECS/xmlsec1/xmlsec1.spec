Summary:        Library providing support for "XML Signature" and "XML Encryption" standards
Name:           xmlsec1
Version:        1.2.29
Release:        6%{?dist}
License:        MIT
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon
Url:            http://www.aleksey.com/xmlsec/
Source0:        http://www.aleksey.com/xmlsec/download/%{name}-%{version}.tar.gz
%define sha512  xmlsec1=07c3012179da4392f0a9d41a51ed51d692ca8b491310488b955d5fef0637f104d3f82374754b0ef175fadc663a8ca8c996178198c5dd77b3a8b34393d1482e4d
BuildRequires: libxml2-devel
BuildRequires: libltdl-devel
BuildRequires: libxslt-devel
Requires:      libxml2
requires:      libltdl
requires:      libxslt
Requires:      nss

%description
XML Security Library is a C library based on LibXML2  and OpenSSL.
The library was created with a goal to support major XML security
standards "XML Digital Signature" and "XML Encryption".

%package devel
Summary: Libraries, includes, etc. to develop applications with XML Digital Signatures and XML Encryption support.
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: libxml2-devel
Requires: libltdl-devel
Requires: libxslt-devel

%description devel
Libraries, includes, etc. you can use to develop applications with XML Digital
Signatures and XML Encryption support.

%prep
%autosetup -p1

%build
%configure  --disable-static
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make DESTDIR=%{buildroot} install %{?_smp_mflags}

%check
make -k check %{?_smp_mflags}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-, root, root)
%{_libdir}/libxmlsec1.so.1
%{_libdir}/libxmlsec1.so.1.2.29
%{_libdir}/libxmlsec1.so
%{_libdir}/libxmlsec1-nss.so.1
%{_libdir}/libxmlsec1-nss.so.1.2.29
%{_libdir}/libxmlsec1-nss.so
%{_libdir}/libxmlsec1-openssl.so.1
%{_libdir}/libxmlsec1-openssl.so.1.2.29
%{_libdir}/libxmlsec1-openssl.so
%{_bindir}/xmlsec1

%files devel
%defattr(-, root, root)

%{_bindir}/xmlsec1-config
%{_includedir}/xmlsec1/xmlsec/*.h
%{_includedir}/xmlsec1/xmlsec/nss/*.h
%{_includedir}/xmlsec1/xmlsec/openssl/*.h
%{_libdir}/pkgconfig/xmlsec1.pc
%{_libdir}/pkgconfig/xmlsec1-nss.pc
%{_libdir}/pkgconfig/xmlsec1-openssl.pc
%{_libdir}/xmlsec1Conf.sh
%{_docdir}/xmlsec1/*
%{_datadir}/aclocal/xmlsec1.m4
%{_mandir}/man1/xmlsec1.1.gz
%{_mandir}/man1/xmlsec1-config.1.gz

%changelog
* Sun Oct 02 2022 Shreenidhi Shedi <sshedi@vmware.com> 1.2.29-6
- Remove .la files
* Sun Jun 19 2022 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 1.2.29-5
- Bump version as a part of libxslt upgrade
* Thu Nov 18 2021 Nitesh Kumar <kunitesh@vmware.com> 1.2.29-4
- Version bump up to use libxml2 2.9.11-4.
* Wed Oct 28 2020 Siju Maliakkal <smaliakkal@vmware.com> 1.2.29-3
- Added XSLT requirement
* Mon Oct 28 2019 Piyush Gupta <guptapi@vmware.com> 1.2.29-2
- Added nss as requires
* Thu Oct 17 2019 Srinidhi Rao <srinidhir@vmware.com> 1.2.29-1
- Update to version 1.2.29
* Tue Sep 25 2018 Alexey Makhalov <amakhalov@vmware.com> 1.2.26-2
- Fix requires.
* Mon Jul 02 2018 Ankit Jain <ankitja@vmware.com> 1.2.26-1
- Initial version
