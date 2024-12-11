Summary:        YAML parser and emitter in C++
Name:           yaml-cpp
Version:        0.7.0
Release:        3%{?dist}
Group:          Development/Libraries/C and C++
Vendor:         VMware, Inc.
Distribution:   Photon
Url:            https://github.com/jbeder/yaml-cpp

Source0:        https://github.com/jbeder/yaml-cpp/archive/%{name}-%{version}.tar.gz
%define sha512 %{name}=2de0f0ec8f003cd3c498d571cda7a796bf220517bad2dc02cba70c522dddde398f33cf1ad20da251adaacb2a07b77844111f297e99d45a7c46ebc01706bbafb5

Source1: license.txt
%include %{SOURCE1}

BuildRequires:  cmake
BuildRequires:  gcc

%description
A YAML parser and emitter in C++ matching the YAML 1.2 spec.

%package devel
Summary:    Development files for %{name}
Group:      Development/Libraries/C and C++
Requires:   %{name} = %{version}-%{release}

%description devel
Development files for %{name} library.

%prep
%autosetup -p1 -n %{name}-%{name}-%{version}

%build
%cmake \
    -DCMAKE_INSTALL_LIBDIR=%{_libdir} \
    -DYAML_BUILD_SHARED_LIBS=ON \
    -DYAML_CPP_BUILD_TESTS=OFF \
    -DCMAKE_C_COMPILER=gcc \
    -DCMAKE_CXX_COMPILER=g++

%cmake_build

%install
%cmake_install

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-, root, root)
%doc CONTRIBUTING.md README.md
%license LICENSE
%{_libdir}/libyaml-cpp.so.*

%files devel
%defattr(-, root, root)
%{_datadir}/pkgconfig/%{name}.pc
%{_datadir}/cmake/%{name}
%{_includedir}/yaml-cpp/
%{_libdir}/libyaml-cpp.so

%changelog
* Wed Dec 11 2024 Tapas Kundu <tapas.kundu@broadcom.com> 0.7.0-3
- Release bump for SRP compliance
* Sat Jun 18 2022 Shreenidhi Shedi <sshedi@vmware.com> 0.7.0-2
- Fix build with latest cmake
* Mon Apr 04 2022 Prashant S Chauhan <psinghchauha@vmware.com> 0.7.0-1
- yaml-cpp initial build
