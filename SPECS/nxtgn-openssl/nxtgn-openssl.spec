Summary:        Management tools and libraries relating to cryptography
Name:           nxtgn-openssl
Version:        1.1.1j
Release:        2%{?dist}
License:        OpenSSL
URL:            http://www.openssl.org
Group:          System Environment/Security
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        http://www.openssl.org/source/openssl-%{version}.tar.gz
%define sha1    openssl=04c340b086828eecff9df06dceff196790bb9268
Source1:        nxtgn-rehash_ca_certificates.sh
Patch0:         nxtgn-c_rehash.patch
Patch1:         nxtgn-openssl-CVE-2021-3449.patch
Patch2:         nxtgn-openssl-CVE-2021-3450.patch
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
Summary: Development Libraries for nxtgn-openssl
Group: Development/Libraries
Requires: nxtgn-openssl = %{version}-%{release}
Obsoletes:  openssl-devel
%description devel
Header files for doing development with openssl.

%package perl
Summary: nxtgn openssl perl scripts
Group: Applications/Internet
Requires: perl
Requires: nxtgn-openssl = %{version}-%{release}
%description perl
Perl scripts that convert certificates and keys to various formats.

%package c_rehash
Summary: nxtgn openssl perl scripts
Group: Applications/Internet
Requires: perl
Requires: perl-DBI
Requires: perl-DBIx-Simple
Requires: perl-DBD-SQLite
Requires: nxtgn-openssl = %{version}-%{release}
%description c_rehash
Perl scripts that convert certificates and keys to various formats.

%prep
%setup -q -n openssl-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
export CFLAGS="%{optflags}"
./config \
    --prefix=%{_prefix} \
    --libdir=%{_libdir} \
    --openssldir=%{_sysconfdir}/nxtgn-openssl \
    --shared \
# does not support -j yet
make
%install
[ %{buildroot} != "/" ] && rm -rf %{buildroot}/*
make DESTDIR=%{buildroot} MANDIR=/usr/share/man MANSUFFIX=nxtgn-openssl install
install -p -m 755 -D %{SOURCE1} %{buildroot}%{_bindir}/

mv %{buildroot}/%{_bindir}/openssl %{buildroot}/%{_bindir}/nxtgn-openssl
mv %{buildroot}/%{_bindir}/c_rehash %{buildroot}/%{_bindir}/nxtgn-c_rehash

ln -sf libssl.so.1.1* %{buildroot}%{_libdir}/libssl.so.1.1.0
ln -sf libcrypto.so.1.1* %{buildroot}%{_libdir}/libcrypto.so.1.1.0

%check
make tests

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig
%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%{_sysconfdir}/nxtgn-openssl/certs
%{_sysconfdir}/nxtgn-openssl/ct_log_list.cnf
%{_sysconfdir}/nxtgn-openssl/ct_log_list.cnf.dist
%{_sysconfdir}/nxtgn-openssl/openssl.cnf.dist
%{_sysconfdir}/nxtgn-openssl/openssl.cnf
%{_sysconfdir}/nxtgn-openssl/private
%{_bindir}/nxtgn-openssl
%{_libdir}/libssl.so.*
%{_libdir}/libcrypto.so.*
%{_libdir}/engines*/*
%exclude %{_mandir}/man1/*
%exclude %{_mandir}/man5/*
%exclude %{_mandir}/man7/*
%exclude %{_docdir}/*

%files devel
%{_includedir}/openssl/
%exclude %{_mandir}/man3/*
%{_libdir}/pkgconfig/*.pc
%{_libdir}/libssl.a
%{_libdir}/libcrypto.a
%{_libdir}/libssl.so
%{_libdir}/libcrypto.so

%files perl
%{_sysconfdir}/nxtgn-openssl/misc/tsget
%{_sysconfdir}/nxtgn-openssl/misc/tsget.pl
%{_sysconfdir}/nxtgn-openssl/misc/CA.pl

%files c_rehash
%{_bindir}/nxtgn-c_rehash
%{_bindir}/nxtgn-rehash_ca_certificates.sh

%changelog
*   Tue Mar 23 2021 Tapas Kundu <tkundu@vmware.com> 1.1.1j-2
-   Fix CVE-2021-3449 and CVE-2021-3450
*   Thu Feb 25 2021 Satya Naga Vasamsetty <svasamsetty@vmware.com> 1.1.1j-1
-   update to openssl 1.1.1j
*   Thu Dec 10 2020 Satya Naga Vasamsetty <svasamsetty@vmware.com> 1.1.1i-1
-   Update openssl to 1.1.1i
*   Wed Dec 09 2020 Satya Naga Vasamsetty <svasamsetty@vmware.com> 1.1.1g-3
-   Fix CVE-2020-1971
*   Wed Jun 24 2020 Alexey Makhalov <amakhalov@vmware.com> 1.1.1g-2
-   Move headers to original location /usr/include/openssl
*   Tue Apr 21 2020 Srinidhi Rao <srinidhir@vmware.com> 1.1.1g-1
-   Upgrade to openssl-1.1.1g release
*   Thu Apr 16 2020 Srinidhi Rao <srinidhir@vmware.com> 1.1.1d-3
-   Fix CVE-2020-1967
*   Mon Feb 03 2020 Tapas Kundu <tkundu@vmware.com> 1.1.1d-2
-   Fix CVE-2019-1551
*   Mon Sep 30 2019 Tapas Kundu <tkundu@vmware.com> 1.1.1d-1
-   Updated to 1.1.1d
-   Fix CVE-2019-1549
*   Fri Jun 14 2019 Srinidhi Rao <srinidhir@vmware.com> 1.1.1b-1
-   Update to 1.1.1b
*   Fri Jun 07 2019 Tapas Kundu <tkundu@vmware.com> 1.0.2s-1
-   Updated to 1.0.2s
*   Fri Dec 07 2018 Sujay G <gsujay@vmware.com> 1.0.2q-1
-   Bump version to 1.0.2q
*   Wed Oct 17 2018 Alexey Makhalov <amakhalov@vmware.com> 1.0.2p-2
-   Move fips logic to spec file
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
