Summary:       confd is a lightweight configuration management tool
Name:          calico-confd
Version:       0.14.0
Release:       3%{?dist}
Group:         Applications/System
Vendor:        VMware, Inc.
License:       MIT
URL:           https://github.com/kelseyhightower/confd/releases
Source0:       %{name}-%{version}.tar.gz
Distribution:  Photon
BuildRequires: glide
BuildRequires: go >= 1.7
%define sha1 calico-confd=1ee7b4f992737f28a970dfeeb35faa35d1601a92

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
*   Fri Jan 03 2020 Ashwin H <ashwinh@vmware.com> 0.14.0-3
-   Bump up version to compile with new go
*   Fri Aug 30 2019 Ashwin H <ashwinh@vmware.com> 0.14.0-2
-   Bump up version to compile with new go
*    Tue Nov 07 2017 Vinay Kulkarni <kulkarniv@vmware.com> 0.14.0-1
-    Calico confd v0.14.0
*    Thu Oct 12 2017 Vinay Kulkarni <kulkarniv@vmware.com> 0.12.0-1
-    Calico confd for PhotonOS.
