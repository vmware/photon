Summary:    High-Level Crypto API
Name:       gpgme
Version:    1.14.0
Release:    2%{?dist}
License:    GPLv2+
URL:        https://www.gnupg.org/(it)/related_software/gpgme/index.html
Group:      System Environment/Security
Vendor:     VMware, Inc.
Distribution:   Photon

Source0:    https://www.gnupg.org/ftp/gcrypt/%{name}/%{name}-%{version}.tar.bz2
%define sha512 %{name}=b7ffa30a046c75215e1c73e2f34e5e65532e4dcf6bea55796adc6f82fd38dafe264bcd4332b2001155d6f9476d6fd82a77112dad31c1bb29db9ddefc532ae668

Requires:   libassuan
Requires:   libgpg-error >= 1.32
# gpgme uses gnupg binaries only at runtime
Requires:   gnupg

BuildRequires:  gnupg
BuildRequires:  libgpg-error-devel >= 1.32
BuildRequires:  libassuan-devel >= 2.2.0

%description
The GPGME package is a C language library that allows to add support for cryptography to a program. It is designed to make access to public key crypto engines like GnuPG or GpgSM easier for applications. GPGME provides a high-level crypto API for encryption, decryption, signing, signature verification and key management.

%package    devel
Group:      Development/Libraries
Summary:    Static libraries and header files from GPGME, GnuPG Made Easy.
Requires:   %{name} = %{version}-%{release}
Requires:   libassuan-devel
Requires:   libgpg-error-devel >= 1.32

%description    devel
Static libraries and header files from GPGME, GnuPG Made Easy.

%prep
%autosetup -p1

%build
sh ./autogen.sh
%configure \
    --disable-fd-passing \
    --disable-static \
    --enable-languages=cl \
    --disable-gpgsm-test

make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install %{?_smp_mflags}
rm -rf %{buildroot}%{_libdir}/*.la \
       %{buildroot}%{_infodir}

%if 0%{?with_check}
%check
cd tests && make check-TESTS %{?_smp_mflags}
%endif

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

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
* Mon May 30 2022 Shreenidhi Shedi <sshedi@vmware.com> 1.14.0-2
- Add libassuan-devel to gpgme-devel Requires
* Thu Jul 16 2020 Gerrit Photon <photon-checkins@vmware.com> 1.14.0-1
- Automatic Version Bump
* Sat Oct 20 2018 Ankit Jain <ankitja@vmware.com> 1.11.1-2
- Removed gpg2, gnupg-2.2.10 doesn't provide gpg2
* Tue Sep 11 2018 Anish Swaminathan <anishs@vmware.com> 1.11.1-1
- Update version to 1.11.1
* Wed Aug 30 2017 Alexey Makhalov <amakhalov@vmware.com> 1.9.0-3
- Add requires gnupg
* Thu Apr 20 2017 Alexey Makhalov <amakhalov@vmware.com> 1.9.0-2
- Disabe C++ bindings
* Thu Apr 13 2017 Danut Moraru <dmoraru@vmware.com> 1.9.0-1
- Update to version 1.9.0
* Thu Nov 24 2016 Alexey Makhalov <amakhalov@vmware.com> 1.6.0-3
- Required libgpg-error-devel.
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.6.0-2
- GA - Bump release of all rpms
* Thu Jan 14 2016 Xiaolin Li <xiaolinl@vmware.com> 1.6.0-1
- Updated to version 1.6.0
* Wed May 20 2015 Touseef Liaqat <tliaqat@vmware.com> 1.5.3-2
- Updated group.
* Tue Dec 30 2014 Divya Thaluru <dthaluru@vmware.com> 1.5.3-1
- Initial version
