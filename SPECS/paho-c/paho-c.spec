Name:          paho-c
Version:       1.3.9
Release:       1%{?dist}
Summary:       MQTT C Client
License:       BSD and EPL
Vendor:        VMware, Inc.
Distribution:  Photon
Group:         Applications/Database
URL:           https://eclipse.org/paho/clients/c

Source0: https://github.com/eclipse/paho.mqtt.c/archive/v%{version}/paho.mqtt.c-%{version}.tar.gz
%define sha512 paho.mqtt.c-%{version}=2a2ad34df508d8d97ef5382310ba28bb5280843bec337770a2e20442405dde3283473a6038b23fbc1a79bd60d1dfb72d6b508ae4338e95d88b370c0e5625dae5

BuildRequires: cmake
BuildRequires: openssl-devel

%description
The Paho MQTT C Client is a fully fledged MQTT client written in C.

%package devel
Summary:            MQTT C Client development kit
Requires:           %{name} = %{version}-%{release}

%description devel
Development files for the the Paho MQTT C Client.

%prep
%autosetup -p1 -n paho.mqtt.c-%{version}

%build
%cmake \
  -DPAHO_WITH_SSL=TRUE \
  -DPAHO_BUILD_DOCUMENTATION=FALSE \
  -DPAHO_BUILD_SAMPLES=TRUE \
  -DPAHO_ENABLE_CPACK=FALSE \
  -DCMAKE_INSTALL_LIBDIR:PATH=%{_libdir}

%cmake_build

%install
%cmake_install

%files
%defattr(-,root,root)
%license LICENSE edl-v10 epl-v20
%{_bindir}/paho*
%{_libdir}/libpaho-mqtt*.so.1*
%exclude %{_docdir}

%files devel
%defattr(-,root,root)
%{_bindir}/MQTT*
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/cmake/eclipse-paho-mqtt-c/

%changelog
* Mon Mar 21 2022 Oliver Kurth <okurth@vmware.com> 1.3.9-1
- first release in Photon
