# once certified fips-provider rpm is published, with_certified_fips switch should be turned off
# with_certified_fips & with_latest_fips can't be 1 at same time, we can have any one at a time
%define with_certified_fips     0
%define with_latest_fips        0
%define fips_provider_version   3.0.0
%define fips_provider_srcname   fips-provider-%{fips_provider_version}

Summary:        Management tools and libraries relating to cryptography
Name:           openssl
Version:        3.0.7
Release:        5%{?dist}
License:        OpenSSL
URL:            http://www.openssl.org
Group:          System Environment/Security
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: http://www.openssl.org/source/%{name}-%{version}.tar.gz
%define sha512 %{name}=6c2bcd1cd4b499e074e006150dda906980df505679d8e9d988ae93aa61ee6f8c23c0fa369e2edc1e1a743d7bec133044af11d5ed57633b631ae479feb59e3424

Source1: rehash_ca_certificates.sh
Source2: provider_default.cnf
Source3: distro.cnf
Source4: user.cnf

%if 0%{?with_certified_fips} || 0%{?with_latest_fips}
Source5: provider_fips.cnf
%endif

%if 0%{?with_check}
Source6: dsapub_noparam.der
%endif

%if 0%{?with_certified_fips}
Source7: %{fips_provider_srcname}.tar.xz
%define sha512 %{fips_provider_srcname}=bad387fd2ba43bc7395c09c6045a102edc4cc22c90d574904494260c6edb041897d0c0e7fc040b8023ec3a935988bae5e4e07c4b97c9cab8118902e1af5426df
%endif

Patch0: openssl-cnf.patch
Patch1: 0001-x509-fix-double-locking-problem.patch

# Fix for multiple security issues
Patch2: 0001-Fix-type-confusion-in-nc_match_single.patch
Patch3: 0002-Add-testcase-for-nc_match_single-type-confusion.patch

Patch4: 0001-Fix-Timing-Oracle-in-RSA-decryption.patch

Patch5: 0001-Avoid-dangling-ptrs-in-header-and-data-params-for-PE.patch
Patch6: 0002-Add-a-test-for-CVE-2022-4450.patch

Patch7: 0001-Fix-a-UAF-resulting-from-a-bug-in-BIO_new_NDEF.patch
Patch8: 0002-Check-CMS-failure-during-BIO-setup-with-stream-is-ha.patch
Patch9: 0003-squash-Fix-a-UAF-resulting-from-a-bug-in-BIO_new_NDE.patch
Patch10: 0004-fixup-Fix-a-UAF-resulting-from-a-bug-in-BIO_new_NDEF.patch

Patch11: 0001-Do-not-dereference-PKCS7-object-data-if-not-set.patch
Patch12: 0002-Add-test-for-d2i_PKCS7-NULL-dereference.patch

Patch13: 0001-Fix-NULL-deference-when-validating-FFC-public-key.patch
Patch14: 0002-Prevent-creating-DSA-and-DH-keys-without-parameters-.patch
Patch15: 0003-Do-not-create-DSA-keys-without-parameters-by-decoder.patch
Patch16: 0004-Add-test-for-DSA-pubkey-without-param-import-and-che.patch

Patch17: 0001-CVE-2023-0286-Fix-GENERAL_NAME_cmp-for-x400Address-3.patch

Patch18: 0001-pk7_doit.c-Check-return-of-BIO_set_md-calls.patch
Patch19: 0002-Add-testcase-for-missing-return-check-of-BIO_set_md-.patch

%if 0%{?with_check}
BuildRequires: zlib-devel
%endif

Requires: bash
Requires: glibc
Requires: libgcc

%description
The OpenSSL package contains management tools and libraries relating
to cryptography. These are useful for providing cryptography
functions to other packages, such as OpenSSH, email applications and
web browsers (for accessing HTTPS sites).

%package devel
Summary:    Development Libraries for openssl
Group:      Development/Libraries
Requires:   %{name} = %{version}-%{release}

%description devel
Header files for doing development with openssl.

