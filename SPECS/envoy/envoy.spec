%global git_commit e95ef6bc43daeda16451ad4ef20979d8e07a5299

Summary:        C++ L7 proxy and communication bus
Name:           envoy
Version:        1.10.0
Release:        2%{?dist}
License:        Apache-2.0
URL:            https://github.com/lyft/envoy
Source0:        %{name}-v%{version}.tar.gz
%define sha1    envoy=d2b3d504de30507ef72604288eece9d6ec735de8
Group:          Development/Tools
Vendor:         VMware, Inc.
Distribution:   Photon
BuildRequires:  backward-cpp
BuildRequires:  c-ares-devel >= 1.11.0
BuildRequires:  cmake
BuildRequires:  automake
BuildRequires:  autoconf
BuildRequires:  clang
BuildRequires:  gcovr
BuildRequires:  python3
BuildRequires:  gcc
BuildRequires:  go >= 1.11
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
BuildRequires:  ninja-build
BuildRequires:  bazel
BuildRequires:  curl
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
%setup -q -c -n %{name}-v%{version}

%build
cd envoy-%{version}
echo -n "%{git_commit}" > SOURCE_VERSION
echo $GOPATH
go get -u github.com/bazelbuild/buildtools/buildifier
export BUILDIFIER_BIN=$GOPATH/bin/buildifier
bazel build //source/exe:envoy-static

%install
cd envoy-%{version}
mkdir -p %{buildroot}%{_sysconfdir}/envoy
mkdir -p %{buildroot}%{_bindir}
cp -pav bazel-bin/source/exe/envoy-static %{buildroot}/%{_bindir}/envoy
cp -rf configs/* %{buildroot}%{_sysconfdir}/envoy

%files
%defattr(-,root,root)
%{_bindir}/envoy
%config(noreplace) %{_sysconfdir}/envoy/*

%changelog
*   Fri Aug 30 2019 Ashwin H <ashwinh@vmware.com> 1.10.0-2
-   Bump up version to compile with new go
*    Mon Jun 03 2019 Harinadh Dommaraju <hdommaraju@vmware.c0m> 1.10.0-1
-    Upgraded envoy package from 1.2.0 to 1.10.0 to fix CVE-2019-9901 & CVE-2019-9900
*    Thu Jun 29 2017 Vinay Kulkarni <kulkarniv@vmware.com> 1.2.0-1
-    Initial version of envoy package for Photon.
