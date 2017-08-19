Summary:       GoBGP based Calico BGP Daemon
Name:          calico-bgp-daemon
Version:       0.2.2
Release:       1%{?dist}
Group:         Applications/System
Vendor:        VMware, Inc.
License:       Apache-2.0
URL:           https://github.com/projectcalico/calico-bgp-daemon
Source0:       %{name}-%{version}.tar.gz
Distribution:  Photon
BuildRequires: git
BuildRequires: glide
BuildRequires: go >= 1.7
BuildRequires: which
%define sha1 calico-bgp-daemon=d823d92d1bbb887ea885080ab2b989a75e3a338d

%description
GoBGP based Calico BGP Daemon, an alternative to BIRD in calico/node.

%prep
%setup -q

%build
mkdir -p /root/.glide
mkdir -p ${GOPATH}/src/github.com/projectcalico/calico-bgp-daemon
cp -r * ${GOPATH}/src/github.com/projectcalico/calico-bgp-daemon/.
pushd ${GOPATH}/src/github.com/projectcalico/calico-bgp-daemon
mkdir -p dist
glide install -strip-vendor
go get -v github.com/osrg/gobgp/gobgp
go build -v -o dist/calico-bgp-daemon -ldflags "-X main.VERSION=%{version} -s -w" main.go ipam.go

%install
install -vdm 755 %{buildroot}%{_bindir}
install ${GOPATH}/bin/gobgp %{buildroot}%{_bindir}/
install ${GOPATH}/src/github.com/projectcalico/calico-bgp-daemon/dist/calico-bgp-daemon %{buildroot}%{_bindir}/

%files
%defattr(-,root,root)
%{_bindir}/gobgp
%{_bindir}/calico-bgp-daemon

%changelog
*    Wed Aug 17 2017 Vinay Kulkarni <kulkarniv@vmware.com> 0.2.2-1
-    Calico BGP daemon for PhotonOS.
