Summary:       A per-host daemon for Calico
Name:          calico-felix
Version:       3.20.2
Release:       10%{?dist}
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
go build -v -i -o bin/calico-felix -v \
     -ldflags " -X github.com/projectcalico/felix/buildinfo.GitVersion=<unknown>" \
               ./cmd/calico-felix

%install
install -vdm 755 %{buildroot}%{_bindir}
install bin/calico-felix %{buildroot}%{_bindir}/

%files
%defattr(-,root,root)
%{_bindir}/calico-felix

%changelog
* Tue Dec 20 2022 Piyush Gupta <gpiyush@vmware.com> 3.20.2-10
- Bump up version to compile with new go
* Sun Nov 13 2022 Piyush Gupta <gpiyush@vmware.com> 3.20.2-9
- Bump up version to compile with new go
* Wed Oct 26 2022 Piyush Gupta <gpiyush@vmware.com> 3.20.2-8
- Bump up version to compile with new go
* Thu Sep 15 2022 Piyush Gupta <gpiyush@vmware.com> 3.20.2-7
- Bump up version to compile with new go
* Fri Aug 19 2022 Piyush Gupta <gpiyush@vmware.com> 3.20.2-6
- Bump up version to compile with new go
* Tue Jul 12 2022 Piyush Gupta <gpiyush@vmware.com> 3.20.2-5
- Bump up version to compile with new go
*   Sat May 07 2022 Piyush Gupta <gpiyush@vmware.com> 3.20.2-4
-   Bump up version to compile with new go
*   Tue Feb 22 2022 Piyush Gupta <gpiyush@vmware.com> 3.20.2-3
-   Bump up version to compile with new go
*   Mon Jan 24 2022 Piyush Gupta <gpiyush@vmware.com> 3.20.2-2
-   Bump up version to compile with new go
*   Thu Nov 18 2021 Prashant S Chauhan <psinghchauha@vmware.com> 3.20.2-1
-   Update calico-felix to v3.20.2
*   Wed Oct 20 2021 Piyush Gupta <gpiyush@vmware.com> 3.17.1-5
-   Bump up version to compile with new go
*   Tue Oct 05 2021 Piyush Gupta <gpiyush@vmware.com> 3.17.1-4
-   Bump up version to compile with new go
*   Fri Jun 11 2021 Piyush Gupta <gpiyush@vmware.com> 3.17.1-3
-   Bump up version to compile with new go
*   Thu Mar 25 2021 Piyush Gupta<gpiyush@vmware.com> 3.17.1-2
-   Bump up version to compile with new go
*   Tue Feb 09 2021 Prashant S Chauhan <psinghchauha@vmware.com> 3.17.1-1
-   Update to version 3.17.1
*   Fri Feb 05 2021 Harinadh D <hdommaraju@vmware.com> 3.16.0-3
-   Bump up version to compile with new go
*   Fri Jan 15 2021 Piyush Gupta<gpiyush@vmware.com> 3.16.0-2
-   Bump up version to compile with new go
*   Tue Jun 23 2020 Gerrit Photon <photon-checkins@vmware.com> 3.16.0-1
-   Automatic Version Bump
*   Wed Jun 17 2020 Ashwin H <ashwinh@vmware.com> 2.6.0-4
-   Fix dependency for cloud.google.com-go
*   Tue Jun 09 2020 Ashwin H <ashwinh@vmware.com> 2.6.0-3
-   Use cache for dependencies
*   Mon Jan 28 2019 Bo Gan <ganb@vmware.com> 2.6.0-2
-   Fix CVE-2018-17846 and CVE-2018-17143
*   Fri Nov 03 2017 Vinay Kulkarni <kulkarniv@vmware.com> 2.6.0-1
-   Calico Felix v2.6.0.
*   Tue Sep 12 2017 Vinay Kulkarni <kulkarniv@vmware.com> 2.4.1-2
-   Build protoc-gen-gogofaster plugin from source.
*   Sat Aug 19 2017 Vinay Kulkarni <kulkarniv@vmware.com> 2.4.1-1
-   Calico Felix for PhotonOS.
