Summary:        Mobile broadband modem manager
Name:           ModemManager
Version:        1.8.2
Release:        1%{?dist}
URL:            https://www.freedesktop.org
License:        GPLv2
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://www.freedesktop.org/software/ModemManager/ModemManager-1.8.2.tar.xz
%define sha1    ModemManager=9c1377fe879a9a36a9cd937425f501d6bf8fa234
BuildRequires:  libqmi-devel
BuildRequires:  gobject-introspection-devel
Requires:       libqmi
Requires:       gobject-introspection
%description
ModemManager provides a unified high level API for communicating
with mobile broadband modems, regardless of the protocol used to
communicate with the actual device.

%package    devel
Summary:    Header and development files for ModemManager
Requires:   %{name} = %{version}
Requires:   libqmi-devel
Requires:   gobject-introspection-devel
%description    devel
It contains the libraries and header files for ModemManager

%prep
%setup -q

%build
%configure --disable-static --enable-more-warnings=no
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install

%check
make  %{?_smp_mflags} check

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_sysconfdir}/dbus-1/system.d/org.freedesktop.ModemManager1.conf
%{_bindir}/mmcli
%{_sbindir}/ModemManager
%{_libdir}/libmm-glib.so*
%{_libdir}/girepository-1.0/ModemManager-1.0.typelib
%{_libdir}/ModemManager/*
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

%changelog
*   Mon Dec 10 2018 Alexey Makhalov <amakhalov@vmware.com> 1.8.2-1
-   Initial build. First version
