Summary:        The GnuTLS Transport Layer Security Library
Name:           gnutls
Version:        3.6.3
Release:        1%{?dist}
License:        GPLv3+ and LGPLv2+
URL:            http://www.gnutls.org
Source0:        https://www.gnupg.org/ftp/gcrypt/gnutls/v3.5/%{name}-%{version}.tar.xz
%define sha1    gnutls=ac96787a7fbd550a2b201e64c0e752821e90fed7
Group:          System Environment/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
Patch0:         gnutls_3.6.3_default_priority.patch
BuildRequires:  nettle-devel
BuildRequires:  autogen-libopts-devel
BuildRequires:  libtasn1-devel
BuildRequires:  ca-certificates
BuildRequires:  openssl-devel
BuildRequires:  guile-devel
BuildRequires:  gc-devel
Requires:       nettle
Requires:       autogen-libopts
Requires:       libtasn1
Requires:       openssl
Requires:       ca-certificates
Requires:       gmp
Requires:       guile
Requires:       gc

%description
GnuTLS is a secure communications library implementing the SSL, TLS and DTLS protocols and technologies around them. It provides a simple C language application programming interface (API) to access the secure communications protocols as well as APIs to parse and write X.509, PKCS #12, OpenPGP and other required structures. It is aimed to be portable and efficient with focus on security and interoperability.

%package devel
Summary:    Development libraries and header files for gnutls
Requires:   gnutls
Requires:   libtasn1-devel
Requires:   nettle-devel

%description devel
The package contains libraries and header files for
developing applications that use gnutls.

%prep
%setup -q
%patch0 -p1
%build
# check for trust store file presence
[ -f %{_sysconfdir}/pki/tls/certs/ca-bundle.crt ] || exit 1

./configure \
    --prefix=%{_prefix} \
    --without-p11-kit \
    --disable-openssl-compatibility \
    --with-included-unistring \
    --with-system-priority-file=%{_sysconfdir}/gnutls/default-priorities \
    --with-default-trust-store-file=%{_sysconfdir}/pki/tls/certs/ca-bundle.crt
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install
rm %{buildroot}%{_infodir}/*
find %{buildroot}%{_libdir} -name '*.la' -delete

%check
make %{?_smp_mflags} check

%post 
/sbin/ldconfig

%postun
/sbin/ldconfig

%files
%defattr(-,root,root)
%{_libdir}/*.so.*
%{_bindir}/*
%{_mandir}/man1/*
%{_datadir}/locale/*
%{_docdir}/gnutls/*.png
%{_libdir}/guile/2.0/*.so*
%{_libdir}/guile/2.0/site-ccache/gnutls*
%{_datadir}/guile/site/2.0/gnutls*

%files devel
%defattr(-,root,root)
%{_includedir}/%{name}/*.h
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%{_mandir}/man3/*

%changelog
*   Thu Sep 06 2018 Anish Swaminathan <anishs@vmware.com> 3.6.3-1
-   Update version to 3.6.3
*   Fri Feb 09 2018 Xiaolin Li <xiaolinl@vmware.com> 3.5.15-2
-   Add default_priority.patch.
*   Tue Oct 10 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 3.5.15-1
-   Update to 3.5.15. Fixes CVE-2017-7507
*   Thu Apr 13 2017 Danut Moraru <dmoraru@vmware.com> 3.5.10-1
-   Update to version 3.5.10
*   Sun Dec 18 2016 Alexey Makhalov <amakhalov@vmware.com> 3.4.11-4
-   configure to use default trust store file
*   Wed Dec 07 2016 Xiaolin Li <xiaolinl@vmware.com> 3.4.11-3
-   Moved man3 to devel subpackage.
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 3.4.11-2
-   GA - Bump release of all rpms
*   Wed Apr 27 2016 Xiaolin Li <xiaolinl@vmware.com> 3.4.11-1
-   Updated to version 3.4.11
*   Tue Feb 23 2016 Xiaolin Li <xiaolinl@vmware.com> 3.4.9-1
-   Updated to version 3.4.9
*   Thu Jan 14 2016 Xiaolin Li <xiaolinl@vmware.com> 3.4.8-1
-   Updated to version 3.4.8
*   Wed Dec 09 2015 Anish Swaminathan <anishs@vmware.com> 3.4.2-3
-   Edit post script.
*   Fri Oct 9 2015 Xiaolin Li <xiaolinl@vmware.com> 3.4.2-2
-   Removing la files from packages.
*   Thu Jun 18 2015 Divya Thaluru <dthaluru@vmware.com> 3.4.2-1
-   Initial build. First version

