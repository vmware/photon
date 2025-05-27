# Ensure that the version used is compatible with mariadb
# during version upgrades

Summary:        Small, safe and fast formatting library for C++
Name:           fmt
Version:        11.1.4
Release:        1%{?dist}
URL:            https://github.com/fmtlib/fmt
License:        MIT
Group:          Applications
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: %{url}/archive/%{name}-%{version}.tar.gz
%define sha512 %{name}=573b7de1bd224b7b1b60d44808a843db35d4bc4634f72a9edcb52cf68e99ca66c744fd5d5c97b4336ba70b94abdabac5fc253b245d0d5cd8bbe2a096bf941e39

BuildRequires:  cmake
BuildRequires:  ninja-build

%description
C++ Format is an open-source formatting library for C++. It can be used as a
safe alternative to printf or as a fast alternative to IOStreams.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name} = %{version}-%{release}

%description    devel
This package contains the header file for using %{name}.

%prep
%autosetup -p1

%build
%{cmake} \
    -G Ninja \
    -DCMAKE_BUILD_TYPE=RelWithDebInfo \
    -DCMAKE_POSITION_INDEPENDENT_CODE:BOOL=ON \
    -DFMT_CMAKE_DIR:STRING=%{_libdir}/cmake/%{name} \
    -DFMT_LIB_DIR:STRING=%{_libdir} \
    -DCMAKE_INSTALL_LIBDIR=%{_libdir} \

%{cmake_build}

%install
%{cmake_install}

%if 0%{?with_check}
%check
%ctest
%endif

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%files
%defattr(-,root,root)
%license LICENSE
%doc ChangeLog.md README.md
%{_libdir}/lib%{name}.so.*

%files devel
%defattr(-,root,root)
%{_includedir}/%{name}
%{_libdir}/lib%{name}.so
%{_libdir}/cmake/%{name}
%{_libdir}/pkgconfig/%{name}.pc

%changelog
* Tue May 27 2025 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 11.1.4-1
- Initial version. Needed by mariadb.
