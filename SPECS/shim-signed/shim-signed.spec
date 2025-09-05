%define debug_package %{nil}
Summary:    Photon shim
Name:       shim-signed
Version:    15.8
Release:    1%{?dist}
License:    Apache License
Group:      System Environment/Base
URL:        https://vmware.github.io/photon/
Vendor:     VMware, Inc.
Distribution:   Photon
Source0:    %{name}-%{version}.tar.xz
%define sha512 shim-signed=c97bda7d637951c62a346d7d814d9c896b63308161fa3fa6dcf28e49e9aa0bc898ea8a61bf163bde159437f397a5b34a2b7e0238819bef71b1438d30fd4e84ad
BuildArch:  x86_64

%description
Shim efi image signed by UEFI CA.

%prep
%autosetup

%install
install -d %{buildroot}/boot/efi/EFI/BOOT
cp shimx64.efi %{buildroot}/boot/efi/EFI/BOOT/bootx64.efi
# Revocation.efi is excluded knowingly as there was no usage in
# ph4 if needed we can always introduce in later point of time

%files
%defattr(-,root,root,-)
/boot/efi/EFI/BOOT/bootx64.efi

%changelog
* Thu Aug 14 2025 Ankit Jain <ankit-aj.jain@broadcom.com> 15.8-1
- Version update. SBAT support.
* Wed Apr 28 2021 Alexey Makhalov <amakhalov@vmware.com> 15.4-1
- Version update. SBAT support.
* Sun Nov 01 2020 Alexey Makhalov <amakhalov@vmware.com> 15-1
- Version update
* Wed Mar 11 2020 Alexey Makhalov <amakhalov@vmware.com> 12-1
- Initial packaging
