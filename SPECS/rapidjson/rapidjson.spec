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

%prep
%setup -q

%build
mkdir build && cd build
cmake ..
make

%install
install -vdm755 %{buildroot}%{_includedir}
install -vdm755 %{buildroot}%{_libdir}
install -vdm755 %{buildroot}%{_libdir}/cmake/RapidJSON

cp build/*.pc %{buildroot}%{_libdir}
cp -r include/* %{buildroot}%{_includedir}
cp build/*.cmake %{buildroot}%{_libdir}/cmake/RapidJSON

%files
%defattr(-,root,root)
%dir %{_libdir}/cmake/RapidJSON
%{_libdir}/cmake/RapidJSON/*
%{_libdir}/*.pc
%{_includedir}
%changelog
*   Fri Jun 09 2017 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 1.1.0-1
-   Initial build. First version
