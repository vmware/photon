Summary:       A per-host daemon for Calico
Name:          calico-felix
Version:       3.17.1
Release:       1%{?dist}
Group:         Applications/System
Vendor:        VMware, Inc.
License:       Apache-2.0
URL:           https://github.com/projectcalico/felix
Source0:       %{name}-%{version}.tar.gz
%define sha1 calico-felix=7f934f44b20b72efe04e221d0a66851d9d8e9a94
Distribution:  Photon
BuildRequires: git
BuildRequires: go

%description
A per-host daemon for Calico.

%prep
%setup -q -n felix-%{version}

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
*    Mon Jan 28 2019 Bo Gan <ganb@vmware.com> 2.6.0-2
-    Fix CVE-2018-17846 and CVE-2018-17143
*    Fri Nov 03 2017 Vinay Kulkarni <kulkarniv@vmware.com> 2.6.0-1
-    Calico Felix v2.6.0.
*    Tue Sep 12 2017 Vinay Kulkarni <kulkarniv@vmware.com> 2.4.1-2
-    Build protoc-gen-gogofaster plugin from source.
*    Sat Aug 19 2017 Vinay Kulkarni <kulkarniv@vmware.com> 2.4.1-1
-    Calico Felix for PhotonOS.
