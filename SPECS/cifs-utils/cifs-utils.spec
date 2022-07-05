Summary:	cifs client utils
Name:		cifs-utils
Version:	6.14
Release:	1%{?dist}
License:	GPLv3
URL:		http://wiki.samba.org/index.php/LinuxCIFS_utils
Group:		Applications/Nfs-utils-client
Source0:        https://ftp.samba.org/pub/linux-cifs/cifs-utils/cifs-utils-%{version}.tar.bz2
%define sha512  cifs-utils=dd875e110988f84ac766900426e1a75c043607de1f24b87e95cd942f2f58561e1133d16466f02863643c8395fc0160df4050636d1ce0db005f2e52a592c7f0ab
Vendor:		VMware, Inc.
Distribution:	Photon
BuildRequires:  libcap-ng-devel
BuildRequires:  libtalloc-devel
Requires:       libcap-ng

%description
Cifs-utils, a package of utilities for doing and managing mounts of the Linux CIFS filesystem.

%package devel
Summary:    The libraries and header files needed for Cifs-Utils development.
Group:      Development/Libraries
Requires:   cifs-utils = %{version}-%{release}

%description devel
Provides header files needed for Cifs-Utils development.

%prep
%autosetup

%build
%configure \
    ROOTSBINDIR=/usr/sbin \
    --disable-pam \
    --disable-systemd &&
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} %{?_smp_mflags} install

%check
make %{?_smp_mflags} check

%files
%defattr(-,root,root)
%{_bindir}/*
%{_sbindir}/mount.cifs
%{_sbindir}/mount.smb3

%files devel
%defattr(-,root,root)
%{_includedir}/cifsidmap.h

%changelog
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
*	Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 6.4-2
-	GA - Bump release of all rpms
*	Mon Jan 25 2016 Divya Thaluru <dthaluru@vmware.com> 6.4-1
-	Initial build.	First version.
