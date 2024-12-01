Name:           libxcrypt
Summary:        Extended crypt library for DES, MD5, Blowfish and others
Version:        4.4.36
Release:        2%{?dist}
License:        LGPLv2+ and BSD and Public Domain
URL:            https://github.com/besser82/%{name}
Distribution:   Photon
Group:          System Environment/Security
Vendor:         VMware, Inc.

BuildRequires: perl

Source0: %{url}/releases/download/v%{version}/%{name}-%{version}.tar.xz
%define sha512 %{name}=468560e6f90877540d22e32c867cbcf3786983a6fdae6ef86454f4b7f2bbaae1b6589d1af75cda73078fa8f6e91b1a32f8353f26d433246eef7be3e96d4ae1c7

Conflicts: glibc < 2.36-5
Conflicts: glibc-libs < 2.36-15

%description
libxcrypt is a modern library for one-way hashing of passwords. It
supports a wide variety of both modern and historical hashing methods:
yescrypt, gost-yescrypt, scrypt, bcrypt, sha512crypt, sha256crypt,
md5crypt, SunMD5, sha1crypt, NT, bsdicrypt, bigcrypt, and descrypt.
It provides the traditional Unix crypt and crypt_r interfaces, as well
as a set of extended interfaces pioneered by Openwall Linux, crypt_rn,
crypt_ra, crypt_gensalt, crypt_gensalt_rn, and crypt_gensalt_ra.

libxcrypt is intended to be used by login(1), passwd(1), and other
similar programs; that is, to hash a small number of passwords during
an interactive authentication dialogue with a human. It is not suitable
for use in bulk password-cracking applications, or in any other situation
where speed is more important than careful handling of sensitive data.
However, it is intended to be fast and lightweight enough for use in
servers that must field thousands of login attempts per minute.

%package devel
Summary:    Development files for %{name}
Requires:   glibc-devel
Requires:   %{name} = %{version}-%{release}
Conflicts:  glibc-devel < 2.36-15
Conflicts:  man-pages < 5.13-2

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%autosetup -p1

%build
%configure \
  --disable-static \
  --enable-shared \
  --enable-hashes=all \
  --enable-obsolete-api=glibc \
  --disable-failure-tokens

%make_build

%install
%make_install %{?_smp_mflags}

%clean
rm -rf %{buildroot}

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%files
%defattr(-,root,root)
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root)
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%{_includedir}/*.h
%{_mandir}/man3/*
%{_mandir}/man5/*

%changelog
* Sun Dec 01 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 4.4.36-2
- libxcrypt-devel should conflict with man-pages
* Tue Oct 08 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 4.4.36-1
- Initial version.
