Summary:	The GnuTLS Transport Layer Security Library
Name:		gnutls
Version:	3.4.2
Release:	2%{?dist}
License:        GPLv3+ and LGPLv2+
URL:            http://www.gnutls.org
Source0:        http://ftp.heanet.ie/mirrors/ftp.gnupg.org/gcrypt/gnutls/v3.4/%{name}-%{version}.tar.xz
%define sha1 gnutls=f29b4d763aee89c860aa5c54574778537239da08
Group:		System Environment/Libraries
Vendor:		VMware, Inc.
Distribution:	Photon
BuildRequires:	nettle-devel
BuildRequires:	autogen-libopts-devel
BuildRequires:	libtasn1-devel
BuildRequires:	ca-certificates
BuildRequires:	openssl-devel
Requires:	nettle
#Requires:	autogen-libopts
Requires:	libtasn1
Requires:	openssl
Requires:	ca-certificates
Requires:	gmp
%description
GnuTLS is a secure communications library implementing the SSL, TLS and DTLS protocols and technologies around them. It provides a simple C language application programming interface (API) to access the secure communications protocols as well as APIs to parse and write X.509, PKCS #12, OpenPGP and other required structures. It is aimed to be portable and efficient with focus on security and interoperability.

%package devel
Summary:	Development libraries and header files for gnutls
Requires:	gnutls
Requires:	libtasn1-devel
Requires:	nettle-devel

%description devel
The package contains libraries and header files for
developing applications that use gnutls.

%prep
%setup -q
%build
./configure \
	--prefix=%{_prefix} \
	--without-p11-kit \
	--enable-openssl-compatibility
make %{?_smp_mflags}
%install
make DESTDIR=%{buildroot} install
rm %{buildroot}%{_infodir}/*
find %{buildroot}%{_libdir} -name '*.la' -delete

%check
make -k check |& tee %{_specdir}/%{name}-check-log || %{nocheck}
%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig
%files
%defattr(-,root,root)
%{_libdir}/*.so.*
%{_bindir}/*
%{_mandir}/man1/*
%{_mandir}/man3/*
%{_datadir}/locale/*
%files devel
%defattr(-,root,root)
%{_includedir}/%{name}/*.h
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%changelog
*   Fri Oct 9 2015 Xiaolin Li <xiaolinl@vmware.com> 3.4.2-2
-   Removing la files from packages.
*	Thu Jun 18 2015 Divya Thaluru <dthaluru@vmware.com> 3.4.2-1
-	Initial build. First version

