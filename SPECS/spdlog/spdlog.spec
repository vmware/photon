%global debug_package %{nil}

Summary:    Very fast, header only, C++ logging library.
Name:       spdlog
Version:    1.15.3
Release:    1%{?dist}
License:    MIT
URL:        https://github.com/gabime/spdlog
Group:      Development/Tools
Vendor:     VMware, Inc.
Distribution:   Photon

Source0: https://github.com/gabime/spdlog/archive/refs/tags/%{name}-%{version}.tar.gz
%define sha512 %{name}=21c35f4091850ea3a0cd6a24867e06e943df70d76cd5a7ec0b15a33e0e9e0cc3584ed7930e1ac6f347e7e06f0e002d0e759884eaf05310014e24ea0e0419fcc4

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
%{cmake} -G Ninja \
    -DBUILD_SHARED_LIBS=ON \
    -DCMAKE_INSTALL_LIBDIR=%{_libdir} \
    -DCMAKE_BUILD_TYPE=Release \
    -DSPDLOG_BUILD_SHARED=ON

%{cmake_build}

%install
%{cmake_install}

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%{_libdir}/libspdlog.so.*

%files devel
%defattr(-,root,root)
%{_libdir}/libspdlog.so
%{_includedir}/%{name}/*
%{_libdir}/cmake/%{name}/*.cmake
%{_libdir}/pkgconfig/spdlog.pc

%changelog
* Wed Jun 25 2025 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 1.15.3-1
- Upgrade to v1.15.3
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
