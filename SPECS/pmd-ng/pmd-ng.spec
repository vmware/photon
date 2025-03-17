%ifarch aarch64
%global gohostarch      arm64
%else
%global gohostarch      amd64
%endif

%global debug_package %{nil}

Summary:        pmd-ng (photon management daemon next gen) is an open source, super light weight remote management API Gateway
Name:           pmd-ng
Version:        0.1
Release:        12%{?dist}
URL:            https://github.com/vmware/pmd-next-gen/archive/refs/tags/v%{version}.tar.gz
Group:          Networking
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: pmd-ng-%{version}.tar.gz

Source1: %{name}.sysusers

Source2: license.txt
%include %{SOURCE2}

BuildRequires:  glibc
BuildRequires:  git
BuildRequires:  go
BuildRequires:  systemd-devel

Requires:  systemd
Requires(pre):    systemd-rpm-macros
Requires(pre):    /usr/sbin/useradd /usr/sbin/groupadd
Requires:  glibc

Obsoletes: pmd-nextgen
Provides:  pmd-nextgen

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
install -p -D -m 0644 %{SOURCE1} %{buildroot}%{_sysusersdir}/%{name}.sysusers

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%{_bindir}/photon-mgmtd
%{_bindir}/pmctl

%{_sysconfdir}/photon-mgmt/mgmt.toml
%{_unitdir}/photon-mgmtd.service
%{_sysusersdir}/%{name}.sysusers

%pre
%sysusers_create_compat %{SOURCE1}

%post
%systemd_post photon-mgmtd.service

%preun
%systemd_preun photon-mgmtd.service

%postun
%systemd_postun_with_restart photon-mgmtd.service

%changelog
* Wed Dec 11 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 0.1-12
- Release bump for SRP compliance
* Thu Sep 19 2024 Mukul Sikka <mukul.sikka@broadcom.com> 0.1-11
- Bump version as a part of go upgrade
* Fri Jul 12 2024 Mukul Sikka <mukul.sikka@broadcom.com> 0.1-10
- Bump version as a part of go upgrade
* Thu Jun 20 2024 Mukul Sikka <msikka@vmware.com> 0.1-9
- Bump version as a part of go upgrade
* Thu Feb 22 2024 Mukul Sikka <msikka@vmware.com> 0.1-8
- Bump version as a part of go upgrade
* Tue Nov 21 2023 Piyush Gupta <gpiyush@vmware.com> 0.1-7
- Bump up version to compile with new go
* Wed Oct 11 2023 Piyush Gupta <gpiyush@vmware.com> 0.1-6
- Bump up version to compile with new go
* Mon Sep 18 2023 Piyush Gupta <gpiyush@vmware.com> 0.1-5
- Bump up version to compile with new go
* Mon Jul 17 2023 Piyush Gupta <gpiyush@vmware.com> 0.1-4
- Bump up version to compile with new go
* Thu Jun 22 2023 Piyush Gupta <gpiyush@vmware.com> 0.1-3
- Bump up version to compile with new go
* Wed May 03 2023 Piyush Gupta <gpiyush@vmware.com> 0.1-2
- Bump up version to compile with new go
* Sat Apr 29 2023 Susant Sahani <ssahani@vmware.com> 0.1-1
- Initial release.
