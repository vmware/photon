Summary:        Collection of kubernetes controllers for Calico
Name:           kube-controllers
Version:        3.6.1
Release:        28%{?dist}
License:        Apache-2.0
URL:            https://github.com/projectcalico/kube-controllers
Source0:        %{name}-%{version}.zip
%define sha512  kube-controllers=aac83cfdc1e5d66847fef1e46469ed8b720f22336edf4652397de34ebaeeaa90c2a5fb06bbfb124ef506fceea7fb859b9cb8223803a85f438865da9c63b78957
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
%autosetup -n %{name}-%{version}

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
CGO_ENABLED=0 GO111MODULE=auto go build -v -o dist/kube-controllers cmd/kube-controllers/main.go
CGO_ENABLED=0 GO111MODULE=auto go build -v -o dist/check-status cmd/check-status/main.go
popd

%install
pushd ${GOPATH}/src/github.com/projectcalico
install -vdm 755 %{buildroot}%{_bindir}
install kube-controllers/dist/kube-controllers %{buildroot}%{_bindir}/
install kube-controllers/dist/check-status %{buildroot}%{_bindir}/
eu-elfcompress -q -p -t none %{buildroot}%{_bindir}/*

%files
%defattr(-,root,root)
%{_bindir}/kube-controllers
%{_bindir}/check-status

%changelog
* Tue Nov 21 2023 Piyush Gupta <gpiyush@vmware.com> 3.6.1-28
- Bump up version to compile with new go
* Wed Oct 11 2023 Piyush Gupta <gpiyush@vmware.com> 3.6.1-27
- Bump up version to compile with new go
* Tue Sep 26 2023 Piyush Gupta <gpiyush@vmware.com> 3.6.1-26
- Bump up version to compile with new go
* Fri Aug 18 2023 Piyush Gupta <gpiyush@vmware.com> 3.6.1-25
- Bump up version to compile with new go
* Thu Jun 22 2023 Piyush Gupta <gpiyush@vmware.com> 3.6.1-24
- Bump up version to compile with new go
* Wed May 03 2023 Piyush Gupta <gpiyush@vmware.com> 3.6.1-23
- Bump up version to compile with new go
* Tue Apr 04 2023 Piyush Gupta <gpiyush@vmware.com> 3.6.1-22
- Bump up version to compile with new go
* Tue Dec 20 2022 Piyush Gupta <gpiyush@vmware.com> 3.6.1-21
- Bump up version to compile with new go
* Sun Nov 13 2022 Piyush Gupta <gpiyush@vmware.com> 3.6.1-20
- Bump up version to compile with new go
* Wed Oct 26 2022 Piyush Gupta <gpiyush@vmware.com> 3.6.1-19
- Bump up version to compile with new go
* Thu Sep 15 2022 Piyush Gupta <gpiyush@vmware.com> 3.6.1-18
- Bump up version to compile with new go
* Thu Aug 18 2022 Piyush Gupta <gpiyush@vmware.com> 3.6.1-17
- Bump up version to compile with new go
* Mon May 09 2022 Piyush Gupta <gpiyush@vmware.com> 3.6.1-16
- Bump up version to compile with new go
* Wed Mar 16 2022 Piyush Gupta <gpiyush@vmware.com> 3.6.1-15
- Bump up version to compile with new go
* Tue Feb 22 2022 Piyush Gupta <gpiyush@vmware.com> 3.6.1-14
- Bump up version to compile with new go
* Mon Jan 24 2022 Piyush Gupta <gpiyush@vmware.com> 3.6.1-13
- Bump up version to compile with new go
* Tue Nov 16 2021 Piyush Gupta <gpiyush@vmware.com> 3.6.1-12
- Bump up version to compile with new go
* Wed Oct 20 2021 Piyush Gupta <gpiyush@vmware.com> 3.6.1-11
- Bump up version to compile with new go
* Sat Aug 21 2021 Piyush Gupta<gpiyush@vmware.com> 3.6.1-10
- Bump up version to compile with new go
* Tue Jun 29 2021 Piyush Gupta <gpiyush@vmware.com> 3.6.1-9
- Bump up version to compile with new go
* Mon May 03 2021 Piyush Gupta<gpiyush@vmware.com> 3.6.1-8
- Bump up version to compile with new go
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
* Fri Jun 28 2019 Ashwin H <ashwinh@vmware.com> 3.6.1-1
- kube-controllers initial version
