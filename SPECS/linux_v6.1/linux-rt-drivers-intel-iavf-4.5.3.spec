%global security_hardening none
%define debug_package %{nil}

Summary:        Intel iavf driver v4.5.3
Name:           linux-rt-drivers-intel-iavf
Version:        4.5.3
Release:        1%{?linuxrt_kernelsubrelease}%{?dist}
License:        GPLv2
URL:            https://sourceforge.net/projects/e1000
Group:          System Environment/Kernel
Vendor:         VMware, Inc.
Distribution:   Photon

%define uname_r %{LINUX_RT_KERNEL_VERSION}-%{LINUX_RT_KERNEL_RELEASE}
%define _modulesdir /lib/modules/%{uname_r}-rt
%define conflicts_ver 6.1.62-9%{?dist}

Source0:       https://sourceforge.net/projects/e1000/files/iavf%20stable/%{version}/iavf-%{version}.tar.gz
%define sha512 iavf=573b6b92ff7d8ee94d1ec01c56b990063c98c6f785a5fb96db30cf9c3fac4ff64277500b8468210464df343831818f576dd97cd172193491e3d47fec146c43fa

Patch0:         iavf-v4.5.3-linux-rt-iavf-Fix-build-errors-on-kernel-6.0.y.patch
Patch1:         iavf-v4.5.3-iavf-Makefile-added-alias-for-i40evf.patch
Patch2:         iavf-v4.5.3-iavf-Make-iavf-driver-honor-default-and-user-defined.patch
Patch3:         iavf-v4.5.3-Fix-build-errors-on-6.1.y.patch

BuildArch:      x86_64

BuildRequires:  kmod-devel
BuildRequires:  linux-rt-devel = %{uname_r}

Requires:       kmod
Requires:       linux-rt = %{uname_r}

Conflicts:      linux-rt < %{conflicts_ver}

%description
This Linux package contains the Intel iavf v4.5.3 driver.

%package docs
Summary:        Kernel docs
Group:          System Environment/Kernel
Conflicts:      linux-rt-docs < %{conflicts_ver}
%description docs
This Linux package contains the Linux kernel doc files including files that
were left unpackaged from Linux-RT in the %{_mandir}.

%prep

%autosetup -p1 -n iavf-%{version}

%build

make -C src KSRC=%{_modulesdir}/build %{?_smp_mflags}

%install

make -C src KSRC=%{_modulesdir}/build INSTALL_MOD_PATH=%{buildroot} \
    INSTALL_MOD_DIR=extra/iavf-%{version} MANDIR=%{_mandir} \
    modules_install mandocs_install %{?_smp_mflags}

find %{buildroot}%{_modulesdir} -name *.ko -type f -print0 | xargs -0 xz

%post
/sbin/depmod -a %{uname_r}-rt

%files
%defattr(-,root,root)
%dir %{_modulesdir}/extra/iavf-%{version}
%{_modulesdir}/extra/iavf-%{version}/iavf.ko.xz
# iavf.conf is used to just blacklist the deprecated i40evf driver and
# create an alias of i40evf to iavf. By default, iavf is used as the
# VF driver. This file creates a package conflict with other kernel
# flavors; hence we exclude this file from packaging.
%exclude %{_sysconfdir}/modprobe.d/iavf.conf

%files docs
%defattr(-,root,root)
%{_mandir}/*

%changelog
* Thu Jan 04 2024 Roye Eshed <roye.eshed@broadcom.com> 4.5.3-1
- Package Intel driver iavf v4.5.3 for linux-rt.
