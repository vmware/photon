Summary:        Library providing support for "XML Signature" and "XML Encryption" standards
Name:           xmlsec1
Version:        1.2.30
Release:        6%{?dist}
License:        MIT
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon
Url:            http://www.aleksey.com/xmlsec/

Source0:        http://www.aleksey.com/xmlsec/download/%{name}-%{version}.tar.gz
%define sha512 xmlsec1=07152470a9fe5d077f8a358608ca1d8a79ee0d2777660f61ed5717dc640714a3adfe66843e6a4023898eb0f5ed79771d70c41132571f3a1aeda82c1894b69c98

BuildRequires: libxml2-devel
BuildRequires: libltdl-devel
BuildRequires: libxslt-devel

Requires:      libxml2
Requires:      libltdl
Requires:      libxslt
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
%configure --disable-static
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make DESTDIR=%{buildroot} install %{?_smp_mflags}

%check
make -k check |& tee %{_specdir}/%{name}-check-log || %{nocheck} %{?_smp_mflags}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-, root, root)
%{_libdir}/libxmlsec1.so.1
%{_libdir}/libxmlsec1.so.%{version}
%{_libdir}/libxmlsec1.so
%{_libdir}/libxmlsec1-nss.so.1
%{_libdir}/libxmlsec1-nss.so.%{version}
%{_libdir}/libxmlsec1-nss.so
%{_libdir}/libxmlsec1-openssl.so.1
%{_libdir}/libxmlsec1-openssl.so.%{version}
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
* Sun Oct 02 2022 Shreenidhi Shedi <sshedi@vmware.com> 1.2.30-6
- Remove .la files
* Thu Nov 18 2021 Nitesh Kumar <kunitesh@vmware.com> 1.2.30-5
- Release bump up to use libxml2 2.9.12-1.
* Wed Aug 04 2021 Satya Naga Vasamsetty <svasamsetty@vmware.com> 1.2.30-4
- Bump up release for openssl
* Wed Oct 28 2020 Siju Maliakkal <smaliakkal@vmware.com> 1.2.30-3
- Added xslt support
* Tue Sep 29 2020 Satya Naga Vasamsetty <svasamsetty@vmware.com> 1.2.30-2
- openssl 1.1.1
* Fri Aug 28 2020 Gerrit Photon <photon-checkins@vmware.com> 1.2.30-1
- Automatic Version Bump
* Tue Oct 22 2019 Piyush Gupta <guptapi@vmware.com> 1.2.26-3
- Added nss as requires
* Tue Sep 25 2018 Alexey Makhalov <amakhalov@vmware.com> 1.2.26-2
- Fix requires.
* Mon Jul 02 2018 Ankit Jain <ankitja@vmware.com> 1.2.26-1
- Initial version
