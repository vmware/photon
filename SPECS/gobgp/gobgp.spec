Summary:       BGP implementation in Go
Name:          gobgp
Version:       2.27.0
Release:       2%{?dist}
Group:         Applications/System
Vendor:        VMware, Inc.
License:       Apache-2.0
URL:           https://github.com/osrg/gobgp
Source0:       %{name}-%{version}.tar.gz
%define sha1   gobgp=02fd9cd1d4f108e96811b376f06876380220ae73
Distribution:  Photon
BuildRequires: git
BuildRequires: go
%define debug_package %{nil}

%description
GoBGP is an open source BGP implementation designed from scratch for modern environment,
and implemented in a modern programming language, the Go Programming Language.

%prep
%setup -q

%build
mkdir -p ${GOPATH}/src/github.com/osrg/gobgp
cp -r * ${GOPATH}/src/github.com/osrg/gobgp/.
pushd ${GOPATH}/src/github.com/osrg/gobgp
go mod download
mkdir -p dist
pushd cmd/gobgp
go build -v -o ../../dist/gobgp -ldflags "-X main.VERSION=%{version} -s -w"
popd
pushd cmd/gobgpd
go build -v -o ../../dist/gobgpd -ldflags "-X main.VERSION=%{version} -s -w"
popd
popd

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
*   Fri Jun 11 2021 Piyush Gupta <gpiyush@vmware.com> 2.27.0-2
-   Bump up version to compile with new go
*   Mon May 03 2021 Gerrit Photon <photon-checkins@vmware.com> 2.27.0-1
-   Automatic Version Bump
*   Thu Apr 29 2021 Gerrit Photon <photon-checkins@vmware.com> 2.26.0-1
-   Automatic Version Bump
*   Fri Feb 05 2021 Harinadh D <hdommaraju@vmware.com> 2.20.0-3
-   Bump up version to compile with new go
*   Fri Jan 15 2021 Piyush Gupta<gpiyush@vmware.com> 2.20.0-2
-   Bump up version to compile with new go
*   Thu Oct 01 2020 Gerrit Photon <photon-checkins@vmware.com> 2.20.0-1
-   Automatic Version Bump
*   Fri Jul 24 2020 Gerrit Photon <photon-checkins@vmware.com> 2.19.0-1
-   Automatic Version Bump
-   Bump up version to compile with go 1.13.3-2
*   Mon Jan 21 2019 Bo Gan <ganb@vmware.com> 1.33-2
-   Build using go 1.9.7
*   Mon Sep 24 2018 Tapas Kundu <tkundu@vmware.com> 1.33-1
-   Updated to 1.33 and Build using go version 1.9
*   Mon Sep 11 2017 Vinay Kulkarni <kulkarniv@vmware.com> 1.23-1
-   Go BGP daemon for PhotonOS.
