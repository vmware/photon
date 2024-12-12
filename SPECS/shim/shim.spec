%define debug_package %{nil}

%define shim_generation 1

%ifarch x86_64
%define efiarch x64
%endif

%ifarch aarch64
%define efiarch aa64
%endif

Summary:       UEFI shim loader
Name:          shim
Version:       15.8
Release:       2%{?dist}
Group:         System/Boot
URL:           https://github.com/rhboot/shim
Vendor:        VMware, Inc.
Distribution:  Photon

Source0: https://github.com/rhboot/%{name}/releases/download/%{version}/%{name}-%{version}.tar.bz2
%define sha512 shim=30b3390ae935121ea6fe728d8f59d37ded7b918ad81bea06e213464298b4bdabbca881b30817965bd397facc596db1ad0b8462a84c87896ce6c1204b19371cd1

Source1:       photon_sb2020.der
Source2:       sbat.photon.csv.in

Source3: license.txt
%include %{SOURCE3}

# No need to bump up generation of 'shim.photon' as our previous shim
# has already been revoked by upstream 'shim' generation bump 1 -> 4
Patch100:      0001-Enforce-SBAT-presence-in-every-image.patch

# Add support to disable netboot and httpboot during build
Patch101:      0001-Add-provision-to-disable-netboot-and-httpboot-in-shi.patch
# Support to build revocations efi stub,
# .sbata and .sbatl would be added later when revocation data changes.
# To be signed by Vendor key
Patch102:      0001-Introduce-support-for-revocations-build.patch

BuildRequires: dos2unix

%if 0%{?with_check}
BuildRequires: vim-extra
BuildRequires: python3-devel
BuildRequires: efivar-devel
%endif

%description
First stage UEFI bootloader that attempts to open, validate, and execute another application. It also installs a protocol which permits the second-stage bootloader to perform similar binary validation.

%prep
%autosetup -p1

%build
sed -e "s,@@NAME@@,%{name},g" \
    -e "s,@@VERSION_RELEASE@@,%{version}-%{release},g" \
    -e "s,@@SHIM_GEN@@,%{shim_generation},g" \
    %{SOURCE2} > data/sbat.photon.csv

%make_build VENDOR_CERT_FILE=%{SOURCE1} \
            EFI_PATH=%{_libdir} 'DEFAULT_LOADER=\\\\grub%{efiarch}.efi' \
            DISABLE_REMOTE_BOOT=yes \
            shim%{efiarch}.efi revocations.efi

%install
install -d -m 755 %{buildroot}%{_datadir}/%{name}
install -m 0644 shim%{efiarch}.efi %{buildroot}%{_datadir}/%{name}/
install -m 0644 revocations.efi %{buildroot}%{_datadir}/%{name}/

%if 0%{?with_check}
%check
make %{?_smp_mflags} test
%endif

%files
%defattr(-,root,root,-)
%{_datadir}/%{name}/shim%{efiarch}.efi
%{_datadir}/%{name}/revocations.efi

%changelog
* Thu Dec 12 2024 Dweep Advani <dweep.advani@broadcom.com> 15.8-2
- Release bump for SRP compliance
* Sat Jan 27 2024 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 15.8-1
- Update to 15.8
- Added DISABLE_REMOTE_BOOT capability which disables httpboot and netboot in shim
* Tue Sep 19 2023 Alexey Makhalov <amakhalov@vmware.com> 15.7-2
- Enforce SBAT
- SBAT entry bump up: "shim,1" to "shim,3"
* Wed Mar 08 2023 Alexey Makhalov <amakhalov@vmware.com> 15.7-1
- Initial version
