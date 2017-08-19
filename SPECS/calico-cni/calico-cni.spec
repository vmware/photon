Summary:        Calico networking for CNI
Name:           calico-cni
Version:        1.10.0
Release:        1%{?dist}
License:        ASL 2.0
URL:            https://github.com/projectcalico/cni-plugin
Source0:        %{name}-%{version}.tar.gz
%define sha1 calico-cni=6c7f7e59e8f632e1630685f5bf092c2e4a60550f
Group:          Development/Tools
Vendor:         VMware, Inc.
Distribution:   Photon
BuildRequires:  git
BuildRequires:  glide
BuildRequires:  go >= 1.7
BuildRequires:  which
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
glide install --strip-vendor
mkdir -p dist
make dist/portmap
CGO_ENABLED=0 go build -v -i -o dist/calico -ldflags "-X main.VERSION= -s -w" calico.go
CGO_ENABLED=0 go build -v -i -o dist/calico-ipam -ldflags "-X main.VERSION= -s -w" ipam/calico-ipam.go

%install
cd ../build/src/github.com/projectcalico/cni-plugin
install -vdm 755 %{buildroot}/opt/bin/cni
install -vpm 0755 -t %{buildroot}/opt/bin/cni/ dist/calico
install -vpm 0755 -t %{buildroot}/opt/bin/cni/ dist/calico-ipam
install -vpm 0755 -t %{buildroot}/opt/bin/cni/ dist/portmap
install -vdm 0755 %{buildroot}/usr/share/calico-cni/k8s
install -vpm 0755 -t %{buildroot}/usr/share/calico-cni/k8s/ k8s-install/scripts/install-cni.sh
install -vpm 0755 -t %{buildroot}/usr/share/calico-cni/k8s/ k8s-install/scripts/calico.conf.default

%files
%defattr(-,root,root)
/opt/bin/cni/calico
/opt/bin/cni/calico-ipam
/opt/bin/cni/portmap
/usr/share/calico-cni/k8s/install-cni.sh
/usr/share/calico-cni/k8s/calico.conf.default

%changelog
*   Mon Aug 14 2017 Vinay Kulkarni <kulkarniv@vmware.com> 1.10.0-1
-   calico-cni for PhotonOS.
