Summary:        Library providing support for "XML Signature" and "XML Encryption" standards
Name:           xmlsec1
Version:        1.2.26
Release:        1%{?dist}
License:        MIT
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon
Url:            http://www.aleksey.com/xmlsec/
Source0:        http://www.aleksey.com/xmlsec/download/%{name}-%{version}.tar.gz
%define sha1 xmlsec1=d55d5be05eac1114e1d9b8655b602ce26f9f4a11
BuildRequires: libxml2-devel
BuildRequires: libltdl-devel
Requires:      libxml2
Requires:      libltdl

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

%description devel
Libraries, includes, etc. you can use to develop applications with XML Digital
Signatures and XML Encryption support.

%prep
%setup -q

%build
%configure --disable-static
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make DESTDIR=%{buildroot} install

%check
make -k check |& tee %{_specdir}/%{name}-check-log || %{nocheck}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-, root, root)

%{_prefix}/lib/libxmlsec1.so.1
%{_prefix}/lib/libxmlsec1.so.1.2.26
%{_prefix}/lib/libxmlsec1.so
#%{_prefix}/lib/libxmlsec1-nss.so.1
#%{_prefix}/lib/libxmlsec1-nss.so.1.2.26
#%{_prefix}/lib/libxmlsec1-nss.so
%{_prefix}/lib/libxmlsec1-openssl.so.1
%{_prefix}/lib/libxmlsec1-openssl.so.1.2.26
%{_prefix}/lib/libxmlsec1-openssl.so
%{_prefix}/bin/xmlsec1

%files devel
%defattr(-, root, root)

%{_prefix}/bin/xmlsec1-config
%{_prefix}/include/xmlsec1/xmlsec/*.h
%{_prefix}/include/xmlsec1/xmlsec/private/*.h
#%{_prefix}/include/xmlsec1/xmlsec/nss/*.h
%{_prefix}/include/xmlsec1/xmlsec/openssl/*.h
%{_prefix}/lib/libxmlsec1.*a
#%{_prefix}/lib/libxmlsec1-nss.*a
%{_prefix}/lib/libxmlsec1-openssl.*a
%{_prefix}/lib/pkgconfig/xmlsec1.pc
#%{_prefix}/lib/pkgconfig/xmlsec1-nss.pc
%{_prefix}/lib/pkgconfig/xmlsec1-openssl.pc
%{_prefix}/lib/xmlsec1Conf.sh
%{_prefix}/share/doc/xmlsec1/*
%{_prefix}/share/aclocal/xmlsec1.m4
%{_prefix}/share/man/man1/xmlsec1.1.gz
%{_prefix}/share/man/man1/xmlsec1-config.1.gz

%changelog
*   Sun Mar 10 2019 Tapas Kundu <tkundu@vmware.com> 1.2.26-1
-   Initial version
