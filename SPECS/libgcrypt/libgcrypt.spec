Summary:	Crypto Libraries
Name:		libgcrypt
Version:	1.6.3
Release:	1%{?dist}
License:        GPLv2+ and LGPLv2+
URL:            http://www.gnu.org/software/libgcrypt/
Source0:        ftp://ftp.gnupg.org/gcrypt/libgcrypt/libgcrypt-1.6.3.tar.bz2
%define sha1 libgcrypt=9456e7b64db9df8360a1407a38c8c958da80bbf1
Group:		System Environment/Libraries
Vendor:		VMware, Inc.
BuildRequires:	libgpg-error
Requires:	libgpg-error
Distribution:	Photon
%description
The libgcrypt package contains a general purpose crypto library based on the code used in GnuPG. The library provides a high level interface to cryptographic building blocks using an extendable and flexible API.

%package devel
Summary:	Development libraries and header files for libgcrypt
Requires:	libgcrypt

%description devel
The package contains libraries and header files for
developing applications that use libgcrypt.

%prep
%setup -q
%build
./configure \
	--prefix=%{_prefix}
make %{?_smp_mflags}
%install
make DESTDIR=%{buildroot} install
rm %{buildroot}%{_infodir}/*
%check
make -k check |& tee %{_specdir}/%{name}-check-log || %{nocheck}
%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig
%files
%defattr(-,root,root)
%{_bindir}/*
%{_libdir}/*.so.*
%{_mandir}/man1/*
%{_libdir}/*.la
/usr/share/aclocal/libgcrypt.m4
%files devel
%defattr(-,root,root)
%{_includedir}/*.h
%{_libdir}/*.so
%changelog
*	Wed Jun 17 2015 Divya Thaluru <dthaluru@vmware.com> 1.6.3-1
-	Initial build. First version

