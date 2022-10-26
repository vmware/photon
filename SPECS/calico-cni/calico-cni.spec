Summary:        Calico networking for CNI
Name:           calico-cni
Version:        3.15.2
Release:        6%{?dist}
License:        ASL 2.0
URL:            https://github.com/projectcalico/cni-plugin
Source0:        https://github.com/projectcalico/calico/archive/refs/tags/%{name}-%{version}.tar.gz
%define sha512  calico-cni=2e6aaf5fd82709cccdfe0175379201d8cb0e7ac19c382bcd3b0bbeb69f7f14ea9c2faa210b0c7c2c87afd42fed0fb5f50ab3bb2645a310d98840961e74328525
Group:          Development/Tools
Vendor:         VMware, Inc.
Distribution:   Photon
BuildRequires:  git
BuildRequires:  go
Requires:       cni
%define debug_package %{nil}

%description
Project Calico network plugin for CNI. This allows kubernetes to use Calico networking. This repository includes a top-level CNI networking plugin, as well as a CNI IPAM plugin which makes use of Calico IPAM.

%prep
%autosetup -p1 -n cni-plugin-%{version}

%build
mkdir -p dist
go build -v -i -o dist/calico -ldflags "-X main.VERSION= -s -w" ./cmd/calico
go build -v -i -o dist/calico-ipam -ldflags "-X main.VERSION= -s -w" ./cmd/calico-ipam

%install
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
%{_datadir}/calico-cni/k8s/install-cni.sh
%{_datadir}/calico-cni/k8s/calico.conf.default

%changelog
* Wed Oct 26 2022 Piyush Gupta <gpiyush@vmware.com> 3.15.2-6
- Bump up version to compile with new go
*   Fri Jun 17 2022 Piyush Gupta <gpiyush@vmware.com> 3.15.2-5
-   Bump up version to compile with new go
*   Fri Jun 11 2021 Piyush Gupta<gpiyush@vmware.com> 3.15.2-4
-   Bump up version to compile with new go
*   Fri Feb 05 2021 Harinadh D <hdommaraju@vmware.com> 3.15.2-3
-   Bump up version to compile with new go
*   Fri Jan 15 2021 Piyush Gupta<gpiyush@vmware.com> 3.15.2-2
-   Bump up version to compile with new go
*   Sat Aug 29 2020 Ashwin H <ashwinh@vmware.com> 3.15.2-1
-   Update to 3.15.2
*   Wed May 08 2019 Ashwin H <ashwinh@vmware.com> 3.6.1-1
-   Update to 3.6.1
*   Mon Jan 21 2019 Bo Gan <ganb@vmware.com> 1.11.2-3
-   Build using go 1.9.7
*   Mon Sep 24 2018 Tapas Kundu <tkundu@vmware.com> 1.11.2-2
-   Build using go version 1.9
*   Fri May 18 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 1.11.2-1
-   calico-cni v1.11.2
*   Thu Dec 07 2017 Vinay Kulkarni <kulkarniv@vmware.com> 1.11.0-2
-   Cache build dependencies in our repo.
*   Fri Nov 03 2017 Vinay Kulkarni <kulkarniv@vmware.com> 1.11.0-1
-   calico-cni v1.11.0.
*   Mon Aug 14 2017 Vinay Kulkarni <kulkarniv@vmware.com> 1.10.0-1
-   calico-cni for PhotonOS.
