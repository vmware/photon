Summary:    cifs client utils
Name:       cifs-utils
Version:    7.0
Release:    1%{?dist}
License:    GPLv3
URL:        http://wiki.samba.org/index.php/LinuxCIFS_utils
Group:      Applications/Nfs-utils-client
Vendor:     VMware, Inc.
Distribution:   Photon

Source0:        https://ftp.samba.org/pub/linux-cifs/cifs-utils/cifs-utils-%{version}.tar.bz2
%define sha512  cifs-utils=4c57741af0c4567a78f352c73caca998881666a5ed36536275cfa775efd66ff1a44ebe539a8ed96c409c5b08a1378266964ce667a27e9fc7f2d43999c63dd0eb

BuildRequires:  libcap-ng-devel
BuildRequires:  libtalloc-devel

Requires:       libcap-ng

%description
Cifs-utils, a package of utilities for doing and managing mounts of the Linux CIFS filesystem.

%package devel
Summary:    The libraries and header files needed for Cifs-Utils development.
Group:      Development/Libraries
Requires:   %{name} = %{version}-%{release}

%description devel
Provides header files needed for Cifs-Utils development.

%prep
%autosetup

%build
%configure \
    ROOTSBINDIR=%{_sbindir} \
    --disable-pam \
    --disable-systemd

%make_build

%install
%make_install %{?_smp_mflags}

%check
%make_build check

%files
%defattr(-,root,root)
%{_bindir}/*
%{_sbindir}/mount.cifs
%{_sbindir}/mount.smb3

%files devel
%defattr(-,root,root)
%{_includedir}/cifsidmap.h

%changelog
*       Thu Dec 15 2022 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 7.0-1
-       Upgrade to version 7.0
*       Tue Dec 06 2022 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 6.14-2
-       Bump version as a part of libtalloc upgrade
*       Mon Apr 18 2022 Gerrit Photon <photon-checkins@vmware.com> 6.14-1
-       Automatic Version Bump
*       Mon Apr 12 2021 Gerrit Photon <photon-checkins@vmware.com> 6.13-1
-       Automatic Version Bump
*       Wed Sep 09 2020 Gerrit Photon <photon-checkins@vmware.com> 6.11-1
-       Automatic Version Bump
*       Wed Jul 08 2020 Gerrit Photon <photon-checkins@vmware.com> 6.10-1
-       Automatic Version Bump
*       Fri Sep 07 2018 Ajay Kaher <akaher@vmware.com> 6.8-1
-       Upgraded to version 6.8
*       Thu Apr 06 2017 Anish Swaminathan <anishs@vmware.com> 6.7-1
-       Upgraded to version 6.7
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 6.4-2
-   GA - Bump release of all rpms
*   Mon Jan 25 2016 Divya Thaluru <dthaluru@vmware.com> 6.4-1
-   Initial build.  First version.