%if 0%{?with_certified_fips} || 0%{?with_latest_fips}
%package fips-provider
Summary:    FIPS Libraries for openssl
Group:      Applications/Internet

%if 0%{?with_certified_fips}
Requires:   %{name} >= %{fips_provider_version}
%else
Requires:   %{name} = %{version}-%{release}
%endif

%description fips-provider
Fips library for enabling fips.
%endif

%package perl
Summary:    openssl perl scripts
Group:      Applications/Internet
Requires:   perl
Requires:   %{name} = %{version}-%{release}

%description perl
Perl scripts that convert certificates and keys to various formats.

%package c_rehash
Summary:    rehash script for ca certificates
Group:      Applications/Internet
Requires:   %{name} = %{version}-%{release}

%description c_rehash
Shell scripts that convert certificates and keys to various formats.

%package docs
Summary:    openssl docs
Group:      Documentation
Requires:   %{name} = %{version}-%{release}

%description docs
The package contains openssl doc files.

%prep
%if 0%{?with_certified_fips} && 0%{?with_latest_fips}
echo "ERROR: with_latest_fips and with_certified_fips both should not be enabled" 1>&2
exit 1
%endif

%if 0%{?with_certified_fips}
%autosetup -p1 -a0 -a7
%else
%autosetup -p1
%endif

%build
# rpm 4.14.x doesn't understand elif, so keep it basic
%if 0%{?with_certified_fips} || 0%{?with_latest_fips}
  %if 0%{?with_certified_fips}
    %undefine with_latest_fips
  %else
    %undefine with_certified_fips
  %endif
%else
  %undefine with_certified_fips
  %undefine with_latest_fips
%endif

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
    %{?with_latest_fips: enable-fips} \
    -Wl,-z,noexecstack

%make_build

%install
%make_install %{?_smp_mflags}

install -p -m 755 -D %{SOURCE1} %{buildroot}%{_bindir}
install -p -m 644 -D %{SOURCE2} %{buildroot}%{_sysconfdir}/ssl
install -p -m 644 -D %{SOURCE3} %{buildroot}%{_sysconfdir}/ssl
install -p -m 644 -D %{SOURCE4} %{buildroot}%{_sysconfdir}/ssl

%if 0%{?with_certified_fips} || 0%{?with_latest_fips}
install -p -m 644 -D %{SOURCE5} %{buildroot}%{_sysconfdir}/ssl
%if 0%{?with_certified_fips}
install -p -m 644 %{fips_provider_srcname}/%{_arch}/fips.so %{buildroot}%{_libdir}/ossl-modules/
%endif
%endif

%if 0%{?with_check}
%check
cp %{SOURCE6} test/recipes/91-test_pkey_check_data/
make tests %{?_smp_mflags}
%endif

%ldconfig_scriptlets

%if 0%{?with_certified_fips} || 0%{?with_latest_fips}
%post fips-provider
if [ "$1" = 2 ]; then
  # fips.so was just updated. Temporarily disable fips mode to regenerate new fipsmodule.cnf
  sed -i '/^.include \/etc\/ssl\/provider_fips.cnf/s/^/#/g' %{_sysconfdir}/ssl/distro.cnf
fi
openssl fipsinstall -out %{_sysconfdir}/ssl/fipsmodule.cnf -module %{_libdir}/ossl-modules/fips.so
sed -i '/^#.include \/etc\/ssl\/provider_fips.cnf/s/^#//g' %{_sysconfdir}/ssl/distro.cnf

%postun fips-provider
# complete uninstall, not an upgrade
if [ "$1" = 0 ]; then
  rm -f %{_sysconfdir}/ssl/fipsmodule.cnf
  sed -i '/^.include \/etc\/ssl\/provider_fips.cnf/s/^/#/g' %{_sysconfdir}/ssl/distro.cnf
