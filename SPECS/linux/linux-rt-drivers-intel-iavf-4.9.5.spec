%global security_hardening none
%define debug_package %{nil}

Summary:        Intel iavf driver v4.9.5
Name:           linux-rt-drivers-intel-iavf
Version:        4.9.5
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
%define sha512 iavf=2e97671d1fd51b5b0017b49dcfa62854ef55a85182fcd4990d2d7faea0c3dc9532fe3896c81eabff3c30fb3b2b9573c22416adfec3a1e0f0107c44a9216fbf3a

Patch0:         iavf-v4.9.5-iavf-Makefile-added-alias-for-i40evf.patch

BuildArch:      x86_64

BuildRequires:  which
BuildRequires:  kmod-devel
BuildRequires:  linux-rt-devel = %{uname_r}

Requires:       kmod
Requires:       linux-rt = %{uname_r}

Conflicts:      linux-rt < %{conflicts_ver}

%description
This Linux package contains the Intel iavf v%{version} driver.

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
* Wed Jan 31 2024 Brennan Lamoreaux <brennan.lamoreaux@broadcom.com> 4.9.5-1
- Add new iavf driver v4.9.5
