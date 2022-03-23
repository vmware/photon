Name:          paho-c
Version:       1.3.9
Release:       1%{?dist}
Summary:       MQTT C Client
License:       BSD and EPL
Vendor:        VMware, Inc.
Distribution:  Photon
Group:         Applications/Database
URL:           https://eclipse.org/paho/clients/c/
Source0:       https://github.com/eclipse/paho.mqtt.c/archive/v%{version}/paho.mqtt.c-%{version}.tar.gz
%define sha1   paho.mqtt.c-%{version}=5a7058ab971522965ef390ffcfa5428e672b5135
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
%autosetup -n paho.mqtt.c-%{version}

%build
mkdir build && cd build
cmake \
  -DPAHO_WITH_SSL=TRUE \
  -DPAHO_BUILD_DOCUMENTATION=FALSE \
  -DPAHO_BUILD_SAMPLES=TRUE \
  -DPAHO_ENABLE_CPACK=FALSE \
  -DCMAKE_INSTALL_PREFIX=%{_prefix} \
  -DCMAKE_INSTALL_LIBDIR:PATH=lib \
  ..

make %{?_smp_mflags}

%install
cd build && make DESTDIR=%{buildroot} install %{?_smp_mflags}

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
* Mon Mar 28 2022 Oliver Kurth <okurth@vmware.com> 1.3.9-1
- first release in Photon
