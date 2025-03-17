%ifarch aarch64
%global gohostarch      arm64
%else
%global gohostarch      amd64
%endif

Summary:        photon-os-container-builder is an open source project to compose and deploy photon OS containers
Name:           photon-os-container-builder
Version:        0.1.1
Release:        12%{?dist}
Group:          Deployment/Tools
Vendor:         VMware, Inc.
Distribution:   Photon

URL:            https://github.com/vmware-samples/%{name}/archive/refs/tags/v%{version}.tar.gz
Source0:        %{name}-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}

BuildRequires:  glibc
BuildRequires:  git
BuildRequires:  go
BuildRequires:  systemd-devel

Requires(pre): systemd-rpm-macros
Requires: systemd
Requires: dbus
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
* Wed Dec 11 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 0.1.1-12
- Release bump for SRP compliance
* Thu Sep 19 2024 Mukul Sikka <mukul.sikka@broadcom.com> 0.1.1-11
- Bump version as a part of go upgrade
* Fri Jul 12 2024 Mukul Sikka <mukul.sikka@broadcom.com> 0.1.1-10
- Bump version as a part of go upgrade
* Thu Jun 20 2024 Mukul Sikka <msikka@vmware.com> 0.1.1-9
- Bump version as a part of go upgrade
* Thu Feb 22 2024 Mukul Sikka <msikka@vmware.com> 0.1.1-8
- Bump version as a part of go upgrade
* Tue Nov 21 2023 Piyush Gupta <gpiyush@vmware.com> 0.1.1-7
- Bump up version to compile with new go
* Wed Oct 11 2023 Piyush Gupta <gpiyush@vmware.com> 0.1.1-6
- Bump up version to compile with new go
* Mon Sep 18 2023 Piyush Gupta <gpiyush@vmware.com> 0.1.1-5
- Bump up version to compile with new go
* Mon Jul 17 2023 Piyush Gupta <gpiyush@vmware.com> 0.1.1-4
- Bump up version to compile with new go
* Thu Jun 22 2023 Piyush Gupta <gpiyush@vmware.com> 0.1.1-3
- Bump up version to compile with new go
* Wed May 03 2023 Piyush Gupta <gpiyush@vmware.com> 0.1.1-2
- Bump up version to compile with new go
* Tue Mar 21 2023 Nitesh Kumar <kunitesh@vmware.com> 0.1.1-1
- Initial release
