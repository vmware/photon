%ifarch aarch64
%global gohostarch      arm64
%else
%global gohostarch      amd64
%endif

Summary:        photon-os-container-builder is an open source project to compose and deploy photon OS containers
Name:           photon-os-container-builder
Version:        0.1.1
Release:        1%{?dist}
License:        Apache-2.0
Group:          Deployment/Tools
Vendor:         VMware, Inc.
Distribution:   Photon

URL:            https://github.com/vmware-samples/%{name}/archive/refs/tags/v%{version}.tar.gz
Source0:        %{name}-%{version}.tar.gz
%define sha512  %{name}=309ec46806fe33e70dcaff4076fee4e748d3889b3122f72771621ecc514b70740fef2352afa8bfe2b0201470cb09ae30b60ecc31d0d31d1d421953f16754b847

BuildRequires:  glibc
BuildRequires:  git
BuildRequires:  go
BuildRequires:  systemd-devel

Requires(pre): systemd-rpm-macros
Requires: systemd
Requires: systemd-container
Requires: glibc

%description
photon-os-container-builder spawns Photon OS image as a light-weight container.
It uses systemd-nspawn to start Photon OS containers. The primary use case for
cntrctl is to run Photon OS test cases in a isolated environment. Photon OS
package manager tdnf integrated with cntrctl. Hence it allows to prepare a root
fs consisting packages depending on the user choice. It automatically prepares the
root fs and boots into the container quickly. VMDK images can be automatically
deployed via cntrctl and tested.

%prep -p exit
%autosetup -p1 -n %{name}-%{version}

%build
mkdir -p bin
go build -ldflags="-X 'main.buildVersion=${VERSION}' -X 'main.buildDate=${BUILD_DATE}'" -o bin/cntrctl ./cmd/cntrctl

%install
install -m 755 -d %{buildroot}%{_bindir}
install -m 755 -d %{buildroot}%{_sysconfdir}/photon-os-container

install bin/cntrctl %{buildroot}%{_bindir}
ln -sf %{_bindir}/cntrctl %{_bindir}/containerctl
install -m 755 distribution/photon-os-container.toml %{buildroot}%{_sysconfdir}/photon-os-container

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%{_bindir}/cntrctl
%{_sysconfdir}/photon-os-container/photon-os-container.toml

%changelog
* Tue Mar 21 2023 Nitesh Kumar <kunitesh@vmware.com> 0.1.1-1
- Initial release
