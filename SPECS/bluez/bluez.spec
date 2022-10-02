Summary:        Bluetooth utilities
Name:           bluez
Version:        5.58
Release:        6%{?dist}
License:        GPLv2+
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        http://www.kernel.org/pub/linux/bluetooth/bluez-%{version}.tar.xz
%define sha512  %{name}=159b554e0afd56af5da6f8333383f2fdf96d77a0e82d762bf4b37786e7312b7e61fbbae0f18b26442a606e0a232f48e0f45a4b38b95de36c7daf384f582315a3

Patch0:         bluez-CVE-2021-41229.patch
Patch1:         bluez-CVE-2021-3658.patch
Patch2:         bluez-CVE-2022-0204.patch
Patch3:         bluez-CVE-2022-39176_39177-1.patch
Patch4:         bluez-CVE-2022-39176_39177-2.patch
Patch5:         bluez-CVE-2022-39176_39177-3.patch

BuildRequires:  libical-devel
BuildRequires:  glib-devel
BuildRequires:  dbus-devel
BuildRequires:  systemd-devel

Requires:       dbus
Requires:       glib
Requires:       libical
Requires:       systemd

%description
Utilities for use in Bluetooth applications.
The BLUETOOTH trademarks are owned by Bluetooth SIG, Inc., U.S.A.

%package	devel
Summary:	Development libraries for Bluetooth applications
Group:		Development/System
Requires: %{name} = %{version}-%{release}

%description	devel
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
%{_datadir}/dbus-1/system-services/org.bluez.service
%{_datadir}/dbus-1/services/org.bluez.obex.service
%{_libdir}/systemd/user/obex.service
/lib/systemd/system/bluetooth.service
%config(noreplace) %{_sysconfdir}/dbus-1/system.d/bluetooth.conf
%doc COPYING TODO

%files devel
%{_includedir}/bluetooth/*.h
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%{_datadir}/man/*

%changelog
* Mon Oct 03 2022 Shreenidhi Shedi <sshedi@vmware.com> 5.58-6
- Remove .la files
* Mon Sep 12 2022 Nitesh Kumar <kunitesh@vmware.com> 5.58-5
- Patched to fix CVE-2022-39176, CVE-2022-39177
* Tue Mar 22 2022 Nitesh Kumar <kunitesh@vmware.com> 5.58-4
- Patched to fix CVE-2022-0204
* Tue Mar 15 2022 Nitesh Kumar <kunitesh@vmware.com> 5.58-3
- Patched to fix CVE-2021-3658
* Fri Dec 03 2021 Nitesh Kumar <kunitesh@vmware.com> 5.58-2
- Patched to fix CVE-2021-41229
* Mon Jun 28 2021 Nitesh Kumar <kunitesh@vmware.com> 5.58-1
- Upgrade to 5.58, Fixes for CVE-2021-0129
* Fri Oct 23 2020 Ajay Kaher <akaher@vmware.com> 5.52-3
- Fix CVE-2020-27153
* Mon Mar 23 2020 Ajay Kaher <akaher@vmware.com> 5.52-2
- Fix CVE-2020-0556
* Mon Jan 6 2020 Ajay Kaher <akaher@vmware.com> 5.52-1
- Initial version
