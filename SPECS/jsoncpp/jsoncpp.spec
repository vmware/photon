Summary:        A JSON implementation in C++
Name:           jsoncpp
Version:        1.9.5
Release:        3%{?dist}
URL:            https://github.com/open-source-parsers/jsoncpp
Group:          System Environment/Base
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        https://github.com/open-source-parsers/jsoncpp/archive/%{name}-%{version}.tar.gz
%define sha512 %{name}=1d06e044759b1e1a4cc4960189dd7e001a0a4389d7239a6d59295af995a553518e4e0337b4b4b817e70da5d9731a4c98655af90791b6287870b5ff8d73ad8873

Source1: license.txt
%include %{SOURCE1}

BuildRequires:  cmake
BuildRequires:  ninja-build
BuildRequires:  python3-devel

%description
JsonCpp is a C++ library that allows manipulating JSON values, including serialization and deserialization to and from strings.
It can also preserve existing comment in unserialization/serialization steps, making it a convenient format to store user input files.

%package devel
Summary:        Development libraries and header files for jsoncpp
Requires:       %{name} = %{version}-%{release}

%description devel
The package contains libraries and header files for
developing applications that use jsoncpp.

%prep
%autosetup -p1

%build
%cmake \
    -DCMAKE_BUILD_TYPE=Debug \
    -DBUILD_SHARED_LIBS=ON \
    -DBUILD_OBJECT_LIBS=OFF \
    -DJSONCPP_WITH_WARNING_AS_ERROR=OFF \
    -DJSONCPP_WITH_PKGCONFIG_SUPPORT=ON \
    -DJSONCPP_WITH_POST_BUILD_UNITTEST=OFF \
    -DPYTHON_EXECUTABLE=%{python3} \
    -DCMAKE_INSTALL_BINDIR:PATH=%{_bindir} \
    -DCMAKE_INSTALL_SBINDIR:PATH=%{_sbindir} \
    -DCMAKE_INSTALL_LIBDIR:PATH=%{_libdir} \
    -DCMAKE_INSTALL_LIBEXECDIR:PATH=%{_libexecdir} \
    -DCMAKE_INSTALL_LOCALSTATEDIR:PATH=%{_localstatedir} \
    -DCMAKE_INSTALL_SHAREDSTATEDIR:PATH=%{_sharedstatedir} \
    -DCMAKE_INSTALL_INCLUDEDIR:PATH=%{_includedir} \
    -DCMAKE_INSTALL_INFODIR:PATH=%{_infodir} \
    -DCMAKE_INSTALL_MANDIR:PATH=%{_mandir} \
    -GNinja

cd %{__cmake_builddir}
%ninja_build

%install
cd %{__cmake_builddir}
%ninja_install

%if 0%{?with_check}
%check
%global _smp_mflags -j1
%ctest
%endif

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_libdir}/*.so.*
%{_libdir}/cmake/jsoncpp/*.cmake

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/*.a
%{_libdir}/*.so
%{_libdir}/pkgconfig/%{name}.pc

%changelog
* Wed Dec 11 2024 Tapas Kundu <tapas.kundu@broadcom.com> 1.9.5-3
- Release bump for SRP compliance
* Tue Dec 06 2022 Prashant S Chauhan <psinghchauha@vmware.com> 1.9.5-2
- Update release to compile with python 3.11
* Mon Jul 11 2022 Gerrit Photon <photon-checkins@vmware.com> 1.9.5-1
- Automatic Version Bump
* Fri Sep 25 2020 Gerrit Photon <photon-checkins@vmware.com> 1.9.4-1
- Automatic Version Bump
* Wed Jul 22 2020 Gerrit Photon <photon-checkins@vmware.com> 1.9.3-1
- Automatic Version Bump
* Fri Nov 15 2019 Alexey Makhalov <amakhalov@vmware.com> 1.7.7-1
- Initial build. First version
