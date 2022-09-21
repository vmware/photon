%global debug_package %{nil}

Summary:    Very fast, header only, C++ logging library.
Name:       spdlog
Version:    1.8.1
Release:    2%{?dist}
License:    MIT
URL:        https://github.com/gabime/spdlog
Group:      Development/Tools
Vendor:     VMware, Inc.
Distribution:   Photon

Source0:    %{name}-%{version}.tar.gz
%define sha512 %{name}=ef855f4f91ed8aba89ef0191a9fd70f73a49567332f7eb42da1604e3a7dda3bbe48db3fd0fae317bb11ee95315d8cd62bf586d2de919ca0978d91e5a971b1c3f

BuildRequires:  automake
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  ninja-build

%description
Very fast, header only, C++ logging library.

%package devel
Summary:        Development files for %{name}
Requires:       %{name} = %{version}-%{release}
Requires:       libstdc++-devel

%description devel
The %{name}-devel package contains C++ header files for developing
applications that use %{name}.

%prep
%autosetup -p1

%build
%cmake -G Ninja \
    -DCMAKE_INSTALL_LIBDIR=%{_lib} \
    -DCMAKE_BUILD_TYPE=Release \
    -DSPDLOG_BUILD_SHARED=ON \
    -DSPDLOG_BUILD_EXAMPLE=OFF \
    -DSPDLOG_BUILD_BENCH=OFF \
    -DSPDLOG_BUILD_TESTS=ON \
    -DSPDLOG_INSTALL=ON

%cmake_build

%install
%cmake_install

%check
%ctest

%files
%defattr(-,root,root)
%license LICENSE
%doc README.md
%{_libdir}/lib%{name}.so.1*

%files devel
%defattr(-,root,root)
%doc example
%{_includedir}/%{name}
%{_libdir}/lib%{name}.so
%{_libdir}/cmake/%{name}
%{_libdir}/pkgconfig/%{name}.pc

%changelog
* Wed Sep 21 2022 Shreenidhi Shedi <sshedi@vmware.com> 1.8.1-2
- Use cmake macros
* Wed Sep 30 2020 Gerrit Photon <photon-checkins@vmware.com> 1.8.1-1
- Automatic Version Bump
* Tue Sep 01 2020 Gerrit Photon <photon-checkins@vmware.com> 1.8.0-1
- Automatic Version Bump
* Tue Jun 30 2020 Gerrit Photon <photon-checkins@vmware.com> 1.7.0-1
- Automatic Version Bump
* Mon Nov 26 2018 Sujay G <gsujay@vmware.com> 1.1.0-2
- Added %check section
* Fri Sep 21 2018 Srinidhi Rao <srinidhir@vmware.com> 1.1.0-1
- Updating the version to 1.1.0-1.
* Wed Jul 05 2017 Vinay Kulkarni <kulkarniv@vmware.com> 0.13.0-1
- Initial version of spdlog package for Photon.
