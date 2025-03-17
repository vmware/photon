Summary:        A collection of PIN or passphrase entry dialogs
Name:           pinentry
Version:        1.2.0
Release:        3%{?dist}
URL:            https://gnupg.org/software/pinentry/index.html
Group:          Applications/Cryptography.
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        https://gnupg.org/ftp/gcrypt/%{name}/%{name}-%{version}.tar.bz2

Source1: license.txt
%include %{SOURCE1}

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
* Wed Dec 11 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 1.2.0-3
- Release bump for SRP compliance
* Thu Dec 22 2022 Guruswamy Basavaiah <bguruswamy@vmware.com> 1.2.0-2
- Bump release as a part of libgpg-error upgrade to 1.46
* Mon Apr 18 2022 Gerrit Photon <photon-checkins@vmware.com> 1.2.0-1
- Automatic Version Bump
* Mon Sep 24 2018 Dweep Advani <dadvani@vmware.com> 1.1.0-1
- Update to version 1.1.0
* Wed Aug 16 2017 Danut Moraru <dmoraru@vmware.com> 1.0.0-2
- Build pinentry-tty
* Wed Jun 07 2017 Danut Moraru <dmoraru@vmware.com> 1.0.0-1
- Initial Build.
