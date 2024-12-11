%global debug_package %{nil}

Summary:    A fast JSON parser/generator for C++ with both SAX/DOM style API
Name:       rapidjson
Version:    1.1.0
Release:    7%{?dist}
URL:        https://github.com/gcc-mirror/gcc/blob/master/gcc/gcov.c
Group:      Development/Tools
Vendor:     VMware, Inc.
Distribution:   Photon

Source0:    https://github.com/miloyip/rapidjson/archive/%{name}-%{version}.tar.gz
%define sha512 %{name}=2e82a4bddcd6c4669541f5945c2d240fb1b4fdd6e239200246d3dd50ce98733f0a4f6d3daa56f865d8c88779c036099c52a9ae85d47ad263686b68a88d832dff

Source1: license.txt
%include %{SOURCE1}

Patch0: rapidjson-fix-Wclass-memaccess-warnings-errors.patch
Patch1: 0001-Supress-implicit-fallthrough-in-GCC.patch
Patch2: 0001-Onley-apply-to-GCC-7.patch

%ifarch aarch64
Patch3: Fix-build-warnings-emitted-by-GCC-10-on-Aarch64.patch
%endif

BuildRequires:  cmake

%description
RapidJSON is a JSON parser and generator for C++. It was inspired by RapidXml.

%package devel
Summary:        Fast JSON parser and generator for C++
Group:          Development/Libraries/C and C++
Requires:       %{name} = %{version}-%{release}
Provides:       %{name} == %{version}

%description devel
RapidJSON is a header-only JSON parser and generator for C++.
This package contains development headers and examples.

%prep
%autosetup -p1

%build
%cmake \
    -DBUILD_SHARED_LIBS=ON \
    -DCMAKE_INSTALL_LIBDIR=%{_libdir} \
    -DCMAKE_BUILD_TYPE=Debug

%cmake_build

%install
%cmake_install

%if 0%{?with_check}
%check
cd %{__cmake_builddir}
make test %{?_smp_mflags}
%endif

%files devel
%defattr(-,root,root)
%dir %{_libdir}/cmake/RapidJSON
%{_libdir}/cmake/RapidJSON/*
%{_libdir}/pkgconfig/*.pc
%{_includedir}
%{_datadir}

%changelog
* Wed Dec 11 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 1.1.0-7
- Release bump for SRP compliance
* Tue Jul 19 2022 Shreenidhi Shedi <sshedi@vmware.com> 1.1.0-6
- Use cmake macros for build
* Tue Feb 09 2021 Alexey Makhalov <amakhalov@vmware.com> 1.1.0-5
- Fix compilation issue with gcc-10.2.0 for aarch64
* Fri Apr 03 2020 Alexey Makhalov <amakhalov@vmware.com> 1.1.0-4
- Fix compilation issue with gcc-8.4.0
* Mon Nov 19 2018 Vasavi Sirnapalli <vsirnapalli@vmware.com> 1.1.0-3
- Fix makecheck
* Wed Aug 08 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 1.1.0-2
- Fix build failure with gcc 7.3
* Fri Jun 09 2017 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 1.1.0-1
- Initial build. First version
