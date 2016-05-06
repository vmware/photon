Summary:       USB Utils
Name:          usbutils
Version:       008
Release:       1%{?dist}
License:       GPLv2+
URL:           http://linux-usb.sourceforge.net
Group:         Applications/System
Vendor:        VMware, Inc.
Distribution:  Photon
Source0:       http://downloads.sourceforge.net/linux-usb/%{name}-%{version}.tar.xz
%define sha1 usbutils=233dee6cd6829476be778554984045663b568b18
Source1:       usb.ids
BuildRequires: libusb-devel
BuildRequires: pkg-config
BuildRequires: systemd
Requires:      libusb
BuildRequires: systemd

%description
The USB Utils package contains an utility used to display information 
about USB buses in the system and the devices connected to them.

%prep
%setup -q -n %{name}-%{version}

%build
./configure --prefix=/usr \
            --datadir=/usr/share/misc \
            --disable-zlib &&
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install
mkdir -p %{buildroot}%{_datadir}/misc/
install -p -m 0644 %{SOURCE1} %{buildroot}%{_datadir}/misc/

%files
%defattr(-,root,root,-)
%{_bindir}/usb-devices
%{_bindir}/lsusb
%{_bindir}/lsusb.py
%{_bindir}/usbhid-dump
%{_mandir}/*/*
%{_datadir}/pkgconfig/usbutils.pc
%{_datadir}/misc/usb.ids

%changelog
* Fri May 06 2016 Nick Shi <nshi@vmware.com> - 008-1
- Initial version

