Summary:       BGP implementation in Go
Name:          gobgp
Version:       1.23
Release:       2%{?dist}
Group:         Applications/System
Vendor:        VMware, Inc.
License:       Apache-2.0
URL:           https://github.com/osrg/gobgp
Source0:       %{name}-%{version}.tar.gz
%define sha1 gobgp=3df002f61911cf56c33bd4350fe9d2ad39bcfca5
Source1:       golang-dep-0.3.0.tar.gz
%define sha1 golang-dep-0.3.0=e5e9952227930fe1e8632edc03d690bffc3e1132
Distribution:  Photon
BuildRequires: git
BuildRequires: go >= 1.7
%define debug_package %{nil}

%description
GoBGP is an open source BGP implementation designed from scratch for modern environment and implemented in a modern programming language, the Go Programming Language.

%prep
%setup -q
%setup -q -D -T -b 1

%build
export GOPATH="$(pwd)"
cd ..
mv "${GOPATH}" gobgp
mkdir -p "${GOPATH}/src/github.com/golang"
mv dep-0.3.0 "${GOPATH}/src/github.com/golang/dep"
mkdir -p "${GOPATH}/src/github.com/osrg"
mv gobgp "${GOPATH}/src/github.com/osrg/"

cd "${GOPATH}/src/github.com/osrg/gobgp"
go get -v github.com/golang/dep/cmd/dep

"${GOPATH}/bin/dep" ensure
mkdir -p dist
go build -v -o dist/gobgp -ldflags "-X main.VERSION=%{version} -s -w" gobgp/main.go
go build -v -o dist/gobgpd -ldflags "-X main.VERSION=%{version} -s -w" gobgpd/main.go gobgpd/util.go

%install
cd src/github.com/osrg/gobgp
install -vdm 755 %{buildroot}%{_bindir}
install dist/gobgp %{buildroot}%{_bindir}/
install dist/gobgpd %{buildroot}%{_bindir}/

%files
%defattr(-,root,root)
%{_bindir}/gobgp
%{_bindir}/gobgpd
%doc src/github.com/osrg/gobgp/LICENSE 
%doc src/github.com/osrg/gobgp/README.md

%changelog
*    Tue Oct 17 2017 Bo Gan <ganb@vmware.com> 1.23-2
-    cleanup GOPATH
*    Mon Sep 11 2017 Vinay Kulkarni <kulkarniv@vmware.com> 1.23-1
-    Go BGP daemon for PhotonOS.
