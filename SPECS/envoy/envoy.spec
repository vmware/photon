Summary:        C++ L7 proxy and communication bus
Name:           envoy
Version:        1.2.0
Release:        3%{?dist}
License:        Apache-2.0
URL:            https://github.com/lyft/envoy
Source0:        %{name}-v%{version}.tar.gz
%define sha1    envoy=725806d38c33d82177f99ae57fd27516adacd604
Source1:        cotire.cmake
Group:          Development/Tools
Vendor:         VMware, Inc.
Distribution:   Photon
BuildArch:      x86_64
BuildRequires:  backward-cpp
BuildRequires:  c-ares-devel >= 1.11.0
BuildRequires:  cmake
BuildRequires:  clang
BuildRequires:  gcovr
BuildRequires:  python3-gcovr
BuildRequires:  gcc
BuildRequires:  git
BuildRequires:  gmp
BuildRequires:  gmp-devel
BuildRequires:  gmock
BuildRequires:  gmock-devel
BuildRequires:  gmock-static
BuildRequires:  gtest
BuildRequires:  gtest-devel
BuildRequires:  gtest-static
BuildRequires:  gperftools-devel
BuildRequires:  http-parser-devel
BuildRequires:  libevent-devel
BuildRequires:  libstdc++-devel
BuildRequires:  lightstep-tracer-cpp
BuildRequires:  nghttp2-devel
BuildRequires:  openssl-devel
BuildRequires:  protobuf-devel
BuildRequires:  rapidjson-devel
BuildRequires:  spdlog
BuildRequires:  tclap
BuildRequires:  which
Requires:       c-ares >= 1.11.0
Requires:       gperftools
Requires:       http-parser
Requires:       libevent
Requires:       libstdc++
Requires:       lightstep-tracer-cpp
Requires:       nghttp2
Requires:       openssl
Requires:       protobuf

%description
Envoy is a L7 proxy and communication bus designed for large modern service oriented architectures.

%package test
Summary: Contains envoy-test and envoy.gdb tools
Group: Development/Tools
Requires: envoy = %{version}-%{release}
%description test
Contains envoy-test and envoy.gdb tools

%prep
%setup -q
cp %{SOURCE1} %{_builddir}/%{name}-%{version}/
git init .
git add .
git -c user.name='Envoy Builder' -c user.email='nobody@noorg.org' commit -m 'Envoy Sources %{name}%{version}'
git -c user.name='Envoy Builder' -c user.email='nobody@noorg.org' tag -a 'v%{version}' -m '%{name}%{version}'
git checkout 'v%{version}'
sed -i "s#-Werror##g" common.cmake
sed -i "s#static-libstdc++#lstdc++#g" CMakeLists.txt
sed -i '/target_link_libraries(envoy-test gmock)/a target_link_libraries(envoy-test gtest)' test/CMakeLists.txt

%build
export CC=`which gcc`
export CXX=`which g++`
export LD_LIBRARY_PATH=%{_libdir}:$(LD_LIBRARY_PATH)
mkdir -p build
cd build
cmake \
    -DCMAKE_INSTALL_PREFIX:PATH=%{_prefix} \
    -DCLANG-FORMAT:FILEPATH=clang-format \
    -DENVOY_COTIRE_MODULE_DIR:FILEPATH=%{_builddir}/%{name}-%{version} \
    -DENVOY_PROTOBUF_INCLUDE_DIR:FILEPATH=%{_includedir} \
    -DENVOY_PROTOBUF_PROTOC:FILEPATH=%{_bindir}/protoc \
    -DENVOY_EXE_EXTRA_LINKER_FLAGS:STRING=-L%{_libdir} \
    -DENVOY_TEST_EXTRA_LINKER_FLAGS:STRING=-L%{_libdir} \
    -DENVOY_DEBUG:BOOL=OFF \
    -DENVOY_STRIP:BOOL=ON \
    ..
cmake -L ..
make %{?_smp_mflags}
make all_pch
make envoy
make envoy-server
make envoy-test
make envoy-common

%install
cd build
make preinstall
mkdir -p %{buildroot}%{_sysconfdir}/envoy
mkdir -p %{buildroot}%{_bindir}
cp source/exe/envoy %{buildroot}%{_bindir}
cp test/envoy-test %{buildroot}%{_bindir}
cp source/exe/envoy.dbg %{buildroot}%{_bindir}
cp ../configs/* %{buildroot}%{_sysconfdir}/envoy

%files
%defattr(-,root,root)
%{_bindir}/envoy
%config(noreplace) %{_sysconfdir}/envoy/*

%files test
%defattr(-,root,root)
%{_bindir}/envoy-test
%{_bindir}/envoy.dbg

%changelog
*   Mon Oct 22 2018 Ajay Kaher <akaher@vmware.com> 1.2.0-3
-   Adding BuildArch
*   Mon Sep 24 2018 Alexey Makhalov <amakhalov@vmware.com> 1.2.0-2
-   Fix compilation issue. Add test subpackage
*   Thu Jun 29 2017 Vinay Kulkarni <kulkarniv@vmware.com> 1.2.0-1
-   Initial version of envoy package for Photon.
