Summary:       BGP implementation in Go
Name:          gobgp
Version:       2.9.0
Release:       5%{?dist}
Group:         Applications/System
Vendor:        VMware, Inc.
License:       Apache-2.0
URL:           https://github.com/osrg/gobgp
Source0:       %{name}-%{version}.tar.gz
%define sha1 gobgp=24228859d09fa63492e2d8fb26de9cb93bbd5f3b
Distribution:  Photon
BuildRequires: git
BuildRequires: go
%define debug_package %{nil}

%description
GoBGP is an open source BGP implementation designed from scratch for modern environment and implemented in a modern programming language, the Go Programming Language.

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
*   Mon Feb 08 2021 Harinadh D <hdommaraju@vmware.com> 2.9.0-5
-   Bump up version to compile with new go
*   Fri Nov 27 2020 HarinadhD <hdommaraju@vmware.com> 2.9.0-4
-   Bump up version to compile with new go
*   Fri Apr 10 2020 Harinadh D <hdommaraju@vmware.com> 2.9.0-3
-   Bump up version to compile with go 1.13.3-2
*   Tue Oct 22 2019 Ashwin H <ashwinh@vmware.com> 2.9.0-2
-   Bump up version to compile with go 1.13.3
*    Fri Oct 11 2019 Ashwin H <ashwinh@vmware.com> 2.9.0-1
-    Update to 2.9.0 to work with go 1.13
*    Fri Aug 30 2019 Ashwin H <ashwinh@vmware.com> 1.33-3
-    Bump up version to compile with new go
*    Mon Jan 21 2019 Bo Gan <ganb@vmware.com> 1.33-2
-    Build using go 1.9.7
*    Mon Sep 24 2018 Tapas Kundu <tkundu@vmware.com> 1.33-1
-    Updated to 1.33 and Build using go version 1.9
*    Mon Sep 11 2017 Vinay Kulkarni <kulkarniv@vmware.com> 1.23-1
-    Go BGP daemon for PhotonOS.
