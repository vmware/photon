Summary:        An URL retrieval utility and library
Name:           curl
Version:        8.12.0
Release:        1%{?dist}
URL:            http://curl.haxx.se
Group:          System Environment/NetworkingLibraries
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: http://curl.haxx.se/download/%{name}-%{version}.tar.xz

Source1: license.txt
%include %{SOURCE1}

BuildRequires: ca-certificates
BuildRequires: openssl-devel
BuildRequires: krb5-devel
BuildRequires: libssh2-devel

%if 0%{?with_check}
BuildRequires: python3
%endif

Requires: ca-certificates
Requires: openssl-libs
Requires: krb5
Requires: libssh2 >= 1.11.0
Requires: %{name}-libs = %{version}-%{release}

%description
The cURL package contains an utility and a library used for
transferring files with URL syntax to any of the following
protocols: FTP, FTPS, HTTP, HTTPS, SCP, SFTP, TFTP, TELNET,
DICT, LDAP, LDAPS and FILE. Its ability to both download and
upload files can be incorporated into other programs to support
functions like streaming media.

%package        devel
Summary:        Libraries and header files for curl
Requires:       %{name} = %{version}-%{release}
Requires:       libssh2-devel >= 1.11.0
Requires:       krb5-devel

%description    devel
Static libraries and header files for the support library for curl

%package        libs
Summary:        Libraries for curl
Group:          System Environment/Libraries
Requires:       ca-certificates-pki
Requires:       libssh2 >= 1.11.0
Requires:       krb5

%description    libs
This package contains minimal set of shared curl libraries.

%prep
%autosetup -p1

%build
%configure \
    CFLAGS="%{optflags}" \
    CXXFLAGS="%{optflags}" \
    --disable-static \
    --enable-threaded-resolver \
    --enable-hidden-symbols \
    --with-ssl \
    --with-gssapi \
    --with-libssh2 \
    --without-libpsl \
    --with-ca-bundle=%{_sysconfdir}/pki/tls/certs/ca-bundle.crt
%make_build

