Summary:        Mobile broadband modem manager
Name:           ModemManager
Version:        1.18.6
Release:        2%{?dist}
URL:            https://www.freedesktop.org
License:        GPLv2
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://www.freedesktop.org/software/ModemManager/ModemManager-%{version}.tar.xz
%define sha512  ModemManager=3b154d459e1196494d7f99303f88088215992aadb57a8cc66f838b068e762fa3d25f19a597922c26a138f670e1da46d627de11cf41d83ce96b3197a086f8e91b
BuildRequires:  libqmi-devel
BuildRequires:  gobject-introspection-devel
BuildRequires:  libgudev-devel
BuildRequires:  systemd-devel
BuildRequires:  systemd-libs
BuildRequires:  gcc
BuildRequires:  pkg-config
BuildRequires:  automake autoconf libtool
BuildRequires:  libxslt

%if %{with_check}
BuildRequires:  dbus-devel
%endif

Requires:       libgudev
Requires:       libqmi
Requires:       gobject-introspection

%description
ModemManager provides a unified high level API for communicating
with mobile broadband modems, regardless of the protocol used to
communicate with the actual device.

%package        devel
Summary:        Header and development files for ModemManager
Requires:       %{name} = %{version}
Requires:       libqmi-devel
Requires:       gobject-introspection-devel

%description    devel
It contains the libraries and header files for ModemManager

%prep
%autosetup

%build
%configure \
    --disable-static \
    --enable-more-warnings=no \
    --without-qmi \
    --without-mbim
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} %{?_smp_mflags} install

%check
make %{?_smp_mflags} check

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
/usr/share/ModemManager/*.conf
%{_sysconfdir}/dbus-1/system.d/org.freedesktop.ModemManager1.conf
%{_bindir}/mmcli
%{_sbindir}/ModemManager
%{_libdir}/libmm-glib.so*
%{_libdir}/girepository-1.0/ModemManager-1.0.typelib
%{_libdir}/ModemManager/*
%{_libdir}/systemd/system/ModemManager.service
%exclude %{_libdir}/debug
%{_mandir}/man1/mmcli.1.gz
%{_mandir}/man8/ModemManager.8.gz
%{_datadir}/dbus-1/*
%{_datadir}/locale/*
%{_datadir}/bash-completion/*
%{_datadir}/gir-1.0/ModemManager-1.0.gir
%exclude %{_datadir}/icons
/lib/udev/rules.d/*

%files devel
%{_includedir}/ModemManager/*
%{_includedir}/libmm-glib/*
%{_libdir}/pkgconfig/ModemManager.pc
%{_libdir}/pkgconfig/mm-glib.pc
%{_libdir}/libmm-glib.la
%{_datadir}/ModemManager/fcc-unlock.available.d/*

%changelog
*   Thu Jun 16 2022 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 1.18.6-2
-   Bump version as a part of libxslt upgrade
*   Mon Apr 18 2022 Gerrit Photon <photon-checkins@vmware.com> 1.18.6-1
-   Automatic Version Bump
*   Wed Apr 21 2021 Gerrit Photon <photon-checkins@vmware.com> 1.16.4-1
-   Automatic Version Bump
*   Mon Apr 12 2021 Gerrit Photon <photon-checkins@vmware.com> 1.16.2-1
-   Automatic Version Bump
*   Mon Dec 14 2020 Susant Sahani <ssahani@vmware.com> 1.14.2-3
-   Add build requires
*   Wed Nov 18 2020 Satya Naga Vasamsetty <svasamsetty@vmware.com> 1.14.2-2
-   Fix make check
*   Mon Aug 24 2020 Gerrit Photon <photon-checkins@vmware.com> 1.14.2-1
-   Automatic Version Bump
*   Wed Jul 22 2020 Gerrit Photon <photon-checkins@vmware.com> 1.14.0-1
-   Automatic Version Bump
*   Mon Dec 10 2018 Alexey Makhalov <amakhalov@vmware.com> 1.8.2-1
-   Initial build. First version
