Summary:        Service Provider Interface for the Assistive Technologies.
Name:           at-spi2-core
Version:        2.45.91
Release:        4%{?dist}
License:        LGPLv2+
URL:            http://www.linuxfoundation.org/en/AT-SPI_on_D-Bus
Group:          System Environment/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        http://ftp.gnome.org/pub/gnome/sources/%{name}/2.45/%{name}-%{version}.tar.xz
%define sha512  at-spi2-core=749039d7c0f729f6d30b5cb8b72ffd7c0072c6f41421bb57b16b975c9ec8798c860c9d73b348980df0264b2d14a45302a5de3e58ed24e0d1396be5dfdb8079e0

BuildRequires:  meson >= 0.50
BuildRequires:  libxml2-devel
BuildRequires:  intltool
BuildRequires:  glib-devel >= 2.68.4
BuildRequires:  dbus-devel
BuildRequires:  libX11-devel
BuildRequires:  libXtst-devel
BuildRequires:  libXext-devel
BuildRequires:  libXi-devel

Requires:       dbus
Requires:       glib >= 2.68.4
Requires:       libX11
Requires:       libXtst
Requires:       libXext
Requires:       libXi
Requires:       atk

%description
The At-Spi2 Core package is a part of the GNOME Accessibility Project. It provides a Service Provider Interface for the Assistive Technologies available on the GNOME platform and a library against which applications can be linked.

%package        devel
Summary:        Header and development files
Requires:       %{name} = %{version}
Requires:       glib-devel >= 2.68.4
Requires:       dbus-devel
Requires:       libX11-devel
Requires:       libXtst-devel
Requires:       libXext-devel
Requires:       libXi-devel
Requires:       atk-devel

%description    devel
It contains the libraries and header files to create applications

%prep
%autosetup -p1

%build
%meson \
      -Dx11=yes \
      %{nil}

%meson_build

%install
%meson_install

rm -rf \
    %{buildroot}%{_libdir}/libatk-1.0* \
    %{buildroot}%{_includedir}/atk-1.0/ \
    %{buildroot}%{_libdir}/pkgconfig/atk.pc

%ldconfig_scriptlets

%check
%meson_test

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%{_sysconfdir}/*
%{_libexecdir}/*
%{_libdir}/libatk-bridge*.so.*
%{_libdir}/libatspi*.so.*

%files devel
%defattr(-,root,root)
%{_datadir}/*
%{_includedir}/at-spi-2.0/*
%{_includedir}/at-spi2-atk/*
%{_libdir}/libatk-bridge*.so
%{_libdir}/libatspi*.so
%{_libdir}/gtk-2.0/modules/libatk-bridge.so
%{_libdir}/gnome-settings-daemon-3.0/gtk-modules/at-spi2-atk.desktop
%{_libdir}/systemd/user/at-spi-dbus-bus.service
%{_libdir}/pkgconfig/*.pc

%changelog
* Sat Oct 07 2023 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 2.45.91-4
- Bump version as part of glib upgrade
* Thu Jun 22 2023 Kuntal Nayak <nkuntal@vmware.com> 2.45.91-3
- Bump version as a part of libXi upgrade
* Wed Jun 14 2023 Shivani Agarwal <shivania2@vmware.com> 2.45.91-2
- Bump version as a part of libX11 upgrade
* Mon Sep 05 2022 Shivani Agarwal <shivania2@vmware.com> 2.45.91-1
- Version update
* Fri Aug 06 2021 Alexey Makhalov <amakhalov@vmware.com> 2.40.3-1
- Version update
* Wed May 27 2015 Alexey Makhalov <amakhalov@vmware.com> 2.16.0-1
- initial version
