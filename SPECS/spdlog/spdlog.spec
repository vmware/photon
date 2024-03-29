%global debug_package %{nil}

Summary:    Very fast, header only, C++ logging library.
Name:       spdlog
Version:    1.11.0
Release:    1%{?dist}
License:    MIT
URL:        https://github.com/gabime/spdlog
Group:      Development/Tools
Vendor:     VMware, Inc.
Distribution:   Photon

Source0:    %{name}-%{version}.tar.gz
%define sha512 %{name}=210f3135c7af3ec774ef9a5c77254ce172a44e2fa720bf590e1c9214782bf5c8140ff683403a85b585868bc308286fbdeb1c988e4ed1eb3c75975254ffe75412

BuildRequires:  automake
BuildRequires:  cmake
BuildRequires:  gcc

%description
Very fast, header only, C++ logging library.

%package devel
Summary:    Development headers and libraries for %{name}
Requires:   %{name} = %{version}-%{release}

%description devel
Development headers and libraries for %{name}.

%prep
%autosetup -p1

%build
%cmake \
    -DBUILD_SHARED_LIBS=ON \
    -DCMAKE_INSTALL_LIBDIR=%{_libdir} \
    -DCMAKE_BUILD_TYPE=Release \
    -DSPDLOG_BUILD_SHARED=ON

%cmake_build

%install
%cmake_install

%if 0%{?with_check}
%check
cd %{__cmake_builddir}
make test %{?_smp_mflags}
%endif

%files
%defattr(-,root,root)
%{_libdir}/libspdlog.so.*

%files devel
%{_libdir}/libspdlog.so
%{_includedir}/%{name}/*
%{_libdir}/cmake/%{name}/*.cmake
%{_libdir}/pkgconfig/spdlog.pc

%changelog
* Wed Dec 14 2022 Gerrit Photon <photon-checkins@vmware.com> 1.11.0-1
- Automatic Version Bump
* Mon Jun 20 2022 Shreenidhi Shedi <sshedi@vmware.com> 1.10.0-2
- Use cmake macros for build
* Tue Apr 19 2022 Gerrit Photon <photon-checkins@vmware.com> 1.10.0-1
- Automatic Version Bump
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
