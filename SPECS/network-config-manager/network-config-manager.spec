Summary:        Configure and introspect the state of the network
Name:           network-config-manager
Version:        0.2
Release:        1%{?dist}
License:        Apache 2.0
URL:            https://github.com/vmware/network-config-manager
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://github.com/vmware/network-config-manager/archive/%{name}-%{version}.tar.gz
%define sha1    %{name}-%{version}=c739bc918a25c0c8fff30ace79b65120d5b74760

BuildRequires:  meson
BuildRequires:  systemd-devel
BuildRequires:  libyaml-devel
BuildRequires:  libmnl-devel
BuildRequires:  libnftnl-devel
BuildRequires:  nftables-devel

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

%description devel
This package contains the headers necessary for building.

%prep
%autosetup
mkdir build

%build
meson --prefix=%{_prefix} build
ninja -C build

%install
DESTDIR=%{buildroot} ninja -C build install
mv %{buildroot}/lib/systemd %{buildroot}/usr/lib/

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

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
*   Sun Nov 15 2020 Susant Sahani <ankitja@vmware.com> 0.2-1
-   Update to v0.2
*   Wed Sep 30 2020 Ankit Jain <ankitja@vmware.com> 0.1-1
-   Initial build. First version
