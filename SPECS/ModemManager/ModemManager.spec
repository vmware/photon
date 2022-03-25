Summary:        Mobile broadband modem manager
Name:           ModemManager
Version:        1.8.2
Release:        3%{?dist}
URL:            https://www.freedesktop.org
License:        GPLv2
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        https://www.freedesktop.org/software/ModemManager/ModemManager-1.8.2.tar.xz
%define sha1    %{name}=9c1377fe879a9a36a9cd937425f501d6bf8fa234

BuildRequires:  libqmi-devel
BuildRequires:  gobject-introspection-devel
BuildRequires:  systemd-devel

%if 0%{?with_check}
BuildRequires:  dbus-devel
%endif

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
%autosetup -p1

%build
%configure --disable-static --enable-more-warnings=no
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} UDEV_BASE_DIR=%{_libdir}/udev install %{?_smp_mflags}

%check
%if 0%{?with_check}
make %{?_smp_mflags} check
%endif

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_sysconfdir}/dbus-1/system.d/org.freedesktop.%{name}1.conf
%{_bindir}/mmcli
%{_sbindir}/%{name}
%{_libdir}/libmm-glib.so*
%{_libdir}/girepository-1.0/%{name}-1.0.typelib
%{_libdir}/%{name}/*
%{_mandir}/man1/mmcli.1.gz
%{_mandir}/man8/%{name}.8.gz
%{_datadir}/dbus-1/*
%{_datadir}/locale/*
%{_datadir}/bash-completion/*
%{_datadir}/gir-1.0/%{name}-1.0.gir
%{_usr}%{_udevrulesdir}/*
%{_unitdir}/%{name}.service
%exclude %dir %{_libdir}/debug
%exclude %{_datadir}/icons

%files devel
%{_includedir}/%{name}/*
%{_includedir}/libmm-glib/*
%{_libdir}/pkgconfig/%{name}.pc
%{_libdir}/pkgconfig/mm-glib.pc
%{_libdir}/libmm-glib.la

%changelog
* Fri Mar 25 2022 Shreenidhi Shedi <sshedi@vmware.com> 1.8.2-3
- Exclude debug symbols properly
* Wed Oct 23 2019 Satya Naga Vasamsetty <svasamsetty@vmware.com> 1.8.2-2
- Fix a dbus daemon make check failure
* Mon Dec 10 2018 Alexey Makhalov <amakhalov@vmware.com> 1.8.2-1
- Initial build. First version
