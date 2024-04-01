Summary:       A set of tools to manage bluetooth devices for linux
Name:          bluez-tools
Version:       0.2.0.20140808
Release:       3%{?dist}
License:       GPL
Group:         Applications/Communication
Vendor:        VMware, Inc.
Distribution:  Photon
URL:           https://code.google.com/p/bluez-tools/

Source0: https://github.com/khvzak/bluez-tools.git/master/%{name}-%{version}.tar.gz
%define sha512 %{name}=d0634e24b9c9748e442971edbdbb9be0533f9ba4da3e3e6ba8db266b87f0c60e15a79fb77c2bd633014862d2dbb34f457cdb0888578d3f64d5bec2bf82633839

BuildRequires: dbus-devel
BuildRequires: dbus-glib-devel

Requires: bluez

%description
A set of tools to manage bluetooth devices for linux.

%prep
%autosetup

%build
./autogen.sh
%configure
%make_build

%install
%make_install %{?_smp_mflags}

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
* Mon Apr 01 2024 Nitesh Kumar <nitesh-nk.kumar@broadcom.com> 0.2.0.20140808-3
- Version Bump up to consume bluez v5.71
* Tue Apr 18 2023 Nitesh Kumar <kunitesh@vmware.com> 0.2.0.20140808-2
- Version Bump up to consume bluez v5.65
* Mon Jan 6 2020 Ajay Kaher <akaher@vmware.com> 0.2.0.20140808-1
- Initial version
