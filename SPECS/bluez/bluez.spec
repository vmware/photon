Summary:        Bluetooth utilities
Name:           bluez
Version:        5.64
Release:        1%{?dist}
License:        GPLv2+
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            http://www.bluez.org
Source0:        http://www.kernel.org/pub/linux/bluetooth/bluez-%{version}.tar.xz
%define sha512    %{name}=f11f9974b29c5c6fce3890d7e42425c1cb02e42c1b8f49c5cc4b249234e67b64317d0e5e82721e2fbf1b53269c8569a9c869d59ce42b5e927f6622f0753e53cd

BuildRequires:  libical-devel
BuildRequires:  glib-devel
BuildRequires:  dbus-devel
BuildRequires:  systemd-devel
BuildRequires:  python3-docutils

Requires:       dbus
Requires:       glib
Requires:       libical
Requires:       systemd
Requires:       python3-docutils

%description
Utilities for use in Bluetooth applications.
The BLUETOOTH trademarks are owned by Bluetooth SIG, Inc., U.S.A.

%package        devel
Summary:        Development libraries for Bluetooth applications
Group:          Development/System
Requires:       %{name} = %{version}-%{release}

%description    devel
bluez-devel contains development libraries and headers for
use in Bluetooth applications.

%prep
%autosetup -p1

%build
%configure \
	--enable-tools \
	--enable-library \
	--enable-usb \
	--enable-threads \
	--enable-monitor \
	--enable-obex \
	--enable-systemd \
	--enable-experimental \
	--enable-deprecated \
	--disable-cups
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install %{?_smp_mflags}

%check
make %{?_smp_mflags} -k check

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_bindir}/*
%{_libexecdir}/bluetooth/obexd
%{_libexecdir}/bluetooth/bluetoothd
%{_datadir}/zsh/site-functions/_bluetoothctl
%{_libdir}/*.so.*
%{_libdir}/libbluetooth.la
%{_datadir}/dbus-1/system-services/org.bluez.service
%{_datadir}/dbus-1/services/org.bluez.obex.service
%{_libdir}/systemd/user/obex.service
%{_libdir}/systemd/system/bluetooth.service
%config(noreplace) %{_sysconfdir}/dbus-1/system.d/bluetooth.conf
%doc COPYING TODO

%files devel
%{_includedir}/bluetooth/*.h
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%{_datadir}/man/*

%changelog
* Mon Apr 18 2022 Gerrit Photon <photon-checkins@vmware.com> 5.64-1
- Automatic Version Bump
* Tue Mar 15 2022 Nitesh Kumar <kunitesh@vmware.com> 5.63-1
- Version upgrade to 5.63, Address CVE-2021-3658
* Fri Dec 03 2021 Nitesh Kumar <kunitesh@vmware.com> 5.58-2
- Patched to fix CVE-2021-41229
* Tue Apr 13 2021 Gerrit Photon <photon-checkins@vmware.com> 5.58-1
- Automatic Version Bump
* Mon Apr 12 2021 Gerrit Photon <photon-checkins@vmware.com> 5.56-1
- Automatic Version Bump
* Wed Sep 09 2020 Gerrit Photon <photon-checkins@vmware.com> 5.55-1
- Automatic Version Bump
* Mon Jul 13 2020 Gerrit Photon <photon-checkins@vmware.com> 5.54-1
- Automatic Version Bump
* Mon Jan 6 2020 Ajay Kaher <akaher@vmware.com> 5.52-1
- Initial version
