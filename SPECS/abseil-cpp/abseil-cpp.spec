Summary:        C++ Common Libraries
Name:           abseil-cpp
Version:        20230125.3
Release:        2%{?dist}
Group:          Development/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://abseil.io

Source0: https://github.com/abseil/abseil-cpp/archive/%{version}/%{name}-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}

BuildRequires: ninja-build
BuildRequires: build-essential
BuildRequires: gmock-devel
BuildRequires: gtest-devel
BuildRequires: cmake

%description
Abseil is an open-source collection of C++ library code designed to augment
the C++ standard library. The Abseil library code is collected from
Google's own C++ code base, has been extensively tested and used in
production, and is the same code we depend on in our daily coding lives.

In some cases, Abseil provides pieces missing from the C++ standard; in
others, Abseil provides alternatives to the standard for special needs we've
found through usage in the Google code base. We denote those cases clearly
within the library code we provide you.

Abseil is not meant to be a competitor to the standard library; we've just
found that many of these utilities serve a purpose within our code base,
and we now want to provide those resources to the C++ community as a whole.

%package devel
Summary:        Development files for %{name}
Requires:       %{name} = %{version}-%{release}

%description devel
Development headers for %{name}

%prep
%autosetup -p1

%build
%{cmake} \
  -GNinja \
  -DABSL_USE_EXTERNAL_GOOGLETEST:BOOL=ON \
  -DABSL_FIND_GOOGLETEST:BOOL=ON \
  -DABSL_ENABLE_INSTALL:BOOL=ON \
%if 0%{?with_check}
  -DABSL_BUILD_TESTING:BOOL=ON \
  -DABSL_BUILD_TEST_HELPERS:BOOL=ON \
%endif
  -DCMAKE_BUILD_TYPE:STRING=RelWithDebInfo \
  -DCMAKE_INSTALL_LIBDIR:PATH=%{_libdir}

%{cmake_build}

%install
%{cmake_install}

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/cmake/absl
%{_libdir}/*.so
%{_libdir}/pkgconfig/absl_*.pc

%changelog
* Wed Dec 11 2024 HarinadhD <harinadh.dommaraju@broadcom.com> 20230125.3-2
- Release bump for SRP compliance
* Wed Jun 07 2023 Shreenidhi Shedi <sshedi@vmware.com> 20230125.3-1
- Initial version, needed by protobuf.
