Summary:        Security client
Name:           nss
Version:        3.78
Release:        11%{?dist}
URL:            https://firefox-source-docs.mozilla.org/security/nss/index.html
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: http://ftp.mozilla.org/pub/security/nss/releases/NSS_3_78_RTM/src/%{name}-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}

# taken from:
# http://lfs.linux-sysadmin.com/patches/downloads/nss/nss-3.78-standalone-1.patch
Patch0: %{name}-%{version}-standalone-1.patch
Patch1: CVE-2022-36320-1.patch
Patch2: CVE-2022-36320-2.patch
Patch3: CVE-2022-3479.patch
Patch4: CVE-2023-0767.patch
Patch5: CVE-2023-5388.patch
Patch6: CVE-2024-0743.patch

BuildRequires:  nspr-devel
BuildRequires:  sqlite-devel

Requires: nspr
Requires: %{name}-libs = %{version}-%{release}

%description
The Network Security Services (NSS) package is a set of libraries
designed to support cross-platform development of security-enabled
client and server applications. Applications built with NSS can
support SSL v2 and v3, TLS, PKCS #5, PKCS #7, PKCS #11, PKCS #12,
S/MIME, X.509 v3 certificates, and other security standards.
This is useful for implementing SSL and S/MIME or other Internet
security standards into an application.

%package        devel
Summary:        Development Libraries for Network Security Services
Group:          Development/Libraries
Requires:       nspr-devel
Requires:       %{name} = %{version}-%{release}

%description    devel
Header files for doing development with Network Security Services.

%package        libs
Summary:        Libraries for Network Security Services
Group:          System Environment/Libraries
Requires:       sqlite-libs
Requires:       nspr

%description    libs
This package contains minimal set of shared %{name} libraries.

%prep
%autosetup -p1

%build
%ifarch aarch64
# Fix build failure on arm64 - https://bugs.gentoo.org/738924
export NS_USE_GCC=1
%endif

cd %{name}
make %{?_smp_mflags} VERBOSE=1 BUILD_OPT=1 \
    NSPR_INCLUDE_DIR=%{_includedir}/nspr \
    USE_SYSTEM_ZLIB=1 \
    ZLIB_LIBS=-lz \
    USE_64=1 \
    NSS_ENABLE_WERROR=0 \
    $([ -f %{_includedir}/sqlite3.h ] && echo NSS_USE_SYSTEM_SQLITE=1)

%install
cd dist
install -vdm 755 %{buildroot}%{_bindir}
install -vdm 755 %{buildroot}%{_includedir}/%{name}
install -vdm 755 %{buildroot}%{_libdir}
install -v -m755 Linux*/lib/*.so %{buildroot}%{_libdir}
install -v -m644 Linux*/lib/{*.chk,libcrmf.a} %{buildroot}%{_libdir}
cp -v -RL {public,private}/%{name}/* %{buildroot}%{_includedir}/%{name}
chmod 644 %{buildroot}%{_includedir}/%{name}/*
install -v -m755 Linux*/bin/{certutil,%{name}-config,pk12util} %{buildroot}%{_bindir}
install -vdm 755 %{buildroot}%{_libdir}/pkgconfig
install -vm 644 Linux*/lib/pkgconfig/%{name}.pc %{buildroot}%{_libdir}/pkgconfig

# Fix to enable nss in fips mode
%define __spec_install_post \
  %{?__debug_package:%{__debug_install_post}} \
  %{__arch_install_post} \
  %{__os_install_post} \
  LD_LIBRARY_PATH=%{buildroot}%{_libdir} Linux*/bin/shlibsign -i %{buildroot}%{_libdir}/libsoftokn3.so \
  LD_LIBRARY_PATH=%{buildroot}%{_libdir} Linux*/bin/shlibsign -i %{buildroot}%{_libdir}/libnssdbm3.so \
  LD_LIBRARY_PATH=%{buildroot}%{_libdir} Linux*/bin/shlibsign -i %{buildroot}%{_libdir}/libfreebl3.so \
  LD_LIBRARY_PATH=%{buildroot}%{_libdir} Linux*/bin/shlibsign -i %{buildroot}%{_libdir}/libfreeblpriv3.so \
%{nil}

