Summary:	Crypto Libraries
Name:		libgcrypt
Version:	1.6.5
Release:	2%{?dist}
License:        GPLv2+ and LGPLv2+
URL:            http://www.gnu.org/software/libgcrypt/
Source0:        ftp://ftp.gnupg.org/gcrypt/libgcrypt/%{name}-%{version}.tar.gz
%define sha1 libgcrypt=765370d9ee9e858c257dc06c3f0621bda8acaf69
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
*	Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 	1.6.5-2
-	GA - Bump release of all rpms
* 	Tue Feb 23 2016 Anish Swaminathan <anishs@vmware.com>  1.6.5-1
- 	Upgrade to 1.6.5
*	Wed Jun 17 2015 Divya Thaluru <dthaluru@vmware.com> 1.6.3-1
-	Initial build. First version

