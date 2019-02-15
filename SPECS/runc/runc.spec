Summary:	CLI tool for spawning and running containers per OCI spec.
Name:		runc
Version:	1.0.0.rc4
Release:	3%{?dist}
License:	ASL 2.0
URL:		https://runc.io/
Source0:	https://github.com/opencontainers/runc/archive/%{name}-1.0.0-rc4.tar.gz
%define sha1 runc=ba166c907ade645ce4a41a2a20fbc13a8a6cd3ef
Source1:	https://github.com/sirupsen/logrus/archive/logrus-1.0.3.tar.gz
%define sha1 logrus=9edcef15ac3860d431b162102533911788885b5f
Source2:	https://github.com/opencontainers/runtime-spec/archive/runtime-spec-1.0.0.tar.gz
%define sha1 runtime-spec=7cd96a1bebe4cdb55d2b5f5df1e52374b016a0bd
Source3:	https://github.com/urfave/cli/archive/urfave-cli-1.19.1.tar.gz
%define sha1 urfave-cli=9044d4e160ebb954c17856785cf8fde02858d9ac
Source4:	https://github.com/golang/sys/archive/golang-sys-07c182904dbd53199946ba614a412c61d3c548f5.zip
%define sha1 golang-sys=940b297797b1defc11d67820a92becefeaa88f59
Source5:	https://github.com/golang/crypto/archive/golang-crypto-eb71ad9bd329b5ac0fd0148dd99bd62e8be8e035.zip
%define sha1 golang-crypto=775ab62e664ee2c89f624d5be6c55775360653ee
Source6:        runc-CVE-2019-5736.patch
Group:		Virtualization/Libraries
Vendor:		VMware, Inc.
Distribution: 	Photon
BuildRequires:  curl
BuildRequires:  gawk
BuildRequires:  go
BuildRequires:  iptables
BuildRequires:  pkg-config
BuildRequires:  libaio-devel
BuildRequires:  libcap-ng-devel
BuildRequires:  libseccomp
BuildRequires:  libseccomp-devel
BuildRequires:  protobuf-devel
BuildRequires:  protobuf-c-devel
BuildRequires:  python2-devel
BuildRequires:  unzip
Requires:       glibc
Requires:       libgcc
Requires:       libseccomp

%description
runC is a CLI tool for spawning and running containers according to the OCI specification. Containers are started as a child process of runC and can be embedded into various other systems without having to run a daemon.

%prep
%setup -q -n %{name}-1.0.0-rc4

%build
pushd ..
tar -xvf %{SOURCE1}
tar -xvf %{SOURCE2}
tar -xvf %{SOURCE3}
unzip %{SOURCE4}
unzip %{SOURCE5}
mkdir -p $GOPATH/src/github.com/opencontainers/runtime-spec/
mkdir -p $GOPATH/src/github.com/sirupsen/logrus
mkdir -p $GOPATH/src/github.com/urfave/cli
mkdir -p $GOPATH/src/golang.org/x/sys/
mkdir -p $GOPATH/src/golang.org/x/crypto/
mkdir -p build/src/github.com/opencontainers/runc
cp -r runtime-spec-1.0.0/* $GOPATH/src/github.com/opencontainers/runtime-spec/ 
cp -r logrus-1.0.3/* $GOPATH/src/github.com/sirupsen/logrus 
cp -r cli-1.19.1/* $GOPATH/src/github.com/urfave/cli
cp -r sys-master/* $GOPATH/src/golang.org/x/sys
cp -r crypto-master/* $GOPATH/src/golang.org/x/crypto
popd
cp -r . ../build/src/github.com/opencontainers/runc
cd ../build
export GOPATH=$GOPATH:`pwd`
cd src/github.com/opencontainers/runc
patch -p1 < %{SOURCE6}
make %{?_smp_mflags}

%install
cd ../build/src/github.com/opencontainers/runc
make install BINDIR=%{buildroot}%{_sbindir}

%files
%defattr(-,root,root)
%{_sbindir}/runc

%changelog
*   Fri Feb 15 2019 Keerthana K <keerthanak@vmware.com> 1.0.0.rc4-3
-   Rename CVE-2019-5736 patch file.
*   Mon Feb 11 2019 Bo Gan <ganb@vmware.com> 1.0.0.rc4-2
-   Fix CVE-2019-5736
*   Tue Aug 22 2017 Dheeraj Shetty <dheerajs@vmware.com> 1.0.0.rc4-1
-   Update runc package to 1.0.0.rc4.
*   Tue Apr 25 2017 Vinay Kulkarni <kulkarniv@vmware.com> 0.1.1-1
-   Initial runc package for PhotonOS.
