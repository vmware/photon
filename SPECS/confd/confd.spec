Summary:        confd is a lightweight configuration management tool
Name:           confd
Version:        3.16
Release:        17%{?dist}
License:        Apache-2.0
URL:            https://github.com/projectcalico/confd
Source0:        %{name}-%{version}.tar.gz
%define sha512  confd=d276f896f143daac441a73234550004c43778f3faa6ec9ec38b1606423afc0e732c3f0a15e890ad451321acc7df7e7fcee1e519b61c396c4d6aaa55249effe9a
Source1:        vendor-%{name}-%{version}.tar.gz
%define sha512  vendor-%{name}-%{version}.tar.gz=5b137364931cbdd2a25f712bbebd53dbbd879225c4f5954a7da3b0681de56b903201fe81122a84f68f80fbd273bec6ec3740b9c0d9392f386b6ac237257f1a03
Obsoletes:       calico-confd
Group:          Development/Tools
Vendor:         VMware, Inc.
Distribution:   Photon
BuildRequires:  go
BuildRequires:  tar

%description
This is a Calico-specific version of confd. It is heavily modified from the original and only supports a single backend type - namely a Calico datastore. It has a single purpose which is to monitor Calico BGP configuration and to autogenerate bird BGP templates from that config.

%prep
%autosetup -n %{name}-release-v%{version}

%build
tar -zxf %{SOURCE1}
mkdir -p dist
go build -v -o dist/confd confd.go

%install
install -vdm 755 %{buildroot}/%{_bindir}/confd
install -vpm 0755 -t %{buildroot}/%{_bindir}/confd dist/confd
cp -r etc/ %{buildroot}%{_sysconfdir}

%files
%defattr(-,root,root)
%{_bindir}/confd/confd
%config(noreplace) %{_sysconfdir}/calico

%changelog
* Thu Mar 16 2023 Piyush Gupta <gpiyush@vmware.com> 3.16-17
- Bump up version to compile with new go
* Tue Dec 20 2022 Piyush Gupta <gpiyush@vmware.com> 3.16-16
- Bump up version to compile with new go
* Sun Nov 13 2022 Piyush Gupta <gpiyush@vmware.com> 3.16-15
- Bump up version to compile with new go
* Wed Oct 26 2022 Piyush Gupta <gpiyush@vmware.com> 3.16-14
- Bump up version to compile with new go
* Thu Sep 15 2022 Piyush Gupta <gpiyush@vmware.com> 3.16-13
- Bump up version to compile with new go
* Fri Aug 19 2022 Piyush Gupta <gpiyush@vmware.com> 3.16-12
- Bump up version to compile with new go
* Tue Jul 12 2022 Piyush Gupta <gpiyush@vmware.com> 3.16-11
- Bump up version to compile with new go
*   Sat May 07 2022 Piyush Gupta <gpiyush@vmware.com> 3.16-10
-   Bump up version to compile with new go
*   Tue Feb 22 2022 Piyush Gupta <gpiyush@vmware.com> 3.16-9
-   Bump up version to compile with new go
*   Mon Jan 24 2022 Piyush Gupta <gpiyush@vmware.com> 3.16-8
-   Bump up version to compile with new go
*   Wed Oct 20 2021 Piyush Gupta <gpiyush@vmware.com> 3.16-7
-   Bump up version to compile with new go
*   Tue Oct 05 2021 Piyush Gupta <gpiyush@vmware.com> 3.16-6
-   Bump up version to compile with new go
*   Fri Jun 11 2021 Piyush Gupta <gpiyush@vmware.com> 3.16-5
-   Bump up version to compile with new go
*   Thu Mar 25 2021 Piyush Gupta<gpiyush@vmware.com> 3.16-4
-   Bump up version to compile with new go
*   Fri Feb 05 2021 Harinadh D <hdommaraju@vmware.com> 3.16-3
-   Bump up version to compile with new go
*   Fri Jan 15 2021 Piyush Gupta<gpiyush@vmware.com> 3.16-2
-   Bump up version to compile with new go
*   Tue Oct 13 2020 Ashwin H <ashwinh@vmware.com> 3.16-1
-   Update to 3.16
*   Wed Jun 17 2020 Ashwin H <ashwinh@vmware.com> 3.6-3
-   Fix dependency for cloud.google.com-go
*   Tue Jun 09 2020 Ashwin H <ashwinh@vmware.com> 3.6-2
-   Use cache for dependencies
*   Fri Aug 16 2019 Ashwin H <ashwinh@vmware.com> 3.6-1
-   project calico-confd initial version
