Summary:        A library providing GObject bindings for libudev
Name:           libgudev
Version:        236
Release:        1%{?dist}
License:        LGPL2.1
URL:            https://git.gnome.org/browse/libgudev/
Source0:        https://git.gnome.org/browse/%{name}/snapshot/%{name}-%{version}.tar.xz
%define sha1 libgudev=24a73f68868c0e42940663a64bea952d29a71d17
Group:          System Environment/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon

BuildRequires:  glib >= 2.22.0
BuildRequires:  glib-devel
BuildRequires:  gnome-common
BuildRequires:  gobject-introspection-devel
BuildRequires:  gtk-doc
BuildRequires:  pkg-config
BuildRequires:  systemd-devel
BuildRequires:  which
BuildRequires:  meson
BuildRequires:  ninja-build

Requires:       systemd

%description
This is libgudev, a library providing GObject bindings for libudev. It
used to be part of udev, and now is a project on its own.

%package devel
Summary:        Header and development files for libgudev
Requires:       %{name} = %{version}
Requires:       glib-devel

%description devel
libgudev-devel package contains header files for building gudev applications.

%prep
%autosetup -p1

%build
%meson -Dgtk_doc=false -Dtests=disabled -Dvapi=disabled
%meson_build

%install
%meson_install

%check
%meson_test

%ldconfig_scriptlets

%files
%defattr(-,root,root)
%{_libdir}/*.so.*
%{_libdir}/girepository-1.0/GUdev-1.0.typelib
%{_datadir}/gir-1.0/GUdev-1.0.gir

%files devel
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/gudev-1.0.pc

%changelog
* Mon Aug 02 2021 Susant Sahani <ssahani@vmware.com> 236-1
- Use autosetup, ldconfig scriptlets, switch to meson
- and version bump
* Mon Sep 21 2020 Gerrit Photon <photon-checkins@vmware.com> 234-1
- Automatic Version Bump
* Mon Jun 22 2020 Gerrit Photon <photon-checkins@vmware.com> 233-1
- Automatic Version Bump
* Sun Sep 30 2018 Bo Gan <ganb@vmware.com> 232-1
- Update to 232
* Mon Apr 10 2017 Harish Udaiya kumar <hudaiyakumar@vmware.com> 231-1
- Updated to version 231.
* Fri Nov 18 2016 Anish Swaminathan <anishs@vmware.com>  230-4
- Change systemd dependency
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 230-3
- GA - Bump release of all rpms
* Thu Aug 13 2015 Vinay Kulkarni <kulkarniv@vmware.com> 230-2
- Split header files into devel package.
* Tue Aug 11 2015 Vinay Kulkarni <kulkarniv@vmware.com> 230-1
- Add libgudev v230
