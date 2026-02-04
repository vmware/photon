%define debug_package %{nil}
%define gopath_comp_bgp_daemon github.com/projectcalico/%{name}

Summary:        GoBGP based Calico BGP Daemon
Name:           calico-bgp-daemon
Version:        0.2.2
Release:        25%{?dist}
Group:          Applications/System
Vendor:         VMware, Inc.
URL:            https://github.com/projectcalico/calico-bgp-daemon
Distribution:   Photon

Source0: https://github.com/projectcalico/calico-bgp-daemon/archive/refs/tags/%{name}-%{version}.tar.gz

# Generated using:
# glide install --strip-vendor
# tar --owner=root --group=root --mtime='2000-01-01 00:00Z' --transform "s,^,${name}-${version}/," -c vendor | gzip -9
Source1: glide-vendor-for-%{name}-%{version}.tar.gz

Source2: license.txt
%include %{SOURCE2}

Patch0: fix-base64-encoding-issue.patch

BuildRequires: git
BuildRequires: glide
BuildRequires: go

%description
GoBGP based Calico BGP Daemon, an alternative to BIRD in calico/node.

%prep
# Using autosetup is not feasible
%setup -q -c
tar -xf %{SOURCE1}

pushd %{name}-%{version}/vendor
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
* Wed Feb 04 2026 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 0.2.2-25
- Bump version as a part of go upgrade
* Thu Oct 09 2025 Mukul Sikka <mukul.sikka@broadcom.com> 0.2.2-24
- Bump version as a part of go upgrade
* Mon Jul 28 2025 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 0.2.2-23
- Clean up unintended licenses
* Thu Dec 12 2024 HarinadhD <harinadh.dommaraju@broadcom.com> 0.2.2-22
- Release bump for SRP compliance
* Thu Sep 19 2024 Mukul Sikka <mukul.sikka@broadcom.com> 0.2.2-21
- Bump version as a part of go upgrade
* Fri Aug 23 2024 Bo Gan <bo.gan@broadcom.com> 0.2.2-20
- Simplify build scripts
* Fri Jul 12 2024 Mukul Sikka <mukul.sikka@broadcom.com> 0.2.2-19
- Bump version as a part of go upgrade
* Thu Jun 20 2024 Mukul Sikka <msikka@vmware.com> 0.2.2-18
- Bump version as a part of go upgrade
* Thu Feb 22 2024 Mukul Sikka <msikka@vmware.com> 0.2.2-17
- Bump version as a part of go upgrade
* Tue Nov 21 2023 Piyush Gupta <gpiyush@vmware.com> 0.2.2-16
- Bump up version to compile with new go
* Wed Oct 11 2023 Piyush Gupta <gpiyush@vmware.com> 0.2.2-15
- Bump up version to compile with new go
* Mon Sep 18 2023 Piyush Gupta <gpiyush@vmware.com> 0.2.2-14
- Bump up version to compile with new go
* Mon Jul 17 2023 Piyush Gupta <gpiyush@vmware.com> 0.2.2-13
- Bump up version to compile with new go
* Thu Jun 22 2023 Piyush Gupta <gpiyush@vmware.com> 0.2.2-12
- Bump up version to compile with new go
* Wed May 03 2023 Piyush Gupta <gpiyush@vmware.com> 0.2.2-11
- Bump up version to compile with new go
* Thu Mar 09 2023 Piyush Gupta <gpiyush@vmware.com> 0.2.2-10
- Bump up version to compile with new go
* Mon Nov 21 2022 Piyush Gupta <gpiyush@vmware.com> 0.2.2-9
- Bump up version to compile with new go
* Wed Oct 26 2022 Piyush Gupta <gpiyush@vmware.com> 0.2.2-8
- Bump up version to compile with new go
* Fri Jun 17 2022 Piyush Gupta <gpiyush@vmware.com> 0.2.2-7
- Bump up version to compile with new go
* Fri Jun 11 2021 Piyush Gupta<gpiyush@vmware.com> 0.2.2-6
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
