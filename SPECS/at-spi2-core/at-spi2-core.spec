Summary:        Service Provider Interface for the Assistive Technologies.
Name:           at-spi2-core
Version:        2.46.0
Release:        7%{?dist}
URL:            http://www.linuxfoundation.org/en/AT-SPI_on_D-Bus
Group:          System Environment/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        http://ftp.gnome.org/pub/gnome/sources/%{name}/2.46/%{name}-%{version}.tar.xz
%define sha512  at-spi2-core=633af2c02fab3b8cb02e37f929ce80dd5ce28ca5641046ef5e25cb29299530b90028e6c6f318a0c098a4270bed3eab48fb55d6967a76bfadd2520f49de47c770

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

Requires:       dbus
Requires:       glib
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
Requires:       glib-devel
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
