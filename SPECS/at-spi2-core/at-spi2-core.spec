%global build_if %{photon_subrelease} >= 91

Summary:        Service Provider Interface for the Assistive Technologies.
Name:           at-spi2-core
Version:        2.60.4
Release:        2%{?dist}
URL:            http://www.linuxfoundation.org/en/AT-SPI_on_D-Bus
Group:          System Environment/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        http://ftp.gnome.org/pub/gnome/sources/%{name}/2.60/%{name}-%{version}.tar.xz

Source1: license.txt
%include %{SOURCE1}

BuildRequires:  meson >= 0.50
BuildRequires:  libxml2-devel
BuildRequires:  intltool
BuildRequires:  glib-devel
BuildRequires:  dbus-devel
BuildRequires:  libX11-devel
BuildRequires:  libXtst-devel
BuildRequires:  libXext-devel
BuildRequires:  libXi-devel
BuildRequires:  gobject-introspection-devel

Requires:       dbus
Requires:       glib
Requires:       libX11
Requires:       libXtst
Requires:       libXext
Requires:       libXi

%description
The At-Spi2 Core package is a part of the GNOME Accessibility Project. It provides a Service Provider Interface for the Assistive Technologies available on the GNOME platform and a library against which applications can be linked.

%package        devel
Summary:        Header and development files
Requires:       %{name} = %{version}
Requires:       glib-devel
Requires:       dbus-devel
Requires:       libX11-devel
Requires:       libXtst-devel
Requires:       libXext-devel
Requires:       libXi-devel

%description    devel
It contains the libraries and header files to create applications

%package -n     atk
Summary:        Interfaces for accessibility support
Requires:       %{name} = %{version}-%{release}
Provides:       atk = %{version}-%{release}

%description -n atk
The ATK library provides a set of interfaces for adding accessibility
support to applications and graphical user interface toolkits.

%package -n     atk-devel
Summary:        Development files for the ATK accessibility toolkit
Requires:       atk
Requires:       gobject-introspection-devel
Provides:       atk-devel = %{version}-%{release}

%description -n atk-devel
This package includes libraries, header files, and developer documentation
needed for development of applications or toolkits which use ATK.

%package -n     at-spi2-atk
Summary:        A GTK+ module that bridges ATK to D-Bus at-spi
Requires:       atk
Requires:       %{name} = %{version}-%{release}

%description -n at-spi2-atk
This package includes a gtk-module that bridges ATK to the new
D-Bus based at-spi.

%package -n     at-spi2-atk-devel
Summary:        Development files for at-spi2-atk
Requires:       at-spi2-atk

%description -n at-spi2-atk-devel
The at-spi2-atk-devel package includes the header files for the at-spi2-atk library.

%prep
%autosetup -p1

%build
%meson \
      -Dx11=enabled \
      %{nil}

%meson_build

%install
%meson_install

%ldconfig_scriptlets

%check
%meson_test

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%{_sysconfdir}/*
%{_libexecdir}/*
%{_libdir}/libatspi*.so.*
%{_libdir}/girepository-1.0/Atspi-2.0.typelib
%{_libdir}/python3.*/site-packages/gi/overrides/Atspi.py
%{_libdir}/python3.*/site-packages/gi/overrides/__pycache__/Atspi.*

%files devel
%defattr(-,root,root)
%{_datadir}/*
%{_includedir}/at-spi-2.0/*
%{_libdir}/libatspi*.so
%{_libdir}/systemd/user/at-spi-dbus-bus.service
%{_libdir}/pkgconfig/atspi-2.pc

%files -n atk
%defattr(-,root,root)
%{_libdir}/libatk-1.0.so.*
%{_libdir}/girepository-1.0/Atk-1.0.typelib

%files -n atk-devel
%defattr(-,root,root)
%{_includedir}/atk-1.0
%{_libdir}/libatk-1.0.so
%{_libdir}/pkgconfig/atk.pc

%files -n at-spi2-atk
%defattr(-,root,root)
%dir %{_libdir}/gtk-2.0
%dir %{_libdir}/gtk-2.0/modules
%{_libdir}/gtk-2.0/modules/libatk-bridge.so
%{_libdir}/gnome-settings-daemon-3.0/gtk-modules/at-spi2-atk.desktop
%{_libdir}/libatk-bridge*.so.*

%files -n at-spi2-atk-devel
%defattr(-,root,root)
%{_includedir}/at-spi2-atk/*
%{_libdir}/libatk-bridge*.so
%{_libdir}/pkgconfig/atk-bridge-2.0.pc

%changelog
* Wed Jun 03 2026 Harinadh Dommaraju <Harinadh.Dommaraju@broadcom.com> 2.60.4-2
- Release version bump as part of libxml2/libxslt
* Tue May 26 2026 Shivani Agarwal <shivani.agarwal@broadcom.com> 2.60.4-1
- Upgrade at-spi2-core to 2.60.4
- Re-architected spec file to use standalone sub-packages (-n atk and -n atk-devel)
* Wed Jan 22 2025 Tapas Kundu <tapas.kundu@broadcom.com> 2.46.0-7
- Bump version as a part of meson upgrade
* Wed Dec 11 2024 HarinadhD <harinadh.dommaraju@broadcom.com> 2.46.0-6
- Release bump for SRP compliance
* Sat Aug 26 2023 Shreenidhi Shedi <sshedi@vmware.com> 2.46.0-5
- Add atk-devel to devel package requires
* Wed Jun 21 2023 Kuntal Nayak <nkuntal@vmware.com> 2.46.0-4
- Bump version as a part of libXi upgrade
* Wed Jun 14 2023 Shivani Agarwal <shivania2@vmware.com> 2.46.0-3
- Bump version as a part of libX11 upgrade
* Thu May 25 2023 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 2.46.0-2
- Bump version as a part of libxml2 upgrade
* Thu Dec 15 2022 Gerrit Photon <photon-checkins@vmware.com> 2.46.0-1
- Automatic Version Bump
* Mon Sep 05 2022 Shivani Agarwal <shivania2@vmware.com> 2.45.91-1
- Version update
* Fri Aug 06 2021 Alexey Makhalov <amakhalov@vmware.com> 2.40.3-1
- Version update
* Wed May 27 2015 Alexey Makhalov <amakhalov@vmware.com> 2.16.0-1
- initial version
