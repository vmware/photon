%global srcname benchmark

Name:       google-benchmark
Version:    1.7.1
Release:    2%{?dist}
Summary:    A microbenchmark support library
URL:        https://github.com/google/%{srcname}
Group:      Applications/System
Vendor:     VMware, Inc.
Distribution:   Photon

Source0: https://github.com/google/benchmark/archive/refs/tags/%{name}-%{version}.tar.gz
%define sha512 %{name}=396af1c1d3eaa2b78c6d23b1472f6088db85a294056ae1c2366dc5c0becdc8f141ba8fc3a235033324ab0a41c2298f5d242ef09b9b6f69d9877de6bcb2062efd

Source1: license.txt
%include %{SOURCE1}

BuildRequires: gtest-devel
BuildRequires: gmock-devel
BuildRequires: ninja-build
BuildRequires: build-essential
BuildRequires: cmake

%description
A library to support the benchmarking of functions, similar to unit-tests.

%package devel
Summary: Development files for %{name}
Requires: %{name} = %{version}-%{release}

%description devel
%{summary}.

%prep
%autosetup -p1 -n %{srcname}-%{version}
sed -e '/get_git_version/d' -e '/-Werror/d' -i CMakeLists.txt

%build
%{cmake} -G Ninja \
    -DCMAKE_BUILD_TYPE=Debug \
    -DGIT_VERSION=%{version} \
    -DBENCHMARK_ENABLE_DOXYGEN:BOOL=OFF \
    -DBENCHMARK_ENABLE_TESTING:BOOL=ON \
    -DBENCHMARK_USE_BUNDLED_GTEST:BOOL=OFF \
    -DBENCHMARK_ENABLE_GTEST_TESTS:BOOL=ON \
    -DBENCHMARK_ENABLE_INSTALL:BOOL=ON \
    -DBENCHMARK_INSTALL_DOCS:BOOL=OFF \
    -DCMAKE_INSTALL_LIBDIR=%{_libdir}

%{cmake_build}

%install
%{cmake_install}

%if 0%{?with_check}
%check
%{ctest}
%endif

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_libdir}/libbenchmark*.so.*

%files devel
%defattr(-,root,root)
%{_libdir}/libbenchmark*.so
%{_includedir}/%{srcname}
%{_libdir}/cmake/%{srcname}
%{_libdir}/pkgconfig/%{srcname}.pc

%changelog
* Wed Dec 11 2024 Tapas Kundu <tapas.kundu@broadcom.com> 1.7.1-2
- Release bump for SRP compliance
* Thu Jan 12 2023 Shreenidhi Shedi <sshedi@vmware.com> 1.7.1-1
- Intial version. Needed by snappy.
