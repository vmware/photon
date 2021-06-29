Summary:       A per-host daemon for Calico
Name:          calico-felix
Version:       3.16.0
Release:       3%{?dist}
Group:         Applications/System
Vendor:        VMware, Inc.
License:       Apache-2.0
URL:           https://github.com/projectcalico/felix
Source0:       %{name}-%{version}.tar.gz
%define sha1 calico-felix=028cf9ca32ebb1b8d2f6e18515236cc0e9ed67e8
Distribution:  Photon
BuildRequires: git
BuildRequires: go

%description
A per-host daemon for Calico.

%prep
%setup -q -n felix-%{version}

%build
mkdir -p bin
GO111MODULE=auto go build -v -i -o bin/calico-felix -v \
     -ldflags " -X github.com/projectcalico/felix/buildinfo.GitVersion=<unknown>" \
               ./cmd/calico-felix

%install
install -vdm 755 %{buildroot}%{_bindir}
install bin/calico-felix %{buildroot}%{_bindir}/

%files
%defattr(-,root,root)
%{_bindir}/calico-felix

%changelog
*   Tue Jun 29 2021 Piyush Gupta <gpiyush@vmware.com> 3.16.0-3
-   Bump up version to compile with new go
*   Wed Jun 02 2021 Piyush Gupta<gpiyush@vmware.com> 3.16.0-2
-   Bump up version to compile with new go
*   Tue May 25 2021 Prashant S Chauhan <psinghchauha@vmware.com> 3.16.0-1
-   Update to version 3.16.0
*   Mon Feb 08 2021 Harinadh D <hdommaraju@vmware.com> 2.6.0-8
-   Bump up version to compile with new go
*   Fri Nov 27 2020 HarinadhD <hdommaraju@vmware.com> 2.6.0-7
-   Bump up version to compile with new go
*   Tue Aug 18 2020 Ashwin H <ashwinh@vmware.com> 2.6.0-6
-   Bump up version to compile with new go
*   Fri Apr 10 2020 Harinadh D <hdommaraju@vmware.com> 2.6.0-5
-   Bump up version to compile with go 1.13.3-2
*   Tue Oct 22 2019 Ashwin H <ashwinh@vmware.com> 2.6.0-4
-   Bump up version to compile with go 1.13.3
*   Fri Aug 30 2019 Ashwin H <ashwinh@vmware.com> 2.6.0-3
-   Bump up version to compile with new go
*    Mon Jan 28 2019 Bo Gan <ganb@vmware.com> 2.6.0-2
-    Fix CVE-2018-17846 and CVE-2018-17143
*    Fri Nov 03 2017 Vinay Kulkarni <kulkarniv@vmware.com> 2.6.0-1
-    Calico Felix v2.6.0.
*    Tue Sep 12 2017 Vinay Kulkarni <kulkarniv@vmware.com> 2.4.1-2
-    Build protoc-gen-gogofaster plugin from source.
*    Sat Aug 19 2017 Vinay Kulkarni <kulkarniv@vmware.com> 2.4.1-1
-    Calico Felix for PhotonOS.
