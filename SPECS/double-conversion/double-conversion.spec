Summary:        Library providing binary-decimal and decimal-binary routines for IEEE doubles
Name:           double-conversion
Version:        3.2.1
Release:        2%{?dist}
Group:          Development/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://github.com/google/double-conversion

Source0:        https://github.com/google/double-conversion/archive/refs/tags/%{name}-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}

BuildRequires:  cmake

Requires:       glibc
Requires:       libgcc
Requires:       libstdc++

%description
This project (double-conversion) provides binary-decimal and decimal-binary routines for IEEE doubles.
The library consists of efficient conversion routines that have been extracted from the V8 JavaScript
engine.The code has been refactored and improved so that it can be used more easily in other projects.

%package devel
Summary:    Library providing binary-decimal and decimal-binary routines for IEEE doubles
Requires:   %{name} = %{version}-%{release}

%description devel
Contains header files for developing applications that use the %{name}
library. There is extensive documentation in src/double-conversion.h. Other
examples can be found in test/cctest/test-conversions.cc.

%prep
%autosetup -p1

%build
export CFLAGS="%{optflags}"
export CXXFLAGS="%{optflags}"
%cmake . \
    -DCMAKE_INSTALL_PREFIX:PATH=%{_prefix}\
    -DCMAKE_INSTALL_LIBDIR=%{_libdir}\
    -DBUILD_SHARED_LIBS:BOOL=ON\
    -DBUILD_TESTING:BOOL=ON
%cmake_build

%install
%cmake_install

%if 0%{?with_check}
%check
%ctest
%endif

%ldconfig_scriptlets

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc LICENSE README.md AUTHORS Changelog
%{_libdir}/libdouble-conversion.so.3*

%files devel
%defattr(-,root,root)
%{_libdir}/libdouble-conversion.so
%{_libdir}/cmake/%{name}
%{_includedir}/%{name}

%changelog
* Thu Dec 12 2024 Guruswamy Basavaiah <guruswamy.basavaiah@broadcom.com> 3.2.1-2
- Release bump for SRP compliance
* Wed Oct 12 2022 Nitesh Kumar <kunitesh@vmware.com> 3.2.1-1
- Initial version,Needed by python3-ujson
