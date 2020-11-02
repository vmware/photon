%define debug_package %{nil}
Summary:    Photon shim
Name:       shim-signed
Version:    15
Release:    1%{?dist}
License:    Apache License
Group:      System Environment/Base
URL:        https://vmware.github.io/photon/
Vendor:     VMware, Inc.
Distribution:   Photon
Source0:    %{name}-%{version}.tar.xz
%define sha1 shim-signed=fc14f323cf4b3db6ba9c097471619f612e30830f
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
* Sun Nov 01 2020 Alexey Makhalov <amakhalov@vmware.com> 15-1
- Version update
* Wed Mar 11 2020 Alexey Makhalov <amakhalov@vmware.com> 12-1
- Initial packaging
