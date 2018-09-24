Summary:        Management tools and libraries relating to cryptography
Name:           openssl
Version:        1.0.2p
Release:        2%{?dist}
License:        OpenSSL
URL:            http://www.openssl.org
Group:          System Environment/Security
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        http://www.openssl.org/source/%{name}-%{version}.tar.gz
%define sha1    openssl=f34b5322e92415755c7d58bf5d0d5cf37666382c
Source1:        rehash_ca_certificates.sh
Patch0:         c_rehash.patch
Patch1:         openssl-ipv6apps.patch
Patch2:         openssl-init-conslidate.patch
Patch3:         openssl-drbg-default-read-system-fips.patch
%if %{with_check}
BuildRequires: zlib-devel
%endif
Requires:       bash glibc libgcc

%description
The OpenSSL package contains management tools and libraries relating
to cryptography. These are useful for providing cryptography
functions to other packages, such as OpenSSH, email applications and
web browsers (for accessing HTTPS sites).

%package devel
Summary: Development Libraries for openssl
Group: Development/Libraries
Requires: openssl = %{version}-%{release}
%description devel
Header files for doing development with openssl.

%package perl
Summary: openssl perl scripts
Group: Applications/Internet
Requires: perl >= 5.28.0
Requires: openssl = %{version}-%{release}
%description perl
Perl scripts that convert certificates and keys to various formats.

%package c_rehash
Summary: openssl perl scripts
Group: Applications/Internet
Requires: perl >= 5.28.0
Requires: perl-DBI
Requires: perl-DBIx-Simple
Requires: perl-DBD-SQLite
Requires: openssl = %{version}-%{release}
%description c_rehash
Perl scripts that convert certificates and keys to various formats.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
export CFLAGS="%{optflags}"
BUILD_PREFIX=%{_prefix}
./config \
    --prefix=$BUILD_PREFIX \
    --libdir=lib \
    --openssldir=/%{_sysconfdir}/ssl \
    shared \
    zlib-dynamic \
    %{?_with_fips} \
    -Wa,--noexecstack "${CFLAGS}" "${LDFLAGS}"
