Summary:        Bluetooth utilities
Name:           bluez
Version:        5.71
Release:        1%{?dist}
License:        GPLv2+
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://github.com/bluez/bluez

Source0: http://www.kernel.org/pub/linux/bluetooth/%{name}-%{version}.tar.xz
%define sha512 %{name}=648394bbe470405aa0e2d3914474e95c122f567deaaac20a5dd74bac29fa430dfb64cdb7bdb4fb7510e62fa73e96112a97197fc212b421bf480b8d1bb24cfb5d

BuildRequires: libical-devel
BuildRequires: glib-devel >= 2.68.4
BuildRequires: dbus-devel
BuildRequires: systemd-devel

Requires: dbus
Requires: glib >= 2.68.4
Requires: libical
Requires: systemd

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
%config(noreplace) %{_datadir}/dbus-1/system.d/bluetooth.conf
%doc COPYING TODO

%files devel
%defattr(-,root,root)
%{_includedir}/bluetooth/*.h
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc

%changelog
* Tue Apr 02 2024 Nitesh Kumar <nitesh-nk.kumar@broadcom.com> 5.71-1
- Version upgrade to v5.71 to fix following CVE's:
- CVE-2023-44431, CVE-2023-51580, CVE-2023-51589,
- CVE-2023-51592 and CVE-2023-51596
* Fri Mar 22 2024 Nitesh Kumar <nitesh-nk.kumar@broadcom.com> 5.65-6
- Patched to fix CVE-2023-50229 and CVE-2023-50230
* Tue Jan 02 2024 Harinadh D <hdommaraju@vmware.com> 5.65-5
- Fix CVE-2023-45866
* Sat Oct 07 2023 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 5.65-4
- Bump version as part of glib upgrade
* Mon Jul 10 2023 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 5.65-3
- Bump version as a part of cups upgrade
* Fri May 12 2023 Nitesh Kumar <kunitesh@vmware.com> 5.65-2
- Patched to fix CVE-2023-27349
* Tue Apr 18 2023 Nitesh Kumar <kunitesh@vmware.com> 5.65-1
- Upgrade to v5.65 to fix following CVE's:
- CVE-2021-43400, CVE-2022-3637 and CVE-2022-3563
* Sun Oct 02 2022 Shreenidhi Shedi <sshedi@vmware.com> 5.58-6
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
* Wed Sep 09 2020 Gerrit Photon <photon-checkins@vmware.com> 5.55-1
- Automatic Version Bump
* Mon Jul 13 2020 Gerrit Photon <photon-checkins@vmware.com> 5.54-1
- Automatic Version Bump
* Mon Jan 6 2020 Ajay Kaher <akaher@vmware.com> 5.52-1
- Initial version
