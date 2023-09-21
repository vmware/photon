Name:       binutils-aarch64-linux-gnu
Summary:    Cross Binutils for Aarch64
Version:    2.35
Release:    7%{?dist}
License:    GPLv2+
URL:        http://www.gnu.org/software/binutils
Group:      System Environment/Base
Vendor:     VMware, Inc.
Distribution: Photon

Source0: https://ftp.gnu.org/gnu/binutils/binutils-%{version}.tar.xz
%define sha512 binutils=9f222e4ab6720036402d03904fb11b73ab87714b85cd84997f7d357f405c7e10581d70202f9165a1ee0c70538632db27ecc9dfe627dddb1e6bc7edb1537cf786

Patch1:         binutils-sync-libiberty-add-no-recurse-limit-make-check-fix.patch
Patch2:         binutils-CVE-2019-1010204.patch
Patch3:         binutils-CVE-2021-3487.patch
Patch4:         binutils-CVE-2021-20294.patch
Patch5:         binutils-CVE-2021-45078.patch
Patch6:         binutils-CVE-2022-38533.patch
Patch7:         binutils-bug-26520.patch
Patch8:         binutils-CVE-2022-4285.patch
Patch9:         binutils-CVE-2023-1972.patch
Patch10:        binutils-CVE-2023-25584.patch
Patch11:        binutils-CVE-2023-25585.patch
Patch12:        binutils-CVE-2023-25588.patch
Patch13:        binutils-CVE-2021-20197-1.patch
Patch14:        binutils-CVE-2021-20197-2.patch
Patch15:        binutils-CVE-2021-20197-3.patch
Patch16:        binutils-CVE-2021-20197-4.patch
Patch17:        binutils-CVE-2020-35448.patch
Patch18:        binutils-CVE-2021-3549.patch
Patch19:        binutils-CVE-2022-47695.patch
Patch20:        binutils-CVE-2021-46174.patch
Patch21:        binutils-CVE-2022-44840.patch
Patch22:        binutils-CVE-2022-48064.patch
Patch23:        binutils-CVE-2022-48063.patch
Patch24:        binutils-CVE-2022-47008.patch
Patch25:        binutils-CVE-2022-47007.patch
Patch26:        binutils-CVE-2022-47011.patch
Patch27:        binutils-CVE-2022-47010.patch
Patch28:        binutils-CVE-2022-48065.patch

BuildArch: x86_64

%define target_arch aarch64-unknown-linux-gnu
%define sysroot /target-aarch64

%description
The Binutils package contains a linker, an assembler,
and other tools for handling object files.

%prep
%autosetup -p1 -n binutils-%{version}

%build
sh ./configure \
    --prefix=%{_prefix} \
    --target=%{target_arch} \
    --with-sysroot=%{sysroot} \
    --disable-multilib

make configure-host %{?_smp_mflags}
make %{?_smp_mflags}

%install
%make_install %{?_smp_mflags}

rm -rf %{buildroot}%{_infodir} \
       %{buildroot}%{_datadir}/locale

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_bindir}/*
%{_datadir}/*
%{_prefix}/%{target_arch}/*

%changelog
* Fri Sep 22 2023 Guruswamy Basavaiah <bguruswamy@vmware.com> 2.35-7
- Fixes CVE-2022-44840, CVE-2022-48064, CVE-2022-47008, CVE-2022-48063
- CVE-2022-47011, CVE-2022-47010 and CVE-2022-47007
- CVE-2022-48065
* Mon Aug 14 2023 Guruswamy Basavaiah <bguruswamy@vmware.com> 2.35-6
- Fix CVE-2022-47695 and CVE-2021-46174
* Mon Aug 14 2023 Guruswamy Basavaiah <bguruswamy@vmware.com> 2.35-5
- Fix CVE-2020-35448 and CVE-2021-3549
* Tue Jul 11 2023 Guruswamy Basavaiah <bguruswamy@vmware.com> 2.35-4
- Fix CVE-2021-20197 and sync applied patches between binutils.spec
- and binutils-aarch64-linux-gnu.spec
* Mon Jun 26 2023 Guruswamy Basavaiah <bguruswamy@vmware.com> 2.35-3
- Fix CVE-2023-25584, CVE-2023-25585, CVE-2023-25588 and CVE-2022-38533
* Sun Oct 02 2022 Shreenidhi Shedi <sshedi@vmware.com> 2.35-2
- Remove .la files
* Fri Oct 16 2020 Ajay Kaher <akaher@vmware.com> 2.35-1
- Update binutils to 2.35
* Fri Nov 02 2018 Alexey Makhalov <amakhalov@vmware.com> 2.31.1-1
- Cloned from cross-aarch64-tools.spec
* Thu Nov 1 2018 Sriram Nambakam <snambakam@vmware.com> 1.0.0-3
- Updated versions of cross toolchain components
* Mon Oct 22 2018 Sriram Nambakam <snambakam@vmware.com> 1.0.0-2
- Replace _sysroot definition with sysroot
* Fri Oct 19 2018 Sriram Nambakam <snambakam@vmware.com> 1.0.0
- Initial build. First version
