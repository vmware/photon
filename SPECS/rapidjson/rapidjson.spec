%global debug_package %{nil}
Summary:	A fast JSON parser/generator for C++ with both SAX/DOM style API
Name:		rapidjson
Version:	1.1.0
Release:	1%{?dist}
License:	BSD, JSON, MIT
URL:		https://github.com/gcc-mirror/gcc/blob/master/gcc/gcov.c
Source0:	https://github.com/miloyip/rapidjson/archive/%{name}-%{version}.tar.gz
%define sha1 rapidjson=a3e0d043ad3c2d7638ffefa3beb30a77c71c869f
Group:		Development/Tools
Vendor:		VMware, Inc.
Distribution: 	Photon
BuildRequires:	cmake
%description
RapidJSON is a JSON parser and generator for C++. It was inspired by RapidXml.

%package devel
Summary:        Fast JSON parser and generator for C++
Group:          Development/Libraries/C and C++
Provides:       %{name} == %{version}

%description devel
RapidJSON is a header-only JSON parser and generator for C++.
This package contains development headers and examples.

%prep
%setup -q

%build
mkdir build && cd build
cmake -DCMAKE_INSTALL_PREFIX:PATH=%{_prefix} -DBUILD_SHARED_LIBS=ON ..
make %{?_smp_mflags}

%install
cd build
make DESTDIR=%{buildroot} install

%files devel
%defattr(-,root,root)
%dir %{_libdir}/cmake/RapidJSON
%{_libdir}/cmake/RapidJSON/*
%{_libdir}/pkgconfig/*.pc
%{_includedir}
%{_datadir}
%changelog
*   Fri Jun 09 2017 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 1.1.0-1
-   Initial build. First version
