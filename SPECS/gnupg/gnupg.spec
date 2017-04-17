Summary:	OpenPGP standard implementation used for encrypted communication and data storage.
Name:		gnupg
Version:	2.1.20
Release:	1%{?dist}
License:	GPLv3+
URL:		https://gnupg.org/index.html
Group:		Applications/Cryptography.
Source0:        https://gnupg.org/ftp/gcrypt/gnupg/%{name}-%{version}.tar.bz2
%define sha1 gnupg=500ddae8e4225ae2e300934090f9b9a427b8def1
Vendor:		VMware, Inc.
Distribution:	Photon
BuildRequires:	zlib-devel
BuildRequires:  bzip2-devel
BuildRequires:  readline-devel
BuildRequires:  npth
BuildRequires:  npth-devel
BuildRequires:  libassuan
BuildRequires:  libksba >= 1.0.7
BuildRequires:  libgcrypt >= 1.7.0
BuildRequires:  libgcrypt-devel
BuildRequires:  libgpg-error >= 1.24
Requires:       libksba
Requires:       npth
Requires:       libassuan
Provides:       gpg


%description
GnuPG is a complete and free implementation of the OpenPGP standard as defined
by RFC4880 (also known as PGP). GnuPG allows to encrypt and sign your data and
communication, features a versatile key management system as well as access 
modules for all kinds of public key directories. GnuPG, also known as GPG, is 
a command line tool with features for easy integration with other applications.

%prep
%setup -q -n %{name}-%{version}

%build
./configure --prefix=%{_prefix}      \
            --sysconfdir=%{_sysconfdir} \
            --with-libusb=no

make
%install
make DESTDIR=%{buildroot} install

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
%exclude /usr/share/doc/*

%changelog
*       Tue Apr 11 2017 Danut Moraru <dmoraru@vmware.com> 2.1.20-1
-       Update to 2.1.20
*       Wed Jul 27 2016 Kumar Kaushik <kaushikk@vmware.com> 2.0.30-1
-       Initial Build.
