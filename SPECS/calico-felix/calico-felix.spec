Summary:       A per-host daemon for Calico
Name:          calico-felix
Version:       3.20.2
Release:       9%{?dist}
Group:         Applications/System
Vendor:        VMware, Inc.
License:       Apache-2.0
URL:           https://github.com/projectcalico/felix
Source0:       %{name}-%{version}.tar.gz
%define sha512  calico-felix=794dc56f812b01bcccc52b925fb5309efb35d94ac4c48b0f6e2a028cce51524c30831b729cae7faa445f091aaf2c2c1d4d92c52bd6985548aaacc9b97bdb328c
Distribution:  Photon
BuildRequires: git
BuildRequires: go

%description
A per-host daemon for Calico.

%prep
%autosetup -n felix-%{version}

%build
mkdir -p bin
GO111MODULE=auto go build -v  -o bin/calico-felix -v \
     -ldflags " -X github.com/projectcalico/felix/buildinfo.GitVersion=<unknown>" \
               ./cmd/calico-felix

%install
install -vdm 755 %{buildroot}%{_bindir}
install bin/calico-felix %{buildroot}%{_bindir}/
eu-elfcompress -q -p -t none %{buildroot}%{_bindir}/*

%files
%defattr(-,root,root)
%{_bindir}/calico-felix

%changelog
* Wed May 03 2023 Piyush Gupta <gpiyush@vmware.com> 3.20.2-9
- Bump up version to compile with new go
* Tue Apr 04 2023 Piyush Gupta <gpiyush@vmware.com> 3.20.2-8
- Bump up version to compile with new go
* Tue Dec 20 2022 Piyush Gupta <gpiyush@vmware.com> 3.20.2-7
- Bump up version to compile with new go
* Sun Nov 13 2022 Piyush Gupta <gpiyush@vmware.com> 3.20.2-6
- Bump up version to compile with new go
* Wed Oct 26 2022 Piyush Gupta <gpiyush@vmware.com> 3.20.2-5
- Bump up version to compile with new go
* Thu Sep 15 2022 Piyush Gupta <gpiyush@vmware.com> 3.20.2-4
- Bump up version to compile with new go
* Thu Aug 18 2022 Piyush Gupta <gpiyush@vmware.com> 3.20.2-3
- Bump up version to compile with new go
* Fri May 27 2022 Piyush Gupta <gpiyush@vmware.com> 3.20.2-2
- Bump up version to compile with new go
* Tue May 17 2022 Prashant S Chauhan <psinghchauha@vmware.com> 3.20.2-1
- Update calico-felix to 3.20.2
* Wed Mar 16 2022 Piyush Gupta <gpiyush@vmware.com> 3.16.0-9
- Bump up version to compile with new go
* Tue Feb 22 2022 Piyush Gupta <gpiyush@vmware.com> 3.16.0-8
- Bump up version to compile with new go
* Mon Jan 24 2022 Piyush Gupta <gpiyush@vmware.com> 3.16.0-7
- Bump up version to compile with new go
* Tue Nov 16 2021 Piyush Gupta <gpiyush@vmware.com> 3.16.0-6
- Bump up version to compile with new go
* Wed Oct 20 2021 Piyush Gupta <gpiyush@vmware.com> 3.16.0-5
- Bump up version to compile with new go
* Sat Aug 21 2021 Piyush Gupta<gpiyush@vmware.com> 3.16.0-4
- Bump up version to compile with new go
* Tue Jun 29 2021 Piyush Gupta <gpiyush@vmware.com> 3.16.0-3
- Bump up version to compile with new go
* Wed Jun 02 2021 Piyush Gupta<gpiyush@vmware.com> 3.16.0-2
- Bump up version to compile with new go
* Tue May 25 2021 Prashant S Chauhan <psinghchauha@vmware.com> 3.16.0-1
- Update to version 3.16.0
* Mon Feb 08 2021 Harinadh D <hdommaraju@vmware.com> 2.6.0-8
- Bump up version to compile with new go
* Fri Nov 27 2020 HarinadhD <hdommaraju@vmware.com> 2.6.0-7
- Bump up version to compile with new go
* Tue Aug 18 2020 Ashwin H <ashwinh@vmware.com> 2.6.0-6
- Bump up version to compile with new go
* Fri Apr 10 2020 Harinadh D <hdommaraju@vmware.com> 2.6.0-5
- Bump up version to compile with go 1.13.3-2
* Tue Oct 22 2019 Ashwin H <ashwinh@vmware.com> 2.6.0-4
- Bump up version to compile with go 1.13.3
* Fri Aug 30 2019 Ashwin H <ashwinh@vmware.com> 2.6.0-3
- Bump up version to compile with new go
* Mon Jan 28 2019 Bo Gan <ganb@vmware.com> 2.6.0-2
- Fix CVE-2018-17846 and CVE-2018-17143
* Fri Nov 03 2017 Vinay Kulkarni <kulkarniv@vmware.com> 2.6.0-1
- Calico Felix v2.6.0.
* Tue Sep 12 2017 Vinay Kulkarni <kulkarniv@vmware.com> 2.4.1-2
- Build protoc-gen-gogofaster plugin from source.
* Sat Aug 19 2017 Vinay Kulkarni <kulkarniv@vmware.com> 2.4.1-1
- Calico Felix for PhotonOS.
