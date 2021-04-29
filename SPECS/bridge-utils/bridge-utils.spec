Summary:        Utilities for configuring and managing bridge devices
Name:           bridge-utils
Version:        1.7.1
Release:        1%{?dist}
License:        GPLv2+
URL:            http://www.linuxfoundation.org/collaborate/workgroups/networking/bridge
Group:          System Environment/Base
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        http://sourceforge.net/projects/bridge/files/bridge/%{name}-%{version}.tar.xz
%define sha1    bridge-utils=07266dff2bf31a24fc912314b6764251ce645a39

%description
The bridge-utils package contains a utility needed to create and manage bridge devices.
This is useful in setting up networks for a hosted virtual machine (VM).

%prep
%setup -q

%build
autoconf
%configure \
	--prefix=%{_prefix}
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install

%files
%defattr(-,root,root)
%{_sbindir}/brctl
%{_mandir}/man8/*

%changelog
*       Thu Apr 29 2021 Gerrit Photon <photon-checkins@vmware.com> 1.7.1-1
-       Automatic Version Bump
*       Thu Apr 06 2017 Anish Swaminathan <anishs@vmware.com> 1.6-1
-       Upgraded to version 1.6
*	Mon Sep 12 2016 Alexey Makhalov <amakhalov@vmware.com> 1.5-3
-	Update patch to fix-2.
*	Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.5-2
-	GA - Bump release of all rpms
*	Tue May 19 2015 Divya Thaluru <dthaluru@vmware.com> 1.5-1
-	Initial build.	First version
