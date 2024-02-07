Summary:        Bluetooth utilities
Name:           bluez
Version:        5.66
Release:        5%{?dist}
License:        GPLv2+
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            http://www.bluez.org

Source0: http://www.kernel.org/pub/linux/bluetooth/bluez-%{version}.tar.xz
%define sha512 %{name}=ed0994932687eacf27207867366671b323671f5d5199daf36ea5eff8f254f2bc99ef989ef7df9883b35c06f2af60452be8bad0a06109428a4717cf2b247b4865

Patch0: bluez-CVE-2023-27349.patch
Patch1: bluez-CVE-2023-45866.patch

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

%files devel
%defattr(-,root,root)
%{_includedir}/bluetooth/*.h
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%{_datadir}/man/*

%changelog
* Wed Feb 07 2024 Harinadh D <hdommaraju@vmware.com> 5.66-5
- Fix CVE-2023-45866
* Mon Jul 10 2023 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 5.66-4
- Bump version as a part of cups upgrade
* Fri May 12 2023 Nitesh Kumar <kunitesh@vmware.com> 5.66-3
- Patched to fix CVE-2023-27349
* Thu Dec 22 2022 Shreenidhi Shedi <sshedi@vmware.com> 5.66-2
- Bump version as a part of readline upgrade
* Fri Dec 16 2022 Nitesh Kumar <kunitesh@vmware.com> 5.66-1
- Version upgrade to v5.66
* Sun Sep 18 2022 Shreenidhi Shedi <sshedi@vmware.com> 5.65-2
- Remove .la files
* Fri Sep 16 2022 Nitesh Kumar <kunitesh@vmware.com> 5.65-1
- Version upgrade to v5.65
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
