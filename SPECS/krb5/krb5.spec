%define minor_ver 1.20

Summary:        The Kerberos newtork authentication system
Name:           krb5
Version:        1.20.2
Release:        6%{?dist}
URL:            http://web.mit.edu/kerberos
Group:          System Environment/Security
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: http://web.mit.edu/kerberos/www/dist/%{name}/%{minor_ver}/%{name}-%{version}.tar.gz
%define sha512 %{name}=69e263ef74116a3332c632a2a243499bcc47b01b1e57d02fe35aa6c2ff655674b6cf2b815457145f788bceac4d466d3f55f8c20ec9ee4a6051128417e1e7e99e

Source1: license.txt
%include %{SOURCE1}

Patch0: CVE-2024-26458.patch
Patch1: CVE-2024-26461.patch
Patch2: CVE-2024-26462.patch
Patch3: CVE-2024-37370-37371.patch

Requires:       openssl-libs
Requires:       e2fsprogs-libs

BuildRequires:  bison
BuildRequires:  openssl-devel
BuildRequires:  e2fsprogs-devel

Provides:       pkgconfig(mit-krb5)
Provides:       pkgconfig(mit-krb5-gssapi)

%description
Kerberos V5 is a trusted-third-party network authentication system,
which can improve your network's security by eliminating the insecure
practice of clear text passwords.

%package devel
Summary:    Libraries and header files for krb5
Requires:   %{name} = %{version}-%{release}
Requires:   e2fsprogs-devel

Conflicts: %{name} < 1.20.2-2%{?dist}

%description devel
Static libraries and header files for the support library for krb5

%package lang
Summary:    Additional language files for krb5
Group:      System Environment/Security
Requires:   %{name} = %{version}-%{release}

%description lang
These are the additional language files of krb5.

%prep
%autosetup -p1

%build
cd src
export CPPFLAGS="-D_GNU_SOURCE"
autoconf
if [ %{_host} != %{_build} ]; then
  export krb5_cv_attr_constructor_destructor=yes,yes
  export ac_cv_func_regcomp=yes
  export ac_cv_printf_positional=yes
  export ac_cv_file__etc_environment=no
  export ac_cv_file__etc_TIMEZONE=no
fi

%configure \
        --with-system-et \
        --with-system-ss \
        --with-system-verto=no \
        --enable-dns-for-realm \
        --enable-pkinit \
        --enable-shared
%make_build

%install
cd src
%make_install %{?_smp_mflags}
%{_fixperms} %{buildroot}/*

%if 0%{?with_check}
%check
# krb5 tests require hostname resolve
echo "127.0.0.1 $HOSTNAME" >> %{_sysconfdir}/hosts
cd src
make check %{?_smp_mflags}
%endif

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%{_bindir}/*
%{_libdir}/*.so.*
%{_libdir}/krb5/plugins/*
%{_sbindir}/*
%{_mandir}/man1/*
%{_mandir}/man5/*
%{_mandir}/man8/*
%{_mandir}/man7/*
%{_datadir}/man/man5/.k5identity.5.gz
%{_datadir}/man/man5/.k5login.5.gz

%files devel
%defattr(-,root,root)
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%{_includedir}/*
%{_datadir}/examples/*

%files lang
%defattr(-,root,root)
%{_datadir}/locale/*

%changelog
* Wed Dec 11 2024 Mukul Sikka <mukul.sikka@broadcom.com> 1.20.2-6
- Release bump for SRP compliance
* Tue Nov 05 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 1.20.2-5
- Release bump for SRP compliance
* Fri Aug 23 2024 Harinadh D <Harinadh.Dommaraju@broadcom.com> 1.20.2-4
- patched CVE-2024-37370, CVE-2024-37371
* Mon Jun 03 2024 Srish Srinivasan <srish.srinivasan@broadcom.com> 1.20.2-3
- patched CVE-2024-26458, CVE-2024-26461 and CVE-2024-26462
* Tue Apr 09 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 1.20.2-2
- Fix spec issues
* Fri Jul 28 2023 Srish Srinivasan <ssrish@vmware.com> 1.20.2-1
- Update to v1.20.2 to fix CVE-2023-36054
* Wed Mar 08 2023 Shreenidhi Shedi <sshedi@vmware.com> 1.20.1-3
- Require openssl-libs
* Mon Feb 20 2023 Tapas Kundu <tkundu@vmware.com> 1.20.1-2
- Add Bison in buildrequires
* Thu Jan 26 2023 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 1.20.1-1
- Upgrade to version 1.20.1
* Fri Sep 17 2021 Satya Naga Vasamsetty <svasamsetty@vmware.com> 1.17.2-2
- Bump up release for openssl
* Tue Apr 13 2021 Gerrit Photon <photon-checkins@vmware.com> 1.17.2-1
- Downgrade to 1.17 since PMD RPC call getting failed.
* Tue Apr 13 2021 Gerrit Photon <photon-checkins@vmware.com> 1.18.3-1
- Automatic Version Bump
* Mon Nov 02 2020 Tapas Kundu <tkundu@vmware.com> 1.17-4
- Fix krb5 build.
* Thu Oct 29 2020 Shreyas B. <shreyasb@vmware.com> 1.17-3
- krb5 v1.18.2 is not stable, creating panic for PMD-Client, so downgrading to v1.17.
* Thu Oct 01 2020 Gerrit Photon <photon-checkins@vmware.com> 1.18.2-1
- Automatic Version Bump
* Tue Sep 29 2020 Satya Naga Vasamsetty <svasamsetty@vmware.com> 1.17-3
- openssl 1.1.1
* Fri Nov 01 2019 Alexey Makhalov <amakhalov@vmware.com> 1.17-2
- Cross compilation support
* Thu Oct 03 2019 Satya Naga Vasamsetty <svasamsetty@vmware.com> 1.17-1
- Update to version 1.17
* Fri Sep 14 2018 Ankit Jain <ankitja@vmware.com> 1.16.1-1
- Update to version 1.16.1
* Wed Dec 13 2017 Xiaolin Li <xiaolinl@vmware.com> 1.16-1
- Update to version 1.16 to address CVE-2017-15088
* Thu Sep 28 2017 Xiaolin Li <xiaolinl@vmware.com> 1.15.2-1
- Update to version 1.15.2
* Mon Jul 10 2017 Alexey Makhalov <amakhalov@vmware.com> 1.15.1-2
- Fix make check: add /etc/hosts entry, deactivate parallel check
* Mon Apr 03 2017 Divya Thaluru <dthaluru@vmware.com> 1.15.1-1
- Updated to version 1.51.1
* Wed Nov 23 2016 Alexey Makhalov <amakhalov@vmware.com> 1.14-6
- Added -lang and -devel subpackages
* Wed Nov 16 2016 Alexey Makhalov <amakhalov@vmware.com> 1.14-5
- Use e2fsprogs-libs as runtime deps
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.14-4
- GA - Bump release of all rpms
* Mon Mar 21 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com>  1.14-3
- Add patch to never unload gssapi mechanisms
* Fri Mar 18 2016 Anish Swaminathan <anishs@vmware.com>  1.14-2
- Add patch for skipping unnecessary mech calls in gss_inquire_cred
* Thu Jan 21 2016 Anish Swaminathan <anishs@vmware.com> 1.14-1
- Upgrade version
* Tue Oct 07 2014 Divya Thaluru <dthaluru@vmware.com> 1.12.2-1
- Initial build. First version
