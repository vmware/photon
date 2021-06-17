Summary:       A set of tools to manage bluetooth devices for linux
Name:          bluez-tools
Version:       0.2.0.20140808
Release:       2%{?dist}
License:       GPL
Group:         Applications/Communication
Vendor:        VMware, Inc.
Distribution:  Photon
URL:           https://code.google.com/p/bluez-tools
Source0:       https://github.com/khvzak/bluez-tools.git/master/bluez-tools-%{version}.tar.gz
%define sha1 %{name}=a24245523f4d87d8a11e2dd41babc1aade1e0870

Patch0:        bluez-tools-gcc-10.patch

BuildRequires: dbus-devel
BuildRequires: dbus-glib-devel

Requires:      bluez

%description
A set of tools to manage bluetooth devices for linux.

%prep
%autosetup -p1

%build
./autogen.sh
%configure
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install %{?_smp_mflags}

%files
%defattr(-,root,root)
%{_bindir}/bt-adapter
%{_bindir}/bt-agent
%{_bindir}/bt-device
%{_bindir}/bt-network
%{_bindir}/bt-obex
%{_mandir}/man1/bt-adapter.1*
%{_mandir}/man1/bt-agent.1*
%{_mandir}/man1/bt-device.1*
%{_mandir}/man1/bt-network.1*
%{_mandir}/man1/bt-obex.1*
%doc AUTHORS COPYING

%changelog
* Thu Jan 14 2021 Alexey Makhalov <amakhalov@vmware.com> 0.2.0.20140808-2
- GCC-10 support.
* Mon Jan 6 2020 Ajay Kaher <akaher@vmware.com> 0.2.0.20140808-1
- Initial version
