Summary:        DBus for systemd
Name:           dbus
Version:        1.13.18
Release:        6%{?dist}
License:        GPLv2+ or AFL
URL:            http://www.freedesktop.org/wiki/Software/dbus
Group:          Applications/File
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: http://dbus.freedesktop.org/releases/dbus/%{name}-%{version}.tar.xz
%define sha512 %{name}=93724660529fb777e2dd5207f953dd0b4c02c079293ae202ffdcabd9c4033110a7f9980b55a443770e0ea0bb8fc6b5717797d954ee268d34e13d364df0f01539

Patch0: CVE-2022-42010.patch
Patch1: CVE-2022-42011.patch
Patch2: CVE-2022-42012.patch
Patch3: CVE-2023-34969.patch

BuildRequires:  expat-devel
BuildRequires:  systemd-devel
BuildRequires:  xz-devel

Requires:       expat
Requires:       systemd
Requires:       xz

%description
The dbus package contains dbus.

%package    devel
Summary:    Header and development files
Requires:   %{name} = %{version}-%{release}
Requires:   expat-devel
%description    devel
It contains the libraries and header files to create applications

%prep
%autosetup -p1

%build
%configure \
    --docdir=%{_defaultdocdir}/%{name}-%{version} \
    --enable-libaudit=no --enable-selinux=no \
    --with-console-auth-dir=/run/console

make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install %{?_smp_mflags}
rm -f %{buildroot}%{_libdir}/*.la

%check
make %{?_smp_mflags} check

%files
%defattr(-,root,root)
%{_sysconfdir}/dbus-1
%{_bindir}/*
%{_libdir}/libdbus-1.so.*
%{_libdir}/tmpfiles.d/dbus.conf
%{_libdir}/systemd/system/*
%exclude %{_libdir}/sysusers.d
%{_libexecdir}/*
%{_docdir}/*
%{_datadir}/dbus-1

%files  devel
%defattr(-,root,root)
%{_includedir}/*
%{_datadir}/xml/dbus-1
%{_libdir}/cmake/DBus1
%dir %{_libdir}/dbus-1.0
%{_libdir}/dbus-1.0/include/
%{_libdir}/pkgconfig/*.pc
%{_libdir}/*.a
%{_libdir}/*.so

%changelog
* Mon May 05 2025 Guruswamy Basavaiah <guruswamy.basavaiah@broadcom.com> 1.13.18-6
- Version bump for expat upgrade
* Fri May 24 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 1.13.18-5
- Fix CVE-2023-34969
* Thu Feb 29 2024 Anmol Jain <anmol.jain@broadcom.com> 1.13.18-4
- Bump version as a part of expat upgrade
* Thu Oct 13 2022 Ajay Kaher <akaher@vmware.com> 1.13.18-3
- Fix CVE-2022-42010, CVE-2022-42011, CVE-2022-42012
* Sun Oct 02 2022 Shreenidhi Shedi <sshedi@vmware.com> 1.13.18-2
- Remove .la files
* Mon Jun 22 2020 Gerrit Photon <photon-checkins@vmware.com> 1.13.18-1
- Automatic Version Bump
* Wed May 06 2020 Susant Sahani <ssahani@vmware.com> 1.13.14-1
- Update to 1.13.14
* Thu Nov 15 2018 Alexey Makhalov <amakhalov@vmware.com> 1.13.6-2
- Cross compilation support
* Mon Sep 10 2018 Ajay Kaher <akaher@vmware.com> 1.13.6-1
- Update to 1.13.6
* Fri Apr 21 2017 Bo Gan <ganb@vmware.com> 1.11.12-1
- Update to 1.11.12
* Tue Dec 20 2016 Xiaolin Li <xiaolinl@vmware.com> 1.8.8-8
- Move all header files to devel subpackage.
* Fri Nov 18 2016 Anish Swaminathan <anishs@vmware.com>  1.8.8-7
- Change systemd dependency
* Wed Oct 05 2016 ChangLee <changlee@vmware.com> 1.8.8-6
- Modified %check
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.8.8-5
- GA - Bump release of all rpms
* Tue Sep 22 2015 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 1.8.8-4
- Created devel sub-package
* Thu Jun 25 2015 Sharath George <sharathg@vmware.com> 1.8.8-3
- Remove debug files.
* Mon May 18 2015 Touseef Liaqat <tliaqat@vmware.com> 1.8.8-2
- Update according to UsrMove.
* Sun Apr 06 2014 Sharath George <sharathg@vmware.com> 1.8.8
- Initial build. First version
