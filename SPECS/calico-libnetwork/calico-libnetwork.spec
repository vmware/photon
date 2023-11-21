Summary:       Docker libnetwork plugin for Calico
Name:          calico-libnetwork
Version:       1.1.0
Release:       31%{?dist}
Group:         Applications/System
Vendor:        VMware, Inc.
License:       Apache-2.0
URL:           https://github.com/projectcalico/libnetwork-plugin
Source0:       %{name}-%{version}.tar.gz
Distribution:  Photon
BuildRequires: git
BuildRequires: glide
BuildRequires: go
%define sha512  calico-libnetwork=bc2a44bd1afa762bda553141bd051ddd71644884da93b5a0555fe0dee1d24a1ee6f7e28c28df2957eaa2ae8f09a2bd1d7affb54081eeb42d33e1168055a38ca8
%define debug_package %{nil}

%description
Docker libnetwork plugin for Calico.

%prep
%autosetup -n libnetwork-plugin-1.1.0

%build
mkdir -p /root/.glide
mkdir -p ${GOPATH}/src/github.com/projectcalico/libnetwork-plugin
cp -r * ${GOPATH}/src/github.com/projectcalico/libnetwork-plugin/.
pushd ${GOPATH}/src/github.com/projectcalico/libnetwork-plugin
mkdir -p dist
glide install --strip-vendor
CGO_ENABLED=0 GO111MODULE=auto go build -v -o dist/libnetwork-plugin -ldflags "-X main.VERSION=%{version} -s -w" main.go

%install
pushd ${GOPATH}/src/github.com/projectcalico/libnetwork-plugin
install -vdm 0755 %{buildroot}/usr/share/calico/docker
install -vpm 0755 -t %{buildroot}/usr/share/calico/docker/ dist/libnetwork-plugin

%files
%defattr(-,root,root)
/usr/share/calico/docker/libnetwork-plugin

%changelog
* Tue Nov 21 2023 Piyush Gupta <gpiyush@vmware.com> 1.1.0-31
- Bump up version to compile with new go
* Wed Oct 11 2023 Piyush Gupta <gpiyush@vmware.com> 1.1.0-30
- Bump up version to compile with new go
* Tue Sep 26 2023 Piyush Gupta <gpiyush@vmware.com> 1.1.0-29
- Bump up version to compile with new go
* Fri Aug 18 2023 Piyush Gupta <gpiyush@vmware.com> 1.1.0-28
- Bump up version to compile with new go
* Thu Jun 22 2023 Piyush Gupta <gpiyush@vmware.com> 1.1.0-27
- Bump up version to compile with new go
* Wed May 03 2023 Piyush Gupta <gpiyush@vmware.com> 1.1.0-26
- Bump up version to compile with new go
* Tue Apr 04 2023 Piyush Gupta <gpiyush@vmware.com> 1.1.0-25
- Bump up version to compile with new go
* Tue Dec 20 2022 Piyush Gupta <gpiyush@vmware.com> 1.1.0-24
- Bump up version to compile with new go
* Sun Nov 13 2022 Piyush Gupta <gpiyush@vmware.com> 1.1.0-23
- Bump up version to compile with new go
* Wed Oct 26 2022 Piyush Gupta <gpiyush@vmware.com> 1.1.0-22
- Bump up version to compile with new go
* Thu Sep 15 2022 Piyush Gupta <gpiyush@vmware.com> 1.1.0-21
- Bump up version to compile with new go
* Thu Aug 18 2022 Piyush Gupta <gpiyush@vmware.com> 1.1.0-20
- Bump up version to compile with new go
* Mon May 09 2022 Piyush Gupta <gpiyush@vmware.com> 1.1.0-19
- Bump up version to compile with new go
* Wed Mar 16 2022 Piyush Gupta <gpiyush@vmware.com> 1.1.0-18
- Bump up version to compile with new go
* Tue Feb 22 2022 Piyush Gupta <gpiyush@vmware.com> 1.1.0-17
- Bump up version to compile with new go
* Mon Jan 24 2022 Piyush Gupta <gpiyush@vmware.com> 1.1.0-16
- Bump up version to compile with new go
* Tue Nov 16 2021 Piyush Gupta <gpiyush@vmware.com> 1.1.0-15
- Bump up version to compile with new go
* Wed Oct 20 2021 Piyush Gupta <gpiyush@vmware.com> 1.1.0-14
- Bump up version to compile with new go
* Sat Aug 21 2021 Piyush Gupta<gpiyush@vmware.com> 1.1.0-13
- Bump up version to compile with new go
* Tue Jun 29 2021 Piyush Gupta <gpiyush@vmware.com> 1.1.0-12
- Bump up version to compile with new go
* Mon May 03 2021 Piyush Gupta<gpiyush@vmware.com> 1.1.0-11
- Bump up version to compile with new go
* Mon Feb 08 2021 Harinadh D <hdommaraju@vmware.com> 1.1.0-10
- Bump up version to compile with new go
* Fri Nov 27 2020 HarinadhD <hdommaraju@vmware.com> 1.1.0-9
- Bump up version to compile with new go
* Tue Aug 18 2020 Ashwin H <ashwinh@vmware.com> 1.1.0-8
- Bump up version to compile with new go
* Fri Apr 10 2020 Harinadh D <hdommaraju@vmware.com> 1.1.0-7
- Bump up version to compile with go 1.13.3-2
* Tue Oct 22 2019 Ashwin H <ashwinh@vmware.com> 1.1.0-6
- Bump up version to compile with go 1.13.3
* Fri Oct 11 2019 Ashwin H <ashwinh@vmware.com> 1.1.0-5
- Build with go 1.13
* Fri Aug 30 2019 Ashwin H <ashwinh@vmware.com> 1.1.0-4
- Bump up version to compile with new go
* Mon Jan 21 2019 Bo Gan <ganb@vmware.com> 1.1.0-3
- Build using go 1.9.7
* Mon Sep 24 2018 Tapas Kundu <tkundu@vmware.com> 1.1.0-2
- Build using go version 1.9
* Fri Aug 18 2017 Vinay Kulkarni <kulkarniv@vmware.com> 1.1.0-1
- Calico libnetwork plugin for PhotonOS.
