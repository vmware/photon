Summary:        YANG data modeling language library
Name:           libyang
Version:        2.1.55
Release:        1%{?dist}
Url:            https://github.com/CESNET/libyang
License:        BSD-3-Clause
Group:          Development/Tools
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://github.com/CESNET/libyang/archive/refs/tags/%{name}-%{version}.tar.gz
%define sha512 %{name}=dd0b58aec7e2d84f62636c62c9e7f67f0b4819e8d5ce9236874a3531607aa6fb58ccdcf537534eae8bfa700c37b8e3524be659929f4e7e03f8f67968bc352cb4

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
%{_libdir}/%{name}.so.2
%{_libdir}/%{name}.so.2.*
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
* Tue Apr 11 2023 Brennan Lamoreaux <blamoreaux@vmware.com> 2.1.55-1
- Update to latest version to resolve CVE-2023-26917 and
- CVE-2023-26916
* Tue Jul 26 2022 Brennan Lamoreaux <blamoreaux@vmware.com> 2.0.164-1
- Initial Build. Modified from provided libyang.spec on GitHub.
