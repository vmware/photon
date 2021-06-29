Summary:       Docker libnetwork plugin for Calico
Name:          calico-libnetwork
Version:       1.1.0
Release:       12%{?dist}
Group:         Applications/System
Vendor:        VMware, Inc.
License:       Apache-2.0
URL:           https://github.com/projectcalico/libnetwork-plugin
Source0:       %{name}-%{version}.tar.gz
Distribution:  Photon
BuildRequires: git
BuildRequires: glide
BuildRequires: go
%define sha1 calico-libnetwork=bed540d714a7b2e0d0138556894541109dc7b792
%define debug_package %{nil}

%description
Docker libnetwork plugin for Calico.

%prep
%setup -q -n libnetwork-plugin-1.1.0

%build
mkdir -p /root/.glide
mkdir -p ${GOPATH}/src/github.com/projectcalico/libnetwork-plugin
cp -r * ${GOPATH}/src/github.com/projectcalico/libnetwork-plugin/.
pushd ${GOPATH}/src/github.com/projectcalico/libnetwork-plugin
mkdir -p dist
glide install --strip-vendor
CGO_ENABLED=0 GO111MODULE=auto go build -v -i -o dist/libnetwork-plugin -ldflags "-X main.VERSION=%{version} -s -w" main.go

%install
pushd ${GOPATH}/src/github.com/projectcalico/libnetwork-plugin
install -vdm 0755 %{buildroot}/usr/share/calico/docker
install -vpm 0755 -t %{buildroot}/usr/share/calico/docker/ dist/libnetwork-plugin

%files
%defattr(-,root,root)
/usr/share/calico/docker/libnetwork-plugin

%changelog
*   Tue Jun 29 2021 Piyush Gupta <gpiyush@vmware.com> 1.1.0-12
-   Bump up version to compile with new go
*   Mon May 03 2021 Piyush Gupta<gpiyush@vmware.com> 1.1.0-11
-   Bump up version to compile with new go
*   Mon Feb 08 2021 Harinadh D <hdommaraju@vmware.com> 1.1.0-10
-   Bump up version to compile with new go
*   Fri Nov 27 2020 HarinadhD <hdommaraju@vmware.com> 1.1.0-9
-   Bump up version to compile with new go
*   Tue Aug 18 2020 Ashwin H <ashwinh@vmware.com> 1.1.0-8
-   Bump up version to compile with new go
*   Fri Apr 10 2020 Harinadh D <hdommaraju@vmware.com> 1.1.0-7
-   Bump up version to compile with go 1.13.3-2
*   Tue Oct 22 2019 Ashwin H <ashwinh@vmware.com> 1.1.0-6
-   Bump up version to compile with go 1.13.3
*    Fri Oct 11 2019 Ashwin H <ashwinh@vmware.com> 1.1.0-5
-    Build with go 1.13
*    Fri Aug 30 2019 Ashwin H <ashwinh@vmware.com> 1.1.0-4
-    Bump up version to compile with new go
*    Mon Jan 21 2019 Bo Gan <ganb@vmware.com> 1.1.0-3
-    Build using go 1.9.7
*    Mon Sep 24 2018 Tapas Kundu <tkundu@vmware.com> 1.1.0-2
-    Build using go version 1.9
*    Fri Aug 18 2017 Vinay Kulkarni <kulkarniv@vmware.com> 1.1.0-1
-    Calico libnetwork plugin for PhotonOS.
