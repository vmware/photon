# FIXME: noarch or generate debuginfo
%define debug_package %{nil}

Summary:        Pretty stack trace printer for C++.
Name:           backward-cpp
Version:        1.3
Release:        1%{?dist}
License:        MIT
URL:            https://github.com/bombela/backward-cpp
Source0:        %{name}-v%{version}.tar.gz
%define sha1    backward-cpp=c5e2672604bbe231bf489ce20369af095fe13fdf
Group:          Development/Tools
Vendor:         VMware, Inc.
Distribution:   Photon
BuildRequires:  automake
BuildRequires:  autoconf
BuildRequires:  cmake
BuildRequires:  gcc

%description
Backward is a beautiful stack trace pretty printer for C++.

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
install -vm644 libbackward.so %{buildroot}%{_libdir}/

%files
%defattr(-,root,root)
%{_includedir}/backward.hpp
%{_libdir}/backward/BackwardConfig.cmake
%{_libdir}/libbackward.so

%changelog
*    Tue Jun 13 2017 Vinay Kulkarni <kulkarniv@vmware.com> 1.3-1
-    Initial version of backward-cpp package for Photon.
