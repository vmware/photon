Summary:       USB Utils
Name:          usbutils
Version:       014
Release:       1%{?dist}
License:       GPLv2+
URL:           http://linux-usb.sourceforge.net
Group:         Applications/System
Vendor:        VMware, Inc.
Distribution:  Photon
Source0:       https://www.kernel.org/pub/linux/utils/usb/usbutils/%{name}-%{version}.tar.xz
%define sha512   usbutils=43c9f6ed14f8d01e014ef39a5d50b3b09031c6bda8261e0945b4cb4287c9107104175b386c2adc61dc7f9f476afb30f9a647a6ece6dee26b4133a4f10af72792
Source1:       usb.ids
BuildRequires: libusb-devel
BuildRequires: pkg-config
BuildRequires: systemd
Requires:      libusb
BuildRequires: systemd-devel

%description
The USB Utils package contains an utility used to display information
about USB buses in the system and the devices connected to them.

%prep
%autosetup -n %{name}-%{version}

%build
%configure \
            --disable-zlib &&
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} %{?_smp_mflags} install
mkdir -p %{buildroot}%{_datadir}/misc/
install -p -m 0644 %{SOURCE1} %{buildroot}%{_datadir}/misc/

%files
%defattr(-,root,root,-)
%{_bindir}/usb-devices
%{_bindir}/lsusb
%{_bindir}/lsusb.py
%{_bindir}/usbhid-dump
%{_mandir}/*/*
%{_datadir}/misc/usb.ids

%changelog
*   Tue Apr 19 2022 Gerrit Photon <photon-checkins@vmware.com> 014-1
-   Automatic Version Bump
*   Thu Apr 29 2021 Gerrit Photon <photon-checkins@vmware.com> 013-1
-   Automatic Version Bump
*   Thu Jul 09 2020 Gerrit Photon <photon-checkins@vmware.com> 012-1
-   Automatic Version Bump
*   Mon Sep 10 2018 Michelle Wang <michellew@vmware.com>  010-1
-   Update version to 010.
*   Fri Nov 18 2016 Anish Swaminathan <anishs@vmware.com>  008-4
-   Change systemd dependency
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 008-3
-   GA - Bump release of all rpms
*   Tue May 10 2016 Nick Shi <nshi@vmware.com> - 008-2
-   Update Source0 to the correct link
*   Fri May 06 2016 Nick Shi <nshi@vmware.com> - 008-1
-   Initial version
