Summary:        Port of libtls from LibreSSL to OpenSSL
Name:           libretls
Version:        3.8.1
Release:        1%{?dist}
# libretls itself is ISC but uses other source codes, breakdown:
# BSD-3-Clause: compat/strsep.c
# MIT: compat/timegm.c
# LicenseRef-Fedora-Public-Domain: compat/{{explicit_bzero,ftruncate,pread,pwrite}.c,chacha_private.h}
License:        ISC AND BSD-3-Clause AND MIT AND LicenseRef-Fedora-Public-Domain
URL:            https://git.causal.agency/libretls/about
Group:          Development/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://causal.agency/libretls/%{name}-%{version}.tar.gz
%define sha512 %{name}=bbf4854622401bfc8662016a73202467714b603425dea2012e72846f0a22412018448fda8befa777d67c5dae44839b81e3b039130cf4970a4026c178d3a43ce2

BuildRequires: openssl-devel

Requires: openssl

%description
LibreTLS is a port of libtls from LibreSSL to OpenSSL. OpenBSD's libtls is a
new TLS library, designed to make it easier to write foolproof applications.

%package devel
Summary:  Development files for libretls
Requires: %{name} = %{version}-%{release}
Requires: pkg-config

%description devel
The libretls-devel package contains libraries and header files for developing
applications that use libtls.

%prep
%autosetup -p1

%build
%configure --disable-static
%make_build

%install
%make_install %{?_smp_mflags}

rm -rf %{buildroot}%{_mandir}

%check
# this currently does nothing
%make_build check

%ldconfig_scriptlets

%files
%defattr(-,root,root)
%{_libdir}/libtls.so.*

%files devel
%defattr(-,root,root)
%{_libdir}/libtls.so
%{_libdir}/pkgconfig/libtls.pc
%{_includedir}/tls.h

%changelog
* Tue Sep 10 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 3.8.1-1
- Initial version. Needed by bsd-netcat.
