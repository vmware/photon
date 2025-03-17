Summary:       Tools and libraries to manipulate EFI variables
Name:          efibootmgr
Version:       18
Release:       3%{?dist}
URL:           https://github.com/rhinstaller/efibootmgr/
Group:         System Environment/System Utilities
Vendor:        VMware, Inc.
Distribution:  Photon

Source0:      https://github.com/rhinstaller/efibootmgr/releases/download/%{name}-%{version}/%{name}-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}

BuildRequires: efivar-devel
BuildRequires: pciutils
BuildRequires: zlib

%description
efibootmgr is a userspace application used to modify the Intel Extensible Firmware Interface (EFI) Boot Manager. This application can create and destroy boot entries, change the boot order, change the next running boot option, and more.

%prep
%autosetup -p1

%build
%make_build EFIDIR=BOOT EFI_LOADER=grubx64.efi

%install
%make_install %{?_smp_mflags} EFIDIR=BOOT EFI_LOADER=grubx64.efi

gzip -9 %{buildroot}%{_mandir}/man8/%{name}.8
gzip -9 %{buildroot}%{_mandir}/man8/efibootdump.8

%clean
rm -rf %{buildroot}/*
%files
%defattr(-,root,root)
%{_sbindir}/*
%{_mandir}/man8/*

%changelog
* Thu Dec 12 2024 Guruswamy Basavaiah <guruswamy.basavaiah@broadcom.com> 18-3
- Release bump for SRP compliance
* Fri Apr 14 2023 Shreenidhi Shedi <sshedi@vmware.com> 18-2
- Bump version as a part of zlib upgrade
* Mon Feb 20 2023 Gerrit Photon <photon-checkins@vmware.com> 18-1
- Automatic Version Bump
* Mon Jun 22 2020 Gerrit Photon <photon-checkins@vmware.com> 17-1
- Automatic Version Bump
* Fri Apr 14 2017 Alexey Makhalov <amakhalov@vmware.com> 15-1
- Version update.
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 0.12-2
- GA - Bump release of all rpms
* Mon Jul 6 2015 Sharath George <sharathg@vmware.com> 0.12-1
- Initial build. First version. Install steps from spec file in source.
