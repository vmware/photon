Summary:       A set of tools to manage bluetooth devices for linux
Name:          bluez-tools
Version:       0.2.0.20140808
Release:       6%{?dist}
License:       GPL
Group:         Applications/Communication
Vendor:        VMware, Inc.
Distribution:  Photon
URL:           https://code.google.com/p/bluez-tools
Source0:       https://github.com/khvzak/bluez-tools.git/master/bluez-tools-%{version}.tar.gz
%define sha512 %{name}=d0634e24b9c9748e442971edbdbb9be0533f9ba4da3e3e6ba8db266b87f0c60e15a79fb77c2bd633014862d2dbb34f457cdb0888578d3f64d5bec2bf82633839

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
* Tue Apr 02 2024 Nitesh Kumar <nitesh-nk.kumar@broadcom.com> 0.2.0.20140808-6
- Version Bump up to consume bluez v5.71
* Fri Dec 16 2022 Nitesh Kumar <kunitesh@vmware.com> 0.2.0.20140808-5
- Version Bump up to consume bluez v5.66
* Fri Sep 16 2022 Nitesh Kumar <kunitesh@vmware.com> 0.2.0.20140808-4
- Version Bump up to consume bluez v5.65
* Thu Mar 17 2022 Nitesh Kumar <kunitesh@vmware.com> 0.2.0.20140808-3
- Version Bump up to consume bluez v5.63
* Thu Jan 14 2021 Alexey Makhalov <amakhalov@vmware.com> 0.2.0.20140808-2
- GCC-10 support.
* Mon Jan 6 2020 Ajay Kaher <akaher@vmware.com> 0.2.0.20140808-1
- Initial version
