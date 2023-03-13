Summary:       A per-host daemon for Calico
Name:          calico-felix
Version:       3.25.0
Release:       1%{?dist}
Group:         Applications/System
Vendor:        VMware, Inc.
License:       Apache-2.0
URL:           https://github.com/projectcalico/calico
Source0:       https://github.com/projectcalico/calico/archive/refs/tags/calico-%{version}.tar.gz
%define sha512 calico=8899b65be0b3b93f371942113f6bb0c958b31ff0db106d181152c3c5bf6f2f3e842719bc3ac21c573ae5fd681176ee46222798b43ebf029140a5c32ab27d9fbf
Distribution:  Photon
BuildRequires: git
BuildRequires: go

%description
ain task is to program routes and ACLs, and anything else required on the host to provide
desired connectivity for the endpoints on that host. Runs on each machine that hosts endpoints.
Runs as an agent daemon.

%prep
%autosetup -p1 -n calico-%{version}

%build
cd felix
mkdir -p dist
CGO_ENABLED=0 go build -v -o dist/calico-felix -v \
  -ldflags " -X github.com/projectcalico/felix/buildinfo.GitVersion=<unknown>" \
  ./cmd/calico-felix

%install
install -vdm 755 %{buildroot}%{_bindir}
install felix/dist/calico-felix %{buildroot}%{_bindir}/

%files
%defattr(-,root,root)
%{_bindir}/calico-felix

%changelog
* Thu Mar 09 2023 Prashant S Chauhan <psinghchauha@vmware.com> 3.25.0-1
- Update to 3.25.0
* Thu Mar 09 2023 Piyush Gupta <gpiyush@vmware.com> 3.17.1-6
- Bump up version to compile with new go
* Mon Nov 21 2022 Piyush Gupta <gpiyush@vmware.com> 3.17.1-5
- Bump up version to compile with new go
* Wed Oct 26 2022 Piyush Gupta <gpiyush@vmware.com> 3.17.1-4
- Bump up version to compile with new go
* Fri Jun 17 2022 Piyush Gupta <gpiyush@vmware.com> 3.17.1-3
- Bump up version to compile with new go
* Fri Jun 11 2021 Piyush Gupta<gpiyush@vmware.com> 3.17.1-2
- Bump up version to compile with new go
* Tue Feb 09 2021 Prashant S Chauhan <psinghchauha@vmware.com> 3.17.1-1
- Update to version 3.17.1
* Fri Feb 05 2021 Harinadh D <hdommaraju@vmware.com> 3.16.0-3
- Bump up version to compile with new go
* Fri Jan 15 2021 Piyush Gupta<gpiyush@vmware.com> 3.16.0-2
- Bump up version to compile with new go
* Tue Jun 23 2020 Gerrit Photon <photon-checkins@vmware.com> 3.16.0-1
- Automatic Version Bump
* Wed Jun 17 2020 Ashwin H <ashwinh@vmware.com> 2.6.0-4
- Fix dependency for cloud.google.com-go
* Tue Jun 09 2020 Ashwin H <ashwinh@vmware.com> 2.6.0-3
- Use cache for dependencies
* Mon Jan 28 2019 Bo Gan <ganb@vmware.com> 2.6.0-2
- Fix CVE-2018-17846 and CVE-2018-17143
* Fri Nov 03 2017 Vinay Kulkarni <kulkarniv@vmware.com> 2.6.0-1
- Calico Felix v2.6.0.
* Tue Sep 12 2017 Vinay Kulkarni <kulkarniv@vmware.com> 2.4.1-2
- Build protoc-gen-gogofaster plugin from source.
* Sat Aug 19 2017 Vinay Kulkarni <kulkarniv@vmware.com> 2.4.1-1
- Calico Felix for PhotonOS.
