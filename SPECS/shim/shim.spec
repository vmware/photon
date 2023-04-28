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
Version:       15.7
Release:       1%{?dist}
License:       BSD-2-Clause
Group:         System/Boot
URL:           https://github.com/rhboot/shim
Vendor:        VMware, Inc.
Distribution:  Photon

Source0: https://github.com/rhboot/%{name}/releases/download/%{version}/%{name}-%{version}.tar.bz2
%define sha512 shim=99a9792be8dd8834ce1f929af341db1fc8ff985b079cebb42a87a770b3672cde573893463c1444c28e30c78207d560c77ad17795dbf19f24795ab3e22d601cec

Source1:       photon_sb2020.der
Source2:       sbat.photon.csv.in

Patch1:        0001-Make-sbat_var.S-parse-right-with-buggy-gcc-binutils.patch
Patch2:        0002-Enable-the-NX-compatibility-flag-by-default.patch
Patch3:        0003-CryptoPkg-BaseCryptLib-Fix-buffer-overflow-issue-in-.patch
Patch4:        0004-pe-Align-section-size-up-to-page-size-for-mem-attrs.patch
Patch5:        0005-pe-Add-IS_PAGE_ALIGNED-macro.patch
Patch6:        0006-Don-t-loop-forever-in-load_certs-with-buggy-firmware.patch

BuildRequires: dos2unix

%if 0%{?with_check}
BuildRequires: vim-extra
BuildRequires: python3-devel
BuildRequires: efivar-devel
%endif

%description
First stage UEFI bootloade that attempts to open, validate, and execute another application. It also installs a protocol which permits the second-stage bootloader to perform similar binary validation.

%prep
%autosetup -p1

%build
sed -e "s,@@NAME@@,%{name},g" \
    -e "s,@@VERSION_RELEASE@@,%{version}-%{release},g" \
    -e "s,@@SHIM_GEN@@,%{shim_generation},g" \
    %{SOURCE2} > data/sbat.photon.csv

%make_build VENDOR_CERT_FILE=%{SOURCE1} \
            EFI_PATH=%{_libdir} 'DEFAULT_LOADER=\\\\grub%{efiarch}.efi' \
            shim%{efiarch}.efi

%install
install -d -m 755 %{buildroot}%{_datadir}/%{name}
install -m 0644 shim%{efiarch}.efi %{buildroot}%{_datadir}/%{name}/

%if 0%{?with_check}
%check
make %{?_smp_mflags} test
%endif

%files
%defattr(-,root,root,-)
%{_datadir}/%{name}/shim%{efiarch}.efi

%changelog
* Wed Mar 08 2023 Alexey Makhalov <amakhalov@vmware.com> 15.7-1
- Initial version
