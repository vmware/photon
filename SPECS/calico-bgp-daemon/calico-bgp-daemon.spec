Summary:        GoBGP based Calico BGP Daemon
Name:           calico-bgp-daemon
Version:        0.2.2
Release:        15%{?dist}
Group:          Applications/System
Vendor:         VMware, Inc.
License:        Apache-2.0
URL:            https://github.com/projectcalico/calico-bgp-daemon
Distribution:   Photon

Source0:        https://github.com/projectcalico/calico-bgp-daemon/archive/refs/tags/%{name}-%{version}.tar.gz
%define sha512  calico-bgp-daemon=d5d68d52797e419f8cf99cf276ae6ffefe4764a3ed321e495b39bf6a8e72ca608a32f6cede08e296b2643a7b648fe9554ea44bd3eade7eb40a1bf0c289464cef
Source1:        glide-cache-for-%{name}-%{version}.tar.xz
%define sha512  glide-cache-for-%{name}=ff17046029e4295c3c2fcf1f93b0a4ce23645ccf53227657d02ce75aad3f3cc2966ef2680fb315ba11216eb07e9dc28d106aca9a49924c0ac5b707721647e68d

BuildRequires: git
BuildRequires: glide
BuildRequires: go >= 1.7

%description
GoBGP based Calico BGP Daemon, an alternative to BIRD in calico/node.

%define debug_package %{nil}

%prep
%autosetup -p1

%build
export GO111MODULE=auto
mkdir -p /root/.glide
tar -C ~/.glide -xf %{SOURCE1}
mkdir -p ${GOPATH}/src/github.com/projectcalico/calico-bgp-daemon
cp -r * ${GOPATH}/src/github.com/projectcalico/calico-bgp-daemon/.
pushd ${GOPATH}/src/github.com/projectcalico/calico-bgp-daemon
mkdir -p dist
#glide install checks by default .glide dir before downloading from internet.
glide install --strip-vendor
go build -v -o dist/calico-bgp-daemon -ldflags "-X main.VERSION=%{version} -s -w" main.go ipam.go

%install
install -vdm 755 %{buildroot}%{_bindir}
install ${GOPATH}/src/github.com/projectcalico/calico-bgp-daemon/dist/calico-bgp-daemon %{buildroot}%{_bindir}/

#%%check
# No tests available for this pkg

%files
%defattr(-,root,root)
%{_bindir}/calico-bgp-daemon

%changelog
* Wed Oct 11 2023 Piyush Gupta <gpiyush@vmware.com> 0.2.2-15
- Bump up version to compile with new go
* Mon Sep 18 2023 Piyush Gupta <gpiyush@vmware.com> 0.2.2-14
- Bump up version to compile with new go
* Mon Jul 17 2023 Piyush Gupta <gpiyush@vmware.com> 0.2.2-13
- Bump up version to compile with new go
* Mon Jul 03 2023 Piyush Gupta <gpiyush@vmware.com> 0.2.2-12
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
