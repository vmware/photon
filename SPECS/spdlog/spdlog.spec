Summary:	Very fast, header only, C++ logging library.
Name:		spdlog
Version:	1.1.0
Release:	1%{?dist}
License:	MIT
URL:		https://github.com/gabime/spdlog
Source0:	%{name}-%{version}.tar.gz
%define sha1    spdlog=9b428a0eb4ace8f4916896dd2b3c021a9dc77f79
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
%setup -q

%build
mkdir -p build
cd build
cmake -DCMAKE_INSTALL_PREFIX:PATH=%{_prefix} -DBUILD_SHARED_LIBS=ON ..
make %{?_smp_mflags}

%install
cd build
make DESTDIR=%{buildroot} install

%files
%defattr(-,root,root)
%{_includedir}/%{name}/*
%{_lib64dir}/cmake/%{name}/*.cmake
%{_lib64dir}/pkgconfig/spdlog.pc

%changelog
*    Fri Sep 21 2018 Srinidhi Rao <srinidhir@vmware.com> 1.1.0-1
-    Updating the version to 1.1.0-1.
*    Wed Jul 05 2017 Vinay Kulkarni <kulkarniv@vmware.com> 0.13.0-1
-    Initial version of spdlog package for Photon.
