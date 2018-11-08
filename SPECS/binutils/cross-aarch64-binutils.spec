Name:    cross-aarch64-binutils
Summary: Cross Binutils for Aarch64
Version: 2.31.1
Release: 1%{?_dist}
Group:   Compiler
Vendor:  VMware, Inc.
Distribution: Photon
License: Apache 2
URL:     http://github.com/vmware/photon
Source0: https://ftp.gnu.org/gnu/binutils/binutils-%{version}.tar.xz
%define sha1 binutils=3b031410897fe224412f3a6a1b052402d2fbcc6a
BuildArch: x86_64

%define target_arch aarch64-unknown-linux-gnu
%define sysroot /target-aarch64

%description
The Binutils package contains a linker, an assembler,
and other tools for handling object files.

%prep
%setup -q -n binutils-%{version}

%build

sh configure \
    --prefix=%{_prefix} \
    --target=%{target_arch} \
    --with-sysroot=%{sysroot} \
    --disable-multilib && \
make configure-host && \
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install
rm -rf %{buildroot}%{_infodir}
rm -rf %{buildroot}%{_datadir}/locale

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_bindir}/*
%{_datadir}/*
%{_prefix}/%{target_arch}/*

%changelog
* Fri Nov 02 2018 Alexey Makhalov <amakhalov@vmware.com> 2.31.1-1
- Cloned from cross-aarch64-tools.spec
* Thu Nov 1 2018 Sriram Nambakam <snambakam@vmware.com> 1.0.0-3
- Updated versions of cross toolchain components
* Mon Oct 22 2018 Sriram Nambakam <snambakam@vmware.com> 1.0.0-2
- Replace _sysroot definition with sysroot
* Fri Oct 19 2018 Sriram Nambakam <snambakam@vmware.com> 1.0.0
- Initial build. First version
