Name:          libnvme
Summary:       Linux-native nvme device management library
Version:       1.3
Release:       3%{?dist}
Group:         Development/Libraries
Vendor:        VMware, Inc.
Distribution:  Photon
URL:           https://github.com/linux-nvme/libnvme
Source0:       https://github.com/linux-nvme/libnvme/archive/v%{version}/%{name}-%{version}.tar.gz
%define sha512 %{name}-%{version}=c874b29b73e55be842f71e74a226a76fcd50dfa72e2be100f0437bc83e740cd146b6d2f2cdaa940c11c3d8c48ff2c065ac0e8a83d4d0dde743edf4179f328670

Source1: license.txt
%include %{SOURCE1}
BuildRequires: gcc
BuildRequires: swig
BuildRequires: python3-devel
BuildRequires: meson
BuildRequires: json-c-devel
BuildRequires: openssl-devel
BuildRequires: dbus-devel
Requires: json-c
Requires: dbus
Requires: openssl

%description
Provides type definitions for NVMe specification structures,
enumerations, and bit fields, helper functions to construct,
dispatch, and decode commands and payloads, and utilities to connect,
scan, and manage nvme devices on a Linux system.

%package  devel
Summary:  %{name} development package
Requires: %{name} = %{version}-%{release}
Requires: dbus-devel
Requires: json-c-devel
Requires: openssl-devel

%description devel
This package provides header files to include and libraries to link with
for Linux-native nvme device management.

%package -n python3-libnvme
Summary:    Python3 bindings for libnvme
Requires:   %{name} = %{version}-%{release}
Requires:   python3
Provides:   python3-nvme = %{version}-%{release}

%description -n python3-libnvme
This package contains Python bindings for libnvme.

%prep
%autosetup

%build
%meson
%meson_build

%install
%meson_install

%ldconfig_scriptlets

%if 0%{?with_check}
%check
%meson_test
%endif

%files
%defattr(-,root,root)
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root)
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%{_includedir}/*.h
%{_includedir}/nvme/*.h

%files -n python3-libnvme
%defattr(-,root,root)
%{python3_sitearch}/%{name}/

%changelog
*  Wed Jan 22 2025 Tapas Kundu <tapas.kundu@broadcom.com> 1.3-3
-  Bump version as a part of meson upgrade
*  Wed Dec 11 2024 Mukul Sikka <mukul.sikka@broadcom.com> 1.3-2
-  Release bump for SRP compliance
*  Fri Mar 10 2023 Srish Srinivasan <ssrish@vmware.com> 1.3-1
-  Initial build.
