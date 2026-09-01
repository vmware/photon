%global build_if %{photon_subrelease} >= 91

Summary:        libssh2 is a library implementing the SSH2 protocol.
Name:           libssh2
Version:        1.11.1
Release:        6%{?dist}
URL:            https://www.libssh2.org
Group:          System Environment/NetworkingLibraries
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://www.libssh2.org/download/libssh2-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}

Patch0: CVE-2026-7598.patch
Patch1: CVE-2026-55200.patch
Patch2: CVE-2026-55199.patch
# Fix CVE-2026-58050
Patch3: CVE-2026-58050.patch
# Fix CVE-2026-66032
Patch4: CVE-2026-66032.patch
# Fix CVE-2026-66033
Patch5: CVE-2026-66033.patch
# Fix CVE-2026-66034
Patch6: CVE-2026-66034.patch
# Fix CVE-2026-66035
Patch7: CVE-2026-66035.patch
# Fix CVE-2026-58051
Patch8: CVE-2026-58051.patch

BuildRequires:  openssl-devel
BuildRequires:  zlib-devel
BuildRequires:  pkg-config

Requires:       openssl-libs
Requires:       zlib

%description
libssh2 is a client-side C library implementing the SSH2 protocol.

%package        devel
Summary:        Header files for libssh2
Group:          System Environment/NetworkingLibraries
Requires:       %{name} = %{version}-%{release}

%description    devel
These are the header files of libssh2.

%prep
%autosetup -n %{name}-%{name}-%{version} -p1

%build
if [ %{_host} != %{_build} ]; then
  PREFIXES="--with-libssl-prefix=/target-%{_arch}/usr --with-libz-prefix=/target-%{_arch}/usr"
else
  PREFIXES=
fi

autoreconf -vif

%configure \
    --disable-static \
    --enable-shared \
    --with-crypto=openssl \
    --enable-clear-memory \
    $PREFIXES

%make_build

%install
%make_install %{?_smp_mflags}

%files
%defattr(-,root,root)
%{_libdir}/libssh2.so.*

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/libssh2.so
%{_libdir}/pkgconfig/*
%{_mandir}/man3/*

%changelog
* Mon Aug 31 2026 Harinadh Dommaraju <harinadh.dommaraju@broadcom.com> 1.11.1-6
- Fix CVE-2026-58051, CVE-2026-58050, CVE-2026-66032, CVE-2026-66033, CVE-2026-66034, CVE-2026-66035
* Tue Jun 30 2026 HarinadhD <harinadh.dommaraju@broadcom.com> 1.11.1-5
- Fix CVE-2026-55199
* Wed Jun 24 2026 HarinadhD <harinadh.dommaraju@broadcom.com> 1.11.1-4
- Fix CVE-2026-55200
* Mon May 25 2026 Harinadh Dommaraju <Harinadh.Dommaraju@broadcom.com> 1.11.1-3
- Fix CVE-2026-7598
* Fri May 15 2026 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 1.11.1-2
- Extended to build for subrelease 91 and above
* Wed Apr 08 2026 Srinidhi Rao <srinidhi.rao@broadcom.com> 1.11.1-1
- Upgrade libssh due to OpenSSL upgrade to v3.5.x
* Wed Dec 11 2024 Mukul Sikka <mukul.sikka@broadcom.com> 1.11.0-4
- Release bump for SRP compliance
* Tue Nov 05 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 1.11.0-3
- Release bump for SRP compliance
* Fri Dec 22 2023 Harinadh D <hdommaraju@vmware.com> 1.11.0-2
- Fix for CVE-2020-48795
* Thu Sep 07 2023 Harinadh D <hdommaraju@vmware.com> 1.11.0-1
- Version upgrade to fix CVE-2020-22218
- fix VCDA fails to perform SFTP upload of its backups to SFTP servers
* Fri Apr 14 2023 Shreenidhi Shedi <sshedi@vmware.com> 1.10.0-3
- Bump version as a part of zlib upgrade
* Wed Mar 08 2023 Shreenidhi Shedi <sshedi@vmware.com> 1.10.0-2
- Require openssl-libs
* Thu Apr 21 2022 Gerrit Photon <photon-checkins@vmware.com> 1.10.0-1
- Automatic Version Bump
* Wed Aug 04 2021 Satya Naga Vasamsetty <svasamsetty@vmware.com> 1.9.0-4
- Bump up release for openssl
* Tue Dec 15 2020 Shreenidhi Shedi <sshedi@vmware.com> 1.9.0-3
- Fix build with new rpm
* Tue Sep 29 2020 Satya Naga Vasamsetty <svasamsetty@vmware.com> 1.9.0-2
- openssl 1.1.1
* Mon Mar 16 2020 Sujay G <gsujay@vmware.com> 1.9.0-1
- Bump version to 1.9.0 and add patch to fix CVE-2019-17498
* Wed Jul 03 2019 Alexey Makhalov <amakhalov@vmware.com> 1.8.0-3
- Cross compilation support
* Thu Mar 28 2019 Tapas Kundu <tkundu@vmware.com> 1.8.0-2
- Fix for CVE-2019-3855
* Wed Nov 30 2016 Xiaolin Li <xiaolinl@vmware.com> 1.8.0-1
- Add libssh2 1.8.0 package.
