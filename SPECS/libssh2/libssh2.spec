Summary:        libssh2 is a library implementing the SSH2 protocol.
Name:           libssh2
Version:        1.9.0
Release:        3%{?dist}
License:        BSD
URL:            https://www.libssh2.org/
Group:          System Environment/NetworkingLibraries
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://www.libssh2.org/download/libssh2-%{version}.tar.gz
%define sha512  libssh2=41a3ebcf84e32eab69b7411ffb0a3b6e6db71491c968602b17392cfe3490ef00239726ec28acb3d25bf0ed62700db7f4d0bb5a9175618f413865f40badca6e17
BuildRequires:  openssl-devel
BuildRequires:  zlib-devel

Requires:       openssl
Requires:       zlib

Patch0:         CVE-2019-17498.patch
Patch1:         CVE-2020-22218.patch

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
%configure --disable-static \
    --enable-shared
make %{_smp_mflags}

%install
make DESTDIR=%{buildroot} install %{_smp_mflags}

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
*   Mon Sep 11 2023 Harinadh D <hdommaraju@vmware.com> 1.9.0-3
-   Add Patch to fix CVE-2020-22218
*   Tue Dec 17 2019 Siddharth Chandrasekran <csiddharth@vmware.com> 1.9.0-2
-   Add Patch to fix CVE-2019-17498
*   Tue Jul 30 2019 Ashwin H <ashwinh@vmware.com> 1.9.0-1
-   Update to 1.9.0
*   Mon Apr 01 2019 Ashwin H <ashwinh@vmware.com> 1.8.2-1
-   Update to 1.8.2
*   Thu Mar 28 2019 Tapas Kundu <tkundu@vmware.com> 1.8.0-2
-   Fix for CVE-2019-3855
*   Wed Nov 30 2016 Xiaolin Li <xiaolinl@vmware.com> 1.8.0-1
-   Add libssh2 1.8.0 package.
