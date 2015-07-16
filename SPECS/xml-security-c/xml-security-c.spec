Summary:	C++ XML Signature and Encryption library.
Name:		xml-security-c
Version:	1.5.1
Release:	1%{?dist}
License:	Apache Software License
URL:		http://pkgs.fedoraproject.org/repo/pkgs/xml-security-c/xml-security-c-1.5.1.tar.gz/2c47c4ec12e8d6abe967aa5e5e99000c/xml-security-c-1.5.1.tar.gz
Group:		Applications/System
Vendor:		VMware, Inc.
Distribution:	Photon
Source0:	http://pkgs.fedoraproject.org/repo/pkgs/xml-security-c/xml-security-c-1.5.1.tar.gz/2c47c4ec12e8d6abe967aa5e5e99000c/%{name}-%{version}.tar.gz
%define sha1 xml-security-c=e51d3dca7f32cfcc2090d4d20cf8a1d032d95d79
Requires:	openssl
Requires:	xerces-c
BuildRequires:	openssl-devel
BuildRequires: 	xerces-c-devel >= 3.1
%description
XML-Security-C is the C++ XML Signature and Encryption library from the Apache Software Foundation. It is used for all XML Signature and Encryption processing in OpenSAML and Shibboleth.
%package	devel
Summary:	XML Security C library headers
Group:         	Development/Libraries
Requires:       %{name} = %{version}-%{release}
%description	devel
This package contains development headers and static library for xml security.
%prep
%setup -q
%build
./configure --prefix=/usr
make %{?_smp_mflags}
%install
make DESTDIR=%{buildroot} install
%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig
%files 
%defattr(-,root,root)
%{_bindir}/*
%{_libdir}/*.so.*
%files	devel
%defattr(-,root,root)
%{_libdir}/*.so
%{_libdir}/*.a
%{_libdir}/*.la
%{_includedir}/*
%changelog
*	Thu Nov 06 2014 Sharath George <sharathg@vmware.com> 1.5.1
	Initial version
