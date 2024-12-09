%define gopath_comp_bgp_daemon github.com/projectcalico/calico-bgp-daemon

Summary:        GoBGP based Calico BGP Daemon
Name:           calico-bgp-daemon
Version:        0.2.2
Release:        22%{?dist}
Group:          Applications/System
Vendor:         VMware, Inc.
URL:            https://github.com/projectcalico/calico-bgp-daemon
Distribution:   Photon

Source0:        https://github.com/projectcalico/calico-bgp-daemon/archive/refs/tags/%{name}-%{version}.tar.gz
%define sha512  calico-bgp-daemon=d5d68d52797e419f8cf99cf276ae6ffefe4764a3ed321e495b39bf6a8e72ca608a32f6cede08e296b2643a7b648fe9554ea44bd3eade7eb40a1bf0c289464cef

# Created by `glide install --strip-vendor && tar --owner=root --group=root --mtime='2000-01-01 00:00Z' --transform "s,^,${name}-${version}/," -c vendor | gzip -9`
Source1:        glide-vendor-for-%{name}-%{version}.tar.gz
%define sha512  glide-vendor-for-%{name}=090a834f2b709e0e5b0d634a5aade2afb0142daacf95c5e05c57e02c8d019583950a6249d550eab311b0f708270c109df9e0af9b1e022e6c8c72f0b350afe1e4

Source2: license.txt
%include %{SOURCE2}

BuildRequires: git
BuildRequires: glide
BuildRequires: go >= 1.7

%description
GoBGP based Calico BGP Daemon, an alternative to BIRD in calico/node.

%define debug_package %{nil}

%prep
# Using autosetup is not feasible
%setup -q -c -n %{name}-%{version}
tar -xf %{SOURCE1}

mkdir -p "$(dirname src/%{gopath_comp_bgp_daemon})"
mv %{name}-%{version} src/%{gopath_comp_bgp_daemon}

%build
export GO111MODULE=auto
export GOPATH="${PWD}"

pushd src/%{gopath_comp_bgp_daemon}
go build -v -o dist/calico-bgp-daemon -ldflags "-X main.VERSION=%{version} -s -w" main.go ipam.go
popd

%install
pushd src/%{gopath_comp_bgp_daemon}
install -vdm 755 %{buildroot}%{_bindir}
install dist/calico-bgp-daemon %{buildroot}%{_bindir}/
popd

#%%check
# No tests available for this pkg

%files
%defattr(-,root,root)
%{_bindir}/calico-bgp-daemon

%changelog
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
