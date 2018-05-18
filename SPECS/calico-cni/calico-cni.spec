Summary:        Calico networking for CNI
Name:           calico-cni
Version:        1.11.2
Release:        1%{?dist}
License:        ASL 2.0
URL:            https://github.com/projectcalico/cni-plugin
Source0:        %{name}-%{version}.tar.gz
%define sha1 calico-cni=c12ce655eb5b1cd42c3976d6bf4ac3ebcbc4dc86
Source1:        %{name}-vendor-cache-%{version}.tar.gz
%define sha1 calico-cni-vendor-cache=7c64de41b90cc74231090441ff359936689737df
Group:          Development/Tools
Vendor:         VMware, Inc.
Distribution:   Photon
BuildRequires:  git
BuildRequires:  glide
BuildRequires:  go >= 1.7
Requires:       cni
%define debug_package %{nil}

%description
Project Calico network plugin for CNI. This allows kubernetes to use Calico networking. This repository includes a top-level CNI networking plugin, as well as a CNI IPAM plugin which makes use of Calico IPAM.

%prep
%setup -n cni-plugin-%{version}

%build
cd ..
mkdir -p build/src/github.com/projectcalico/cni-plugin
cp -r cni-plugin-%{version}/* build/src/github.com/projectcalico/cni-plugin/.
cd build
mkdir bin
export GOPATH=`pwd`
cd bin
export GOBIN=`pwd`
export PATH=$PATH:$GOBIN
cd ../src/github.com/projectcalico/cni-plugin
install %{SOURCE1} .
mkdir -p ~/.glide
tar -C ~/.glide -xf %{SOURCE1}
glide install --strip-vendor
mkdir -p dist
CGO_ENABLED=0 go build -v -i -o dist/calico -ldflags "-X main.VERSION= -s -w" calico.go
CGO_ENABLED=0 go build -v -i -o dist/calico-ipam -ldflags "-X main.VERSION= -s -w" ipam/calico-ipam.go

%install
cd ../build/src/github.com/projectcalico/cni-plugin
install -vdm 755 %{buildroot}/opt/cni/bin
install -vpm 0755 -t %{buildroot}/opt/cni/bin/ dist/calico
install -vpm 0755 -t %{buildroot}/opt/cni/bin/ dist/calico-ipam
install -vdm 0755 %{buildroot}/usr/share/calico-cni/k8s
install -vpm 0755 -t %{buildroot}/usr/share/calico-cni/k8s/ k8s-install/scripts/install-cni.sh
install -vpm 0755 -t %{buildroot}/usr/share/calico-cni/k8s/ k8s-install/scripts/calico.conf.default

%files
%defattr(-,root,root)
/opt/cni/bin/calico
/opt/cni/bin/calico-ipam
/usr/share/calico-cni/k8s/install-cni.sh
/usr/share/calico-cni/k8s/calico.conf.default

%changelog
*   Fri May 18 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 1.11.2-1
-   calico-cni v1.11.2 and support to cache-build dependencies in our repo.
*   Tue Nov 07 2017 Vinay Kulkarni <kulkarniv@vmware.com> 1.11.0-1
-   calico-cni v1.11.0.
*   Thu Oct 12 2017 Vinay Kulkarni <kulkarniv@vmware.com> 1.10.0-1
-   calico-cni for PhotonOS.
