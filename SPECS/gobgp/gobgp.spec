Summary:       BGP implementation in Go
Name:          gobgp
Version:       2.19.0
Release:       1%{?dist}
Group:         Applications/System
Vendor:        VMware, Inc.
License:       Apache-2.0
URL:           https://github.com/osrg/gobgp
Source0:       %{name}-%{version}.tar.gz
%define sha1   gobgp=bc91b2b088493d945c910764cdbb0c290f235680
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
*   Fri Jul 24 2020 Gerrit Photon <photon-checkins@vmware.com> 2.19.0-1
-   Automatic Version Bump
-   Bump up version to compile with go 1.13.3-2
*   Mon Jan 21 2019 Bo Gan <ganb@vmware.com> 1.33-2
-   Build using go 1.9.7
*   Mon Sep 24 2018 Tapas Kundu <tkundu@vmware.com> 1.33-1
-   Updated to 1.33 and Build using go version 1.9
*   Mon Sep 11 2017 Vinay Kulkarni <kulkarniv@vmware.com> 1.23-1
-   Go BGP daemon for PhotonOS.
