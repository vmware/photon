Summary:	Google's C++ logging module
Name:		glog
Version:	0.6.0
Release:	1%{?dist}
License:	BSD
URL:		https://github.com/google/glog
Source0:	https://github.com/google/glog/archive/%{name}-%{version}.tar.gz
%define sha512  glog=fd2c42583d0dd72c790a8cf888f328a64447c5fb9d99b2e2a3833d70c102cb0eb9ae874632c2732424cc86216c8a076a3e24b23a793eaddb5da8a1dc52ba9226
Group:		Development/Tools
Vendor:		VMware, Inc.
Distribution: 	Photon
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  libgcc
BuildRequires:  libtool

%description
Google's C++ logging module

%package        devel
Summary:        glog devel
Group:          Development/Tools

%description    devel
This contains development tools and libraries for glog.

%package        docs
Summary:        glog docs
Group:          Development/Tools

%description    docs
The contains glog package doc files.

%prep
%autosetup -n %{name}-%{version}

%build
cmake -S . -B build -G "Unix Makefiles"
cmake --build build
cmake --build build --target all

%install
cmake --build build --target install DESTDIR=%{buildroot}
find %{buildroot} -name '*.la' -delete
mv %{buildroot}%{_prefix}/local/* %{buildroot}%{_prefix}/
rm -rf %{buildroot}%{_prefix}/local

%check
cmake --build build --target test

%files
%defattr(-,root,root)
%{_lib64dir}/libglog.so.*

%files devel
%defattr(-,root,root)
%{_includedir}/%{name}/*
%{_lib64dir}/libglog.so
%{_lib64dir}/pkgconfig/libglog.pc
%{_lib64dir}/cmake/glog/*.cmake

%files docs
%defattr(-,root,root)

%changelog
*   Tue Apr 13 2021 Gerrit Photon <photon-checkins@vmware.com> 0.6.0-1
-   Automatic Version Bump
*   Mon Jun 22 2020 Gerrit Photon <photon-checkins@vmware.com> 0.4.0-1
-   Automatic Version Bump
*   Mon Sep 10 2018 Michelle Wang <michellew@vmware.com> 0.3.5-1
-   Update version to 0.3.5.
*   Fri Oct 13 2017 Alexey Makhalov <amakhalov@vmware.com> 0.3.4-3
-   Use standard configure macros
*   Thu Jun 1  2017 Bo Gan <ganb@vmware.com> 0.3.4-2
-   Fix file paths
*   Sat Mar 25 2017 Vinay Kulkarni <kulkarniv@vmware.com> 0.3.4-1
-   Initial version of glog for Photon.
