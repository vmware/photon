Summary:    A collection of PIN or passphrase entry dialogs
Name:       pinentry
Version:    1.1.0
Release:    1%{?dist}
License:    GPLv2
URL:        https://gnupg.org/software/pinentry/index.html
Group:      Applications/Cryptography.
Vendor:     VMware, Inc.
Distribution:   Photon

Source0:        https://gnupg.org/ftp/gcrypt/%{name}/%{name}-%{version}.tar.bz2
%define sha512 %{name}=5012672925bcb5f683358c259e55e4b87c67cf063ad52c759308933733025c33f7ce08e5b8019ffc101cbf7ef30499040ef2fd34a7611698e65e1593f80948cd

BuildRequires:  libassuan-devel
BuildRequires:  libgpg-error-devel

Requires: libassuan
Requires: libgpg-error

%description
pinentry is a small collection of dialog programs that allow GnuPG to read passphrases and PIN numbers in a secure manner.
There are versions for the common GTK and Qt toolkits as well as for the text terminal (Curses).
They utilize the Assuan protocol as specified in the Libassuan manual.

%prep
%autosetup -p1 -n %{name}-%{version}

%build
%configure --with-libusb=no \
           --enable-pinentry-tty

make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install %{?_smp_mflags}

%files
%defattr(-,root,root)
%{_bindir}/*
%{_infodir}/*
%exclude %{_infodir}/dir

%changelog
* Mon Sep 24 2018 Dweep Advani <dadvani@vmware.com> 1.1.0-1
- Update to version 1.1.0
* Wed Aug 16 2017 Danut Moraru <dmoraru@vmware.com> 1.0.0-2
- Build pinentry-tty
* Wed Jun 07 2017 Danut Moraru <dmoraru@vmware.com> 1.0.0-1
- Initial Build.