fi
%endif

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%{_sysconfdir}/ssl/certs
%{_sysconfdir}/ssl/ct_log_list.cnf
%{_sysconfdir}/ssl/ct_log_list.cnf.dist
%{_sysconfdir}/ssl/%{name}.cnf.dist
%config(noreplace) %{_sysconfdir}/ssl/%{name}.cnf
%config(noreplace) %{_sysconfdir}/ssl/user.cnf
%{_sysconfdir}/ssl/provider_default.cnf
%{_sysconfdir}/ssl/distro.cnf
%{_sysconfdir}/ssl/private
%{_bindir}/%{name}
%{_libdir}/*.so.*
%{_libdir}/engines*/*
%{_libdir}/ossl-modules/legacy.so

%if 0%{?with_certified_fips} || 0%{?with_latest_fips}
%files fips-provider
%defattr(-,root,root)
%{_libdir}/ossl-modules/fips.so
%{_sysconfdir}/ssl/provider_fips.cnf

%if 0%{?with_latest_fips}
%exclude %{_sysconfdir}/ssl/fipsmodule.cnf
%endif
%endif

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
* Tue Feb 21 2023 Shreenidhi Shedi <sshedi@vmware.com> 3.0.7-5
- Package fips certified fips.so in openssl-fips-provider
* Sat Feb 04 2023 Srinidhi Rao <srinidhir@vmware.com> 3.0.7-4
- Fix for Various Security issues
* Thu Jan 12 2023 Shreenidhi Shedi <sshedi@vmware.com> 3.0.7-3
- Fix openssl.cnf
- Keep default provider enabled & activated at all times
* Wed Jan 04 2023 Srinidhi Rao <srinidhir@vmware.com> 3.0.7-2
- Fix for CVE-2022-3996
* Tue Nov 01 2022 Srinidhi Rao <srinidhir@vmware.com> 3.0.7-1
- Update to version 3.0.7
* Wed Oct 26 2022 Srinidhi Rao <srinidhir@vmware.com> 3.0.6-2
- Fix for CVE-2022-3602.
* Tue Oct 18 2022 Srinidhi Rao <srinidhir@vmware.com> 3.0.6-1
- update to openssl-3.0.6
* Mon Jul 04 2022 Satya Naga Vasamsetty <svasamsetty@vmware.com> 3.0.3-3
- Fix CVE-2022-2097
* Thu Jun 16 2022 Satya Naga Vasamsetty <svasamsetty@vmware.com> 3.0.3-2
- Fix CVE-2022-2068
* Wed May 04 2022 Satya Naga Vasamsetty <svasamsetty@vmware.com> 3.0.3-1
- update to openssl 3.0.3
* Thu Mar 17 2022 Satya Naga Vasamsetty <svasamsetty@vmware.com> 3.0.0-6
- Fix CVE-2021-4160
* Wed Mar 09 2022 Satya Naga Vasamsetty <svasamsetty@vmware.com> 3.0.0-5
- Fix CVE-2022-0778
* Tue Jan 11 2022 Piyush Gupta <gpiyush@vmware.com> 3.0.0-4
- Bump up openssl to build openssl-fips-provider.
* Fri Jan 07 2022 Shreenidhi Shedi <sshedi@vmware.com> 3.0.0-3
- Spec improvements
* Mon Jan 03 2022 Satya Naga Vasamsetty <svasamsetty@vmware.com> 3.0.0-2
- Fix CVE-2021-4044
* Tue Sep 07 2021 Satya Naga Vasamsetty <svasamsetty@vmware.com> 3.0.0-1
- update to openssl 3.0.0
* Fri Aug 27 2021 Srinidhi Rao <srinidhir@vmware.com> 1.1.1l-1
- update to openssl 1.1.1l
* Fri Jun 18 2021 Satya Naga Vasamsetty <svasamsetty@vmware.com> 1.1.1k-2
- use openssl rehash functionality and remove unused patches
* Mon Mar 29 2021 Satya Naga Vasamsetty <svasamsetty@vmware.com> 1.1.1k-1
- Update openssl to 1.1.1k
* Tue Mar 23 2021 Tapas Kundu <tkundu@vmware.com> 1.1.1j-1
- Update to 1.1.1j
- Fix CVE-2021-3449 and CVE-2021-3450
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
