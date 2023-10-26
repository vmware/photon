%global security_hardening none
%define debug_package %{nil}

Summary:        Intel ice driver v1.12.7
Name:           linux-rt-drivers-intel-ice
Version:        1.12.7
Release:        1%{?linuxrt_kernelsubrelease}%{?dist}
License:        GPLv2
URL:            https://sourceforge.net/projects/e1000
Group:          System Environment/Kernel
Vendor:         VMware, Inc.
Distribution:   Photon

%define uname_r %{LINUX_RT_KERNEL_VERSION}-%{LINUX_RT_KERNEL_RELEASE}
%define _modulesdir /lib/modules/%{uname_r}-rt
%define conflicts_ver 6.1.70-2%{?dist}

Source0:       https://sourceforge.net/projects/e1000/files/ice%20stable/%{version}/ice-%{version}.tar.gz
%define sha512 ice=71b08c90ee6c03242b0b11eef2425ec55fe089fa7735cc5ae9bae7469e14768b67505315a456e98b0b09ce0be71ffd35f119f2df211b927265f4d4eb8cbdf60b

Patch0:         ice-v1.12.7-Remove-inline-from-ethtool_sprintf.patch

BuildArch:      x86_64

BuildRequires:  which
BuildRequires:  kmod-devel
BuildRequires:  linux-rt-devel = %{uname_r}

Requires:       kmod
Requires:       linux-rt = %{uname_r}

Conflicts:      linux-rt < %{conflicts_ver}

%description
This Linux package contains the Intel ice v1.11.14 driver.

%package docs
Summary:        Kernel docs
Group:          System Environment/Kernel
Conflicts:      linux-rt-docs < %{conflicts_ver}
%description docs
This Linux package contains the Linux kernel doc files including files that
were left unpackaged from Linux-RT in the %{_mandir}.

%prep

%autosetup -p1 -n ice-%{version}

%build

make -C src KSRC=%{_modulesdir}/build %{?_smp_mflags}

%install

make -C src KSRC=%{_modulesdir}/build INSTALL_MOD_PATH=%{buildroot} \
    INSTALL_MOD_DIR=extra/ice-%{version} MANDIR=%{_mandir} \
    modules_install mandocs_install %{?_smp_mflags}

find %{buildroot}%{_modulesdir} -name *.ko -type f -print0 | xargs -0 xz

%post
/sbin/depmod -a %{uname_r}-rt

%files
%defattr(-,root,root)
%dir %{_modulesdir}/extra/ice-%{version}
%{_modulesdir}/extra/ice-%{version}/ice.ko.xz
# ICE driver firmware files are packaged in linux-firmware
%exclude /lib/firmware/updates/intel/ice

%files docs
%defattr(-,root,root)
%{_mandir}/*

%changelog
* Thu Jan 04 2024 Roye Eshed <roye.eshed@broadcom.com> 1.12.7-1
- Package Intel driver ice v1.12.7 for linux-rt.
