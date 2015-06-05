Summary:	High-Level Crypto API
Name:		gpgme
Version:	1.5.3
Release:	2%{?dist}
License:	GPLv2+
URL:		https://www.gnupg.org/(it)/related_software/gpgme/index.html
Group:		System Environment/Security
Vendor:		VMware, Inc.
Distribution:	Photon
Source0:	ftp://ftp.gnupg.org/gcrypt/%{name}/%{name}-%{version}.tar.bz2
Requires:	libassuan
Requires:	libgpg-error
BuildRequires:	libgpg-error
BuildRequires:	libassuan >= 2.2.0
%description
The GPGME package is a C language library that allows to add support for cryptography to a program. It is designed to make access to public key crypto engines like GnuPG or GpgSM easier for applications. GPGME provides a high-level crypto API for encryption, decryption, signing, signature verification and key management.  

%package 	devel
Group:          Development/Libraries
Summary:        Static libraries and header files from GPGME, GnuPG Made Easy.
Requires:	%{name} = %{version}
%description 	devel
Static libraries and header files from GPGME, GnuPG Made Easy.

%prep
%setup -q
%build
./configure \
	--prefix=%{_prefix} \
 	--disable-fd-passing \
        --disable-gpgsm-test
make %{?_smp_mflags}
%install
make DESTDIR=%{buildroot} install
rm %{buildroot}/%{_libdir}/*.la
rm -rf %{buildroot}/%{_infodir}
%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig
%files 
%defattr(-,root,root)
%{_libdir}/*.so.*
%{_datadir}/common-lisp/source/gpgme/*.lisp
%{_datadir}/common-lisp/source/gpgme/gpgme.asd
%files devel
%defattr(-,root,root)
%{_bindir}/*
%{_includedir}/*.h
%{_libdir}/*.so*
%{_datadir}/aclocal/*
%{_datadir}/common-lisp/source/gpgme/*
%changelog
*   Wed May 20 2015 Touseef Liaqat <tliaqat@vmware.com> 1.5.3-2
-   Updated group.
*	Tue Dec 30 2014 Divya Thaluru <dthaluru@vmware.com> 1.5.3-1
	Initial version
