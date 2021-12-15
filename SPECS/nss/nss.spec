Summary:        Security client
Name:           nss
Version:        3.44
Release:        7%{?dist}
License:        MPLv2.0
URL:            http://ftp.mozilla.org/pub/security/nss/releases/NSS_3_44_RTM/src/%{name}-%{version}.tar.gz
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        %{name}-%{version}.tar.gz
%define sha1    nss=11eab8681754472a9d1eb196e3c604d794ebe7f3
Patch0:         nss-3.44-standalone-1.patch
Patch1:         nss-CVE-2020-12403.patch
Patch2:         nss-CVE-2021-43527.patch
Requires:       nspr
BuildRequires:  nspr-devel
BuildRequires:  sqlite-devel
Requires:       nss-libs = %{version}-%{release}

%description
 The Network Security Services (NSS) package is a set of libraries
 designed to support cross-platform development of security-enabled
 client and server applications. Applications built with NSS can
 support SSL v2 and v3, TLS, PKCS #5, PKCS #7, PKCS #11, PKCS #12,
 S/MIME, X.509 v3 certificates, and other security standards.
 This is useful for implementing SSL and S/MIME or other Internet
 security standards into an application.

%package devel
Summary: Development Libraries for Network Security Services
Group: Development/Libraries
Requires: nspr-devel
Requires: nss = %{version}-%{release}
%description devel
Header files for doing development with Network Security Services.

%package libs
Summary: Libraries for Network Security Services
Group:      System Environment/Libraries
Requires:   sqlite-libs
Requires:   nspr
%description libs
This package contains minimal set of shared nss libraries.

%prep
%autosetup -p1
%build
cd nss
# make doesn't support _smp_mflags
make VERBOSE=1 BUILD_OPT=1 \
    NSPR_INCLUDE_DIR=%{_includedir}/nspr \
    USE_SYSTEM_ZLIB=1 \
    ZLIB_LIBS=-lz \
    USE_64=1 \
    $([ -f %{_includedir}/sqlite3.h ] && echo NSS_USE_SYSTEM_SQLITE=1)

%install
cd nss
cd ../dist
install -vdm 755 %{buildroot}%{_bindir}
install -vdm 755 %{buildroot}%{_includedir}/nss
install -vdm 755 %{buildroot}%{_libdir}
install -v -m755 Linux*/lib/*.so %{buildroot}%{_libdir}
install -v -m644 Linux*/lib/{*.chk,libcrmf.a} %{buildroot}%{_libdir}
cp -v -RL {public,private}/nss/* %{buildroot}%{_includedir}/nss
chmod 644 %{buildroot}%{_includedir}/nss/*
install -v -m755 Linux*/bin/{certutil,nss-config,pk12util} %{buildroot}%{_bindir}
install -vdm 755 %{buildroot}%{_libdir}/pkgconfig
install -vm 644 Linux*/lib/pkgconfig/nss.pc %{buildroot}%{_libdir}/pkgconfig
%define __spec_install_post \
  %{?__debug_package:%{__debug_install_post}} \
  %{__arch_install_post} \
  %{__os_install_post} \
  LD_LIBRARY_PATH=%{buildroot}%{_libdir} Linux*/bin/shlibsign -i %{buildroot}%{_libdir}/libsoftokn3.so \
  LD_LIBRARY_PATH=%{buildroot}%{_libdir} Linux*/bin/shlibsign -i %{buildroot}%{_libdir}/libnssdbm3.so \
  LD_LIBRARY_PATH=%{buildroot}%{_libdir} Linux*/bin/shlibsign -i %{buildroot}%{_libdir}/libfreebl3.so \
  LD_LIBRARY_PATH=%{buildroot}%{_libdir} Linux*/bin/shlibsign -i %{buildroot}%{_libdir}/libfreeblpriv3.so \
%{nil}

