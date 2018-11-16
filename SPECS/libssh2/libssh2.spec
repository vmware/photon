Summary:        libssh2 is a library implementing the SSH2 protocol.
Name:           libssh2
Version:        1.8.0
Release:        2%{?dist}
License:        BSD
URL:            https://www.libssh2.org/
Group:          System Environment/NetworkingLibraries
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://www.libssh2.org/download/libssh2-%{version}.tar.gz
%define sha1    libssh2=baf2d1fb338eee531ba9b6b121c64235e089e0f5
BuildRequires:  openssl-devel
BuildRequires:  zlib-devel

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
*   Thu Nov 15 2018 Alexey Makhalov <amakhalov@vmware.com> 1.8.0-2
-   Cross compilation support
*   Wed Nov 30 2016 Xiaolin Li <xiaolinl@vmware.com> 1.8.0-1
-   Add libssh2 1.8.0 package.


