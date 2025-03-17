%global debug_package %{nil}

Name:           cereal
Version:        1.3.2
Release:        2%{?dist}
Summary:        A header-only C++11 serialization library
Url:            http://uscilab.github.io/cereal
Group:          Development/Tools
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://github.com/USCiLab/cereal/archive/refs/tags/%{name}-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}

BuildRequires:  gcc
BuildRequires:  boost-devel
BuildRequires:  cmake >= 3.0

Requires: boost

%description
cereal is a header-only C++11 serialization library. cereal takes arbitrary
data types and reversibly turns them into different representations, such as
compact binary encodings, XML, or JSON. cereal was designed to be fast,
light-weight, and easy to extend - it has no external dependencies and can be
easily bundled with other code or used standalone.

%package devel
Summary:        Development headers and libraries for %{name}
Provides:       %{name} = %{version}-%{release}

%description devel
cereal is a header-only C++11 serialization library. cereal takes arbitrary
data types and reversibly turns them into different representations, such as
compact binary encodings, XML, or JSON. cereal was designed to be fast,
light-weight, and easy to extend - it has no external dependencies and can be
easily bundled with other code or used standalone.

This package contains development headers and libraries for the cereal library

%prep
%autosetup -p1

%build
%cmake \
    -DSKIP_PORTABILITY_TEST=ON \
    -DWITH_WERROR=OFF \
    -DCMAKE_INSTALL_LIBDIR=%{_libdir} \
    -DCMAKE_BUILD_TYPE=Debug

%cmake_build

%install
%cmake_install

%if 0%{?with_check}
%check
%ctest --output-on-failure %{?testargs}
%endif

%files devel
%defattr(-,root,root)
%doc README.md
%license LICENSE
%{_includedir}/%{name}
%{_libdir}/cmake/%{name}

%changelog
* Thu Dec 12 2024 HarinadhD <harinadh.dommaraju@broadcom.com> 1.3.2-2
- Release bump for SRP compliance
* Wed Sep 28 2022 Shreenidhi Shedi <sshedi@vmware.com> 1.3.2-1
- First build, needed for bpftrace.
