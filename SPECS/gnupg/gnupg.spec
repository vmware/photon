Summary:        OpenPGP standard implementation used for encrypted communication and data storage.
Name:           gnupg
Version:        2.2.27
Release:        4%{?dist}
License:        GPLv3+
URL:            https://gnupg.org/index.html
Group:          Applications/Cryptography.
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        https://gnupg.org/ftp/gcrypt/gnupg/%{name}-%{version}.tar.bz2
%define sha512 %{name}=cf336962116c9c08ac80b1299654b94948033ef51d6d5e7f54c2f07bbf7d92c7b0bddb606ceee2cdd837063f519b8d59af5a82816b840a0fc47d90c07b0e95ab

BuildRequires:  zlib-devel
BuildRequires:  bzip2-devel
BuildRequires:  readline-devel
BuildRequires:  npth-devel
BuildRequires:  libassuan-devel >= 2.5.0
BuildRequires:  libksba-devel
BuildRequires:  libgcrypt-devel
BuildRequires:  libgpg-error >= 1.24

Requires:       libksba
Requires:       libgcrypt >= 1.7.0
Requires:       npth
Requires:       libassuan
Requires:       pinentry

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
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install %{?_smp_mflags}

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
%{_datadir}/%{name}/*
%exclude %{_infodir}/dir
%exclude %{_docdir}/*

%changelog
* Fri Apr 14 2023 Shreenidhi Shedi <sshedi@vmware.com> 2.2.27-4
- Bump version as a part of zlib upgrade
* Thu Dec 22 2022 Guruswamy Basavaiah <bguruswamy@vmware.com> 2.2.27-3
- Bump release as a part of libgpg-error upgrade to 1.46
* Tue Dec 20 2022 Guruswamy Basavaiah <bguruswamy@vmware.com> 2.2.27-2
- Bump release as a part of readline upgrade
* Tue Apr 13 2021 Gerrit Photon <photon-checkins@vmware.com> 2.2.27-1
- Automatic Version Bump
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
