Summary:        Configure and introspect the state of the network
Name:           network-config-manager
Version:        0.7
Release:        1%{?dist}
License:        Apache 2.0
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://github.com/vmware/network-config-manager

Source0: https://github.com/vmware/network-config-manager/archive/%{name}-%{version}.tar.gz
%define sha512 %{name}-%{version}=d24accdc621fa96145123fe5f0815730fd3412ea9b39a3f1081fd3b1b3e3b74b75a813f961d1dad5f90484bbc7e7a674bf093a03e042b5f2fdce8b4afbf515e2

BuildRequires: glib-devel
BuildRequires: json-c-devel
BuildRequires: meson
BuildRequires: systemd-devel
BuildRequires: libyaml-devel
BuildRequires: libmnl-devel
BuildRequires: libnftnl-devel
BuildRequires: nftables-devel

Requires: json-c
Requires: libyaml
Requires: systemd
Requires: glib
Requires: libmnl
Requires: nftables

%description
The network-config-manager nmctl allows to configure and introspect
the state of the network links as seen by systemd-networkd.
nmctl can be used to query and configure links for Address, Routes,
Gateways and also hostname, DNS, NTP or Domain.

%package devel
Summary:        Headers for building against network-config-manager
Group:          Development/Libraries/C and C++
Requires:       %{name} = %{version}-%{release}
Requires:       libmnl-devel
Requires:       json-c-devel
Requires:       libnftnl-devel
Requires:       nftables-devel
Requires:       systemd-devel
Requires:       libyaml-devel
Requires:       glib-devel

%description devel
This package contains the headers necessary for building.

%prep
%autosetup -p1
mkdir build

%build
%meson
%meson_build

%install
%meson_install
mv %{buildroot}/lib/systemd %{buildroot}/usr/lib/
%ldconfig_scriptlets

%files
%defattr(-,root,root)
%doc LICENSE.txt README.md
%{_bindir}/nmctl
%{_libdir}/libnetwork_config_manager.so.*
%{_sysconfdir}/network-config-manager/yaml/99-dhcp.yaml.example
%{_unitdir}/network-config-manager-generator.service
%{_unitdir}/network-config-manager-yaml-generator.service

%files devel
%defattr(-,root,root)
%{_includedir}/%{name}.h
%{_libdir}/libnetwork_config_manager.so
%{_libdir}/pkgconfig/%{name}.pc

%changelog
* Mon Dec 18 2023 Tapas Kundu <tapas.kundu@broadcom.com> 0.7-1
- Update to 0.7
* Thu Nov 30 2023 Nitesh Kumar <kunitesh@vmware.com> 0.6.6-1
- Version upgrade to v0.6.6
* Tue Oct 17 2023 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 0.6.5-1
- Update to v0.6.5
* Thu Sep 14 2023 Susant Sahani <ssahani@vmware.com> 0.6.4-1
- Update to v0.6.4
* Fri Jun 09 2023 Susant Sahani <ssahani@vmware.com> 0.6.3-1
- Update to v0.6.3
* Tue Jun 06 2023 Nitesh Kumar <kunitesh@vmware.com> 0.6.2-1
- Version upgrade to v0.6.2
* Wed Apr 19 2023 Susant Sahani <ssahani@vmware.com> 0.6.0-1
- Update to v0.6.0
* Fri Mar 31 2023 Susant Sahani <ssahani@vmware.com> 0.6.b2-1
- Update to v0.6.b2
* Mon Mar 20 2023 Nitesh Kumar <kunitesh@vmware.com> 0.6.b1-1
- Update to v0.6.b1
* Sat Dec 17 2022 Susant Sahani <ssahani@vmware.com> 0.6.b-1
- Update to v0.6.b
* Wed Nov 30 2022 Susant Sahani <ssahani@vmware.com> 0.6.a-1
- Update to v0.6.a
* Wed Mar 02 2022 Nitesh Kumar <kunitesh@vmware.com> 0.5.2-1
- Update to v0.5.2
* Wed Feb 02 2022 Susant Sahani <ssahani@vmware.com> 0.5.1-1
- Update to v0.5.1
* Wed Sep 15 2021 Susant Sahani <ssahani@vmware.com> 0.5-1
- Update to v0.5
* Thu Apr 22 2021 Susant Sahani <ssahani@vmware.com> 0.4-1
- Update to v0.4
* Tue Jan 05 2021 Susant Sahani <ssahani@vmware.com> 0.3-1
- Update to v0.3
* Mon Dec 07 2020 Ankit Jain <ankitja@vmware.com> 0.2-2
- Added requires for devel package to fix install failure
* Sun Nov 15 2020 Susant Sahani <ankitja@vmware.com> 0.2-1
- Update to v0.2
* Wed Sep 30 2020 Ankit Jain <ankitja@vmware.com> 0.1-1
- Initial build. First version
