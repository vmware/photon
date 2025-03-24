Summary:        YANG data modeling language library
Name:           libyang
Version:        3.7.8
Release:        1%{?dist}
Url:            https://github.com/CESNET/libyang
License:        BSD-3-Clause
Group:          Development/Tools
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://github.com/CESNET/libyang/archive/refs/tags/%{name}-%{version}.tar.gz
%define sha512 %{name}=399e67c91a0d18cf65ef9bb4c7fb2fae26000daa664495563f9de9ab6861cbadc294a7d214d957af54fe5a7fe8c67bdd5cf46800c7683c0dc582708bf1f2345e

BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  pcre2-devel

%if 0%{?with_check}
BuildRequires:   cmocka-devel
%endif

Requires:   pcre2

%description
Libyang is YANG data modeling language parser and toolkit
written (and providing API) in C.

%package devel
Summary:    Development files for libyang
Requires:   %{name} = %{version}-%{release}

%description devel
Files needed to develop with libyang.

%package tools
Summary:        YANG validator tools
Requires:       %{name} = %{version}-%{release}

%description tools
YANG validator tools.

%prep
%autosetup -p1

%build
%cmake \
    -DCMAKE_BUILD_TYPE=Debug \
    -DCMAKE_INSTALL_LIBDIR=%{_libdir} \
    -DENABLE_TESTS=ON \
    -DENABLE_VALGRIND_TESTS=OFF

%cmake_build

%install
%cmake_install

%if 0%{?with_check}
%check
%ctest
%endif

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-, root, root)
%license LICENSE
%{_libdir}/%{name}.so.*
%exclude %dir %{_libdir}/debug
%{_datadir}/yang/modules/%{name}/*

%files tools
%defattr(-, root, root)
%{_bindir}/yanglint
%{_bindir}/yangre
%{_mandir}/man1/yanglint.1.gz
%{_mandir}/man1/yangre.1.gz

%files devel
%defattr(-, root, root)
%{_libdir}/*.so
%{_libdir}/pkgconfig/%{name}.pc
%{_includedir}/%{name}/*.h

%changelog
* Mon Mar 24 2025 Harinadh Dommaraju <Harinadh.Dommaraju@vmware.com> 3.7.8-1
- Version upgrade to satisfy frr version upgrade
* Tue Apr 11 2023 Brennan Lamoreaux <blamoreaux@vmware.com> 2.1.55-1
- Update to latest version to resolve CVE-2023-26917 and
- CVE-2023-26916
* Tue Jul 26 2022 Brennan Lamoreaux <blamoreaux@vmware.com> 2.0.164-1
- Initial Build. Modified from provided libyang.spec on GitHub.
