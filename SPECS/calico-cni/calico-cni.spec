Summary:        Calico networking for CNI
Name:           calico-cni
Version:        3.21.0
Release:        5%{?dist}
License:        ASL 2.0
URL:            https://github.com/projectcalico/cni-plugin
Source0:        %{name}-%{version}.tar.gz
%define sha512  calico-cni=56428498eb2c92b9d45f2e54d8698b3f9099c757049b8072167033df8ae74bf371e97b8634e3662c3c95b9adf6c19b0d723e69d2ff3f9ff59761968e4d0f80d0
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
export GO111MODULE=auto
mkdir -p dist
go build -v -o dist/calico -ldflags "-X main.VERSION= -s -w" ./cmd/calico
go build -v -o dist/calico-ipam -ldflags "-X main.VERSION= -s -w" ./cmd/calico
go build -v -o dist/install -ldflags "-X main.VERSION= -s -w" ./cmd/calico

%install
install -vdm 755 %{buildroot}/opt/cni/bin
install -vpm 0755 -t %{buildroot}/opt/cni/bin/ dist/calico
install -vpm 0755 -t %{buildroot}/opt/cni/bin/ dist/calico-ipam
install -vpm 0755 -t %{buildroot}/opt/cni/bin/ dist/install

%files
%defattr(-,root,root)
/opt/cni/bin/calico
/opt/cni/bin/calico-ipam
/opt/cni/bin/install

%changelog
* Wed Oct 26 2022 Piyush Gupta <gpiyush@vmware.com> 3.21.0-5
- Bump up version to compile with new go
* Thu Sep 15 2022 Piyush Gupta <gpiyush@vmware.com> 3.21.0-4
- Bump up version to compile with new go
* Thu Aug 18 2022 Piyush Gupta <gpiyush@vmware.com> 3.21.0-3
- Bump up version to compile with new go
* Fri May 27 2022 Piyush Gupta <gpiyush@vmware.com> 3.21.0-2
- Bump up version to compile with new go.
* Thu May 05 2022 Prashant S Chauhan <psinghchauha@vmware.com> 3.21.0-1
- Update to 3.21.0
* Wed Mar 16 2022 Piyush Gupta <gpiyush@vmware.com> 3.15.2-9
- Bump up version to compile with new go
* Tue Feb 22 2022 Piyush Gupta <gpiyush@vmware.com> 3.15.2-8
- Bump up version to compile with new go
* Mon Jan 24 2022 Piyush Gupta <gpiyush@vmware.com> 3.15.2-7
- Bump up version to compile with new go
* Tue Nov 16 2021 Piyush Gupta <gpiyush@vmware.com> 3.15.2-6
- Bump up version to compile with new go
* Wed Oct 20 2021 Piyush Gupta <gpiyush@vmware.com> 3.15.2-5
- Bump up version to compile with new go
* Sat Aug 21 2021 Piyush Gupta<gpiyush@vmware.com> 3.15.2-4
- Bump up version to compile with new go
* Tue Jun 29 2021 Piyush Gupta <gpiyush@vmware.com> 3.15.2-3
- Bump up version to compile with new go
* Wed Jun 02 2021 Piyush Gupta<gpiyush@vmware.com> 3.15.2-2
- Bump up version to compile with new go
* Tue May 25 2021 Prashant S Chauhan <psinghchauha@vmware.com> 3.15.2-1
- Update to version 3.15.2
* Mon Feb 08 2021 Harinadh D <hdommaraju@vmware.com> 3.6.1-7
- Bump up version to compile with new go
* Fri Nov 27 2020 HarinadhD <hdommaraju@vmware.com> 3.6.1-6
- Bump up version to compile with new go
* Tue Aug 18 2020 Ashwin H <ashwinh@vmware.com> 3.6.1-5
- Bump up version to compile with new go
* Fri Apr 10 2020 Harinadh D <hdommaraju@vmware.com> 3.6.1-4
- Bump up version to compile with go 1.13.3-2
* Tue Oct 22 2019 Ashwin H <ashwinh@vmware.com> 3.6.1-3
- Bump up version to compile with go 1.13.3
* Fri Aug 30 2019 Ashwin H <ashwinh@vmware.com> 3.6.1-2
- Bump up version to compile with new go
* Wed May 08 2019 Ashwin H <ashwinh@vmware.com> 3.6.1-1
- Update to 3.6.1
* Mon Jan 21 2019 Bo Gan <ganb@vmware.com> 1.11.2-3
- Build using go 1.9.7
* Mon Sep 24 2018 Tapas Kundu <tkundu@vmware.com> 1.11.2-2
- Build using go version 1.9
* Fri May 18 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 1.11.2-1
- calico-cni v1.11.2
* Thu Dec 07 2017 Vinay Kulkarni <kulkarniv@vmware.com> 1.11.0-2
- Cache build dependencies in our repo.
* Fri Nov 03 2017 Vinay Kulkarni <kulkarniv@vmware.com> 1.11.0-1
- calico-cni v1.11.0.
* Mon Aug 14 2017 Vinay Kulkarni <kulkarniv@vmware.com> 1.10.0-1
- calico-cni for PhotonOS.
