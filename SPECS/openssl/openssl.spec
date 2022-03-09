# Set this flag to 0 to build without fips provider
%global fips 1

Summary:        Management tools and libraries relating to cryptography
Name:           openssl
Version:        3.0.1
Release:        3%{?dist}
License:        OpenSSL
URL:            http://www.openssl.org
Group:          System Environment/Security
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        http://www.openssl.org/source/%{name}-%{version}.tar.gz
%define sha1    %{name}=33b00311e7a910f99ff041deebc6dd7bb9f459de
Source1:        rehash_ca_certificates.sh
Source2:        provider_default.cnf
%if %{?fips}
Source3:        provider_fips.cnf
Source4:        jitterentropy.c
%endif

Patch0:         openssl-providers.patch
Patch1:         openssl-CVE-2022-0778.patch

%if 0%{?with_check:1}
BuildRequires: zlib-devel
%endif

Requires:       bash
Requires:       glibc
Requires:       libgcc

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

%if %{?fips}
%package fips-provider
Summary:    FIPS Libraries for openssl
Group:      Applications/Internet
Requires:   %{name} = %{version}-%{release}

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
    -Wl,-z,noexecstack \
%if %{?fips}
    enable-fips
%endif

make %{?_smp_mflags}

%install
[ %{buildroot} != "/" ] && rm -rf %{buildroot}/*
make DESTDIR=%{buildroot} MANDIR=%{_mandir} MANSUFFIX=ssl install %{?_smp_mflags}
install -p -m 755 -D %{SOURCE1} %{buildroot}%{_bindir}/
install -p -m 644 -D %{SOURCE2} %{buildroot}%{_sysconfdir}/ssl/

%if %{?fips}
install -p -m 644 -D %{SOURCE3} %{buildroot}%{_sysconfdir}/ssl/
gcc -shared -Wall -O2 -g -fPIC -I%{buildroot}%{_includedir} -lcrypto -L%{buildroot}%{_libdir} \
%{SOURCE4} -o %{buildroot}%{_libdir}/ossl-modules/jitterentropy.so
%endif

%check
%if 0%{?with_check:1}
make tests %{?_smp_mflags}
%endif

%ldconfig_scriptlets

%if %{?fips}
%post fips-provider
# fips.so was just updated. Temporarily disable fips mode to regenerate new fipsmodule.cnf
sed -i 's#.include /etc/ssl/provider_fips.cnf#.include /etc/ssl/provider_default.cnf#' /etc/ssl/openssl.cnf
openssl fipsinstall -out /etc/ssl/fipsmodule.cnf -module %{_libdir}/ossl-modules/fips.so
sed -i 's#.include /etc/ssl/provider_default.cnf#.include /etc/ssl/provider_fips.cnf#' /etc/ssl/openssl.cnf

%postun fips-provider
# complete uninstall, not an upgrade
if [ "$1" = 0 ]; then
test -f /etc/ssl/fipsmodule.cnf && rm /etc/ssl/fipsmodule.cnf
sed -i 's#.include /etc/ssl/provider_fips.cnf#.include /etc/ssl/provider_default.cnf#' /etc/ssl/openssl.cnf
fi
%endif

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%{_sysconfdir}/ssl/certs
%{_sysconfdir}/ssl/ct_log_list.cnf
%{_sysconfdir}/ssl/ct_log_list.cnf.dist
%{_sysconfdir}/ssl/openssl.cnf.dist
%config(noreplace) %{_sysconfdir}/ssl/openssl.cnf
%{_sysconfdir}/ssl/provider_default.cnf
%{_sysconfdir}/ssl/private
%{_bindir}/openssl
%{_libdir}/*.so.*
%{_libdir}/engines*/*
%{_libdir}/ossl-modules/legacy.so

%if %{?fips}
%files fips-provider
%defattr(-,root,root)
%{_libdir}/ossl-modules/fips.so
%{_libdir}/ossl-modules/jitterentropy.so
%{_sysconfdir}/ssl/provider_fips.cnf
%exclude %{_sysconfdir}/ssl/fipsmodule.cnf
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
