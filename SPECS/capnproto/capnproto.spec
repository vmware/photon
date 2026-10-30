%global build_if %{photon_subrelease} >= 92

Summary:    A data interchange format and capability-based RPC system
Name:       capnproto
Version:    1.5.0
Release:    1%{?dist}
URL:        https://capnproto.org
Group:      Applications/System
Vendor:     VMware, Inc.
Distribution:   Photon

Source0: https://github.com/capnproto/capnproto/archive/refs/tags/%{name}-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}

BuildRequires: cmake

Requires: %{name}-libs = %{version}-%{release}

%description
Cap'n Proto is an insanely fast data interchange format
and capability-based RPC system. Think JSON, except binary.
Or think Protocol Buffers, except faster. In fact, in benchmarks,
Cap'n Proto is INFINITY TIMES faster than Protocol Buffers.

This package contains the schema compiler and command-line
encoder/decoder tools.

%package        libs
Summary:        Libraries for %{name}
Requires:       libgcc
Requires:       libstdc++
Requires:       openssl-libs
Requires:       zlib

%description    libs
The %{name}-libs package contains the libraries for using %{name}
in applications.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name} = %{version}-%{release}
Requires:       openssl-devel
Requires:       zlib-devel

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%autosetup -p1

%build
export CFLAGS="%{build_cflags} -DHOLES_NOT_SUPPORTED=1"
export CXXFLAGS="%{build_cxxflags} -DHOLES_NOT_SUPPORTED=1"

%{cmake} \
  -DBUILD_TESTING=%{?with_check:ON}%{!?with_check:OFF} \
  -DCMAKE_BUILD_TYPE=RelWithDebInfo \
  -DWITH_OPENSSL=ON \
  -DWITH_ZLIB=ON \
  -DCMAKE_INSTALL_PREFIX=%{_prefix} \
  -DCMAKE_INSTALL_LIBDIR=%{_libdir}

  %{cmake_build}

%install
%{cmake_install}
find %{buildroot} -name '*.la' -delete

%if 0%{?with_check}
%check
%ctest
%endif

%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_bindir}/capnp
%{_bindir}/capnpc
%{_bindir}/capnpc-c++
%{_bindir}/capnpc-capnp

%files libs
%defattr(-,root,root)
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%{_libdir}/cmake/CapnProto/

%changelog
* Mon Oct 26 2026 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 1.5.0-1
- Initial version, needed by sequoia-sq.
