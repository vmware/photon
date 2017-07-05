Summary:	Very fast, header only, C++ logging library.
Name:		spdlog
Version:	0.13.0
Release:	1%{?dist}
License:	MIT
URL:		https://github.com/gabime/spdlog
Source0:	%{name}-v%{version}.tar.gz
%define sha1    spdlog=e9968ab555f9f7bb86d6257e98d7a92313a91297
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
%{_libdir}/cmake/%{name}/*.cmake
%{_libdir}/pkgconfig/spdlog.pc

%changelog
*    Wed Jul 05 2017 Vinay Kulkarni <kulkarniv@vmware.com> 0.13.0-1
-    Initial version of spdlog package for Photon.
