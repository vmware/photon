%define gopath_comp_k8sdns k8s.io/dns

Summary:        Kubernetes DNS
Name:           kubernetes-dns
Version:        1.22.20
Release:        13%{?dist}
URL:            https://github.com/kubernetes/dns/archive/%{version}.tar.gz
Source0:        https://github.com/kubernetes/dns/archive/refs/tags/%{name}-%{version}.tar.gz
%define sha512  %{name}=d62ea9ed6eae29e023530777896732bff4964d06f09bf1b80575af9ecb76b82ea6e7fc0ac04be41e92609cb6d5bb87de68488d57ef923c77d38cd60930e9f6cf

Source1: license.txt
%include %{SOURCE1}
Group:          Development/Tools
Vendor:         VMware, Inc.
Distribution:   Photon
BuildRequires:  go
BuildRequires:  ca-certificates

%description
Kubernetes DNS is a name lookup service for kubernetes pods.

%prep
# Using autosetup is not feasible
%setup -q -c -n dns-%{version}

mkdir -p "$(dirname src/%{gopath_comp_k8sdns})"
mv dns-%{version} src/%{gopath_comp_k8sdns}

%build
export GO111MODULE=auto
export GOPATH="${PWD}"

cd src/%{gopath_comp_k8sdns}
CGO_ENABLED=0 go install \
    -installsuffix "static" \
    -ldflags "-X %{gopath_comp_k8sdns}/pkg/version.VERSION=%{version}" \
    ./...

%install
install -m 755 -d %{buildroot}%{_bindir}
binaries=(dnsmasq-nanny e2e kube-dns sidecar sidecar-e2e)
for bin in "${binaries[@]}"; do
  echo "+++ INSTALLING ${bin}"
  install -pm 755 -t %{buildroot}%{_bindir} bin/${bin}
done

%check
export GO111MODULE=auto
export GOPATH="${PWD}"
cd src/%{gopath_comp_k8sdns}
./build/test.sh cmd pkg

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%{_bindir}/dnsmasq-nanny
%{_bindir}/e2e
%{_bindir}/kube-dns
%{_bindir}/sidecar
%{_bindir}/sidecar-e2e

%changelog
* Wed Dec 11 2024 Mukul Sikka <mukul.sikka@broadcom.com> 1.22.20-13
- Release bump for SRP compliance
* Thu Sep 19 2024 Mukul Sikka <mukul.sikka@broadcom.com> 1.22.20-12
- Bump version as a part of go upgrade
* Fri Aug 23 2024 Bo Gan <bo.gan@broadcom.com> 1.22.20-11
- Simplify build scripts
* Fri Jul 12 2024 Mukul Sikka <mukul.sikka@broadcom.com> 1.22.20-10
- Bump version as a part of go upgrade
* Thu Jun 20 2024 Mukul Sikka <msikka@vmware.com> 1.22.20-9
- Bump version as a part of go upgrade
* Thu Feb 22 2024 Mukul Sikka <msikka@vmware.com> 1.22.20-8
- Bump version as a part of go upgrade
* Tue Nov 21 2023 Piyush Gupta <gpiyush@vmware.com> 1.22.20-7
- Bump up version to compile with new go
* Wed Oct 11 2023 Piyush Gupta <gpiyush@vmware.com> 1.22.20-6
- Bump up version to compile with new go
* Mon Sep 18 2023 Piyush Gupta <gpiyush@vmware.com> 1.22.20-5
- Bump up version to compile with new go
* Mon Jul 17 2023 Piyush Gupta <gpiyush@vmware.com> 1.22.20-4
- Bump up version to compile with new go
* Thu Jun 22 2023 Piyush Gupta <gpiyush@vmware.com> 1.22.20-3
- Bump up version to compile with new go
* Wed May 03 2023 Piyush Gupta <gpiyush@vmware.com> 1.22.20-2
- Bump up version to compile with new go
* Thu Mar 09 2023 Prashant S Chauhan <psinghchauha@vmware.com> 1.22.20-1
- Update to 1.22.20
* Thu Mar 09 2023 Piyush Gupta <gpiyush@vmware.com> 1.15.6-8
- Bump up version to compile with new go
* Mon Nov 21 2022 Piyush Gupta <gpiyush@vmware.com> 1.15.6-7
- Bump up version to compile with new go
* Wed Oct 26 2022 Piyush Gupta <gpiyush@vmware.com> 1.15.6-6
- Bump up version to compile with new go
* Fri Jun 17 2022 Piyush Gupta <gpiyush@vmware.com> 1.15.6-5
- Bump up version to compile with new go
* Fri Jun 11 2021 Piyush Gupta<gpiyush@vmware.com> 1.15.6-4
- Bump up version to compile with new go
* Fri Feb 05 2021 Harinadh D <hdommaraju@vmware.com> 1.15.6-3
- Bump up version to compile with new go
* Fri Jan 15 2021 Piyush Gupta<gpiyush@vmware.com> 1.15.6-2
- Bump up version to compile with new go
* Tue Jun 30 2020 Gerrit Photon <photon-checkins@vmware.com> 1.15.6-1
- Automatic Version Bump
* Fri May 18 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 1.14.8-1
- kubernetes-dns 1.14.8.
* Tue Nov 14 2017 Alexey Makhalov <amakhalov@vmware.com> 1.14.6-3
- Aarch64 support
* Wed Nov 01 2017 Vinay Kulkarni <kulkarniv@vmware.com> 1.14.6-2
- Remove go testing framework binary.
* Mon Oct 02 2017 Vinay Kulkarni <kulkarniv@vmware.com> 1.14.6-1
- kubernetes-dns 1.14.6.
* Mon Sep 11 2017 Vinay Kulkarni <kulkarniv@vmware.com> 1.14.4-1
- kubernetes-dns 1.14.4.
* Wed Jun 28 2017 Vinay Kulkarni <kulkarniv@vmware.com> 1.14.2-1
- kubernetes-dns for PhotonOS.
