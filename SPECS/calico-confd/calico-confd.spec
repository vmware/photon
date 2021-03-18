Summary:       confd is a lightweight configuration management tool
Name:          calico-confd
Version:       0.16.0
Release:       1%{?dist}
Group:         Applications/System
Vendor:        VMware, Inc.
License:       MIT
URL:           https://github.com/kelseyhightower/confd/releases
Source0:       %{name}-%{version}.tar.gz
Distribution:  Photon
BuildRequires: glide
BuildRequires: go
%define sha1 calico-confd=185217d319d6681ef0ef617b24241c2b2b359404

%description
confd is a lightweight configuration management tool that keeps local configuration files up-to-date, and reloading applications to pick up new config file changes.

%prep
%setup -q -n confd-%{version}

%build
#mkdir -p /root/.glide
mkdir -p ${GOPATH}/src/github.com/kelseyhightower/confd
cp -r * ${GOPATH}/src/github.com/kelseyhightower/confd/.
pushd ${GOPATH}/src/github.com/kelseyhightower/confd
make build

%install
pushd ${GOPATH}/src/github.com/kelseyhightower/confd
install -vdm 755 %{buildroot}%{_bindir}
install -vpm 0755 -t %{buildroot}%{_bindir}/ bin/confd

%files
%defattr(-,root,root)
%{_bindir}/confd

%changelog
*   Tue May 25 2021 Prashant S Chauhan <psinghchauha@vmware.com> 0.16.0-1
-   Update to version 0.16.0
*   Sat Aug 22 2020 Ashwin H <ashwinh@vmware.com> 0.14.0-7
-   Remove hardcoded go dependecy
*   Fri Apr 10 2020 Harinadh D <hdommaraju@vmware.com> 0.14.0-6
-   Bump up version to compile with go 1.13.5-2
*   Tue Jan 07 2020 Ashwin H <ashwinh@vmware.com> 0.14.0-5
-   Bump up version to compile with new go
*   Fri Aug 30 2019 Ashwin H <ashwinh@vmware.com> 0.14.0-4
-   Bump up version to compile with new go
*    Tue Aug 27 2019 Harinadh Dommaraju <hdommaraju@vmware.com> 0.14.0-3
-    version bump to build using go version 1.9.4-6
*    Mon Aug 06 2018 Dheeraj Shetty <dheerajs@vmware.com> 0.14.0-2
-    Build using go version 1.9.4
*    Fri Nov 03 2017 Vinay Kulkarni <kulkarniv@vmware.com> 0.14.0-1
-    Calico confd v0.14.0
*    Fri Aug 18 2017 Vinay Kulkarni <kulkarniv@vmware.com> 0.12.0-1
-    Calico confd for PhotonOS.