%install
%make_install %{?_smp_mflags}
install -v -d -m755 %{buildroot}%{_docdir}/%{name}-%{version}
%{_fixperms} %{buildroot}/*

%check
%make_build check

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%{_bindir}/*
%{_mandir}/man1/*

%files devel
%defattr(-,root,root)
%{_libdir}/*.so
%{_libdir}/pkgconfig/*
%{_includedir}/*
%{_mandir}/man3/*
%{_datadir}/aclocal/libcurl.m4
%{_docdir}/%{name}-%{version}

%files libs
%defattr(-,root,root)
%{_libdir}/libcurl.so.*

%changelog
* Mon Feb 17 2025 Harinadh Dommaraju <Harinadh.Dommaraju@broadcom.com> 8.12.0-1
- Version upgrade
- Fixes CVE-2024-8096,CVE-2024-11053,CVE-2025-0167
* Wed Dec 11 2024 Guruswamy Basavaiah <guruswamy.basavaiah@broadcom.com> 8.7.1-7
- Release bump for SRP compliance
* Fri Nov 08 2024 Brennan Lamoreaux <brennan.lamoreaux@broadcom.com> 8.7.1-6
- Remove standalone license exceptions
* Tue Nov 05 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 8.7.1-5
- Release bump for SRP compliance
* Mon Nov 04 2024 Tapas Kundu <tapas.kundu@broadcom.com> 8.7.1-4
- Fix CVE-2024-9681
* Wed Jul 31 2024 Harinadh D <Harinadh.Dommaraju@broadcom.com> 8.7.1-3
- Fix CVE-2024-7264
* Tue Jul 16 2024 Harinadh D <Harinadh.Dommaraju@broadcom.com> 8.7.1-2
- Fix CVE-2024-6197
* Mon May 06 2024 Harinadh D <harinadh.dommaraju@broadcom.com> 8.7.1-1
- Version upgrade
* Mon Mar 25 2024 Harinadh D <harinadh.dommaraju@broadcom.com> 8.1.2-8
- Fix of CVE-2024-2004,CVE-2024-2398
* Tue Dec 05 2023 Harinadh D <hdommaraju@vmware.com> 8.1.2-7
- Fix of CVE-2023-46218,CVE-2023-46219
* Fri Oct 06 2023 Harinadh D <hdommaraju@vmware.com> 8.1.2-6
- Fix of CVE-2023-38546,CVE-2023-38545
* Tue Sep 12 2023 Dweep Advani <dadvani@vmware.com> 8.1.2-5
- Fix of CVE-2023-38039
* Thu Sep 07 2023 Harinadh D <hdommaraju@vmware.com> 8.1.2-4
- Version bump to use libssh2 1.11.0
* Fri Jul 28 2023 Srish Srinivasan <ssrish@vmware.com> 8.1.2-3
- Bump version as a part of krb5 upgrade
* Fri Jul 14 2023 Shivani Agarwal <shivania2@vmware.com> 8.1.2-2
- Fix CVE-2023-32001
* Tue Jul 11 2023 Shreenidhi Shedi <sshedi@vmware.com> 8.1.2-1
- Upgrade to v8.1.2
* Mon Jun 19 2023 Harinadh D <hdommaraju@vmware.com> 8.0.1-2
- curl-libs requires krb5
* Thu Apr 13 2023 Harinadh D <hdommaraju@vmware.com> 8.0.1-1
- version upgrade
* Wed Mar 08 2023 Shreenidhi Shedi <sshedi@vmware.com> 7.86.0-3
- Require openssl-libs
* Thu Jan 26 2023 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 7.86.0-2
- Bump version as a part of krb5 upgrade
* Fri Oct 28 2022 Gerrit Photon <photon-checkins@vmware.com> 7.86.0-1
- Automatic Version Bump
* Tue Jun 28 2022 Dweep Advani <dadvani@vmware.com> 7.84.0-1
- Upgrade to latest version 7.84.0 to fix multiple CVEs
* Thu Jun 16 2022 Dweep Advani <dadvani@vmware.com> 7.83.1-1
- Upgrade to 7.83.1 to fix multiple CVEs
* Mon Apr 18 2022 Gerrit Photon <photon-checkins@vmware.com> 7.82.0-1
- Automatic Version Bump
* Fri Dec 10 2021 Harinadh D<hdommaraju@vmware.com> 7.78.0-4
- Fix makecheck issues
* Fri Sep 17 2021 Satya Naga Vasamsetty <svasamsetty@vmware.com> 7.78.0-3
- Bump up release for openssl
* Tue Sep 14 2021 Dweep Advani <dadvani@vmware.com> 7.78.0-2
- Fixed CVE-2021-22945, CVE-2021-22946, CVE-2021-22947
* Mon Aug 23 2021 Harinadh D <hdommaraju@vmware.com> 7.78.0-1
- Version update
* Thu Aug 12 2021 Sujay G <gsujay@vmware.com> 7.77.0-3
- Fix check_spec errors by replacing %setup with %autosetup
* Thu Jul 22 2021 Harinadh D <hdommaraju@vmware.com> 7.77.0-2
- Fix CVE-2021-22924,CVE-2021-22925
- Metalink disabled to fix CVE-2021-22922,CVE-2021-22923
* Mon Jun 28 2021 Nitesh Kumar <kunitesh@vmware.com> 7.77.0-1
- Upgrade to 7.77.0, Fix for CVE-2021-22897
* Fri May 21 2021 Harinadh D <hdommaraju@vmware.com> 7.75.0-2
- Fix CVE-2021-22901, CVE-2021-22898
* Mon Mar 29 2021 Harinadh D <hdommaraju@vmware.com> 7.75.0-1
- Fix CVE-2021-22876, CVE-2021-22890
* Wed Jan 13 2021 Siju Maliakkal <smaliakkal@vmware.com> 7.74.0-1
- Upgrade to 7.74.0
* Mon Dec 07 2020 Dweep Advani <dadvani@vmware.com> 7.72.0-3
- Patched for  CVE-2020-8284, CVE-2020-8285 and CVE-2020-8286
* Tue Sep 29 2020 Satya Naga Vasamsetty <svasamsetty@vmware.com> 7.72.0-2
- openssl 1.1.1
* Tue Jul 14 2020 Gerrit Photon <photon-checkins@vmware.com> 7.72.0-1
- Automatic Version Bump
* Wed Jun 17 2020 Ankit Jain <ankitja@vmware.com> 7.61.1-5
- Fix for CVE-2020-8177
* Thu Jun 04 2020 Tapas Kundu <tkundu@vmware.com> 7.61.1-4
- Build with libmetalink support
* Tue Sep 24 2019 Dweep Advani <dadvani@vmware.com> 7.61.1-3
- Fix CVEs CVE-2018-16890, CVE-2019-{3822/3823/5436/5481/5482}
* Tue Jan 08 2019 Dweep Advani <dadvani@vmware.com> 7.61.1-2
- Fix of CVE-2018-16839, CVE-2018-16840 and CVE-2018-16842
* Mon Sep 10 2018 Ajay Kaher <akaher@vmware.com> 7.61.1-1
- Upgraded to version 7.61.1
* Wed Apr 04 2018 Dheeraj Shetty <dheerajs@vmware.com> 7.59.0-1
- Update to version 7.59.0
* Thu Feb 08 2018 Xiaolin Li <xiaolinl@vmware.com> 7.58.0-1
- Fix CVE-2017-8817.
* Thu Dec 21 2017 Xiaolin Li <xiaolinl@vmware.com> 7.56.1-2
- Fix CVE-2017-8818.
* Wed Dec 13 2017 Xiaolin Li <xiaolinl@vmware.com> 7.56.1-1
- Update to version 7.56.1
* Mon Nov 27 2017 Xiaolin Li <xiaolinl@vmware.com> 7.54.1-4
- Fix CVE-2017-1000257
* Mon Nov 06 2017 Xiaolin Li <xiaolinl@vmware.com> 7.54.1-3
- Fix CVE-2017-1000254
* Thu Nov 02 2017 Xiaolin Li <xiaolinl@vmware.com> 7.54.1-2
- Fix CVE-2017-1000099, CVE-2017-1000100, CVE-2017-1000101
* Tue Jul 11 2017 Divya Thaluru <dthaluru@vmware.com> 7.54.1-1
- Update to 7.54.1
* Mon Apr 24 2017 Bo Gan <ganb@vmware.com> 7.54.0-1
- Update to 7.54.0
* Fri Apr 14 2017 Alexey Makhalov <amakhalov@vmware.com> 7.51.0-5
- Added -libs subpackage
* Wed Dec 07 2016 Xiaolin Li <xiaolinl@vmware.com> 7.51.0-4
- Added -devel subpackage.
* Wed Nov 30 2016 Xiaolin Li <xiaolinl@vmware.com> 7.51.0-3
- Enable sftp support.
* Thu Nov 24 2016 Alexey Makhalov <amakhalov@vmware.com> 7.51.0-2
- Required krb5-devel.
* Wed Nov 02 2016 Anish Swaminathan <anishs@vmware.com> 7.51.0-1
- Upgrade curl to 7.51.0
* Wed Oct 05 2016 ChangLee <changlee@vmware.com> 7.50.3-2
- Modified %check
* Thu Sep 15 2016 Xiaolin Li <xiaolinl@vmware.com> 7.50.3-1
- Update curl to version 7.50.3.
* Tue Aug 23 2016 Xiaolin Li <xiaolinl@vmware.com> 7.47.1-3
- Enable gssapi in curl.
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 7.47.1-2
- GA - Bump release of all rpms
* Tue Feb 23 2016 Xiaolin Li <xiaolinl@vmware.com> 7.47.1-1
- Updated to version 7.47.1
* Thu Jan 14 2016 Xiaolin Li <xiaolinl@vmware.com> 7.46.0-1
- Updated to version 7.46.0
* Thu Aug 13 2015 Divya Thaluru <dthaluru@vmware.com> 7.43.0-1
- Update to version 7.43.0.
* Mon Apr 6 2015 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 7.41.0-1
- Update to version 7.41.0.
