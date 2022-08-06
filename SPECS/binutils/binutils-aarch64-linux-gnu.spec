Name:       binutils-aarch64-linux-gnu
Summary:    Cross Binutils for Aarch64
Version:    2.35
Release:    1%{?dist}
License:    GPLv2+
URL:        http://www.gnu.org/software/binutils
Group:      System Environment/Base
Vendor:     VMware, Inc.
Distribution: Photon

Source0:    https://ftp.gnu.org/gnu/binutils/binutils-%{version}.tar.xz
%define sha512 binutils=9f222e4ab6720036402d03904fb11b73ab87714b85cd84997f7d357f405c7e10581d70202f9165a1ee0c70538632db27ecc9dfe627dddb1e6bc7edb1537cf786

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

%make_build configure-host
%make_build

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
