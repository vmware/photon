Summary:        Management tools and libraries relating to cryptography
Name:           openssl
Version:        1.1.1g
Release:        4%{?dist}
License:        OpenSSL
URL:            http://www.openssl.org
Group:          System Environment/Security
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        http://www.openssl.org/source/openssl-1.1.1g.tar.gz
%define sha1    openssl=18012543aface209ea2579cb628a49e22ea4ec29
Patch0:         01-DirectoryString-is-a-CHOICE-type-and-therefore-uses-explicit-tagging.patch
Patch1:         02-Correctly-compare-EdiPartyName-in-GENERAL_NAME_cmp.patch
Patch2:         03-Check-that-multi-strings-CHOICE-types-dont-use-implicit-tagging.patch
Patch3:         04-Complain-if-we-are-attempting-to-encode-with-an-invalid-ASN.1-template.patch
Patch4:         05-Add-a-test-for-GENERAL_NAME_cmp.patch
Patch5:         06-Add-a-test-for-encoding-decoding-using-an-invalid-ASN.1-template.patch
Source1:        rehash_ca_certificates.sh
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
Requires: perl
Requires: openssl = %{version}-%{release}
%description perl
Perl scripts that convert certificates and keys to various formats.

%package c_rehash
Summary: openssl perl scripts
Group: Applications/Internet
Requires: perl
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
%patch4 -p1
%patch5 -p1

%build
if [ %{_host} != %{_build} ]; then
#  export CROSS_COMPILE=%{_host}-
  export CC=%{_host}-gcc
  export AR=%{_host}-ar
  export AS=%{_host}-as
  export LD=%{_host}-ld
fi
export CFLAGS="%{optflags}"
export MACHINE=%{_arch}
./config \
    --prefix=%{_prefix} \
    --libdir=%{_libdir} \
    --openssldir=/%{_sysconfdir}/ssl \
    --shared \
    --with-rand-seed=os,egd \
    enable-egd \
    -Wl,-z,noexecstack

# does not support -j yet
make
%install
[ %{buildroot} != "/" ] && rm -rf %{buildroot}/*
make DESTDIR=%{buildroot} MANDIR=/usr/share/man MANSUFFIX=ssl install
install -p -m 755 -D %{SOURCE1} %{buildroot}%{_bindir}/

ln -sf libssl.so.1.1 %{buildroot}%{_libdir}/libssl.so.1.1.0
ln -sf libssl.so.1.1 %{buildroot}%{_libdir}/libssl.so.1.1.1
ln -sf libcrypto.so.1.1 %{buildroot}%{_libdir}/libcrypto.so.1.1.0
ln -sf libcrypto.so.1.1 %{buildroot}%{_libdir}/libcrypto.so.1.1.1

%check
make tests

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig
%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%{_sysconfdir}/ssl/certs
%{_sysconfdir}/ssl/ct_log_list.cnf
%{_sysconfdir}/ssl/ct_log_list.cnf.dist
%{_sysconfdir}/ssl/openssl.cnf.dist
%{_sysconfdir}/ssl/openssl.cnf
%{_sysconfdir}/ssl/private
%{_bindir}/openssl
%{_libdir}/*.so.*
%{_libdir}/engines*/*
%{_mandir}/man1/*
%{_mandir}/man5/*
%{_mandir}/man7/*
%{_docdir}/*

%files devel
%{_includedir}/*
%{_mandir}/man3/*
%{_libdir}/pkgconfig/*.pc
%{_libdir}/*.a
%{_libdir}/*.so

%files perl
/%{_sysconfdir}/ssl/misc/tsget
/%{_sysconfdir}/ssl/misc/tsget.pl
/%{_sysconfdir}/ssl/misc/CA.pl

%files c_rehash
/%{_bindir}/c_rehash
/%{_bindir}/rehash_ca_certificates.sh

%changelog
*   Thu Dec 03 2020 Satya Naga Vasamsetty <svasamsetty@vmware.com> 1.1.1g-4
-   Fix CVE-2020-1971
*   Tue Oct 27 2020 Satya Naga Vasamsetty <svasamsetty@vmware.com> 1.1.1g-3
-   move perl dependencies to perl sub-package
*   Mon Sep 28 2020 Satya Naga Vasamsetty <svasamsetty@vmware.com> 1.1.1g-2
-   Add libcrypto symlinks
*   Wed Jul 22 2020 Satya Naga Vasamsetty <svasamsetty@vmware.com> 1.1.1g-1
-   Update to 1.1.1g
*   Tue May 26 2020 Tapas Kundu <tkundu@vmware.com> 1.0.2v-1
-   Update to 1.0.2v.
-   Included fix for Implement blinding for scalar multiplication.
*   Fri Feb 28 2020 Tapas Kundu <tkundu@vmware.com> 1.0.2u-3
-   Use 2.0.20 fips
*   Mon Jan 20 2020 Tapas Kundu <tkundu@vmware.com> 1.0.2u-2
-   Configure with Wl flag.
*   Thu Jan 09 2020 Tapas Kundu <tkundu@vmware.com> 1.0.2u-1
-   Updated to 1.0.2u
-   Fix CVE-2019-1551
*   Fri Sep 27 2019 Alexey Makhalov <amakhalov@vmware.com> 1.0.2t-2
-   Cross compilation support
*   Thu Sep 19 2019 Tapas Kundu <tkundu@vmware.com> 1.0.2t-1
-   Updated to 1.0.2t
-   Fix multiple CVEs
*   Fri Jun 07 2019 Tapas Kundu <tkundu@vmware.com> 1.0.2s-1
-   Updated to 1.0.2s
*   Mon Mar 25 2019 Tapas Kundu <tkundu@vmware.com> 1.0.2r-1
-   Updated to 1.0.2r for CVE-2019-1559
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
