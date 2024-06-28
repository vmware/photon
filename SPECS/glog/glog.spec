Summary:    Google's C++ logging module
Name:       glog
Version:    0.6.0
Release:    3%{?dist}
License:    BSD
URL:        https://github.com/google/glog
Group:      Development/Tools
Vendor:     VMware, Inc.
Distribution:   Photon

Source0: https://github.com/google/glog/archive/%{name}-%{version}.tar.gz
%define sha512 %{name}=fd2c42583d0dd72c790a8cf888f328a64447c5fb9d99b2e2a3833d70c102cb0eb9ae874632c2732424cc86216c8a076a3e24b23a793eaddb5da8a1dc52ba9226

BuildRequires:  build-essential
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
Requires:       %{name} = %{version}-%{release}

%description    devel
This contains development tools and libraries for glog.

%prep
%autosetup -p1

%build
%cmake \
    -DCMAKE_INSTALL_LIBDIR=%{_libdir} \
    -DCMAKE_BUILD_TYPE=Release

%cmake_build

%install
%cmake_install

%if 0%{?with_check}
%check
cd %{__cmake_builddir}
make test %{?_smp_mflags}
%endif

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%files
%defattr(-,root,root)
%{_libdir}/libglog.so.*

%files devel
%defattr(-,root,root)
%{_includedir}/%{name}/*
%{_libdir}/libglog.so
%{_libdir}/pkgconfig/libglog.pc
%{_libdir}/cmake/glog/*.cmake

%changelog
* Mon Feb 20 2023 Shreenidhi Shedi <sshedi@vmware.com> 0.6.0-3
- Fix spec issues
* Mon Jun 20 2022 Shreenidhi Shedi <sshedi@vmware.com> 0.6.0-2
- Use cmake macros for build
* Tue Apr 13 2021 Gerrit Photon <photon-checkins@vmware.com> 0.6.0-1
- Automatic Version Bump
* Mon Jun 22 2020 Gerrit Photon <photon-checkins@vmware.com> 0.4.0-1
- Automatic Version Bump
* Mon Sep 10 2018 Michelle Wang <michellew@vmware.com> 0.3.5-1
- Update version to 0.3.5.
* Fri Oct 13 2017 Alexey Makhalov <amakhalov@vmware.com> 0.3.4-3
- Use standard configure macros
* Thu Jun 1  2017 Bo Gan <ganb@vmware.com> 0.3.4-2
- Fix file paths
* Sat Mar 25 2017 Vinay Kulkarni <kulkarniv@vmware.com> 0.3.4-1
- Initial version of glog for Photon.