%if 0%{?with_check}
%check
cd %{name}/tests
chmod g+w . -R
useradd test -G root -m
HOST=localhost DOMSUF=localdomain BUILD_OPT=1
sudo -u test ./all.sh && userdel test -r -f
%endif

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_bindir}/*
%{_libdir}/*.chk
%{_libdir}/*.so
%exclude %{_libdir}/libfreeblpriv3.so
%exclude %{_libdir}/libnss3.so
%exclude %{_libdir}/libnssutil3.so
%exclude %{_libdir}/libsoftokn3.so
%exclude %{_libdir}/libfreeblpriv3.chk
%exclude %{_libdir}/libsoftokn3.chk

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/*.a
%{_libdir}/pkgconfig/*.pc

%files libs
%defattr(-,root,root)
%{_libdir}/libfreeblpriv3.so
%{_libdir}/libfreeblpriv3.chk
%{_libdir}/libnss3.so
%{_libdir}/libnssutil3.so
%{_libdir}/libsoftokn3.so
%{_libdir}/libsoftokn3.chk

%changelog
* Wed Dec 11 2024 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 3.78-11
- Release bump for SRP compliance
* Tue Nov 05 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 3.78-10
- Release bump for SRP compliance
* Tue Aug 06 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 3.78-9
- Fix CVE-2024-0743
* Thu Mar 14 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 3.78-8
- Fix CVE-2023-5388
* Fri Feb 23 2024 Nitesh Kumar <nitesh-nk.kumar@broadcom.com> 3.78-7
- Bump version as a part of sqlite upgrade to v3.43.2
* Fri Jan 12 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 3.78-6
- Fix CVE-2023-0767
* Fri May 26 2023 Nitesh Kumar <kunitesh@vmware.com> 3.78-5
- Patched for CVE-2022-3479
* Tue May 09 2023 Shreenidhi Shedi <sshedi@vmware.com> 3.78-4
- Fix CVE-2022-36320
* Wed Jan 11 2023 Oliver Kurth <okurth@vmware.com> 3.78-3
- bump release as part of sqlite update
* Sat Jul 30 2022 Shreenidhi Shedi <sshedi@vmware.com> 3.78-2
- Bump version as a part of sqlite upgrade
* Mon Apr 18 2022 Gerrit Photon <photon-checkins@vmware.com> 3.78-1
- Automatic Version Bump
* Wed Dec 01 2021 Satya Naga Vasamsetty <svasamsetty@vmware.com> 3.66-2
- Fix CVE-2021-43527
* Fri Jun 11 2021 Satya Naga Vasamsetty <svasamsetty@vmware.com> 3.66-1
- update nss to version 3.66
* Tue Apr 13 2021 Gerrit Photon <photon-checkins@vmware.com> 3.64-1
- Automatic Version Bump
* Wed Nov 18 2020 Tapas Kundu <tkundu@vmware.com> 3.57-2
- Package libsoftokn3.chk and libfreeblpriv3.chk in nss-libs
* Tue Sep 22 2020 Gerrit Photon <photon-checkins@vmware.com> 3.57-1
- Automatic Version Bump
* Tue Sep 15 2020 Michelle Wang <michellew@vmware.com> 3.56-2
- Fix nss build in aarch64 platform with adding NS_USE_GCC=1
- Fix to enable nss in fips mode
* Wed Sep 09 2020 Gerrit Photon <photon-checkins@vmware.com> 3.56-1
- Automatic Version Bump
* Tue Jul 14 2020 Gerrit Photon <photon-checkins@vmware.com> 3.55-1
- Automatic Version Bump
* Mon Sep 10 2018 Him Kalyan Bordoloi <bordoloih@vmware.com> 3.39-1
- Upgrade to 3.39.
* Thu Dec 07 2017 Alexey Makhalov <amakhalov@vmware.com> 3.31-5
- Add static libcrmf.a library to devel package
* Tue Nov 14 2017 Alexey Makhalov <amakhalov@vmware.com> 3.31-4
- Aarch64 support
* Fri Jul 07 2017 Vinay Kulkarni <kulkarniv@vmware.com> 3.31-3
- Fix buildrequires.
* Thu Jun 29 2017 Xiaolin Li <xiaolinl@vmware.com> 3.31-2
- Fix check.
* Tue Jun 20 2017 Xiaolin Li <xiaolinl@vmware.com> 3.31-1
- Upgrade to 3.31.
* Sat Apr 15 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 3.30.1-1
- Update to 3.30.1
* Fri Apr 14 2017 Alexey Makhalov <amakhalov@vmware.com> 3.25-4
- Added libs subpackage to reduce tdnf dependent tree
* Wed Nov 16 2016 Alexey Makhalov <amakhalov@vmware.com> 3.25-3
- Use sqlite-libs as runtime dependency
* Tue Oct 04 2016 ChangLee <changLee@vmware.com> 3.25-2
- Modified %check
* Tue Jul 05 2016 Anish Swaminathan <anishs@vmware.com> 3.25-1
- Upgrade to 3.25
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 3.21-2
- GA - Bump release of all rpms
* Thu Jan 21 2016 Xiaolin Li <xiaolinl@vmware.com> 3.21
- Updated to version 3.21
* Tue Aug 04 2015 Kumar Kaushik <kaushikk@vmware.com> 3.19-2
- Version update. Firefox requirement.
* Fri May 29 2015 Alexey Makhalov <amakhalov@vmware.com> 3.19-1
- Version update. Firefox requirement.
* Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 3.15.4-1
- Initial build. First version
