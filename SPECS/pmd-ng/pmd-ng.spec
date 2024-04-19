%ifarch aarch64
%global gohostarch      arm64
%else
%global gohostarch      amd64
%endif

Summary:        pmd-ng (photon management daemon next gen) is an open source, super light weight remote management API Gateway
Name:           pmd-ng
Version:        0.1
Release:        6%{?dist}
License:        Apache-2.0
URL:            https://github.com/vmware/pmd-next-gen/archive/refs/tags/v%{version}.tar.gz
Source0:        pmd-ng-%{version}.tar.gz
%define sha512  %{name}=44a2813c8e454515a0a161203ce6a5f2d5ff72fb14b0456a5b19ca386ea9d2e1c002a34faced1fb883cc60ba53a9ebcb7c86da00e19aba5ab1630866a6b153ba
Group:          Networking
Vendor:         VMware, Inc.
Distribution:   Photon

BuildRequires:  glibc
BuildRequires:  git
BuildRequires:  go
BuildRequires:  systemd-devel

Requires:  systemd
Requires(pre):    systemd-rpm-macros
Requires(pre):    /usr/sbin/useradd /usr/sbin/groupadd
Requires:  glibc
Obsoletes: pmd-nextgen
Provides: pmd-nextgen

%global debug_package %{nil}

%description
pmd-ng is a high performance open-source, simple, and pluggable REST API gateway
designed with stateless architecture.It is written in Go, and built with performance in mind.
It features real time health monitoring, configuration and performance for systems,
networking and applications.

%prep -p exit
%autosetup -p1 -n pmd-next-gen-%{version}

%build
mkdir -p bin
go build -buildmode=pie -ldflags="-X 'main.buildVersion=${VERSION}' -X 'main.buildDate=${BUILD_DATE}'" -o bin/photon-mgmtd ./cmd/photon-mgmt
go build -ldflags="-X 'main.buildVersion=${VERSION}' -X 'main.buildDate=${BUILD_DATE}'" -o bin/pmctl ./cmd/pmctl

%install
install -m 755 -d %{buildroot}%{_bindir}
install -m 755 -d %{buildroot}%{_sysconfdir}/photon-mgmt
install -m 755 -d %{buildroot}%{_unitdir}

install bin/photon-mgmtd %{buildroot}%{_bindir}
install bin/pmctl %{buildroot}%{_bindir}
install -m 755 distribution/mgmt.toml %{buildroot}%{_sysconfdir}/photon-mgmt
install -m 0644 distribution/photon-mgmtd.service %{buildroot}%{_unitdir}

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%{_bindir}/photon-mgmtd
%{_bindir}/pmctl

%{_sysconfdir}/photon-mgmt/mgmt.toml
%{_unitdir}/photon-mgmtd.service

%pre
if ! getent group photon-mgmt >/dev/null; then
    /sbin/groupadd -r photon-mgmt
fi

if ! getent passwd photon-mgmt >/dev/null; then
    /sbin/useradd -g photon-mgmt photon-mgmt -s /sbin/nologin
fi

%post
%systemd_post photon-mgmtd.service

%preun
%systemd_preun photon-mgmtd.service

%postun
%systemd_postun_with_restart photon-mgmtd.service

%changelog
* Thu Apr 18 2024 Mukul Sikka <msikka@vmware.com> 0.1-6
- Bump version as a part of go upgrade
* Tue Nov 21 2023 Piyush Gupta <gpiyush@vmware.com> 0.1-5
- Bump up version to compile with new go
* Wed Oct 11 2023 Piyush Gupta <gpiyush@vmware.com> 0.1-4
- Bump up version to compile with new go
* Fri Aug 18 2023 Piyush Gupta <gpiyush@vmware.com> 0.1-3
- Bump up version to compile with new go
* Tue Jun 20 2023 Piyush Gupta <gpiyush@vmware.com> 0.1-2
- Bump up version to compile with new go
* Sat Apr 29 2023 Susant Sahani <ssahani@vmware.com> 0.1-1
- Initial release.
