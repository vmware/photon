Summary:       BGP implementation in Go
Name:          gobgp
Version:       1.23
Release:       5%{?dist}
Group:         Applications/System
Vendor:        VMware, Inc.
License:       Apache-2.0
URL:           https://github.com/osrg/gobgp
Source0:       %{name}-%{version}.tar.gz
%define sha1 gobgp=3df002f61911cf56c33bd4350fe9d2ad39bcfca5
Source1:       golang-dep-0.5.3.tar.gz
%define sha1 golang-dep-0.5.3=b9ad7242f751db0229c77cf6c8c5879cbcfb4ebb
Distribution:  Photon
BuildRequires: git
BuildRequires: go >= 1.7
%define debug_package %{nil}

%description
GoBGP is an open source BGP implementation designed from scratch for modern environment and implemented in a modern programming language, the Go Programming Language.

%prep
%setup -q
mkdir -p ${GOPATH}/src/github.com/golang/dep
tar xf %{SOURCE1} --no-same-owner --strip-components 1 -C ${GOPATH}/src/github.com/golang/dep/

%build
pushd ${GOPATH}/src/github.com/golang/dep
CGO_ENABLED=0 GOOS=linux go build -v -ldflags "-s -w" -o ${GOPATH}/bin/dep ./cmd/dep/
popd
mkdir -p ${GOPATH}/src/github.com/osrg/gobgp
cp -r * ${GOPATH}/src/github.com/osrg/gobgp/.
pushd ${GOPATH}/src/github.com/osrg/gobgp
${GOPATH}/bin/dep ensure -v
mkdir -p dist
go build -v -o dist/gobgp -ldflags "-X main.VERSION=%{version} -s -w" gobgp/main.go
go build -v -o dist/gobgpd -ldflags "-X main.VERSION=%{version} -s -w" gobgpd/main.go gobgpd/util.go

%install
pushd ${GOPATH}/src/github.com/osrg/gobgp
install -vdm 755 %{buildroot}%{_bindir}
install ${GOPATH}/src/github.com/osrg/gobgp/dist/gobgp %{buildroot}%{_bindir}/
install ${GOPATH}/src/github.com/osrg/gobgp/dist/gobgpd %{buildroot}%{_bindir}/

%files
%defattr(-,root,root)
%{_bindir}/gobgp
%{_bindir}/gobgpd
%doc LICENSE README.md

%changelog
*   Fri Apr 24 2020 Harinadh D <hdommaraju@vmware.com> 1.23-5
-   Bump up version to compile with new go version
*   Fri Jan 03 2020 Ashwin H <ashwinh@vmware.com> 1.23-4
-   Bump up version to compile with new go
*   Fri Aug 30 2019 Ashwin H <ashwinh@vmware.com> 1.23-3
-   Bump up version to compile with new go
*    Tue Jun 04 2019 Ashwin H <ashwinh@vmware.com> 1.23-2
-    Update golang-dep to work with go 1.11
*    Thu Oct 12 2017 Vinay Kulkarni <kulkarniv@vmware.com> 1.23-1
-    Go BGP daemon for PhotonOS.
