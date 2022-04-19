Summary:	Very fast, header only, C++ logging library.
Name:		spdlog
Version:	1.10.0
Release:	1%{?dist}
License:	MIT
URL:		https://github.com/gabime/spdlog
Source0:	%{name}-%{version}.tar.gz
%define sha512  spdlog=e82ec0a0c813ed2f1c8a31a0f21dbb733d0a7bd8d05284feae3bd66040bc53ad47a93b26c3e389c7e5623cfdeba1854d690992c842748e072aab3e6e6ecc5666
Group:		Development/Tools
Vendor:		VMware, Inc.
Distribution: 	Photon
BuildRequires:  automake
BuildRequires:  cmake
BuildRequires:  gcc

%description
Very fast, header only, C++ logging library.

%global debug_package %{nil}

%prep
%autosetup

%build
mkdir -p build
cd build
cmake -DCMAKE_INSTALL_PREFIX:PATH=%{_prefix} -DBUILD_SHARED_LIBS=ON ..
make %{?_smp_mflags}

%install
cd build
make DESTDIR=%{buildroot} %{?_smp_mflags} install

%check
cd build
make test %{?_smp_mflags}

%files
%defattr(-,root,root)
%{_includedir}/%{name}/*
%{_lib64dir}/cmake/%{name}/*.cmake
%{_lib64dir}/pkgconfig/spdlog.pc
%{_lib64dir}/libspdlog.so
%{_lib64dir}/libspdlog.so.*

%changelog
*    Tue Apr 19 2022 Gerrit Photon <photon-checkins@vmware.com> 1.10.0-1
-    Automatic Version Bump
*    Wed Sep 30 2020 Gerrit Photon <photon-checkins@vmware.com> 1.8.1-1
-    Automatic Version Bump
*    Tue Sep 01 2020 Gerrit Photon <photon-checkins@vmware.com> 1.8.0-1
-    Automatic Version Bump
*    Tue Jun 30 2020 Gerrit Photon <photon-checkins@vmware.com> 1.7.0-1
-    Automatic Version Bump
*    Mon Nov 26 2018 Sujay G <gsujay@vmware.com> 1.1.0-2
-    Added %check section
*    Fri Sep 21 2018 Srinidhi Rao <srinidhir@vmware.com> 1.1.0-1
-    Updating the version to 1.1.0-1.
*    Wed Jul 05 2017 Vinay Kulkarni <kulkarniv@vmware.com> 0.13.0-1
-    Initial version of spdlog package for Photon.
