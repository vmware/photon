Summary:        Configure and introspect the state of the network
Name:           network-config-manager
Version:        0.6.a
Release:        1%{?dist}
License:        Apache 2.0
URL:            https://github.com/vmware/network-config-manager
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://github.com/vmware/network-config-manager/archive/%{name}-%{version}.tar.gz
%define sha512  %{name}-%{version}=4e8d2abd3212f4406e0335776464ea369ef609e44b4d528d6ab6fae8f2035e4e84b1648e9d4d3d0b25ea54676a98e39f2b80e938adc1892962b996fa4fdf0c92

BuildRequires:  glib-devel
BuildRequires:  json-c-devel
BuildRequires:  meson
BuildRequires:  systemd-devel
BuildRequires:  libyaml-devel
BuildRequires:  libmnl-devel
BuildRequires:  libnftnl-devel
BuildRequires:  nftables-devel

Requires:       json-c
Requires:       libyaml
Requires:       systemd
Requires:       glib
Requires:       libmnl
Requires:       nftables

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
%autosetup
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
%{_unitdir}/network-config-manager-generator.service
%{_unitdir}/network-config-manager-yaml-generator.service

%files devel
%defattr(-,root,root)
%{_includedir}/%{name}.h
%{_libdir}/libnetwork_config_manager.so
%{_libdir}/pkgconfig/%{name}.pc

%changelog
* Wed Nov 30 2022 Susant Sahani <ssahani@vmware.com> 0.6.a-1
- Update to 0.60.a
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
