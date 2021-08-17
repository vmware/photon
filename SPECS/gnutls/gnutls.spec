Summary:        The GnuTLS Transport Layer Security Library
Name:           gnutls
Version:        3.7.1
Release:        3%{?dist}
License:        GPLv3+ and LGPLv2+
URL:            http://www.gnutls.org
Source0:        https://www.gnupg.org/ftp/gcrypt/gnutls/v3.7/%{name}-%{version}.tar.xz
%define sha1    gnutls=5de5d25534ee5910ea9ee6aaeeb6af1af4350c1e
Group:          System Environment/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon

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
GnuTLS is a secure communications library implementing the SSL, TLS and DTLS protocols and technologies around them.
It provides a simple C language application programming interface (API) to access the secure communications protocols as well as APIs to parse and write X.509,
PKCS #12, OpenPGP and other required structures. It is aimed to be portable and efficient with focus on security and interoperability.

%package devel
Summary:    Development libraries and header files for gnutls
Requires:   gnutls
Requires:   libtasn1-devel
Requires:   nettle-devel

%description devel
The package contains libraries and header files for
developing applications that use gnutls.

%prep
%autosetup -p1

%build
# check for trust store file presence
[ -f %{_sysconfdir}/pki/tls/certs/ca-bundle.crt ] || exit 1
%configure \
    --without-p11-kit \
    --disable-openssl-compatibility \
    --with-included-unistring \
    --with-system-priority-file=%{_sysconfdir}/gnutls/default-priorities \
    --with-default-trust-store-file=%{_sysconfdir}/pki/tls/certs/ca-bundle.crt

make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install %{?_smp_mflags}
rm %{buildroot}%{_infodir}/*
find %{buildroot}%{_libdir} -name '*.la' -delete
mkdir -p %{buildroot}/etc/%{name}
chmod 755 %{buildroot}/etc/%{name}
cat > %{buildroot}/etc/%{name}/default-priorities << "EOF"
SYSTEM=NONE:!VERS-SSL3.0:!VERS-TLS1.0:+VERS-TLS1.1:+VERS-TLS1.2:+AES-128-CBC:+RSA:+SHA1:+COMP-NULL
EOF

%check
sed -i 's/&&/||/' ./tests/system-override-default-priority-string.sh
make check %{?_smp_mflags}

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
%{_libdir}/guile/2.2/extensions/*.so*
%{_libdir}/guile/2.2/site-ccache/gnutls*
%{_datadir}/guile/site/2.2/gnutls*
%config(noreplace) %{_sysconfdir}/gnutls/default-priorities

%files devel
%defattr(-,root,root)
%{_includedir}/%{name}/*.h
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%{_mandir}/man3/*

%changelog
*   Tue Aug 17 2021 Shreenidhi Shedi <sshedi@vmware.com> 3.7.1-3
-   Bump version as a part of nettle upgrade
*   Tue Apr 13 2021 Gerrit Photon <photon-checkins@vmware.com> 3.7.1-2
-   Update gnutls with guile 2.2.7
*   Tue Apr 13 2021 Gerrit Photon <photon-checkins@vmware.com> 3.7.1-1
-   Automatic Version Bump
*   Tue Oct 06 2020 Prashant S Chauhan <psinghchauha@vmware.com> 3.6.15-3
-   Fix make check
*   Tue Sep 29 2020 Satya Naga Vasamsetty <svasamsetty@vmware.com> 3.6.15-2
-   openssl 1.1.1
*   Wed Sep 09 2020 Gerrit Photon <photon-checkins@vmware.com> 3.6.15-1
-   Automatic Version Bump
*   Wed Aug 19 2020 Shreenidhi Shedi <sshedi@vmware.com> 3.6.13-3
-   Bump version as a part of nettle-3.6 upgrade
*   Wed Jul 22 2020 Tapas Kundu <tkundu@vmware.com> 3.6.13-2
-   Bump to build with latest libffi
*   Fri Apr 10 2020 Tapas Kundu <tkundu@vmware.com> 3.6.13-1
-   Update to 3.6.13
-   Fix CVE-2020-11501
*   Thu Oct 24 2019 Shreenidhi Shedi <sshedi@vmware.com> 3.6.9-2
-   Added default priority patch.
*   Thu Oct 17 2019 Shreenidhi Shedi <sshedi@vmware.com> 3.6.9-1
-   Upgrade to version 3.6.9
*   Mon Apr 15 2019 Keerthana K <keerthanak@vmware.com> 3.6.3-3
-   Fix CVE-2019-3829, CVE-2019-3836
*   Wed Oct 03 2018 Tapas Kundu <tkundu@vmware.com> 3.6.3-2
-   Including default-priority in the RPM packaging.
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
