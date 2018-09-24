Summary:       BGP implementation in Go
Name:          gobgp
Version:       1.33
Release:       1%{?dist}
Group:         Applications/System
Vendor:        VMware, Inc.
License:       Apache-2.0
URL:           https://github.com/osrg/gobgp
Source0:       %{name}-%{version}.tar.gz
%define sha1 gobgp=8bd87fc99895eef4fd80e4f4f2217df93b0cfea3
Source1:       golang-dep-0.3.0.tar.gz
%define sha1 golang-dep-0.3.0=e5e9952227930fe1e8632edc03d690bffc3e1132
Distribution:  Photon
BuildRequires: git
BuildRequires: go = 1.9.4
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
${GOPATH}/bin/dep ensure
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
*    Mon Sep 24 2018 Tapas Kundu <tkundu@vmware.com> 1.33-1
-    Updated to 1.33 and Build using go version 1.9.4
*    Mon Sep 11 2017 Vinay Kulkarni <kulkarniv@vmware.com> 1.23-1
-    Go BGP daemon for PhotonOS.
