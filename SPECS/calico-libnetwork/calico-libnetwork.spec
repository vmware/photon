Summary:       Docker libnetwork plugin for Calico
Name:          calico-libnetwork
Version:       1.1.0
Release:       2%{?dist}
Group:         Applications/System
Vendor:        VMware, Inc.
License:       Apache-2.0
URL:           https://github.com/projectcalico/libnetwork-plugin
Source0:       %{name}-%{version}.tar.gz
Distribution:  Photon
BuildRequires: git
BuildRequires: glide
BuildRequires: go >= 1.7
%define sha1 calico-libnetwork=bed540d714a7b2e0d0138556894541109dc7b792
%define debug_package %{nil}

%description
Docker libnetwork plugin for Calico.

%prep
%setup -q -n libnetwork-plugin-1.1.0

%build
export GOPATH="$(pwd)"
cd ..
mv "${GOPATH}" libnetwork-plugin
mkdir -p "${GOPATH}/src/github.com/projectcalico"
mv libnetwork-plugin "${GOPATH}/src/github.com/projectcalico/"

mkdir -p /root/.glide
cd "${GOPATH}/src/github.com/projectcalico/libnetwork-plugin"
mkdir -p dist
glide install --strip-vendor
CGO_ENABLED=0 go build -v -i -o dist/libnetwork-plugin -ldflags "-X main.VERSION=%{version} -s -w" main.go

%install
install -vdm 0755 %{buildroot}%{_datadir}/calico/docker
install -vpm 0755 -t %{buildroot}%{_datadir}/calico/docker/ src/github.com/projectcalico/libnetwork-plugin/dist/libnetwork-plugin

%files
%defattr(-,root,root)
%{_datadir}/calico/docker/libnetwork-plugin

%changelog
*    Mon Oct 16 2017 Bo Gan <ganb@vmware.com> 1.1.0-2
-    cleanup GOPATH
*    Fri Aug 18 2017 Vinay Kulkarni <kulkarniv@vmware.com> 1.1.0-1
-    Calico libnetwork plugin for PhotonOS.
