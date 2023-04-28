Summary:       confd is a lightweight configuration management tool
Name:          calico-confd
Version:       0.16.0
Release:       18%{?dist}
Group:         Applications/System
Vendor:        VMware, Inc.
License:       MIT
URL:           https://github.com/kelseyhightower/confd/releases
Source0:       %{name}-%{version}.tar.gz
Distribution:  Photon
BuildRequires: glide
BuildRequires: go
%define sha512  calico-confd=eafabf85d1d7193847a78dcfde7b9961bdf5b634165d27acc760aff6e4ef79cac9688abdfcac049773a28f997f87ea94e6a7606ee7f7d7aaaeaa8ba67f7e48b7

%description
confd is a lightweight configuration management tool that keeps local configuration files up-to-date, and reloading applications to pick up new config file changes.

%prep
%autosetup -n confd-%{version}

%build
#mkdir -p /root/.glide
mkdir -p ${GOPATH}/src/github.com/kelseyhightower/confd
cp -r * ${GOPATH}/src/github.com/kelseyhightower/confd/.
pushd ${GOPATH}/src/github.com/kelseyhightower/confd
go mod init
%make_build

%install
pushd ${GOPATH}/src/github.com/kelseyhightower/confd
install -vdm 755 %{buildroot}%{_bindir}
install -vpm 0755 -t %{buildroot}%{_bindir}/ bin/confd

%files
%defattr(-,root,root)
%{_bindir}/confd

%changelog
* Thu Mar 16 2023 Piyush Gupta <gpiyush@vmware.com> 0.16.0-18
- Bump up version to compile with new go
* Tue Dec 20 2022 Piyush Gupta <gpiyush@vmware.com> 0.16.0-17
- Bump up version to compile with new go
* Sun Nov 13 2022 Piyush Gupta <gpiyush@vmware.com> 0.16.0-16
- Bump up version to compile with new go
* Wed Oct 26 2022 Piyush Gupta <gpiyush@vmware.com> 0.16.0-15
- Bump up version to compile with new go
* Thu Sep 15 2022 Piyush Gupta <gpiyush@vmware.com> 0.16.0-14
- Bump up version to compile with new go
* Fri Aug 19 2022 Piyush Gupta <gpiyush@vmware.com> 0.16.0-13
- Bump up version to compile with new go
* Tue Jul 12 2022 Piyush Gupta <gpiyush@vmware.com> 0.16.0-12
- Bump up version to compile with new go
*   Sat May 07 2022 Piyush Gupta <gpiyush@vmware.com> 0.16.0-11
-   Bump up version to compile with new go
*   Tue Feb 22 2022 Piyush Gupta <gpiyush@vmware.com> 0.16.0-10
-   Bump up version to compile with new go
*   Mon Jan 24 2022 Piyush Gupta <gpiyush@vmware.com> 0.16.0-9
-   Bump up version to compile with new go
*   Wed Oct 20 2021 Piyush Gupta <gpiyush@vmware.com> 0.16.0-8
-   Bump up version to compile with new go
*   Tue Oct 05 2021 Piyush Gupta <gpiyush@vmware.com> 0.16.0-7
-   Bump up version to compile with new go
*   Fri Jun 11 2021 Piyush Gupta <gpiyush@vmware.com> 0.16.0-6
-   Bump up version to compile with new go
*   Thu Mar 25 2021 Piyush Gupta<gpiyush@vmware.com> 0.16.0-5
-   Bump up version to compile with new go
*   Fri Feb 05 2021 Harinadh D <hdommaraju@vmware.com> 0.16.0-4
-   Bump up version to compile with new go
*   Fri Jan 15 2021 Piyush Gupta<gpiyush@vmware.com> 0.16.0-3
-   Bump up version to compile with new go
*    Tue Oct 06 2020 Ashwin H <ashwinh@vmware.com> 0.16.0-2
-    Build using go 1.14
*    Mon Jun 22 2020 Gerrit Photon <photon-checkins@vmware.com> 0.16.0-1
-    Automatic Version Bump
*    Mon Jan 21 2019 Bo Gan <ganb@vmware.com> 0.14.0-3
-    Build using go 1.9.7
*    Mon Sep 24 2018 Tapas Kundu <tkundu@vmware.com> 0.14.0-2
-    Build using go version 1.9
*    Fri Nov 03 2017 Vinay Kulkarni <kulkarniv@vmware.com> 0.14.0-1
-    Calico confd v0.14.0
*    Fri Aug 18 2017 Vinay Kulkarni <kulkarniv@vmware.com> 0.12.0-1
-    Calico confd for PhotonOS.
