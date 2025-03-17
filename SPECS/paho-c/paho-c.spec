Name:          paho-c
Version:       1.3.11
Release:       2%{?dist}
Summary:       MQTT C Client
Vendor:        VMware, Inc.
Distribution:  Photon
Group:         Applications/Database
URL:           https://eclipse.org/paho/clients/c

Source0:       https://github.com/eclipse/paho.mqtt.c/archive/v%{version}/paho.mqtt.c-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}

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
* Wed Dec 11 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 1.3.11-2
- Release bump for SRP compliance
* Fri Oct 28 2022 Gerrit Photon <photon-checkins@vmware.com> 1.3.11-1
- Automatic Version Bump
* Wed Jul 13 2022 Shreenidhi Shedi <sshedi@vmware.com> 1.3.10-2
- Use cmake macros for build
* Wed Jun 01 2022 Gerrit Photon <photon-checkins@vmware.com> 1.3.10-1
- Automatic Version Bump
* Mon Mar 21 2022 Oliver Kurth <okurth@vmware.com> 1.3.9-1
- first release in Photon
