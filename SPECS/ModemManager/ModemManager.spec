Summary:        Mobile broadband modem manager
Name:           ModemManager
Version:        1.18.12
Release:        3%{?dist}
URL:            https://www.freedesktop.org
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://www.freedesktop.org/software/ModemManager/%{name}-%{version}.tar.xz

Source1: license.txt
%include %{SOURCE1}

BuildRequires:  libqmi-devel
BuildRequires:  gobject-introspection-devel
BuildRequires:  libgudev-devel
BuildRequires:  systemd-devel
BuildRequires:  gcc
BuildRequires:  pkg-config
BuildRequires:  automake
BuildRequires:  autoconf
BuildRequires:  libtool
BuildRequires:  libxslt-devel

%if 0%{?with_check}
BuildRequires:  dbus-devel
%endif

Requires:       systemd
Requires:       glib
Requires:       libgudev
Requires:       libqmi
Requires:       gobject-introspection

%description
%{name} provides a unified high level API for communicating
with mobile broadband modems, regardless of the protocol used to
communicate with the actual device.

%package        devel
Summary:        Header and development files for %{name}
Requires:       %{name} = %{version}-%{release}
Requires:       libqmi-devel
Requires:       gobject-introspection-devel

%description    devel
It contains the libraries and header files for %{name}

%prep
%autosetup -p1

%build
%configure \
    --disable-static \
    --enable-more-warnings=no \
    --without-qmi \
    --without-mbim

%make_build

%install
%make_install UDEV_BASE_DIR=%{_libdir}/udev %{?_smp_mflags}

%if 0%{?with_check}
%check
make %{?_smp_mflags} check
%endif

%clean
rm -rf %{buildroot}/*

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_datadir}/%{name}/*.conf
%{_sysconfdir}/dbus-1/system.d/org.freedesktop.ModemManager1.conf
%{_bindir}/mmcli
%{_sbindir}/%{name}
%{_libdir}/*.so.*
%{_libdir}/girepository-1.0/%{name}-1.0.typelib
%{_libdir}/%{name}/*
%{_unitdir}/%{name}.service
%{_mandir}/man1/mmcli.1.gz
%{_mandir}/man8/%{name}.8.gz
%{_datadir}/dbus-1/*
%{_datadir}/locale/*
%{_datadir}/bash-completion/*
%{_datadir}/gir-1.0/%{name}-1.0.gir
%{_udevrulesdir}/*
%exclude %{_datadir}/icons
%exclude %dir %{_libdir}/debug

%files devel
%defattr(-,root,root)
%{_libdir}/*.so
%{_includedir}/%{name}/*
%{_includedir}/libmm-glib/*
%{_libdir}/pkgconfig/%{name}.pc
%{_libdir}/pkgconfig/mm-glib.pc
%{_datadir}/%{name}/fcc-unlock.available.d/*
%{_datadir}/%{name}/connection.available.d/*

%changelog
* Thu Dec 12 2024 Ajay Kaher <ajay.kaher@broadcom.com> 1.18.12-3
- Release bump for SRP compliance
* Tue Jan 03 2023 Guruswamy Basavaiah <bguruswamy@vmware.com> 1.18.12-2
- Bump release as a part of libgudev upgrade to 237-1
* Fri Dec 23 2022 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 1.18.12-1
- Update to v1.18.12
* Fri Oct 07 2022 Shreenidhi Shedi <sshedi@vmware.com> 1.18.10-3
- Bump version as a part of libxslt upgrade
* Sun Aug 07 2022 Shreenidhi Shedi <sshedi@vmware.com> 1.18.10-2
- Remove .la files
* Mon Jul 11 2022 Gerrit Photon <photon-checkins@vmware.com> 1.18.10-1
- Automatic Version Bump
* Wed Jun 22 2022 Shreenidhi Shedi <sshedi@vmware.com> 1.18.6-3
- Fix binary path
* Thu Jun 16 2022 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 1.18.6-2
- Bump version as a part of libxslt upgrade
* Mon Apr 18 2022 Gerrit Photon <photon-checkins@vmware.com> 1.18.6-1
- Automatic Version Bump
* Wed Apr 21 2021 Gerrit Photon <photon-checkins@vmware.com> 1.16.4-1
- Automatic Version Bump
* Mon Apr 12 2021 Gerrit Photon <photon-checkins@vmware.com> 1.16.2-1
- Automatic Version Bump
* Mon Dec 14 2020 Susant Sahani <ssahani@vmware.com> 1.14.2-3
- Add build requires
* Wed Nov 18 2020 Satya Naga Vasamsetty <svasamsetty@vmware.com> 1.14.2-2
- Fix make check
* Mon Aug 24 2020 Gerrit Photon <photon-checkins@vmware.com> 1.14.2-1
- Automatic Version Bump
* Wed Jul 22 2020 Gerrit Photon <photon-checkins@vmware.com> 1.14.0-1
- Automatic Version Bump
* Mon Dec 10 2018 Alexey Makhalov <amakhalov@vmware.com> 1.8.2-1
- Initial build. First version
