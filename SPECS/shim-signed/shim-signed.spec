%define debug_package %{nil}
Summary:    Photon shim
Name:       shim-signed
Version:    15.8
Release:    5%{?dist}
Group:      System Environment/Base
URL:        https://vmware.github.io/photon/
Vendor:     VMware, Inc.
Distribution:   Photon
Source0:    %{name}-%{version}.tar.xz

Source1: license.txt
%include %{SOURCE1}
BuildArch:  x86_64

# Requirements for signing artifacts
%if "%{?signing_script}" != ""
%define network_required 1
BuildRequires:  ca-certificates-pki
BuildRequires:  sbsigntools
BuildRequires:  python3-requests
%endif

%description
Shim efi image signed by UEFI CA.

%prep
%autosetup

%install
install -d %{buildroot}/boot/efi/EFI/BOOT
cp shimx64.efi %{buildroot}/boot/efi/EFI/BOOT/bootx64.efi
cp revocations.efi %{buildroot}/boot/efi/EFI/BOOT/revocations.efi

%if "%{?signing_script}" != ""
python3 %{signing_script} --file_type pe \
      --config_file %{signing_params} \
      --auth_file %{signing_auth} \
      --artifact %{buildroot}/boot/efi/EFI/BOOT/revocations.efi
%endif

%files
%defattr(-,root,root,-)
/boot/efi/EFI/BOOT/bootx64.efi
/boot/efi/EFI/BOOT/revocations.efi

%changelog
* Mon Jan 20 2025 Kuntal Nayak <kuntal.nayak@broadcom.com> 15.8-5
- Add network required option with PE image signing
* Mon Dec 16 2024 Kuntal Nayak <kuntal.nayak@broadcom.com> 15.8-4
- Sign PE image inplace with SRP signer
* Wed Dec 11 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 15.8-3
- Release bump for SRP compliance
* Thu Jul 25 2024 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 15.8-2
- Version bump to sign revocations
* Wed Jul 17 2024 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 15.8-1
- Version update. Revocations support.
* Wed Apr 28 2021 Alexey Makhalov <amakhalov@vmware.com> 15.4-1
- Version update. SBAT support.
* Sun Nov 01 2020 Alexey Makhalov <amakhalov@vmware.com> 15-1
- Version update
* Wed Mar 11 2020 Alexey Makhalov <amakhalov@vmware.com> 12-1
- Initial packaging
