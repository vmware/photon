%global security_hardening none
%define debug_package %{nil}

Summary:        Intel iavf driver v4.9.1
Name:           linux-rt-drivers-intel-iavf
Version:        4.9.1
Release:        1%{?linuxrt_kernelsubrelease}%{?dist}
License:        GPLv2
URL:            https://sourceforge.net/projects/e1000
Group:          System Environment/Kernel
Vendor:         VMware, Inc.
Distribution:   Photon

%define uname_r %{LINUX_RT_KERNEL_VERSION}-%{LINUX_RT_KERNEL_RELEASE}
%define _modulesdir /lib/modules/%{uname_r}-rt
%define conflicts_ver 6.1.70-2%{?dist}

Source0:       https://sourceforge.net/projects/e1000/files/iavf%20stable/%{version}/iavf-%{version}.tar.gz
%define sha512 iavf=6a52b06373eda09824fc2674ce5a5ff488dc86331c9022faf2857c38a3002a969c6bb039271fc31e70310589701ac65d57d310d08459aa3402acbec9af1f7683

Patch0:         iavf-v4.9.1-iavf-Makefile-added-alias-for-i40evf.patch

BuildArch:      x86_64

BuildRequires:  which
BuildRequires:  kmod-devel
BuildRequires:  linux-rt-devel = %{uname_r}

Requires:       kmod
Requires:       linux-rt = %{uname_r}

Conflicts:      linux-rt < %{conflicts_ver}

%description
This Linux package contains the Intel iavf v4.8.2 driver.

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
* Thu Jan 04 2024 Roye Eshed <roye.eshed@broadcom.com> 4.9.1-1
- Package Intel driver iavf v4.9.1 for linux-rt.
