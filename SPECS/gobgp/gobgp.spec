%define network_required 1
%define debug_package %{nil}
Summary:       BGP implementation in Go
Name:          gobgp
Version:       3.1.0
Release:       18%{?dist}
Group:         Applications/System
Vendor:        VMware, Inc.
URL:           https://github.com/osrg/gobgp
Source0:       https://github.com/osrg/gobgp/archive/refs/tags/%{name}-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}
Distribution:  Photon
BuildRequires: git
BuildRequires: go

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
* Fri Jan 10 2025 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 3.1.0-18
- Fix go input dependencies which have Capital letters in name.
* Wed Jan 08 2025 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 3.1.0-17
- Release bump for network_required packages
* Wed Dec 11 2024 Tapas Kundu <tapas.kundu@broadcom.com> 3.1.0-16
- Release bump for SRP compliance
* Thu Sep 19 2024 Mukul Sikka <mukul.sikka@broadcom.com> 3.1.0-15
- Bump version as a part of go upgrade
* Fri Jul 12 2024 Mukul Sikka <mukul.sikka@broadcom.com> 3.1.0-14
- Bump version as a part of go upgrade
* Thu Jun 20 2024 Mukul Sikka <msikka@vmware.com> 3.1.0-13
- Bump version as a part of go upgrade
* Thu Feb 22 2024 Mukul Sikka <msikka@vmware.com> 3.1.0-12
- Bump version as a part of go upgrade
* Tue Nov 21 2023 Piyush Gupta <gpiyush@vmware.com> 3.1.0-11
- Bump up version to compile with new go
* Wed Oct 11 2023 Piyush Gupta <gpiyush@vmware.com> 3.1.0-10
- Bump up version to compile with new go
* Mon Sep 18 2023 Piyush Gupta <gpiyush@vmware.com> 3.1.0-9
- Bump up version to compile with new go
* Mon Jul 17 2023 Piyush Gupta <gpiyush@vmware.com> 3.1.0-8
- Bump up version to compile with new go
* Thu Jun 22 2023 Piyush Gupta <gpiyush@vmware.com> 3.1.0-7
- Bump up version to compile with new go
* Wed May 03 2023 Piyush Gupta <gpiyush@vmware.com> 3.1.0-6
- Bump up version to compile with new go
* Thu Mar 09 2023 Piyush Gupta <gpiyush@vmware.com> 3.1.0-5
- Bump up version to compile with new go
* Mon Nov 21 2022 Piyush Gupta <gpiyush@vmware.com> 3.1.0-4
- Bump up version to compile with new go
* Wed Oct 26 2022 Piyush Gupta <gpiyush@vmware.com> 3.1.0-3
- Bump up version to compile with new go
* Fri Jun 17 2022 Piyush Gupta <gpiyush@vmware.com> 3.1.0-2
- Bump up version to compile with new go
* Mon Apr 18 2022 Gerrit Photon <photon-checkins@vmware.com> 3.1.0-1
- Automatic Version Bump
* Fri Jun 11 2021 Piyush Gupta <gpiyush@vmware.com> 2.27.0-2
- Bump up version to compile with new go
* Mon May 03 2021 Gerrit Photon <photon-checkins@vmware.com> 2.27.0-1
- Automatic Version Bump
* Thu Apr 29 2021 Gerrit Photon <photon-checkins@vmware.com> 2.26.0-1
- Automatic Version Bump
* Fri Feb 05 2021 Harinadh D <hdommaraju@vmware.com> 2.20.0-3
- Bump up version to compile with new go
* Fri Jan 15 2021 Piyush Gupta<gpiyush@vmware.com> 2.20.0-2
- Bump up version to compile with new go
* Thu Oct 01 2020 Gerrit Photon <photon-checkins@vmware.com> 2.20.0-1
- Automatic Version Bump
* Fri Jul 24 2020 Gerrit Photon <photon-checkins@vmware.com> 2.19.0-1
- Automatic Version Bump
- Bump up version to compile with go 1.13.3-2
* Mon Jan 21 2019 Bo Gan <ganb@vmware.com> 1.33-2
- Build using go 1.9.7
* Mon Sep 24 2018 Tapas Kundu <tkundu@vmware.com> 1.33-1
- Updated to 1.33 and Build using go version 1.9
* Mon Sep 11 2017 Vinay Kulkarni <kulkarniv@vmware.com> 1.23-1
- Go BGP daemon for PhotonOS.
