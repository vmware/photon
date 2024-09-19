Summary:       BGP implementation in Go
Name:          gobgp
Version:       2.20.0
Release:       26%{?dist}
Group:         Applications/System
Vendor:        VMware, Inc.
License:       Apache-2.0
URL:           https://github.com/osrg/gobgp
Source0:       %{name}-%{version}.tar.gz
%define sha512  gobgp=a344be35f70bbbfde696677a89728b3861081407b69a01e592f4b46ebd9e1e04a565837ff65a1adf762c9ad80e145451759b8248e5e15f05d419791679a118f7
Distribution:  Photon
BuildRequires: git
BuildRequires: go
%define debug_package %{nil}

%description
GoBGP is an open source BGP implementation designed from scratch for modern environment,
and implemented in a modern programming language, the Go Programming Language.

%prep
%autosetup

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
* Thu Sep 19 2024 Mukul Sikka <mukul.sikka@broadcom.com> 2.20.0-26
- Bump version as a part of go upgrade
* Fri Jul 12 2024 Mukul Sikka <mukul.sikka@broadcom.com> 2.20.0-25
- Bump version as a part of go upgrade
* Thu Jun 20 2024 Mukul Sikka <msikka@vmware.com> 2.20.0-24
- Bump version as a part of go upgrade
* Thu Apr 18 2024 Mukul Sikka <msikka@vmware.com> 2.20.0-23
- Bump version as a part of go upgrade
* Tue Nov 21 2023 Piyush Gupta <gpiyush@vmware.com> 2.20.0-22
- Bump up version to compile with new go
* Wed Oct 11 2023 Piyush Gupta <gpiyush@vmware.com> 2.20.0-21
- Bump up version to compile with new go
* Fri Aug 18 2023 Piyush Gupta <gpiyush@vmware.com> 2.20.0-20
- Bump up version to compile with new go
* Tue Jun 20 2023 Piyush Gupta <gpiyush@vmware.com> 2.20.0-19
- Bump up version to compile with new go
* Wed May 03 2023 Piyush Gupta <gpiyush@vmware.com> 2.20.0-18
- Bump up version to compile with new go
* Thu Mar 16 2023 Piyush Gupta <gpiyush@vmware.com> 2.20.0-17
- Bump up version to compile with new go
* Tue Dec 20 2022 Piyush Gupta <gpiyush@vmware.com> 2.20.0-16
- Bump up version to compile with new go
* Sun Nov 13 2022 Piyush Gupta <gpiyush@vmware.com> 2.20.0-15
- Bump up version to compile with new go
* Wed Oct 26 2022 Piyush Gupta <gpiyush@vmware.com> 2.20.0-14
- Bump up version to compile with new go
* Thu Sep 15 2022 Piyush Gupta <gpiyush@vmware.com> 2.20.0-13
- Bump up version to compile with new go
* Fri Aug 19 2022 Piyush Gupta <gpiyush@vmware.com> 2.20.0-12
- Bump up version to compile with new go
* Tue Jul 12 2022 Piyush Gupta <gpiyush@vmware.com> 2.20.0-11
- Bump up version to compile with new go
*   Sat May 07 2022 Piyush Gupta <gpiyush@vmware.com> 2.20.0-10
-   Bump up version to compile with new go
*   Tue Feb 22 2022 Piyush Gupta <gpiyush@vmware.com> 2.20.0-9
-   Bump up version to compile with new go
*   Mon Jan 24 2022 Piyush Gupta <gpiyush@vmware.com> 2.20.0-8
-   Bump up version to compile with new go
*   Wed Oct 20 2021 Piyush Gupta <gpiyush@vmware.com> 2.20.0-7
-   Bump up version to compile with new go
*   Tue Oct 05 2021 Piyush Gupta <gpiyush@vmware.com> 2.20.0-6
-   Bump up version to compile with new go
*   Fri Jun 11 2021 Piyush Gupta <gpiyush@vmware.com> 2.20.0-5
-   Bump up version to compile with new go
*   Thu Mar 25 2021 Piyush Gupta<gpiyush@vmware.com> 2.20.0-4
-   Bump up version to compile with new go
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
