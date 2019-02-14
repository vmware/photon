Summary:        Kubernetes Metrics Server
Name:           kubernetes-metrics-server
Version:        0.2.1
Release:        2%{?dist}
License:        Apache License 2.0
URL:            https://github.com/kubernetes-incubator/metrics-server/%{name}-%{version}.tar.gz
Source0:        %{name}-%{version}.tar.gz
%define sha1    kubernetes-metrics-server-%{version}.tar.gz=ac18b1360aede4647c9dbaa72bddf735b228daf3
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
%setup -qn metrics-server-%{version}

pushd vendor/golang.org/x/net
%patch0 -p1
%patch1 -p1
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
export CGO_ENABLED=0
mkdir -p ${GOPATH}/src/github.com/kubernetes-incubator/metrics-server
cp -r * ${GOPATH}/src/github.com/kubernetes-incubator/metrics-server/
pushd ${GOPATH}/src/github.com/kubernetes-incubator/metrics-server
make build

%install
install -m 755 -d %{buildroot}%{_bindir}
install -pm 755 -t %{buildroot}%{_bindir} ${GOPATH}/src/github.com/kubernetes-incubator/metrics-server/metrics-server


%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%{_bindir}/metrics-server

%changelog
*   Mon Jan 28 2019 Bo Gan <ganb@vmware.com> 0.2.1-2
-   Fix CVE-2018-17846 and CVE-2018-17143
*   Tue Jul 10 2018 Dheeraj Shetty <dheerajs@vmware.com> 0.2.1-1
-   kubernetes-metrics-server 0.2.1
