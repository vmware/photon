%define debug_package %{nil}
%define gopath_comp_bgp_daemon github.com/projectcalico/%{name}

Summary:       GoBGP based Calico BGP Daemon
Name:          calico-bgp-daemon
Version:       0.2.2
Release:       29%{?dist}
Group:         Applications/System
Vendor:        VMware, Inc.
License:       Apache-2.0
URL:           https://github.com/projectcalico/calico-bgp-daemon
Distribution:  Photon

Source0:       %{name}-%{version}.tar.gz
%define sha512  calico-bgp-daemon=d5d68d52797e419f8cf99cf276ae6ffefe4764a3ed321e495b39bf6a8e72ca608a32f6cede08e296b2643a7b648fe9554ea44bd3eade7eb40a1bf0c289464cef
Source1:        glide-vendor-for-%{name}-%{version}.tar.gz
%define sha512  glide-vendor-for-%{name}=090a834f2b709e0e5b0d634a5aade2afb0142daacf95c5e05c57e02c8d019583950a6249d550eab311b0f708270c109df9e0af9b1e022e6c8c72f0b350afe1e4

BuildRequires: git
BuildRequires: glide
BuildRequires: go >= 1.7

%define debug_package %{nil}

Patch0:     fix-base64-encoding-issue.patch

%description
GoBGP based Calico BGP Daemon, an alternative to BIRD in calico/node.

%prep
# Using autosetup is not feasible
%setup -q -c
tar -xf %{SOURCE1}

pushd %{name}-%{version}
%patch -p1 0
popd

mkdir -p "$(dirname src/%{gopath_comp_bgp_daemon})"
mv %{name}-%{version} src/%{gopath_comp_bgp_daemon}

# Remove files to handle unintended inclusions
rm src/%{gopath_comp_bgp_daemon}/vendor/golang.org/x/text/cases/map_test.go
rm src/%{gopath_comp_bgp_daemon}/vendor/golang.org/x/text/internal/testtext/text.go
rm src/%{gopath_comp_bgp_daemon}/vendor/golang.org/x/text/unicode/norm/normalize_test.go

%build
export GO111MODULE=auto
export GOPATH="${PWD}"

pushd src/%{gopath_comp_bgp_daemon}
go build -v -o dist/%{name} -ldflags "-X main.VERSION=%{version} -s -w" main.go ipam.go
popd

%install
pushd src/%{gopath_comp_bgp_daemon}
install -vDm 755 dist/%{name} %{buildroot}%{_bindir}/%{name}
popd

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%{_bindir}/%{name}

%changelog
* Mon Nov 10 2025 Mukul Sikka <mukul.sikka@broadcom.com> 0.2.2-29
- Bump up as part of go upgrade
* Thu Sep 19 2024 Mukul Sikka <mukul.sikka@broadcom.com> 0.2.2-28
- Bump version as a part of go upgrade
* Fri Jul 12 2024 Mukul Sikka <mukul.sikka@broadcom.com> 0.2.2-27
- Bump version as a part of go upgrade
* Thu Jun 20 2024 Mukul Sikka <msikka@vmware.com> 0.2.2-26
- Bump version as a part of go upgrade
* Thu Apr 18 2024 Mukul Sikka <msikka@vmware.com> 0.2.2-25
- Bump version as a part of go upgrade
* Tue Nov 21 2023 Piyush Gupta <gpiyush@vmware.com> 0.2.2-24
- Bump up version to compile with new go
* Wed Oct 11 2023 Piyush Gupta <gpiyush@vmware.com> 0.2.2-23
- Bump up version to compile with new go
* Fri Aug 18 2023 Piyush Gupta <gpiyush@vmware.com> 0.2.2-22
- Bump up version to compile with new go
* Tue Jun 20 2023 Piyush Gupta <gpiyush@vmware.com> 0.2.2-21
- Bump up version to compile with new go
* Wed May 03 2023 Piyush Gupta <gpiyush@vmware.com> 0.2.2-20
- Bump up version to compile with new go
* Thu Mar 16 2023 Piyush Gupta <gpiyush@vmware.com> 0.2.2-19
- Bump up version to compile with new go
* Tue Dec 20 2022 Piyush Gupta <gpiyush@vmware.com> 0.2.2-18
- Bump up version to compile with new go
* Sun Nov 13 2022 Piyush Gupta <gpiyush@vmware.com> 0.2.2-17
- Bump up version to compile with new go
* Wed Oct 26 2022 Piyush Gupta <gpiyush@vmware.com> 0.2.2-16
- Bump up version to compile with new go
* Thu Sep 15 2022 Piyush Gupta <gpiyush@vmware.com> 0.2.2-15
- Bump up version to compile with new go
* Fri Aug 19 2022 Piyush Gupta <gpiyush@vmware.com> 0.2.2-14
- Bump up version to compile with new go
* Tue Jul 12 2022 Piyush Gupta <gpiyush@vmware.com> 0.2.2-13
- Bump up version to compile with new go
* Sat May 07 2022 Piyush Gupta <gpiyush@vmware.com> 0.2.2-12
- Bump up version to compile with new go
* Tue Feb 22 2022 Piyush Gupta <gpiyush@vmware.com> 0.2.2-11
- Bump up version to compile with new go
* Mon Jan 24 2022 Piyush Gupta <gpiyush@vmware.com> 0.2.2-10
- Bump up version to compile with new go
* Wed Oct 20 2021 Piyush Gupta <gpiyush@vmware.com> 0.2.2-9
- Bump up version to compile with new go
* Tue Oct 05 2021 Piyush Gupta <gpiyush@vmware.com> 0.2.2-8
- Bump up version to compile with new go
* Fri Jun 11 2021 Piyush Gupta <gpiyush@vmware.com> 0.2.2-7
- Bump up version to compile with new go
* Thu Mar 25 2021 Piyush Gupta<gpiyush@vmware.com> 0.2.2-6
- Bump up version to compile with new go
* Fri Feb 05 2021 Harinadh D <hdommaraju@vmware.com> 0.2.2-5
- Bump up version to compile with new go
* Fri Jan 15 2021 Piyush Gupta<gpiyush@vmware.com> 0.2.2-4
- Bump up version to compile with new go
* Tue Jun 09 2020 Ashwin H <ashwinh@vmware.com> 0.2.2-3
- Use cache for dependencies
* Mon Sep 11 2017 Vinay Kulkarni <kulkarniv@vmware.com> 0.2.2-2
- gobgp comes from the Go BGP package.
* Thu Aug 17 2017 Vinay Kulkarni <kulkarniv@vmware.com> 0.2.2-1
- Calico BGP daemon for PhotonOS.
