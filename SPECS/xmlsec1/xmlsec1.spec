Summary:        Library providing support for "XML Signature" and "XML Encryption" standards
Name:           xmlsec1
Version:        1.2.33
Release:        4%{?dist}
License:        MIT
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon
Url:            http://www.aleksey.com/xmlsec

Source0: http://www.aleksey.com/xmlsec/download/%{name}-%{version}.tar.gz
%define sha512 %{name}=6354554b5cdc0a1389f6991efeac919bea912330b36d3be3d3496d61331e9edd2771786d50d2571a439f62ccfc3bd32be0a50bb5a037c4993aac076ad94b46e8

BuildRequires: libxml2-devel
BuildRequires: libltdl-devel
BuildRequires: libxslt-devel
BuildRequires: sed

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
%make_build

%install
%make_install %{?_smp_mflags}

%check
make -k check %{?_smp_mflags}

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-, root, root)
%{_libdir}/lib%{name}.so.1
%{_libdir}/lib%{name}.so.%{version}
%{_libdir}/lib%{name}-nss.so.1
%{_libdir}/lib%{name}-nss.so.%{version}
%{_libdir}/lib%{name}-openssl.so.1
%{_libdir}/lib%{name}-openssl.so.%{version}
%{_bindir}/%{name}

%files devel
%defattr(-, root, root)
%{_libdir}/lib%{name}.so
%{_libdir}/lib%{name}-nss.so
%{_libdir}/lib%{name}-openssl.so
%{_bindir}/%{name}-config
%{_includedir}/%{name}/xmlsec/*.h
%{_includedir}/%{name}/xmlsec/nss/*.h
%{_includedir}/%{name}/xmlsec/openssl/*.h
%{_libdir}/pkgconfig/%{name}.pc
%{_libdir}/pkgconfig/%{name}-nss.pc
%{_libdir}/pkgconfig/%{name}-openssl.pc
%{_libdir}/%{name}Conf.sh
%{_docdir}/%{name}/*
%{_datadir}/aclocal/%{name}.m4
%{_mandir}/man1/%{name}.1.gz
%{_mandir}/man1/%{name}-config.1.gz

%changelog
* Fri Oct 07 2022 Shreenidhi Shedi <sshedi@vmware.com> 1.2.33-4
- Bump version as a part of libxslt upgrade
* Sun Aug 07 2022 Shreenidhi Shedi <sshedi@vmware.com> 1.2.33-3
- Remove .la files
* Thu Jun 16 2022 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 1.2.33-2
- Bump version as a part of libxslt upgrade
* Tue Apr 19 2022 Gerrit Photon <photon-checkins@vmware.com> 1.2.33-1
- Automatic Version Bump
* Wed Nov 17 2021 Nitesh Kumar <kunitesh@vmware.com> 1.2.32-3
- Release bump up to use libxml2 2.9.12-1.
* Wed Aug 04 2021 Satya Naga Vasamsetty <svasamsetty@vmware.com> 1.2.32-2
- Bump up release for openssl
* Tue Apr 13 2021 Gerrit Photon <photon-checkins@vmware.com> 1.2.32-1
- Automatic Version Bump
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
