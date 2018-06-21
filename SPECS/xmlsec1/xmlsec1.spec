Summary:        Library providing support for "XML Signature" and "XML Encryption" standards
Name:           xmlsec1
Version:        1.2.26
Release:        1%{?dist}
License:        MIT
Group:          Productivity/Security
Vendor:         VMware, Inc.
Distribution:   Photon
Url:            http://www.aleksey.com/xmlsec/
Source0:        http://www.aleksey.com/xmlsec/download/xmlsec1-%{version}.tar.gz
%define sha1 xmlsec1=d55d5be05eac1114e1d9b8655b602ce26f9f4a11
Requires: libxml2 >= 2.8.0
Requires: libxslt >= 1.1.0
Requires: libtool
BuildRequires: libxml2-devel >= 2.8.0
BuildRequires: libxslt-devel >= 1.1.0
BuildRequires: libltdl-devel
Prefix: %{_prefix}

%description
XML Security Library is a C library based on LibXML2  and OpenSSL. 
The library was created with a goal to support major XML security 
standards "XML Digital Signature" and "XML Encryption". 

%package devel 
Summary: Libraries, includes, etc. to develop applications with XML Digital Signatures and XML Encryption support.
Group: Development/Libraries 
Requires: xmlsec1 = %{version}
Requires: libxml2-devel >= 2.8.0
Requires: libxslt-devel >= 1.1.0
Requires: openssl-devel >= 0.9.6
Requires: zlib-devel
Requires: libtool
Requires: libltdl-devel

%description devel
Libraries, includes, etc. you can use to develop applications with XML Digital 
Signatures and XML Encryption support.

%package openssl
Summary: OpenSSL crypto plugin for XML Security Library
Group: Development/Libraries 
Requires: xmlsec1 = %{version}
Requires: libxml2 >= 2.8.0
Requires: libxslt >= 1.1.0
Requires: openssl >= 0.9.6
BuildRequires: openssl-devel >= 0.9.6
BuildRequires: libltdl-devel

%description openssl
OpenSSL plugin for XML Security Library provides OpenSSL based crypto services
for the xmlsec library

%package openssl-devel
Summary: OpenSSL crypto plugin for XML Security Library
Group: Development/Libraries 
Requires: xmlsec1 = %{version}
Requires: xmlsec1-devel = %{version}
Requires: xmlsec1-openssl = %{version}
Requires: libxml2-devel >= 2.8.0
Requires: libxslt-devel >= 1.1.0
Requires: openssl >= 0.9.6
Requires: openssl-devel >= 0.9.6
Requires: libltdl-devel

%description openssl-devel
Libraries, includes, etc. for developing XML Security applications with OpenSSL

%package nss
Summary: NSS crypto plugin for XML Security Library
Group: Development/Libraries 
Requires: xmlsec1 = %{version}
Requires: libxml2 >= 2.8.0
Requires: libxslt >= 1.1.0

%description nss
NSS plugin for XML Security Library provides NSS based crypto services
for the xmlsec library

%package nss-devel
Summary: NSS crypto plugin for XML Security Library
Group: Development/Libraries 
Requires: xmlsec1 = %{version}
Requires: xmlsec1-devel = %{version}
Requires: xmlsec1-nss = %{version}
Requires: libxml2-devel >= 2.8.0
Requires: libxslt-devel >= 1.1.0

%description nss-devel
Libraries, includes, etc. for developing XML Security applications with NSS

%prep
%setup -q

%build
./configure --prefix=%prefix --sysconfdir="/etc" --mandir=%{_mandir}
if [ "$SMP" != "" ]; then
  (make "MAKE=make -k -j $SMP"; exit 0)
  make
else
  make
fi

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/usr/bin
mkdir -p $RPM_BUILD_ROOT/usr/include/xmlsec1
mkdir -p $RPM_BUILD_ROOT/usr/lib
mkdir -p $RPM_BUILD_ROOT/usr/man/man1
make prefix=$RPM_BUILD_ROOT%{prefix} mandir=$RPM_BUILD_ROOT%{_mandir} install

%clean

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files 
%defattr(-, root, root)

%doc AUTHORS ChangeLog NEWS README Copyright
%doc %{_mandir}/man1/xmlsec1.1.gz

%{prefix}/lib/libxmlsec1.so.1
%{prefix}/lib/libxmlsec1.so.1.2.26
%{prefix}/lib/libxmlsec1.so
%{prefix}/bin/xmlsec1

%files devel
%defattr(-, root, root)  

%{prefix}/bin/xmlsec1-config
%{prefix}/include/xmlsec1/xmlsec/*.h
%{prefix}/include/xmlsec1/xmlsec/private/*.h
%{prefix}/lib/libxmlsec1.*a
%{prefix}/lib/pkgconfig/xmlsec1.pc
%{prefix}/lib/xmlsec1Conf.sh
%{prefix}/share/doc/xmlsec1/* 
%{prefix}/share/aclocal/xmlsec1.m4
%doc AUTHORS HACKING ChangeLog NEWS README Copyright
%doc %{_mandir}/man1/xmlsec1-config.1*

%files openssl
%defattr(-, root, root)  

%{prefix}/lib/libxmlsec1-openssl.so.1
%{prefix}/lib/libxmlsec1-openssl.so.1.2.26
%{prefix}/lib/libxmlsec1-openssl.so

%files openssl-devel
%defattr(-, root, root)  

%{prefix}/include/xmlsec1/xmlsec/openssl/*.h
%{prefix}/lib/libxmlsec1-openssl.la
%{prefix}/lib/libxmlsec1-openssl.a
%{prefix}/lib/pkgconfig/xmlsec1-openssl.pc

%files nss
%defattr(-, root, root)  

%{prefix}/lib/libxmlsec1-nss.so.1
%{prefix}/lib/libxmlsec1-nss.so.1.2.26
%{prefix}/lib/libxmlsec1-nss.so

%files nss-devel
%defattr(-, root, root)  

%{prefix}/include/xmlsec1/xmlsec/nss/*.h
%{prefix}/lib/libxmlsec1-nss.la
%{prefix}/lib/libxmlsec1-nss.a
%{prefix}/lib/pkgconfig/xmlsec1-nss.pc

%changelog
*   Thu Jun 21 2018 Ankit Jain <ankitja@vmware.com> 1.2.26-1
-   Initial version
