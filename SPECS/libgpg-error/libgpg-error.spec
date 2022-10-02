Summary:      	libgpg-error
Name:         	libgpg-error
Version:      	1.39
Release:      	1%{?dist}
License:      	GPLv2+
URL:          	ftp://ftp.gnupg.org/gcrypt/libgpg-error/
Group:		Development/Libraries
Vendor:		VMware, Inc.
Distribution:	Photon

Source0:	ftp://ftp.gnupg.org/gcrypt/libgpg-error/%{name}-%{version}.tar.bz2
%define sha512 libgpg-error=b28be183ac3d3920363558c4b5b2c24f9074a302799915cc076674bb349dcfb6f09160bec1d3fb62e04047c3ce432d345f36b0905100a88cc730b53d4eb78e42

%description
This is a library that defines common error values for all GnuPG
components.  Among these are GPG, GPGSM, GPGME, GPG-Agent, libgcrypt,
pinentry, SmartCard Daemon and possibly more in the future.

%package devel
Summary:	Libraries and header files for libgpg-error
Requires:	%{name} = %{version}-%{release}
%description devel
Static libraries and header files for the support library for libgpg-error

%package lang
Summary: Additional language files for libgpg-error
Group:		Applications/System
Requires: %{name} = %{version}-%{release}
%description lang
These are the additional language files of libgpg-error.

%prep
%autosetup -p1

%build
%configure
make %{?_smp_mflags}

%install
%make_install %{?_smp_mflags}

rm -rf %{buildroot}%{_infodir} \
       %{buildroot}%{_libdir}/*.la

%find_lang %{name}

%check
make %{?_smp_mflags} check

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%files
%defattr(-,root,root)
%{_bindir}/gpg-error
%{_bindir}/yat2m
%{_libdir}/libgpg-error.so.*
%{_mandir}/man1/*

%files devel
%defattr(-,root,root)
%{_bindir}/gpg-error-config
%{_bindir}/gpgrt-config
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/gpg-error.pc
%{_datadir}/libgpg-error
%{_datadir}/aclocal/*
%{_datadir}/common-lisp/source/gpg-error

%files lang -f %{name}.lang
%defattr(-,root,root)

%changelog
* Wed Sep 09 2020 Gerrit Photon <photon-checkins@vmware.com> 1.39-1
- Automatic Version Bump
* Wed Jul 08 2020 Gerrit Photon <photon-checkins@vmware.com> 1.38-1
- Automatic Version Bump
* Mon Sep 10 2018 Bo Gan <ganb@vmware.com> 1.32-1
- Update to 1.32
* Tue Apr 04 2017 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 1.27-1
- Upgraded to new version 1.27
* Wed Nov 23 2016 Alexey Makhalov <amakhalov@vmware.com> 1.21-3
- Added -lang subpackage
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.21-2
- GA - Bump release of all rpms
* Fri Jan 15 2016 Xiaolin Li <xiaolinl@vmware.com> 1.21-1
- Updated to version 1.21
* Tue Nov 10 2015 Xiaolin Li <xiaolinl@vmware.com> 1.17-2
- Handled locale files with macro find_lang
* Tue Dec 30 2014 Priyesh Padmavilasom <ppadmavilasom@vmware.com>
- initial specfile.
