Summary:        C++ L7 proxy and communication bus
Name:           envoy
Version:        1.2.0
Release:        1%{?dist}
License:        Apache-2.0
URL:            https://github.com/lyft/envoy
Source0:        %{name}-v%{version}.tar.gz
#%define sha1    envoy=c993825bb8d4745f9f3c20a29a2a58f379099fc9
%define sha1    envoy=725806d38c33d82177f99ae57fd27516adacd604
Source1:        cotire.cmake
#Patch0:         openssl_compability.patch
Group:          Development/Tools
Vendor:         VMware, Inc.
Distribution:   Photon
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
BuildRequires:  lightstep-tracer-cpp-devel
BuildRequires:  nghttp2-devel
BuildRequires:  openssl-devel
BuildRequires:  protobuf3-devel
BuildRequires:  rapidjson-devel
BuildRequires:  spdlog
BuildRequires:  tclap
BuildRequires:  which
BuildRequires:  docker
Requires:       c-ares >= 1.11.0
Requires:       gperftools
Requires:       http-parser
Requires:       libevent
Requires:       libstdc++
Requires:       lightstep-tracer-cpp
Requires:       nghttp2
Requires:       openssl
Requires:       protobuf3

%description
Envoy is a L7 proxy and communication bus designed for large modern service oriented architectures.

%prep
%setup -q
#%patch0 -p1
cp %{SOURCE1} %{_builddir}/%{name}-%{version}/
git init .
git add .
git -c user.name='Envoy Builder' -c user.email='nobody@noorg.org' commit -m 'Envoy Sources %{name}%{version}'
git -c user.name='Envoy Builder' -c user.email='nobody@noorg.org' tag -a 'v%{version}' -m '%{name}%{version}'
git checkout 'v%{version}'
sed -i "s#-Werror##g" common.cmake
sed -i "s#static-libstdc++#lstdc++#g" CMakeLists.txt

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

%files debuginfo
%defattr(-,root,root)
%{_bindir}/envoy-test
%{_bindir}/envoy.dbg

%changelog
#*    Fri Mar 10 2019 Tapas Kundu <tkundu@vmware.com> 1.9.0-1
#-    Updated to 1.9.0
*    Thu Jun 29 2017 Vinay Kulkarni <kulkarniv@vmware.com> 1.2.0-1
-    Initial version of envoy package for Photon.
