Summary:      	libgpg-error
Name:         	libgpg-error
Version:      	1.27
Release:      	1%{?dist}
License:      	GPLv2+
URL:          	ftp://ftp.gnupg.org/gcrypt/alpha/libgpg-error/
Group:		Development/Libraries
Source0:	ftp://ftp.gnupg.org/gcrypt/alpha/libgpg-error/%{name}-%{version}.tar.bz2
%define sha1 libgpg-error=a428758999ff573e62d06892e3d2c0b0f335787c
Vendor:		VMware, Inc.
Distribution:	Photon

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
%setup -q

%build
./configure --prefix=%{_prefix} --bindir=%{_bindir} --libdir=%{_libdir}
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install
echo $%{_libdir}
echo $%{_bindir}
#mkdir -p %{buildroot}%{_libdir}
#cp %{buildroot}/usr/local/lib/* %{buildroot}%{_libdir}/
find %{buildroot}/%{_libdir} -name '*.la' -delete
rm -rf %{buildroot}/%{_infodir}
%find_lang %{name}

%check
make %{?_smp_mflags} check

%post 
/sbin/ldconfig

%postun 
/sbin/ldconfig

echo %{_libdir}
%files
%defattr(-,root,root)
%{_bindir}/*
%{_libdir}/libgpg-error.so*
%exclude %{_datadir}/aclocal/gpg-error.m4
%{_mandir}/man1/*
%exclude %{_datarootdir}/common-lisp/*

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_datadir}/*

%files lang -f %{name}.lang
%defattr(-,root,root)

%changelog
*	Tue Apr 04 2017 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 1.27-1
-	Upgraded to new version 1.27
*   Wed Nov 23 2016 Alexey Makhalov <amakhalov@vmware.com> 1.21-3
-   Added -lang subpackage
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.21-2
-   GA - Bump release of all rpms
*   Fri Jan 15 2016 Xiaolin Li <xiaolinl@vmware.com> 1.21-1
-   Updated to version 1.21
*   Tue Nov 10 2015 Xiaolin Li <xiaolinl@vmware.com> 1.17-2
-   Handled locale files with macro find_lang
*   Tue Dec 30 2014 Priyesh Padmavilasom <ppadmavilasom@vmware.com>
-   initial specfile.

