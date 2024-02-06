Summary:        Glib interfaces to D-Bus API
Name:           dbus-glib
Version:        0.112
Release:        5%{?dist}
License:        AFL and GPLv2+
Group:          System Environment/Libraries
URL:            https://dbus.freedesktop.org/doc/dbus-glib
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        http://dbus.freedesktop.org/releases/dbus-glib/%{name}-%{version}.tar.gz
%define sha512 %{name}=7c9f393f065dfb3d698f35e6554caf15fe539f5dd52d2b2bb6ed1770e130f5dab8e45379232520301455bae9bb77e25a109faf175153fcd4b9dd11d7de4a546e

BuildRequires:  glib-devel
BuildRequires:  dbus-devel
BuildRequires:  systemd-devel

Requires:       glib
Requires:       dbus
Requires:       libffi
Requires:       systemd
Provides:       pkgconfig(dbus-glib-1)

%description
The D-Bus GLib package contains GLib interfaces to the D-Bus API.

%package devel
Summary:    Libraries and headers for the D-Bus GLib bindings
Requires:   glib-devel
Requires:   dbus-devel
Requires:   %{name} = %{version}-%{release}

%description devel
Headers and static libraries for the D-Bus GLib bindings

%prep
%autosetup -p1

%build
%configure \
  --disable-static \
  --disable-gtk-doc

%make_build

%install
%make_install %{?_smp_mflags}

%if 0%{?with_check}
%check
make %{?_smp_mflags} check
%endif

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_sysconfdir}/bash_completion.d/*
%{_bindir}/*
%{_libdir}/*.so.*
%{_libexecdir}/*
%{_mandir}/man1/*
%{_datadir}/gtk-doc/*

%files devel
%defattr(-,root,root)
%{_includedir}/dbus-1.0/dbus/*.h
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc

%changelog
* Wed Feb 07 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 0.112-5
- Bump version as a part of dbus upgrade
* Wed Sep 06 2023 Shreenidhi Shedi <sshedi@vmware.com> 0.112-4
- Add URL to spec header
* Sun Aug 07 2022 Shreenidhi Shedi <sshedi@vmware.com> 0.112-3
- Remove .la files
* Tue May 10 2022 Shreenidhi Shedi <sshedi@vmware.com> 0.112-2
- Bump version as a part of libffi upgrade
* Mon Apr 12 2021 Gerrit Photon <photon-checkins@vmware.com> 0.112-1
- Automatic Version Bump
* Mon Dec 14 2020 Susant Sahani<ssahani@vmware.com> 0.110-2
- Add build requres and requires.
* Mon Sep 10 2018 Ajay Kaher <akaher@vmware.com> 0.110-1
- Upgraded to 0.110
* Wed May 03 2017 Bo Gan <ganb@vmware.com> 0.108-1
- Update to 0.108
* Wed Oct 05 2016 ChangLee <changlee@vmware.com> 0.106-5
- Modified %check
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 0.106-4
- GA - Bump release of all rpms
* Mon Feb 22 2016 XIaolin Li <xiaolinl@vmware.com> 0.106-1
- Updated to version 0.106
* Thu Jan 28 2016 Anish Swaminathan <anishs@vmware.com> 0.104-3
- Add requires to dbus-glib-devel
* Tue Sep 22 2015 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 0.104-2
- Updated build requires after creating devel package for dbus
* Tue Jun 23 2015 Divya Thaluru <dthaluru@vmware.com> 0.104-1
- Initial build.
