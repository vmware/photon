Summary:        A collection of PIN or passphrase entry dialogs
Name:           pinentry
Version:        1.2.0
Release:        1%{?dist}
License:        GPLv2
URL:            https://gnupg.org/software/pinentry/index.html
Group:          Applications/Cryptography.
Source0:        https://gnupg.org/ftp/gcrypt/%{name}/%{name}-%{version}.tar.bz2
%define sha512  pinentry=19cea79aa3982d1f0d75220c8e24ca38d6c49475c6f4c5aa7101151b4690db23ed316096a4a411136e716ba4eb471f48f9b09556e5c9837533c2356b9b384b63
Vendor:         VMware, Inc.
Distribution:   Photon
BuildRequires:  libassuan
BuildRequires:  libgpg-error
BuildRequires:  libgpg-error-devel

%description
pinentry is a small collection of dialog programs that allow GnuPG to read passphrases and PIN numbers in a secure manner.
There are versions for the common GTK and Qt toolkits as well as for the text terminal (Curses).
They utilize the Assuan protocol as specified in the Libassuan manual.

%prep
%autosetup -n %{name}-%{version}

%build
%configure \
     --with-libusb=no \
     --enable-pinentry-tty
make %{?_smp_mflags}

%install
make %{?_smp_mflags} DESTDIR=%{buildroot} install

%files
%defattr(-,root,root)
%{_bindir}/*
%{_infodir}/*
%exclude %{_infodir}/dir

%changelog
*  Mon Apr 18 2022 Gerrit Photon <photon-checkins@vmware.com> 1.2.0-1
-  Automatic Version Bump
*  Mon Sep 24 2018 Dweep Advani <dadvani@vmware.com> 1.1.0-1
-  Update to version 1.1.0
*  Wed Aug 16 2017 Danut Moraru <dmoraru@vmware.com> 1.0.0-2
-  Build pinentry-tty
*  Wed Jun 07 2017 Danut Moraru <dmoraru@vmware.com> 1.0.0-1
-  Initial Build.
