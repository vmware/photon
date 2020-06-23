Summary:        Pretty stack trace printer for C++.
Name:           backward-cpp
Version:        1.5
Release:        1%{?dist}
License:        MIT
URL:            https://github.com/bombela/backward-cpp
Source0:        %{name}-v%{version}.tar.gz
%define sha1    backward-cpp=c76754a92d92690be9cf99a35823839da8cced89
Group:          Development/Tools
Vendor:         VMware, Inc.
Distribution:   Photon
BuildArch:      x86_64
BuildRequires:  automake
BuildRequires:  autoconf
BuildRequires:  cmake
BuildRequires:  gcc

%description
Backward is a beautiful stack trace pretty printer for C++.

%global debug_package %{nil}

%prep
%setup -q

%build
mkdir -p build
cd build
cmake -DCMAKE_INSTALL_PREFIX:PATH=%{_prefix} -DBUILD_SHARED_LIBS=ON ..
make %{?_smp_mflags}

%install
cd build
make DESTDIR=%{buildroot} install
install -vm644 libbackward.so %{buildroot}%{_lib64dir}/

%check
cd build
cd ..
cmake -DBUILD_SHARED_LIBS=ON CMakeLists.txt
# By default builds.sh returns exit status of cmds from do_action()
# exit 0 added explicitly for clean exit from the script else cmake fails
echo "exit 0" >> builds.sh
sh builds.sh cmake make
make
make test

%files
%defattr(-,root,root)
%{_includedir}/backward.hpp
%{_lib64dir}/backward/BackwardConfig.cmake
%{_lib64dir}/libbackward.so

%changelog
*    Mon Jun 22 2020 Gerrit Photon <photon-checkins@vmware.com> 1.5-1
-    Automatic Version Bump
*    Tue Nov 20 2018 Sujay G <gsujay@vmware.com> 1.4-3
-    Added %check section
*    Mon Oct 22 2018 Ajay Kaher <akaher@vmware.com> 1.4-2
-    Adding BuildArch
*    Mon Sep 03 2018 Keerthana K <keerthanak@vmware.com> 1.4-1
-    Updated to version 1.4.
*    Wed Jul 05 2017 Vinay Kulkarni <kulkarniv@vmware.com> 1.3-1
-    Initial version of backward-cpp package for Photon.
