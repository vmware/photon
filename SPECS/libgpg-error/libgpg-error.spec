
Summary:      	libgpg-error
Name:         	libgpg-error
Version:      	1.17
Release:      	1%{?dist}
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

%post 
/sbin/ldconfig

%postun 
/sbin/ldconfig

echo %{_libdir}
%files
%defattr(-,root,root)
%{_bindir}/*
%{_libdir}/*gpg-error.so*
%{_includedir}/gpg-error.h
%{_datadir}/aclocal/gpg-error.m4
%{_mandir}/man1/*
%{_datarootdir}/common-lisp/*
%lang(cs) %{_datarootdir}/locale/cs/LC_MESSAGES/libgpg-error.mo
%lang(da) %{_datarootdir}/locale/da/LC_MESSAGES/libgpg-error.mo
%lang(de) %{_datarootdir}/locale/de/LC_MESSAGES/libgpg-error.mo
%lang(eo) %{_datarootdir}/locale/eo/LC_MESSAGES/libgpg-error.mo
%lang(fr) %{_datarootdir}/locale/fr/LC_MESSAGES/libgpg-error.mo
%lang(it) %{_datarootdir}/locale/it/LC_MESSAGES/libgpg-error.mo
%lang(ja) %{_datarootdir}/locale/ja/LC_MESSAGES/libgpg-error.mo
%lang(nl) %{_datarootdir}/locale/nl/LC_MESSAGES/libgpg-error.mo
%lang(pl) %{_datarootdir}/locale/pl/LC_MESSAGES/libgpg-error.mo
%lang(ro) %{_datarootdir}/locale/ro/LC_MESSAGES/libgpg-error.mo
%lang(sv) %{_datarootdir}/locale/sv/LC_MESSAGES/libgpg-error.mo
%lang(uk) %{_datarootdir}/locale/uk/LC_MESSAGES/libgpg-error.mo
%lang(vi) %{_datarootdir}/locale/vi/LC_MESSAGES/libgpg-error.mo
%lang(zh_CN) %{_datarootdir}/locale/zh_CN/LC_MESSAGES/libgpg-error.mo


%changelog
* Tue Dec 30 2014 Priyesh Padmavilasom <ppadmavilasom@vmware.com>
- initial specfile.

# EOF
