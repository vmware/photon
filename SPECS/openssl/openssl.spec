Summary:        Management tools and libraries relating to cryptography
Name:           openssl
Version:        3.0.16
Release:        1%{?dist}
URL:            http://www.openssl.org
Group:          System Environment/Security
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: http://www.openssl.org/source/%{name}-%{version}.tar.gz
%define sha512 %{name}=5eea2b0c60d870549fc2b8755f1220a57f870d95fbc8d5cc5abb9589f212d10945f355c3e88ff48540a7ee1c4db774b936023ca33d7c799ea82d91eef9c1c16d

Source1: rehash_ca_certificates.sh
Source2: provider_default.cnf
Source3: distro.cnf
Source4: user.cnf

Source5: jitterentropy.c

Source6: license.txt
%include %{SOURCE6}

Patch0: openssl-cnf.patch
Patch1: CVE-2023-50782.patch

%if 0%{?with_check}
BuildRequires: zlib-devel
%endif

Requires: glibc
Requires: libgcc
Requires: %{name}-libs = %{version}-%{release}

Provides: nxtgn-openssl
Obsoletes: nxtgn-openssl

%description
The OpenSSL package contains management tools and libraries relating
to cryptography. These are useful for providing cryptography
functions to other packages, such as OpenSSH, email applications and
web browsers (for accessing HTTPS sites).

%package libs
Summary: Core libraries and other files needed by openssl.
Conflicts: %{name} < 3.0.8-1
Conflicts: %{name}-fips-provider <= 3.0.8-3
Requires: bash

%description libs
%{summary}

%package devel
Summary:    Development Libraries for openssl
Group:      Development/Libraries
Requires:   %{name} = %{version}-%{release}
Provides:   nxtgn-openssl-devel
Obsoletes:  nxtgn-openssl-devel

%description devel
Header files for doing development with openssl.

%package perl
Summary:    openssl perl scripts
Group:      Applications/Internet
Requires:   perl
Requires:   %{name} = %{version}-%{release}
Provides:   nxtgn-openssl-perl
Obsoletes:  nxtgn-openssl-perl

%description perl
Perl scripts that convert certificates and keys to various formats.

%package c_rehash
Summary:    rehash script for ca certificates
Group:      Applications/Internet
Requires:   %{name} = %{version}-%{release}
Provides:   nxtgn-openssl-c_rehash
Obsoletes:  nxtgn-openssl-c_rehash

%description c_rehash
Shell scripts that convert certificates and keys to various formats.

%package docs
Summary:    openssl docs
Group:      Documentation
Requires:   %{name} = %{version}-%{release}

%description docs
The package contains openssl doc files.

%prep
%autosetup -p1

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
    --openssldir=%{_sysconfdir}/ssl \
    --api=1.1.1 \
    --shared \
    --with-rand-seed=os,egd \
    enable-egd \
    -Wl,-z,noexecstack

%make_build

%install
%make_install %{?_smp_mflags}
install -p -m 755 -D %{SOURCE1} %{buildroot}%{_bindir}
install -p -m 644 -D %{SOURCE2} %{buildroot}%{_sysconfdir}/ssl
install -p -m 644 -D %{SOURCE3} %{buildroot}%{_sysconfdir}/ssl
install -p -m 644 -D %{SOURCE4} %{buildroot}%{_sysconfdir}/ssl

fn="$(basename -s .c %{SOURCE5})"

gcc -Wall -Werror -Wextra -O2 -g -fPIC \
  -I%{buildroot}%{_includedir} \
  -lcrypto -L%{buildroot}%{_libdir} \
  -shared \
  -Wl,-e,main \
  -o %{buildroot}%{_libdir}/ossl-modules/${fn}.so \
  %{SOURCE5}

%check
%make_build tests

%ldconfig_scriptlets libs

%post libs
if [ "$1" = 2 ] && [ -s "%{_sysconfdir}/ssl/provider_fips.cnf" ]; then
  sed -i '/^#.include \/etc\/ssl\/provider_fips.cnf/s/^#//g' %{_sysconfdir}/ssl/distro.cnf
fi

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%{_bindir}/%{name}

