Summary:        C++ XML Signature and Encryption library.
Name:           xml-security-c
Version:        2.0.2
Release:        1%{?dist}
License:        Apache Software License
URL:            http://santuario.apache.org/index.html
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        http://apache.mirrors.lucidnetworks.net/santuario/c-library/%{name}-%{version}.tar.gz
%define sha1 xml-security-c=281efe6701397036af420244be26815589cec982
Requires:       openssl
Requires:       xerces-c
BuildRequires:  openssl-devel
BuildRequires:  xerces-c-devel >= 3.2
%description
XML-Security-C is the C++ XML Signature and Encryption library from the Apache Software Foundation. It is used for all XML Signature and Encryption processing in OpenSAML and Shibboleth.
%package        devel
Summary:        XML Security C library headers
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
%description    devel
This package contains development headers and static library for xml security.
%prep
%setup -q
%build
./configure --prefix=/usr
make %{?_smp_mflags}
%install
make DESTDIR=%{buildroot} install
%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig
%files 
%defattr(-,root,root)
%{_bindir}/*
%{_libdir}/*.so.*
%{_libdir}/libxml-security-c.la
%exclude %{_libdir}/pkgconfig/xml-security-c.pc
%files  devel
%defattr(-,root,root)
%{_libdir}/*.so
%{_libdir}/*.a
%{_includedir}/*
%changelog
*   Tue Mar 05 2019 Tapas Kundu <tkundu@vmware.com> 2.0.2-1
-   Update to 2.0.2
*   Wed Apr 18 2018 Xiaolin Li <xiaolinl@vmware.com> 1.7.3-3
-   Rebuild with xerces-c 3.2.1
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.7.3-2
-   GA - Bump release of all rpms
*   Wed Jan 20 2016 Anish Swaminathan <anishs@vmware.com> 1.7.3-1
-   Upgrade version.
*   Thu Nov 06 2014 Sharath George <sharathg@vmware.com> 1.5.1-1
    Initial version