%check
chmod g+w . -R
cd nss/tests
useradd test -G root -m
sed -i '/RUN_FIPS/a export HOST=localhost DOMSUF=localdomain BUILD_OPT=1 USE_64=1' all.sh
HOST=localhost DOMSUF=localdomain BUILD_OPT=1
sudo -u test ./all.sh && userdel test -r -f

%post   -p /sbin/ldconfig

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
%{_includedir}/*
%{_libdir}/*.a
%{_libdir}/pkgconfig/*.pc

%files libs
%{_libdir}/libfreeblpriv3.so
%{_libdir}/libfreeblpriv3.chk
%{_libdir}/libnss3.so
%{_libdir}/libnssutil3.so
%{_libdir}/libsoftokn3.so
%{_libdir}/libsoftokn3.chk

%changelog
*   Wed Dec 01 2021 Satya Naga Vasamsetty <svasamsetty@vmware.com> 3.44-7
-   Fix CVE-2021-43527
*   Fri Jun 11 2021 Satya Naga Vasamsetty <svasamsetty@vmware.com> 3.44-6
-   Fix CVE-2020-12403
*   Wed Nov 18 2020 Tapas Kundu <tkundu@vmware.com> 3.44-5
-   Package libsoftokn3.chk and libfreeblpriv3.chk in nss-libs
*   Mon Jun 01 2020 Siju Maliakkal <smaliakkal@vmware.com> 3.44-4
-   Use latest sqlite
*   Thu Oct 10 2019 Harinadh Dommaraju <hdommaraju@vmware.com> 3.44-3
-   Makecheck fixes
*   Fri Aug 09 2019 Ashwin H <ashwinh@vmware.com> 3.44-2
-   Fix to enable nss in fips mode
*   Wed May 29 2019 Michelle Wang <michellew@vmware.com> 3.44-1
-   Upgrade to 3.44 for CVE-2018-12404
*   Mon Sep 10 2018 Him Kalyan Bordoloi <bordoloih@vmware.com> 3.39-1
-   Upgrade to 3.39.
*   Thu Dec 07 2017 Alexey Makhalov <amakhalov@vmware.com> 3.31-5
-   Add static libcrmf.a library to devel package
*   Tue Nov 14 2017 Alexey Makhalov <amakhalov@vmware.com> 3.31-4
-   Aarch64 support
*   Fri Jul 07 2017 Vinay Kulkarni <kulkarniv@vmware.com> 3.31-3
-   Fix buildrequires.
*   Thu Jun 29 2017 Xiaolin Li <xiaolinl@vmware.com> 3.31-2
-   Fix check.
*   Tue Jun 20 2017 Xiaolin Li <xiaolinl@vmware.com> 3.31-1
-   Upgrade to 3.31.
*   Sat Apr 15 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 3.30.1-1
-   Update to 3.30.1
*   Fri Apr 14 2017 Alexey Makhalov <amakhalov@vmware.com> 3.25-4
-   Added libs subpackage to reduce tdnf dependent tree
*   Wed Nov 16 2016 Alexey Makhalov <amakhalov@vmware.com> 3.25-3
-   Use sqlite-libs as runtime dependency
*   Tue Oct 04 2016 ChangLee <changLee@vmware.com> 3.25-2
-   Modified %check
*   Tue Jul 05 2016 Anish Swaminathan <anishs@vmware.com> 3.25-1
-   Upgrade to 3.25
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 3.21-2
-   GA - Bump release of all rpms
*   Thu Jan 21 2016 Xiaolin Li <xiaolinl@vmware.com> 3.21
-   Updated to version 3.21
*   Tue Aug 04 2015 Kumar Kaushik <kaushikk@vmware.com> 3.19-2
-   Version update. Firefox requirement.
*   Fri May 29 2015 Alexey Makhalov <amakhalov@vmware.com> 3.19-1
-   Version update. Firefox requirement.
*   Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 3.15.4-1
-   Initial build. First version
