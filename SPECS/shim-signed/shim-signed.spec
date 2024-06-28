%define debug_package %{nil}
Summary:    Photon shim
Name:       shim-signed
Version:    15.4
Release:    1%{?dist}
License:    Apache License
Group:      System Environment/Base
URL:        https://vmware.github.io/photon/
Vendor:     VMware, Inc.
Distribution:   Photon
Source0:    %{name}-%{version}.tar.xz
%define sha1 shim-signed=0668621db3112f742c4ba3118857d0bee96320bb
BuildArch:  x86_64

%description
Shim efi image signed by UEFI CA.

%prep
%setup -q

%install
install -d %{buildroot}/boot/efi/EFI/BOOT
cp shimx64.efi %{buildroot}/boot/efi/EFI/BOOT/bootx64.efi

%files
%defattr(-,root,root,-)
/boot/efi/EFI/BOOT/bootx64.efi

%changelog
* Wed Apr 28 2021 Alexey Makhalov <amakhalov@vmware.com> 15.4-1
- Version update. SBAT support.
* Sun Nov 01 2020 Alexey Makhalov <amakhalov@vmware.com> 15-1
- Version update
* Wed Mar 11 2020 Alexey Makhalov <amakhalov@vmware.com> 12-1
- Initial packaging
