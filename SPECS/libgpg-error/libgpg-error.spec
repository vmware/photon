
Summary:      	libgpg-error
Name:         	libgpg-error
Version:      	1.17
Release:      	2%{?dist}
License:      	GPLv2+
URL:          	ftp://ftp.gnupg.org/gcrypt/alpha/libgpg-error/
Group:		Development/Libraries
Source0:	ftp://ftp.gnupg.org/gcrypt/alpha/libgpg-error/%{name}-%{version}.tar.bz2
%define sha1 libgpg-error=ba5858b2947e7272dd197c87bac9f32caf29b256
Vendor:		VMware, Inc.
Distribution:	Photon

%description
This is a library that defines common error values for all GnuPG
components.  Among these are GPG, GPGSM, GPGME, GPG-Agent, libgcrypt,
pinentry, SmartCard Daemon and possibly more in the future.

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

%post 
/sbin/ldconfig

%postun 
/sbin/ldconfig

echo %{_libdir}
%files -f %{name}.lang
%defattr(-,root,root)
%{_bindir}/*
%{_libdir}/*gpg-error.so*
%{_includedir}/gpg-error.h
%{_datadir}/aclocal/gpg-error.m4
%{_mandir}/man1/*
%{_datarootdir}/common-lisp/*

%changelog
*	Tue Nov 10 2015 Xiaolin Li <xiaolinl@vmware.com> 1.17-2
-	Handled locale files with macro find_lang
* Tue Dec 30 2014 Priyesh Padmavilasom <ppadmavilasom@vmware.com>
- initial specfile.

# EOF
