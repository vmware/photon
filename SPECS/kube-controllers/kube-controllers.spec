Summary:        Collection of kubernetes controllers for Calico
Name:           kube-controllers
Version:        3.6.1
Release:        8%{?dist}
License:        Apache-2.0
URL:            https://github.com/projectcalico/kube-controllers
Source0:        %{name}-%{version}.zip
%define sha1 kube-controllers=e871c7aa4746b5e6dc18506c5f2c6c9fae4d7df8
Source1:         go-27704.patch
Source2:         go-27842.patch
Group:          Development/Tools
Vendor:         VMware, Inc.
Distribution:   Photon
BuildRequires:  git
BuildRequires:  glide
BuildRequires:  go >= 1.11
BuildRequires:  make
BuildRequires:  unzip

%description
Collection of kubernetes controllers for Calico. There are several controllers, each of which monitors the resources in the Kubernetes API and performs a specific job in response to events.

%prep
%setup -n %{name}-%{version}

%build
mkdir -p /root/.glide
mkdir -p ${GOPATH}/src/github.com/projectcalico/kube-controllers
cp -r * ${GOPATH}/src/github.com/projectcalico/kube-controllers
pushd ${GOPATH}/src/github.com/projectcalico/kube-controllers
glide install --strip-vendor
pushd vendor/golang.org/x/net
patch -p1 < %{SOURCE1}
patch -p1 < %{SOURCE2}
popd
mkdir -p dist
mkdir -p .go-pkg-cache
CGO_ENABLED=0 GO111MODULE=auto go build -v -i -o dist/kube-controllers cmd/kube-controllers/main.go
CGO_ENABLED=0 GO111MODULE=auto go build -v -i -o dist/check-status cmd/check-status/main.go
popd

%install
pushd ${GOPATH}/src/github.com/projectcalico
install -vdm 755 %{buildroot}%{_bindir}
install kube-controllers/dist/kube-controllers %{buildroot}%{_bindir}/
install kube-controllers/dist/check-status %{buildroot}%{_bindir}/

%files
%defattr(-,root,root)
%{_bindir}/kube-controllers
%{_bindir}/check-status

%changelog
*   Mon May 03 2021 Piyush Gupta<gpiyush@vmware.com> 3.6.1-8
-   Bump up version to compile with new go
*   Mon Feb 08 2021 Harinadh D <hdommaraju@vmware.com> 3.6.1-7
-   Bump up version to compile with new go
*   Fri Nov 27 2020 HarinadhD <hdommaraju@vmware.com> 3.6.1-6
-   Bump up version to compile with new go
*   Tue Aug 18 2020 Ashwin H <ashwinh@vmware.com> 3.6.1-5
-   Bump up version to compile with new go
*   Fri Apr 10 2020 Harinadh D <hdommaraju@vmware.com> 3.6.1-4
-   Bump up version to compile with go 1.13.3-2
*   Tue Oct 22 2019 Ashwin H <ashwinh@vmware.com> 3.6.1-3
-   Bump up version to compile with go 1.13.3
*   Fri Aug 30 2019 Ashwin H <ashwinh@vmware.com> 3.6.1-2
-   Bump up version to compile with new go
*   Fri Jun 28 2019 Ashwin H <ashwinh@vmware.com> 3.6.1-1
-   kube-controllers initial version
