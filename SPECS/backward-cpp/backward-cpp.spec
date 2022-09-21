%global debug_package %{nil}

Summary:        Pretty stack trace printer for C++.
Name:           backward-cpp
Version:        1.5
Release:        2%{?dist}
License:        MIT
URL:            https://github.com/bombela/backward-cpp
Group:          Development/Tools
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://github.com/bombela/backward-cpp/archive/refs/tags/%{name}-v%{version}.tar.gz
%define sha512 %{name}=c81c286bf04f1ea2c64874a3385b7938dc53af9c5012114d5c8cf15d03562461344089694a856b4e6cbe07ecb52b4db25322f3f58e4f40a12bb8c5997ced32da

BuildArch:      x86_64

BuildRequires:  automake
BuildRequires:  autoconf
BuildRequires:  cmake
BuildRequires:  gcc

%description
Backward is a beautiful stack trace pretty printer for C++.

%prep
%autosetup -p1

%build
%cmake \
    -DCMAKE_BUILD_TYPE=Debug \
    -DBUILD_SHARED_LIBS=ON \
    -DCMAKE_INSTALL_LIBDIR=%{_libdir}

%cmake_build

%install
%cmake_install
install -vm644 %{__cmake_builddir}/libbackward.so %{buildroot}%{_libdir}

%if 0%{?with_check}
%check
cd %{__cmake_builddir}
# By default builds.sh returns exit status of cmds from do_action()
# exit 0 added explicitly for clean exit from the script else cmake fails
echo "exit 0" >> builds.sh
sh builds.sh cmake make
make %{?_smp_mflags}
make test %{?_smp_mflags}
%endif

%files
%defattr(-,root,root)
%{_includedir}/backward.hpp
%{_libdir}/backward/BackwardConfig.cmake
%{_libdir}/libbackward.so

%changelog
* Wed Sep 21 2022 Shreenidhi Shedi <sshedi@vmware.com> 1.5-2
- Use cmake macros
* Mon Jun 22 2020 Gerrit Photon <photon-checkins@vmware.com> 1.5-1
- Automatic Version Bump
* Tue Nov 20 2018 Sujay G <gsujay@vmware.com> 1.4-3
- Added %check section
* Mon Oct 22 2018 Ajay Kaher <akaher@vmware.com> 1.4-2
- Adding BuildArch
* Mon Sep 03 2018 Keerthana K <keerthanak@vmware.com> 1.4-1
- Updated to version 1.4.
* Wed Jul 05 2017 Vinay Kulkarni <kulkarniv@vmware.com> 1.3-1
- Initial version of backward-cpp package for Photon.
