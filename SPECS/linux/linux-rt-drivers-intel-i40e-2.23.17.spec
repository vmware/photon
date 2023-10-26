%global security_hardening none
%define debug_package %{nil}

Summary:        Intel i40e driver v2.23.17
Name:           linux-rt-drivers-intel-i40e
Version:        2.23.17
Release:        1%{?linuxrt_kernelsubrelease}%{?dist}
License:        GPLv2
URL:            https://sourceforge.net/projects/e1000
Group:          System Environment/Kernel
Vendor:         VMware, Inc.
Distribution:   Photon

%define uname_r %{LINUX_RT_KERNEL_VERSION}-%{LINUX_RT_KERNEL_RELEASE}
%define _modulesdir /lib/modules/%{uname_r}-rt
%define conflicts_ver 6.1.62-9%{?dist}

Source0:    https://sourceforge.net/projects/e1000/files/i40e%20stable/%{version}/i40e-%{version}.tar.gz
%define sha512 i40e=5dbe5186f23d14aac185f74283377d9bfc0837ab16b145a107f735d5439a207e27db871e278656cd06ba595f426d7095a294d39110df5ad6b30ea9f6d3a2a3a7

Patch0:         i40e-v2.23.17-Add-support-for-gettimex64-interface.patch
Patch1:         i40e-v2.23.17-i40e-Make-i40e-driver-honor-default-and-user-defined.patch

BuildArch:      x86_64

BuildRequires:  which
BuildRequires:  kmod-devel
BuildRequires:  linux-rt-devel = %{uname_r}

Requires:       kmod
Requires:       linux-rt = %{uname_r}

Conflicts:      linux-rt < %{conflicts_ver}

%description
This Linux package contains the Intel i40e v2.22.18 driver.

%package docs
Summary:        Kernel docs
Group:          System Environment/Kernel
Conflicts:      linux-rt-docs < %{conflicts_ver}
%description docs
This Linux package contains the Linux kernel doc files including files that
were left unpackaged from Linux-RT in the %{_mandir}.

%prep

%autosetup -p1 -n i40e-%{version}

%build

make -C src KSRC=%{_modulesdir}/build %{?_smp_mflags}

%install

make -C src KSRC=%{_modulesdir}/build INSTALL_MOD_PATH=%{buildroot} \
    INSTALL_MOD_DIR=extra/i40e-%{version} MANDIR=%{_mandir} \
    modules_install mandocs_install %{?_smp_mflags}

find %{buildroot}%{_modulesdir} -name *.ko -type f -print0 | xargs -0 xz

%post
/sbin/depmod -a %{uname_r}-rt

%files
%defattr(-,root,root)
%dir %{_modulesdir}/extra/i40e-%{version}
%{_modulesdir}/extra/i40e-%{version}/i40e.ko.xz

%files docs
%defattr(-,root,root)
%{_mandir}/*

%changelog
* Thu Jan 04 2024 Roye Eshed <roye.eshed@broadcom.com> 2.23.17-1
- Package Intel driver i40e v2.23.17 for linux-rt.
