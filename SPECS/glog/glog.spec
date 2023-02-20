Summary:    Google's C++ logging module
Name:       glog
Version:    0.3.5
Release:    2%{?dist}
License:    BSD
URL:        https://github.com/google/glog
Group:      Development/Tools
Vendor:     VMware, Inc.
Distribution:   Photon

Source0: https://github.com/google/glog/archive/%{name}-%{version}.tar.gz
%define sha512 %{name}=a54a3b8b4b7660d7558ba5168c659bc3c8323c30908a4f6a4bbc6f9cd899350f3243aabc720daebfdeb799b276b51ba1eaa1a0f83149c4e1a038d552ada1ed72

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  make
BuildRequires:  gcc
BuildRequires:  libgcc
BuildRequires:  libtool

%description
Google's C++ logging module

%package devel
Summary:        glog devel
Group:          Development/Tools
Requires:       %{name} = %{version}-%{release}

%description devel
This contains development tools and libraries for glog.

%package docs
Summary:        glog docs
Group:          Development/Tools
Requires:       %{name} = %{version}-%{release}

%description docs
The contains glog package doc files.

%prep
%autosetup -p1

%build
%configure \
    --disable-silent-rules

%make_build

%install
%make_install %{?_smp_mflags}

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
%{_libdir}/libglog.a
%{_libdir}/libglog.so
%{_libdir}/pkgconfig/libglog.pc

%files docs
%defattr(-,root,root)
%{_docdir}/*

%changelog
* Mon Feb 20 2023 Shreenidhi Shedi <sshedi@vmware.com> 0.3.5-2
- Fix spec issues
* Mon Sep 10 2018 Michelle Wang <michellew@vmware.com> 0.3.5-1
- Update version to 0.3.5.
* Fri Oct 13 2017 Alexey Makhalov <amakhalov@vmware.com> 0.3.4-3
- Use standard configure macros
* Thu Jun 1  2017 Bo Gan <ganb@vmware.com> 0.3.4-2
- Fix file paths
* Sat Mar 25 2017 Vinay Kulkarni <kulkarniv@vmware.com> 0.3.4-1
- Initial version of glog for Photon.
