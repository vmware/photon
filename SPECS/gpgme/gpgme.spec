Summary:	High-Level Crypto API
Name:		gpgme
Version:	1.6.0
Release:	3%{?dist}
License:	GPLv2+
URL:		https://www.gnupg.org/(it)/related_software/gpgme/index.html
Group:		System Environment/Security
Vendor:		VMware, Inc.
Distribution:	Photon
Source0:	ftp://ftp.gnupg.org/gcrypt/%{name}/%{name}-%{version}.tar.bz2
%define sha1 gpgme=21510323495f6220f8f67610c3c27a23d761d43d
Requires:	libassuan
Requires:	libgpg-error
BuildRequires:	libgpg-error-devel
BuildRequires:	libassuan >= 2.2.0
%description
The GPGME package is a C language library that allows to add support for cryptography to a program. It is designed to make access to public key crypto engines like GnuPG or GpgSM easier for applications. GPGME provides a high-level crypto API for encryption, decryption, signing, signature verification and key management.  

%package 	devel
Group:          Development/Libraries
Summary:        Static libraries and header files from GPGME, GnuPG Made Easy.
Requires:	%{name} = %{version}-%{release}
Requires:	libgpg-error-devel
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

%check
cd tests && make check-TESTS

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
*   Thu Nov 24 2016 Alexey Makhalov <amakhalov@vmware.com> 1.6.0-3
-   Required libgpg-error-devel.
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.6.0-2
-   GA - Bump release of all rpms
*   Thu Jan 14 2016 Xiaolin Li <xiaolinl@vmware.com> 1.6.0-1
-   Updated to version 1.6.0
*   Wed May 20 2015 Touseef Liaqat <tliaqat@vmware.com> 1.5.3-2
-   Updated group.
*   Tue Dec 30 2014 Divya Thaluru <dthaluru@vmware.com> 1.5.3-1
-   Initial version
