Summary:        Bluetooth utilities
Name:           bluez
Version:        5.65
Release:        3%{?dist}
License:        GPLv2+
Group:          Applications/System
Vendor:         VMware, Inc.
Url:            https://github.com/bluez/bluez
Distribution:   Photon

Source0: http://www.kernel.org/pub/linux/bluetooth/%{name}-%{version}.tar.xz
%define sha512  %{name}=c20c09a1a75053c77d73b3ce15ac7fd321eb6df5ca1646d57c6848b87c0c9957908bc17dd928da4ef2aacfc8667877cbc7511c1ba43db839bfa9bf1fb8269907

Patch0: bluez-CVE-2023-27349.patch

BuildRequires: libical-devel
BuildRequires: glib-devel >= 2.58.3
BuildRequires: dbus-devel
BuildRequires: systemd-devel

Requires: dbus
Requires: glib >= 2.58.3
Requires: libical
Requires: systemd

%description
Utilities for use in Bluetooth applications.
The BLUETOOTH trademarks are owned by Bluetooth SIG, Inc., U.S.A.

%package        devel
Summary:        Development libraries for Bluetooth applications
Group:          Development/System
Requires: %{name} = %{version}-%{release}

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
    --disable-cups \
    --disable-manpages

%make_build

%install
%make_install %{?_smp_mflags}

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
%{_unitdir}/bluetooth.service
%config(noreplace) %{_sysconfdir}/dbus-1/system.d/bluetooth.conf
%doc COPYING TODO

%files devel
%defattr(-,root,root)
%{_includedir}/bluetooth/*.h
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc

%changelog
* Wed Nov 15 2023 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 5.65-3
- Version bump due to glib change
* Fri May 12 2023 Nitesh Kumar <kunitesh@vmware.com> 5.65-2
- Patched to fix CVE-2023-27349
* Tue Apr 18 2023 Nitesh Kumar <kunitesh@vmware.com> 5.65-1
- Upgrade to v5.65 to fix following CVE's:
- CVE-2021-43400, CVE-2022-3637 and CVE-2022-3563
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
