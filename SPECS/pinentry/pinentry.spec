Summary:	A collection of PIN or passphrase entry dialogs
Name:		pinentry
Version:	1.1.0
Release:	1%{?dist}
License:	GPLv2
URL:		https://gnupg.org/software/pinentry/index.html
Group:		Applications/Cryptography.
Source0:        https://gnupg.org/ftp/gcrypt/%{name}/%{name}-%{version}.tar.bz2
%define sha1 pinentry=693bdf9f48dfb3e040d92f50b1bb464e268b9fb0
Vendor:		VMware, Inc.
Distribution:	Photon
BuildRequires:  libassuan
BuildRequires:  libgpg-error
BuildRequires:  libgpg-error-devel


%description
pinentry is a small collection of dialog programs that allow GnuPG to read passphrases and PIN numbers in a secure manner.
There are versions for the common GTK and Qt toolkits as well as for the text terminal (Curses).
They utilize the Assuan protocol as specified in the Libassuan manual. 


%prep
%setup -q -n %{name}-%{version}

%build
./configure --prefix=%{_prefix}      \
            --sysconfdir=%{_sysconfdir} \
            --with-libusb=no \
            --enable-pinentry-tty

make
%install
make DESTDIR=%{buildroot} install

%files
%defattr(-,root,root)
%{_bindir}/*
%{_infodir}/*
%exclude %{_infodir}/dir

%changelog
*       Mon Sep 24 2018 Dweep Advani <dadvani@vmware.com> 1.1.0-1
-       Update to version 1.1.0
*       Wed Aug 16 2017 Danut Moraru <dmoraru@vmware.com> 1.0.0-2
-       Build pinentry-tty
*       Wed Jun 07 2017 Danut Moraru <dmoraru@vmware.com> 1.0.0-1
-       Initial Build.

