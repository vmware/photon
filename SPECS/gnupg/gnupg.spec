Summary:        OpenPGP standard implementation used for encrypted communication and data storage.
Name:           gnupg
Version:        2.2.23
Release:        4%{?dist}
License:        GPLv3+
URL:            https://gnupg.org/index.html
Group:          Applications/Cryptography.
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        https://gnupg.org/ftp/gcrypt/gnupg/%{name}-%{version}.tar.bz2
%define sha512 %{name}=736b39628f7e4adc650b3f9937c81f27e9ad41e77f5345dc54262c91c1cf7004243fa7f932313bcde955e0e9b3f1afc639bac18023ae878b1d26e3c5a3cabb90
Patch0:         CVE-2022-34903.patch
BuildRequires:  zlib-devel
BuildRequires:  bzip2-devel
BuildRequires:  readline-devel
BuildRequires:  npth-devel
BuildRequires:  libassuan-devel >= 2.5.0
BuildRequires:  libksba-devel >= 1.0.7
BuildRequires:  libgcrypt-devel
BuildRequires:  libgpg-error >= 1.24
BuildRequires:  gnutls-devel
BuildRequires:  sqlite-devel
BuildRequires:  gettext

Requires:       libksba >= 1.4.0-4
Requires:       libgcrypt >= 1.7.0
Requires:       npth
Requires:       libassuan
Requires:       pinentry
Requires:       gnutls
Requires:       sqlite-libs
Provides:       gpg

%description
GnuPG is a complete and free implementation of the OpenPGP standard as defined
by RFC4880 (also known as PGP). GnuPG allows to encrypt and sign your data and
communication, features a versatile key management system as well as access
modules for all kinds of public key directories. GnuPG, also known as GPG, is
a command line tool with features for easy integration with other applications.

%prep
%autosetup -p1 -n %{name}-%{version}

%build
%configure
%make_build %{?_smp_mflags}

%install
%make_install %{?_smp_mflags}

%if 0%{?with_check}
%check
make %{?_smp_mflags} check
%endif

%files
%defattr(-,root,root)
%{_bindir}/*
%{_sbindir}/*
%{_datadir}/locale/*/*/*
%{_mandir}/*
%{_infodir}/gnupg*
%{_libexecdir}/*
%{_datadir}/gnupg/*
%exclude %{_infodir}/dir
%exclude %{_docdir}/*

%changelog
* Tue Nov 28 2023 Shreenidhi Shedi <sshedi@vmware.com> 2.2.23-4
- Bump version as a part of gnutls upgrade
* Tue Jan 24 2023 Guruswamy Basavaiah <bguruswamy@vmware.com> 2.2.23-3
- Bump release as a part fix to CVE-2022-3515 in libksba
* Tue Jul 19 2022 Shivani Agarwal <shivania2@vmware.com> 2.2.23-2
- Fix CVE-2022-34903
* Wed Sep 09 2020 Gerrit Photon <photon-checkins@vmware.com> 2.2.23-1
- Automatic Version Bump
* Thu Jul 16 2020 Gerrit Photon <photon-checkins@vmware.com> 2.2.21-1
- Automatic Version Bump
* Thu Apr 02 2020 Siddharth Chandrasekaran <csiddharth@vmware.com> 2.2.18-1
- Upgrade to 2.2.18 to fix CVE-2019-14855
* Sat Oct 20 2018 Ankit Jain <ankitja@vmware.com> 2.2.10-1
- Update to 2.2.10
* Wed Aug 30 2017 Alexey Makhalov <amakhalov@vmware.com> 2.1.20-3
- Add requires libgcrypt
* Wed Jun 07 2017 Danut Moraru <dmoraru@vmware.com> 2.1.20-2
- Add pinentry dependency
* Tue Apr 11 2017 Danut Moraru <dmoraru@vmware.com> 2.1.20-1
- Update to 2.1.20
* Wed Jul 27 2016 Kumar Kaushik <kaushikk@vmware.com> 2.0.30-1
- Initial Build.
