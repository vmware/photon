Summary:        Utilities for configuring and managing bridge devices
Name:           bridge-utils
Version:        1.7.1
Release:        2%{?dist}
URL:            http://www.linuxfoundation.org/collaborate/workgroups/networking/bridge
Group:          System Environment/Base
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://mirrors.edge.kernel.org/pub/linux/utils/net/bridge-utils/%{name}-%{version}.tar.xz

Source1: license.txt
%include %{SOURCE1}

%description
The bridge-utils package contains a utility needed to create and manage bridge devices.
This is useful in setting up networks for a hosted virtual machine (VM).

%prep
%autosetup -p1

%build
autoconf
%configure
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install %{?_smp_mflags}

%files
%defattr(-,root,root)
%{_sbindir}/brctl
%{_mandir}/man8/*

%changelog
*   Thu Dec 12 2024 HarinadhD <harinadh.dommaraju@broadcom.com> 1.7.1-2
-   Release bump for SRP compliance
*   Thu Apr 29 2021 Gerrit Photon <photon-checkins@vmware.com> 1.7.1-1
-   Automatic Version Bump
*   Thu Apr 06 2017 Anish Swaminathan <anishs@vmware.com> 1.6-1
-   Upgraded to version 1.6
*   Mon Sep 12 2016 Alexey Makhalov <amakhalov@vmware.com> 1.5-3
-   Update patch to fix-2.
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.5-2
-   GA - Bump release of all rpms
*   Tue May 19 2015 Divya Thaluru <dthaluru@vmware.com> 1.5-1
-   Initial build.First version
