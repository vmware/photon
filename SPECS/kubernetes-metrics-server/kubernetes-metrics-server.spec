Summary:        Kubernetes Metrics Server
Name:           kubernetes-metrics-server
Version:        0.3.7
Release:        24%{?dist}
License:        Apache License 2.0
URL:            https://github.com/kubernetes-incubator/metrics-server/%{name}-%{version}.tar.gz
Source0:        %{name}-%{version}.tar.gz
%define sha512  kubernetes-metrics-server-%{version}.tar.gz=bb405974322a7c249ad40deb1ae1acaf9f73dee992a895173452181b4d5dc31b3538829cf478ab090e5e170985c21baf0162b98aed10f6ea035de4c112d8fb14
Patch0:         go-27704.patch
Patch1:         go-27842.patch
Group:          Development/Tools
Vendor:         VMware, Inc.
Distribution:   Photon
BuildRequires:  go
BuildRequires:  which

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
export GO111MODULE=auto
#CGO_ENABLED=0 go build -ldflags -X sigs.k8s.io/metrics-server/pkg/version.gitVersion=v0.3.7 -o dist/metrics-server  cmd/metrics-server
export GIT_TAG=v0.3.7
export GIT_COMMIT=ce4a44e5341552d3b0b568cfe06b849a637fea53
export ARCH=amd64
export VERSION=%{version}
export PKG=k8s.io/dns
export GOARCH=${ARCH}
export GOHOSTARCH=${ARCH}
export GOOS=linux
export GOHOSTOS=linux
export GOROOT=/usr/lib/golang
export GOPATH=/usr/share/gocode
export CGO_ENABLED=0
mkdir -p ${GOPATH}/src/github.com/kubernetes-incubator/metrics-server
cp -r * ${GOPATH}/src/github.com/kubernetes-incubator/metrics-server/
pushd ${GOPATH}/src/github.com/kubernetes-incubator/metrics-server
make all %{?_smp_mflags}

%install
install -m 755 -d %{buildroot}%{_bindir}
install -pm 755 -t %{buildroot}%{_bindir} ${GOPATH}/src/github.com/kubernetes-incubator/metrics-server/_output/amd64/metrics-server

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%{_bindir}/metrics-server

%changelog
* Thu Jun 20 2024 Mukul Sikka <msikka@vmware.com> 0.3.7-24
- Bump version as a part of go upgrade
* Thu Apr 18 2024 Mukul Sikka <msikka@vmware.com> 0.3.7-23
- Bump version as a part of go upgrade
* Tue Nov 21 2023 Piyush Gupta <gpiyush@vmware.com> 0.3.7-22
- Bump up version to compile with new go
* Wed Oct 11 2023 Piyush Gupta <gpiyush@vmware.com> 0.3.7-21
- Bump up version to compile with new go
* Fri Aug 18 2023 Piyush Gupta <gpiyush@vmware.com> 0.3.7-20
- Bump up version to compile with new go
* Tue Jun 20 2023 Piyush Gupta <gpiyush@vmware.com> 0.3.7-19
- Bump up version to compile with new go
* Wed May 03 2023 Piyush Gupta <gpiyush@vmware.com> 0.3.7-18
- Bump up version to compile with new go
* Thu Mar 16 2023 Piyush Gupta <gpiyush@vmware.com> 0.3.7-17
- Bump up version to compile with new go
* Tue Dec 20 2022 Piyush Gupta <gpiyush@vmware.com> 0.3.7-16
- Bump up version to compile with new go
* Sun Nov 13 2022 Piyush Gupta <gpiyush@vmware.com> 0.3.7-15
- Bump up version to compile with new go
* Wed Oct 26 2022 Piyush Gupta <gpiyush@vmware.com> 0.3.7-14
- Bump up version to compile with new go
* Thu Sep 15 2022 Piyush Gupta <gpiyush@vmware.com> 0.3.7-13
- Bump up version to compile with new go
* Fri Aug 19 2022 Piyush Gupta <gpiyush@vmware.com> 0.3.7-12
- Bump up version to compile with new go
* Tue Jul 12 2022 Piyush Gupta <gpiyush@vmware.com> 0.3.7-11
- Bump up version to compile with new go
*   Sat May 07 2022 Piyush Gupta <gpiyush@vmware.com> 0.3.7-10
-   Bump up version to compile with new go
*   Tue Feb 22 2022 Piyush Gupta <gpiyush@vmware.com> 0.3.7-9
-   Bump up version to compile with new go
*   Mon Jan 24 2022 Piyush Gupta <gpiyush@vmware.com> 0.3.7-8
-   Bump up version to compile with new go
*   Wed Oct 20 2021 Piyush Gupta <gpiyush@vmware.com> 0.3.7-7
-   Bump up version to compile with new go
*   Tue Oct 05 2021 Piyush Gupta <gpiyush@vmware.com> 0.3.7-6
-   Bump up version to compile with new go
*   Fri Jun 11 2021 Piyush Gupta <gpiyush@vmware.com> 0.3.7-5
-   Bump up version to compile with new go
*   Thu Mar 25 2021 Piyush Gupta<gpiyush@vmware.com> 0.3.7-4
-   Bump up version to compile with new go
*   Fri Feb 05 2021 Harinadh D <hdommaraju@vmware.com> 0.3.7-3
-   Bump up version to compile with new go
*   Fri Jan 15 2021 Piyush Gupta<gpiyush@vmware.com> 0.3.7-2
-   Bump up version to compile with new go
*   Mon Jun 22 2020 Gerrit Photon <photon-checkins@vmware.com> 0.3.7-1
-   Automatic Version Bump
*   Mon Jan 28 2019 Bo Gan <ganb@vmware.com> 0.2.1-2
-   Fix CVE-2018-17846 and CVE-2018-17143
*   Tue Jul 10 2018 Dheeraj Shetty <dheerajs@vmware.com> 0.2.1-1
-   kubernetes-metrics-server 0.2.1