# does not support -j yet
make
%install
[ %{buildroot} != "/"] && rm -rf %{buildroot}/*
make INSTALL_PREFIX=%{buildroot} MANDIR=/usr/share/man MANSUFFIX=ssl install
install -p -m 755 -D %{SOURCE1} %{buildroot}%{_bindir}/
ln -sf libssl.so.1.0.0 %{buildroot}%{_libdir}/libssl.so.1.0.2
ln -sf libcrypto.so.1.0.0 %{buildroot}%{_libdir}/libcrypto.so.1.0.2

%check
make tests

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig
%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%{_sysconfdir}/ssl/certs
%{_sysconfdir}/ssl/misc/CA.sh
%{_sysconfdir}/ssl/misc/c_hash
%{_sysconfdir}/ssl/misc/c_info
%{_sysconfdir}/ssl/misc/c_issuer
%{_sysconfdir}/ssl/misc/c_name
%{_sysconfdir}/ssl/openssl.cnf
%{_sysconfdir}/ssl/private
%{_bindir}/openssl
%{_libdir}/*.so.*
%{_libdir}/engines/*
%{_mandir}/man1/*
%{_mandir}/man5/*
%{_mandir}/man7/*

%files devel
%{_includedir}/*
%{_mandir}/man3/*
%{_libdir}/pkgconfig/*.pc
%{_libdir}/*.a
%{_libdir}/*.so

%files perl
/%{_sysconfdir}/ssl/misc/tsget
/%{_sysconfdir}/ssl/misc/CA.pl

%files c_rehash
/%{_bindir}/c_rehash
/%{_bindir}/rehash_ca_certificates.sh

%changelog
*   Fri Sep 21 2018 Dweep Advani <dadvani@vmware.com> 1.0.2p-2
-   Consuming perl version upgrade of 5.28.0
*   Fri Aug 17 2018 Him Kalyan Bordoloi <bordoloih@vmware.com> 1.0.2p-1
-   Upgrade to 1.0.2p
*   Wed Mar 21 2018 Dheeraj Shetty <dheerajs@vmware.com> 1.0.2n-2
-   Add script which rehashes the certificates
*   Tue Jan 02 2018 Xiaolin Li <xiaolinl@vmware.com> 1.0.2n-1
-   Upgrade to 1.0.2n
*   Tue Nov 07 2017 Anish Swaminathan <anishs@vmware.com> 1.0.2m-1
-   Upgrade to 1.0.2m
*   Tue Oct 10 2017 Vinay Kulkarni <kulkarniv@vmware.com> 1.0.2l-2
-   Fix CVE-2017-3735 OOB read.
*   Fri Aug 11 2017 Anish Swaminathan <anishs@vmware.com> 1.0.2l-1
-   Upgrade to 1.0.2l
*   Thu Aug 10 2017 Chang Lee <changlee@vmware.com> 1.0.2k-4
-   Add zlib-devel for %check
*   Fri Jul 28 2017 Anish Swaminathan <anishs@vmware.com> 1.0.2k-3
-   Patch to support enabling FIPS_mode through kernel parameter
*   Sun Jun 04 2017 Bo Gan <ganb@vmware.com> 1.0.2k-2
-   Fix symlink
*   Fri Apr 07 2017 Anish Swaminathan <anishs@vmware.com> 1.0.2k-1
-   Upgrade to 1.0.2k
*   Wed Dec 07 2016 Xiaolin Li <xiaolinl@vmware.com> 1.0.2j-3
-   Moved man3 to devel subpackage.
*   Wed Oct 05 2016 ChangLee <changlee@vmware.com> 1.0.2j-2
-   Modified %check
*   Mon Sep 26 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.0.2j-1
-   Update to 1.0.2.j
*   Wed Sep 21 2016 Kumar Kaushik <kaushikk@vmware.com> 1.0.2h-5
-   Security bug fix, CVE-2016-2182.
*   Tue Sep 20 2016 Kumar Kaushik <kaushikk@vmware.com> 1.0.2h-4
-   Security bug fix, CVE-2016-6303.
*   Wed Jun 22 2016 Anish Swaminathan <anishs@vmware.com> 1.0.2h-3
-   Add patches for using openssl_init under all initialization and changing default RAND
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.0.2h-2
-   GA - Bump release of all rpms
*   Fri May 20 2016 Divya Thaluru <dthaluru@vmware.com> 1.0.2h-1
-   Upgrade to 1.0.2h
*   Mon Mar 07 2016 Anish Swaminathan <anishs@vmware.com> 1.0.2g-1
-   Upgrade to 1.0.2g
*   Wed Feb 03 2016 Xiaolin Li <xiaolinl@vmware.com> 1.0.2f-1
-   Update to version 1.0.2f
*   Mon Feb 01 2016 Anish Swaminathan <anishs@vmware.com> 1.0.2e-3
-   Add symlink for libcrypto
*   Fri Jan 15 2016 Xiaolin Li <xiaolinl@vmware.com> 1.0.2e-2
-   Move c_rehash to a seperate subpackage.
*   Fri Dec 04 2015 Xiaolin Li <xiaolinl@vmware.com> 1.0.2e-1
-   Update to 1.0.2e.
*   Wed Dec 02 2015 Anish Swaminathan <anishs@vmware.com> 1.0.2d-3
-   Follow similar logging to previous openssl versions for c_rehash.
*   Fri Aug 07 2015 Sharath George <sharathg@vmware.com> 1.0.2d-2
-   Split perl scripts to a different package.
*   Fri Jul 24 2015 Chang Lee <changlee@vmware.com> 1.0.2d-1
-   Update new version.
*   Wed Mar 25 2015 Divya Thaluru <dthaluru@vmware.com> 1.0.2a-1
-   Initial build.  First version