%files libs
%defattr(-,root,root)
%{_libdir}/*.so.*
%{_libdir}/engines*/*
%{_libdir}/ossl-modules/legacy.so
%{_libdir}/ossl-modules/jitterentropy.so
%{_sysconfdir}/ssl/openssl.cnf.dist
%config(noreplace) %{_sysconfdir}/ssl/openssl.cnf
%config(noreplace) %{_sysconfdir}/ssl/user.cnf
%{_sysconfdir}/ssl/provider_default.cnf
%{_sysconfdir}/ssl/distro.cnf
%{_sysconfdir}/ssl/certs
%{_sysconfdir}/ssl/ct_log_list.cnf
%{_sysconfdir}/ssl/ct_log_list.cnf.dist
%{_sysconfdir}/ssl/private

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_mandir}/man3/*
%{_libdir}/pkgconfig/*.pc
%{_libdir}/*.a
%{_libdir}/*.so

%files perl
%defattr(-,root,root)
%{_sysconfdir}/ssl/misc/tsget
%{_sysconfdir}/ssl/misc/tsget.pl
%{_sysconfdir}/ssl/misc/CA.pl

%files c_rehash
%defattr(-,root,root)
%exclude %{_bindir}/c_rehash
%{_bindir}/rehash_ca_certificates.sh

%files docs
%defattr(-,root,root)
%{_docdir}/*
%{_mandir}/man1/*
%{_mandir}/man5/*
%{_mandir}/man7/*

%changelog
* Mon Feb 17 2025 Tapas Kundu <tapas.kundu@broadcom.com> 3.0.16-1
- Update to 3.0.16
* Mon Jan 27 2025 Alexey Makhalov <alexey.makhalov@broadcom.com> 3.0.15-7
- Jitterentropy provider (v0.3): retry recvmsg() on -EINTR and -EAGAIN
* Wed Dec 11 2024 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 3.0.15-6
- Release bump for SRP compliance
* Fri Nov 29 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 3.0.15-5
- Use syslog to log jitterentropy errors
* Thu Nov 28 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 3.0.15-4
- Optimize checking fips mode function in jitterentropy.c
* Tue Nov 19 2024 Alexey Makhalov <alexey.makhalov@broadcom.com> 3.0.15-3
- Jitterentropy provider enhancements (v0.2)
* Tue Nov 05 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 3.0.15-2
- Release bump for SRP compliance
* Tue Sep 03 2024 Tapas Kundu <tapas.kundu@broadcom.com> 3.0.15-1
- Update to 3.0.15
* Thu Aug 08 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 3.0.14-6
- Resolve openssl-libs installation issue before bash
* Wed Jul 24 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 3.0.14-5
- Move fips-provider out of openssl spec
* Mon Jul 15 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 3.0.14-4
- Improve logging in jitterentropy.c
- Add `-Wl,-e,main` to make jitterentropy shared object run like a binary
- Move jitterentropy.so to openssl-libs
* Fri Jul 05 2024 Mukul Sikka <mukul.sikka@broadcom.com> 3.0.14-3
- Fix for CVE-2024-5535
* Thu Jul 04 2024 Keerthana K <keerthana.kalyanasundaram@broadcom.com> 3.0.14-2
- Fix regression in EVP_PKEY_CTX_add1_hkdf_info()
* Tue Jun 18 2024 Mukul Sikka <mukul.sikka@broadcom.com> 3.0.14-1
- Update to openssl-3.0.14 to fix CVE-2024-4741
* Wed Apr 10 2024 Mukul Sikka <mukul.sikka@broadcom.com> 3.0.13-4
- Fix CVE-2024-2511
* Fri Mar 22 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 3.0.13-3
- Remove dead symlinks during certificate rehash
* Mon Mar 04 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 3.0.13-2
- Fix CVE-2023-50782
* Thu Feb 15 2024 Mukul Sikka <mukul.sikka@broadcom.com> 3.0.13-1
- Update to openssl-3.0.13
* Tue Jan 30 2024 Mukul Sikka <msikka@vmware.com> 3.0.9-10
- Fix for CVE-2024-0727
* Tue Dec 12 2023 Shreenidhi Shedi <sshedi@vmware.com> 3.0.9-9
- Add provides & obsoletes for nxtgn-openssl
* Fri Nov 17 2023 Mukul Sikka <msikka@vmware.com> 3.0.9-8
- Fix for CVE-2023-5678
* Mon Oct 16 2023 Srinidhi Rao <srinidhir@vmware.com> 3.0.9-7
- Fix for CVE-2023-5363
* Wed Sep 13 2023 Mukul Sikka <msikka@vmware.com> 3.0.9-6
- Fix for CVE-2023-4807
* Thu Aug 17 2023 Shreenidhi Shedi <sshedi@vmware.com> 3.0.9-5
- Re-enable fips in distro.cnf if fips is enabled
* Wed Aug 09 2023 Mukul Sikka <msikka@vmware.com> 3.0.9-4
- Fix for CVE-2023-3817
* Mon Jul 24 2023 Mukul Sikka <msikka@vmware.com> 3.0.9-3
- Fix for CVE-2023-3446
* Wed Jul 19 2023 Mukul Sikka <msikka@vmware.com> 3.0.9-2
- Fix for CVE-2023-2975
* Fri Jun 23 2023 Mukul Sikka <msikka@vmware.com> 3.0.9-1
- Update to openssl-3.0.9
* Fri Jun 16 2023 Mukul Sikka <msikka@vmware.com> 3.0.8-3
- Enable Openssl 3.0.8 fips provider
- Fix for CVE-2023-0464 and CVE-2023-0465
* Fri Apr 14 2023 Shreenidhi Shedi <sshedi@vmware.com> 3.0.8-2
- Bump version as a part of zlib upgrade
* Wed Mar 08 2023 Shreenidhi Shedi <sshedi@vmware.com> 3.0.8-1
- Add openssl-libs subpackage
- Upgrade to v3.0.8
* Tue Feb 21 2023 Shreenidhi Shedi <sshedi@vmware.com> 3.0.7-3
- Package fips certified fips.so in openssl-fips-provider
- Fix various security issues
- Use strict gcc flags while compiling jitterentropy
* Thu Jan 12 2023 Shreenidhi Shedi <sshedi@vmware.com> 3.0.7-2
- Fix openssl.cnf
- Keep default provider enabled & activated at all times
- Fix CVE-2022-3996
* Wed Nov 16 2022 Srinidhi Rao <srinidhir@vmware.com> 3.0.7-1
- Upgrade toversion 3.0.7
* Thu Jun 16 2022 Satya Naga Vasamsetty <svasamsetty@vmware.com> 3.0.3-2
- Fix CVE-2022-2068
* Wed May 04 2022 Satya Naga Vasamsetty <svasamsetty@vmware.com> 3.0.3-1
- update to openssl 3.0.3
* Wed Mar 16 2022 Satya Naga Vasamsetty <svasamsetty@vmware.com> 3.0.2-1
- update to openssl 3.0.2
* Wed Mar 09 2022 Satya Naga Vasamsetty <svasamsetty@vmware.com> 3.0.1-3
- Fix CVE-2022-0778
* Thu Jan 27 2022 Alexey Makhalov <amakhalov@vmware.com> 3.0.1-2
- Add jitterentropy provider
* Fri Jan 07 2022 Shreenidhi Shedi <sshedi@vmware.com> 3.0.1-1
- Upgrade to v3.0.1 to fix CVE-2021-4044
* Wed Nov 10 2021 Satya Naga Vasamsetty <svasamsetty@vmware.com> 3.0.0-1
- update to openssl 3.0.0
* Thu Aug 26 2021 Satya Naga Vasamsetty <svasamsetty@vmware.com> 1.1.1l-1
- update to openssl 1.1.1l
* Fri Jun 18 2021 Satya Naga Vasamsetty <svasamsetty@vmware.com> 1.1.1k-2
- use openssl rehash functionality and remove unused patches
* Mon Mar 29 2021 Satya Naga Vasamsetty <svasamsetty@vmware.com> 1.1.1k-1
- update to openssl 1.1.1k
* Tue Mar 23 2021 Tapas Kundu <tkundu@vmware.com> 1.1.1j-2
- Fix CVE-2021-3449 and CVE-2021-3450
* Thu Feb 25 2021 Satya Naga Vasamsetty <svasamsetty@vmware.com> 1.1.1j-1
- update to openssl 1.1.1j
* Mon Dec 14 2020 Satya Naga Vasamsetty <svasamsetty@vmware.com> 1.1.1i-2
- Move documents to docs sub-package
* Thu Dec 10 2020 Satya Naga Vasamsetty <svasamsetty@vmware.com> 1.1.1i-1
- Update openssl to 1.1.1i
* Thu Dec 03 2020 Satya Naga Vasamsetty <svasamsetty@vmware.com> 1.1.1g-4
- Fix CVE-2020-1971
* Tue Oct 27 2020 Satya Naga Vasamsetty <svasamsetty@vmware.com> 1.1.1g-3
- move perl dependencies to perl sub-package
* Mon Sep 28 2020 Satya Naga Vasamsetty <svasamsetty@vmware.com> 1.1.1g-2
- Add libcrypto symlinks
* Wed Jul 22 2020 Satya Naga Vasamsetty <svasamsetty@vmware.com> 1.1.1g-1
- Update to 1.1.1g
* Tue May 26 2020 Tapas Kundu <tkundu@vmware.com> 1.0.2v-1
- Update to 1.0.2v.
- Included fix for Implement blinding for scalar multiplication.
* Fri Feb 28 2020 Tapas Kundu <tkundu@vmware.com> 1.0.2u-3
- Use 2.0.20 fips
* Mon Jan 20 2020 Tapas Kundu <tkundu@vmware.com> 1.0.2u-2
- Configure with Wl flag.
* Thu Jan 09 2020 Tapas Kundu <tkundu@vmware.com> 1.0.2u-1
- Updated to 1.0.2u
- Fix CVE-2019-1551
* Fri Sep 27 2019 Alexey Makhalov <amakhalov@vmware.com> 1.0.2t-2
- Cross compilation support
* Thu Sep 19 2019 Tapas Kundu <tkundu@vmware.com> 1.0.2t-1
- Updated to 1.0.2t
- Fix multiple CVEs
* Fri Jun 07 2019 Tapas Kundu <tkundu@vmware.com> 1.0.2s-1
- Updated to 1.0.2s
* Mon Mar 25 2019 Tapas Kundu <tkundu@vmware.com> 1.0.2r-1
- Updated to 1.0.2r for CVE-2019-1559
* Fri Dec 07 2018 Sujay G <gsujay@vmware.com> 1.0.2q-1
- Bump version to 1.0.2q
* Wed Oct 17 2018 Alexey Makhalov <amakhalov@vmware.com> 1.0.2p-2
- Move fips logic to spec file
* Fri Aug 17 2018 Him Kalyan Bordoloi <bordoloih@vmware.com> 1.0.2p-1
- Upgrade to 1.0.2p
* Wed Mar 21 2018 Dheeraj Shetty <dheerajs@vmware.com> 1.0.2n-2
- Add script which rehashes the certificates
* Tue Jan 02 2018 Xiaolin Li <xiaolinl@vmware.com> 1.0.2n-1
- Upgrade to 1.0.2n
* Tue Nov 07 2017 Anish Swaminathan <anishs@vmware.com> 1.0.2m-1
- Upgrade to 1.0.2m
* Tue Oct 10 2017 Vinay Kulkarni <kulkarniv@vmware.com> 1.0.2l-2
- Fix CVE-2017-3735 OOB read.
* Fri Aug 11 2017 Anish Swaminathan <anishs@vmware.com> 1.0.2l-1
- Upgrade to 1.0.2l
* Thu Aug 10 2017 Chang Lee <changlee@vmware.com> 1.0.2k-4
- Add zlib-devel for %check
* Fri Jul 28 2017 Anish Swaminathan <anishs@vmware.com> 1.0.2k-3
- Patch to support enabling FIPS_mode through kernel parameter
* Sun Jun 04 2017 Bo Gan <ganb@vmware.com> 1.0.2k-2
- Fix symlink
* Fri Apr 07 2017 Anish Swaminathan <anishs@vmware.com> 1.0.2k-1
- Upgrade to 1.0.2k
* Wed Dec 07 2016 Xiaolin Li <xiaolinl@vmware.com> 1.0.2j-3
- Moved man3 to devel subpackage.
* Wed Oct 05 2016 ChangLee <changlee@vmware.com> 1.0.2j-2
- Modified %check
* Mon Sep 26 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.0.2j-1
- Update to 1.0.2.j
* Wed Sep 21 2016 Kumar Kaushik <kaushikk@vmware.com> 1.0.2h-5
- Security bug fix, CVE-2016-2182.
* Tue Sep 20 2016 Kumar Kaushik <kaushikk@vmware.com> 1.0.2h-4
- Security bug fix, CVE-2016-6303.
* Wed Jun 22 2016 Anish Swaminathan <anishs@vmware.com> 1.0.2h-3
- Add patches for using openssl_init under all initialization and changing default RAND
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.0.2h-2
- GA - Bump release of all rpms
* Fri May 20 2016 Divya Thaluru <dthaluru@vmware.com> 1.0.2h-1
- Upgrade to 1.0.2h
* Mon Mar 07 2016 Anish Swaminathan <anishs@vmware.com> 1.0.2g-1
- Upgrade to 1.0.2g
* Wed Feb 03 2016 Xiaolin Li <xiaolinl@vmware.com> 1.0.2f-1
- Update to version 1.0.2f
* Mon Feb 01 2016 Anish Swaminathan <anishs@vmware.com> 1.0.2e-3
- Add symlink for libcrypto
* Fri Jan 15 2016 Xiaolin Li <xiaolinl@vmware.com> 1.0.2e-2
- Move c_rehash to a seperate subpackage.
* Fri Dec 04 2015 Xiaolin Li <xiaolinl@vmware.com> 1.0.2e-1
- Update to 1.0.2e.
* Wed Dec 02 2015 Anish Swaminathan <anishs@vmware.com> 1.0.2d-3
- Follow similar logging to previous openssl versions for c_rehash.
* Fri Aug 07 2015 Sharath George <sharathg@vmware.com> 1.0.2d-2
- Split perl scripts to a different package.
* Fri Jul 24 2015 Chang Lee <changlee@vmware.com> 1.0.2d-1
- Update new version.
* Wed Mar 25 2015 Divya Thaluru <dthaluru@vmware.com> 1.0.2a-1
- Initial build.  First version
