Summary:        Kubernetes Metrics Server
Name:           kubernetes-metrics-server
Version:        0.2.1
Release:        28%{?dist}
License:        Apache License 2.0
URL:            https://github.com/kubernetes-incubator/metrics-server/%{name}-%{version}.tar.gz
Source0:        %{name}-%{version}.tar.gz
%define sha512  kubernetes-metrics-server-%{version}.tar.gz=4dd9c802bc0b7f5cfd778b05bf26bf701c848b30b89cc682647a44ee8c4c601252197b44ef3d6a1cff55b61b52e4cf5376e445cf4f872b22a02d6010c6cc4149
Patch0:         go-27704.patch
Patch1:         go-27842.patch
Group:          Development/Tools
Vendor:         VMware, Inc.
Distribution:   Photon
BuildRequires:  go

%description
In Kubernetes, resource usage metrics, such as container CPU and memory usage, are available through the Metrics API.
These metrics can be either accessed directly by user, for example by using kubectl top command, or used by a controller
in the cluster, e.g. Horizontal Pod Autoscaler, to make decisions.

%prep -p exit
# Using autosetup is not feasible
%setup -qn metrics-server-%{version}

pushd vendor/golang.org/x/net
%autopatch -p1
popd

%build
export ARCH=amd64
export VERSION=%{version}
export PKG=k8s.io/dns
export GOARCH=${ARCH}
export GOHOSTARCH=${ARCH}
export GOOS=linux
export GOHOSTOS=linux
export GOROOT=/usr/lib/golang
export GOPATH=/usr/share/gocode
export GO111MODULE=auto
export CGO_ENABLED=0
mkdir -p ${GOPATH}/src/github.com/kubernetes-incubator/metrics-server
cp -r * ${GOPATH}/src/github.com/kubernetes-incubator/metrics-server/
pushd ${GOPATH}/src/github.com/kubernetes-incubator/metrics-server
%make_build

%install
install -m 755 -d %{buildroot}%{_bindir}
install -pm 755 -t %{buildroot}%{_bindir} ${GOPATH}/src/github.com/kubernetes-incubator/metrics-server/metrics-server

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%{_bindir}/metrics-server

%changelog
* Tue Nov 21 2023 Piyush Gupta <gpiyush@vmware.com> 0.2.1-28
- Bump up version to compile with new go
* Wed Oct 11 2023 Piyush Gupta <gpiyush@vmware.com> 0.2.1-27
- Bump up version to compile with new go
* Tue Sep 26 2023 Piyush Gupta <gpiyush@vmware.com> 0.2.1-26
- Bump up version to compile with new go
* Fri Aug 18 2023 Piyush Gupta <gpiyush@vmware.com> 0.2.1-25
- Bump up version to compile with new go
* Thu Jun 22 2023 Piyush Gupta <gpiyush@vmware.com> 0.2.1-24
- Bump up version to compile with new go
* Wed May 03 2023 Piyush Gupta <gpiyush@vmware.com> 0.2.1-23
- Bump up version to compile with new go
* Tue Apr 04 2023 Piyush Gupta <gpiyush@vmware.com> 0.2.1-22
- Bump up version to compile with new go
* Tue Dec 20 2022 Piyush Gupta <gpiyush@vmware.com> 0.2.1-21
- Bump up version to compile with new go
* Sun Nov 13 2022 Piyush Gupta <gpiyush@vmware.com> 0.2.1-20
- Bump up version to compile with new go
* Wed Oct 26 2022 Piyush Gupta <gpiyush@vmware.com> 0.2.1-19
- Bump up version to compile with new go
* Thu Sep 15 2022 Piyush Gupta <gpiyush@vmware.com> 0.2.1-18
- Bump up version to compile with new go
* Thu Aug 18 2022 Piyush Gupta <gpiyush@vmware.com> 0.2.1-17
- Bump up version to compile with new go
* Mon May 09 2022 Piyush Gupta <gpiyush@vmware.com> 0.2.1-16
- Bump up version to compile with new go
* Wed Mar 16 2022 Piyush Gupta <gpiyush@vmware.com> 0.2.1-15
- Bump up version to compile with new go
* Tue Feb 22 2022 Piyush Gupta <gpiyush@vmware.com> 0.2.1-14
- Bump up version to compile with new go
* Mon Jan 24 2022 Piyush Gupta <gpiyush@vmware.com> 0.2.1-13
- Bump up version to compile with new go
* Tue Nov 16 2021 Piyush Gupta <gpiyush@vmware.com> 0.2.1-12
- Bump up version to compile with new go
* Wed Oct 20 2021 Piyush Gupta <gpiyush@vmware.com> 0.2.1-11
- Bump up version to compile with new go
* Sat Aug 21 2021 Piyush Gupta<gpiyush@vmware.com> 0.2.1-10
- Bump up version to compile with new go
* Tue Jun 29 2021 Piyush Gupta <gpiyush@vmware.com> 0.2.1-9
- Bump up version to compile with new go
* Mon May 03 2021 Piyush Gupta<gpiyush@vmware.com> 0.2.1-8
- Bump up version to compile with new go
* Mon Feb 08 2021 Harinadh D <hdommaraju@vmware.com> 0.2.1-7
- Bump up version to compile with new go
* Fri Nov 27 2020 HarinadhD <hdommaraju@vmware.com> 0.2.1-6
- Bump up version to compile with new go
* Fri Apr 10 2020 Harinadh D <hdommaraju@vmware.com> 0.2.1-5
- Bump up version to compile with go 1.13.3-2
* Tue Oct 22 2019 Ashwin H <ashwinh@vmware.com> 0.2.1-4
- Bump up version to compile with go 1.13.3
* Fri Aug 30 2019 Ashwin H <ashwinh@vmware.com> 0.2.1-3
- Bump up version to compile with new go
* Mon Jan 28 2019 Bo Gan <ganb@vmware.com> 0.2.1-2
- Fix CVE-2018-17846 and CVE-2018-17143
* Tue Jul 10 2018 Dheeraj Shetty <dheerajs@vmware.com> 0.2.1-1
- kubernetes-metrics-server 0.2.1
