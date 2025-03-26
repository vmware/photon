Name:           kexec-tools
Summary:        The kexec kdump tools
Version:        2.0.25
Release:        4%{?dist}
Group:          Applications/System
Url:            https://www.kernel.org/doc/Documentation/kdump/kdump.txt
Source0:        https://www.kernel.org/pub/linux/utils/kernel/kexec/%{name}-%{version}.tar.xz

Source1: license.txt
%include %{SOURCE1}
Patch0:         kexec-tools-disable-test.patch
Vendor:         VMware, Inc.
Distribution:   Photon
BuildRequires:  zlib-devel
BuildRequires:  zlib
Requires:       zlib

%description
kexec-tools allows booting of a linux kernel from the context of a running kernel using kernel's kexec feature

%prep
%autosetup -p1

%build
%configure
make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot} %{?_smp_mflags}

%files
%{_sbindir}/*
%{_mandir}/man8/*
%doc News
%doc COPYING
%doc TODO

%changelog
*   Wed Dec 11 2024 Tapas Kundu <tapas.kundu@broadcom.com> 2.0.25-4
-   Release bump for SRP compliance
*   Mon Apr 17 2023 Brennan Lamoreaux <blamoreaux@vmware.com> 2.0.25-3
-   Enable build for ARM
*   Fri Apr 14 2023 Shreenidhi Shedi <sshedi@vmware.com> 2.0.25-2
-   Bump version as a part of zlib upgrade
*   Wed Aug 17 2022 Gerrit Photon <photon-checkins@vmware.com> 2.0.25-1
-   Automatic Version Bump
*   Mon Apr 18 2022 Gerrit Photon <photon-checkins@vmware.com> 2.0.24-1
-   Automatic Version Bump
*   Mon May 03 2021 Gerrit Photon <photon-checkins@vmware.com> 2.0.22-1
-   Automatic Version Bump
*   Tue Apr 13 2021 Gerrit Photon <photon-checkins@vmware.com> 2.0.21-1
-   Automatic Version Bump
*   Fri Jan 15 2021 Alexey Makhalov <amakhalov@vmware.com> 2.0.20-2
-   GCC-10 support.
*   Mon Jun 22 2020 Gerrit Photon <photon-checkins@vmware.com> 2.0.20-1
-   Automatic Version Bump
*   Mon Oct 22 2018 Ajay Kaher <akaher@vmware.com> 2.0.17-2
-   Adding BuildArch
*   Mon Sep 10 2018 Alexey Makhalov <amakhalov@vmware.com> 2.0.17-1
-   Version update to fix compilation issue againts glibc-2.28
*   Mon Apr 03 2017 Divya Thaluru <dthaluru@vmware.com> 2.0.14-1
-   Updated to version 2.0.14
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.0.11-2
-   GA - Bump release of all rpms
*   Fri Feb 26 2016 Anish Swaminathan <anishs@vmware.com>  2.0.11-1
-   Initial version.
