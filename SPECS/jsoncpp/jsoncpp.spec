Summary:        A JSON implementation in C++
Name:           jsoncpp
Version:        1.9.4
Release:        1%{?dist}
License:        MIT
URL:            https://github.com/open-source-parsers/jsoncpp
Source0:        https://github.com/open-source-parsers/jsoncpp/archive/%{name}-%{version}.tar.gz
%define sha1    %{name}=aed798e3d3214e4d3f996054e6c8a0a529afda69
Group:          System Environment/Base
Vendor:         VMware, Inc.
Distribution:   Photon
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
%setup -q

%build
cmake \
        -DCMAKE_BUILD_TYPE=Release \
        -DBUILD_SHARED_LIBS=ON \
        -DJSONCPP_WITH_WARNING_AS_ERROR=OFF \
        -DJSONCPP_WITH_PKGCONFIG_SUPPORT=ON \
        -DJSONCPP_WITH_POST_BUILD_UNITTEST=OFF \
        -DPYTHON_EXECUTABLE=/usr/bin/python3 \
        -DCMAKE_INSTALL_PREFIX:PATH=%{_prefix} \
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
%ninja_build
%install
%ninja_install

%check
%global _smp_mflags -j1
ctest

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
%{_libdir}/objects-Release/jsoncpp_object/*.o
%{_libdir}/pkgconfig/%{name}.pc

%changelog
* Fri Sep 25 2020 Gerrit Photon <photon-checkins@vmware.com> 1.9.4-1
- Automatic Version Bump
* Wed Jul 22 2020 Gerrit Photon <photon-checkins@vmware.com> 1.9.3-1
- Automatic Version Bump
* Fri Nov 15 2019 Alexey Makhalov <amakhalov@vmware.com> 1.7.7-1
- Initial build. First version
