Summary:	High-Level Crypto API
Name:		gpgme
Version:	1.14.0
Release:	1%{?dist}
License:	GPLv2+
URL:		https://www.gnupg.org/(it)/related_software/gpgme/index.html
Group:		System Environment/Security
Vendor:		VMware, Inc.
Distribution:	Photon
Source0:	https://www.gnupg.org/ftp/gcrypt/%{name}/%{name}-%{version}.tar.bz2
%define sha1 gpgme=90a1b678703b0cabdb953035a4bee012e5685dce
Requires:	libassuan
Requires:	libgpg-error >= 1.32
# gpgme uses gnupg binaries only at runtime
Requires:	gnupg
BuildRequires:	gnupg
BuildRequires:	libgpg-error-devel >= 1.32
BuildRequires:	libassuan >= 2.2.0

%description
The GPGME package is a C language library that allows to add support for cryptography to a program. It is designed to make access to public key crypto engines like GnuPG or GpgSM easier for applications. GPGME provides a high-level crypto API for encryption, decryption, signing, signature verification and key management.

%package 	devel
Group:          Development/Libraries
Summary:        Static libraries and header files from GPGME, GnuPG Made Easy.
Requires:	%{name} = %{version}-%{release}
Requires:	libgpg-error-devel >= 1.32

%description 	devel
Static libraries and header files from GPGME, GnuPG Made Easy.

%prep
%setup -q

%build
./autogen.sh
%configure \
 	--disable-fd-passing \
	--disable-static \
	--enable-languages=cl \
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

%files devel
%defattr(-,root,root)
%{_bindir}/*
%{_includedir}/*.h
%{_libdir}/*.so
%{_datadir}/aclocal/*
%{_datadir}/common-lisp/source/gpgme/*
%{_libdir}/pkgconfig/*.pc

%changelog
*   Thu Jul 16 2020 Gerrit Photon <photon-checkins@vmware.com> 1.14.0-1
-   Automatic Version Bump
*   Sat Oct 20 2018 Ankit Jain <ankitja@vmware.com> 1.11.1-2
-   Removed gpg2, gnupg-2.2.10 doesn't provide gpg2
*   Tue Sep 11 2018 Anish Swaminathan <anishs@vmware.com> 1.11.1-1
-   Update version to 1.11.1
*   Wed Aug 30 2017 Alexey Makhalov <amakhalov@vmware.com> 1.9.0-3
-   Add requires gnupg
*   Thu Apr 20 2017 Alexey Makhalov <amakhalov@vmware.com> 1.9.0-2
-   Disabe C++ bindings
*   Thu Apr 13 2017 Danut Moraru <dmoraru@vmware.com> 1.9.0-1
-   Update to version 1.9.0
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
