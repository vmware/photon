Summary:        libssh2 is a library implementing the SSH2 protocol.
Name:           libssh2
Version:        1.9.0
Release:        2%{?dist}
License:        BSD
URL:            https://www.libssh2.org/
Group:          System Environment/NetworkingLibraries
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://www.libssh2.org/download/libssh2-%{version}.tar.gz
%define sha1    libssh2=21e98282b103307a16792e5e2d4c99beaf0b3b9c
Patch0:         CVE-2019-17498.patch
BuildRequires:  openssl-devel
BuildRequires:  zlib-devel
BuildRequires:  pkg-config

Requires:       openssl
Requires:       zlib

%description
libssh2 is a client-side C library implementing the SSH2 protocol.

%package devel
Summary: Header files for libssh2
Group: System Environment/NetworkingLibraries
Requires: libssh2
%description devel
These are the header files of libssh2.

%prep
%setup -q
%patch0 -p1

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
make

%install
make DESTDIR=%{buildroot} install
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
*   Tue Sep 29 2020 Satya Naga Vasamsetty <svasamsetty@vmware.com> 1.9.0-2
-   openssl 1.1.1
*   Mon Mar 16 2020 Sujay G <gsujay@vmware.com> 1.9.0-1
-   Bump version to 1.9.0 and add patch to fix CVE-2019-17498
*   Wed Jul 03 2019 Alexey Makhalov <amakhalov@vmware.com> 1.8.0-3
-   Cross compilation support
*   Thu Mar 28 2019 Tapas Kundu <tkundu@vmware.com> 1.8.0-2
-   Fix for CVE-2019-3855
*   Wed Nov 30 2016 Xiaolin Li <xiaolinl@vmware.com> 1.8.0-1
-   Add libssh2 1.8.0 package.
