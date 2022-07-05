Summary:       GoBGP based Calico BGP Daemon
Name:          calico-bgp-daemon
Version:       0.2.2
Release:       6%{?dist}
Group:         Applications/System
Vendor:        VMware, Inc.
License:       Apache-2.0
URL:           https://github.com/projectcalico/calico-bgp-daemon
Distribution:  Photon

Source0:       %{name}-%{version}.tar.gz
%define sha1 calico-bgp-daemon=d823d92d1bbb887ea885080ab2b989a75e3a338d
Source1:        glide-cache-for-%{name}-%{version}.tar.xz
%define sha1 glide-cache-for-%{name}=f331a0f7e0e18d524f111849fdf2325c419ca29e

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
