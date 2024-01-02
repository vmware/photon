Summary:        libssh2 is a library implementing the SSH2 protocol.
Name:           libssh2
Version:        1.11.0
Release:        2%{?dist}
License:        BSD
URL:            https://www.libssh2.org/
Group:          System Environment/NetworkingLibraries
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://www.libssh2.org/download/libssh2-%{version}.tar.gz
%define sha512  libssh2=ef85e152dc252bd9b1c05276972b9c22313f5d492743dde090235742746d67f634f2a419eff9162132e2274c8582113b75279b074e0c7b34b2526b92fd1a1e8e
BuildRequires:  openssl-devel
BuildRequires:  zlib-devel
BuildRequires:  pkg-config

Requires:       openssl
Requires:       zlib

Patch0:         fix-libssh2-linking-error.patch
patch1:         libssh2-CVE-2023-48795.patch

%description
libssh2 is a client-side C library implementing the SSH2 protocol.

%package devel
Summary: Header files for libssh2
Group: System Environment/NetworkingLibraries
Requires: libssh2
%description devel
These are the header files of libssh2.

%prep
%autosetup -p1

%build
if [ %{_host} != %{_build} ]; then
  PREFIXES="--with-libssl-prefix=/target-%{_arch}/usr --with-libz-prefix=/target-%{_arch}/usr"
else
  PREFIXES=
fi
%configure \
    --disable-static \
    --enable-shared \
    $PREFIXES
%make_build

%install
%make_install %{?_smp_mflags}
find %{buildroot} -name '*.la' -exec rm -f {} ';'

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
* Tue Jan 02 2024 Harinadh D <hdommaraju@vmware.com> 1.11.0-2
- Fix CVE-2023-48795
* Wed Aug 30 2023 Harinadh D <hdommaraju@vmware.com> 1.11.0-1
- Version upgrade to fix CVE-2020-22218
- fix VCDA fails to perform SFTP upload of its backups to SFTP servers
* Thu Apr 27 2023 Harinadh D <hdommaraju@vmware.com> 1.10.0-1
- Version upgrade
* Mon Sep 12 2022 Keerthana K <keerthanak@vmware.com> 1.9.0-5
- Fix EVP_Cipher interface change in openssl 3
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
