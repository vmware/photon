%global debug_package %{nil}

%ifarch aarch64
%global gohostarch      arm64
%else
%global gohostarch      amd64
%endif

Summary:        Configures network interfaces in cloud enviroment
Name:           cloud-network-setup
Version:        0.2.2
Release:        10%{?dist}
License:        Apache-2.0
Group:          Networking
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://github.com/vmware/%{name}/archive/refs/tags/v%{version}.tar.gz

Source0:        https://github.com/vmware/%{name}/archive/refs/tags/%{name}-%{version}.tar.gz
%define sha512  %{name}=bf1e917dc016e46dbb3012dc3603f8e24696ce26e9a671bcc98d8d248312bcbb7f5711c4344f230bda374b3c00c8f63121e420ea75110f032acdd43b4ff47882
Source1:        %{name}.sysusers

BuildRequires:  go
BuildRequires:  systemd-devel

Requires(pre): systemd-rpm-macros
Requires:  systemd

%description
cloud-network configures network in cloud environment. In cloud environment
instances are set public IPs and private IPs. If more than one private IP is
configured then except the IP which is provided by DHCP others can't be fetched
and configured. This project is adopting towards cloud network environment such
as Azure, GCP and Amazon EC2.

%prep -p exit
%autosetup -p1 -n %{name}-%{version}

%build
export ARCH=%{gohostarch}
export VERSION=%{version}
export PKG=github.com/%{name}/%{name}
export GOARCH=${ARCH}
export GOHOSTARCH=${ARCH}
export GOOS=linux
export GOHOSTOS=linux
export GOROOT=/usr/lib/golang
export GOPATH=/usr/share/gocode
export GOBIN=/usr/share/gocode/bin
export PATH=$PATH:$GOBIN

mkdir -p ${GOPATH}/src/${PKG}
cp -rf . ${GOPATH}/src/${PKG}
pushd ${GOPATH}/src/${PKG}

go build -o bin/cloud-network ./cmd/cloud-network
go build -o bin/cnctl ./cmd/cnctl

popd

%install
install -m 755 -d %{buildroot}%{_bindir}
install -m 755 -d %{buildroot}%{_sysconfdir}/cloud-network
install -m 755 -d %{buildroot}%{_unitdir}

install -pm 755 -t %{buildroot}%{_bindir} ${GOPATH}/src/github.com/%{name}/%{name}/bin/cloud-network
install -pm 755 -t %{buildroot}%{_bindir} ${GOPATH}/src/github.com/%{name}/%{name}/bin/cnctl

install -pm 755 -t %{buildroot}%{_sysconfdir}/cloud-network ${GOPATH}/src/github.com/%{name}/%{name}/distribution/cloud-network.toml
install -pm 755 -t %{buildroot}%{_unitdir}/ ${GOPATH}/src/github.com/%{name}/%{name}/distribution/cloud-network.service
install -p -D -m 0644 %{SOURCE1} %{buildroot}%{_sysusersdir}/%{name}.sysusers

%clean
rm -rf %{buildroot}/*

%pre
%sysusers_create_compat %{SOURCE1}

%post
%systemd_post cloud-network.service

%preun
%systemd_preun cloud-network.service

%postun
%systemd_postun_with_restart cloud-network.service

%files
%defattr(-,root,root)
%{_bindir}/cloud-network
%{_bindir}/cnctl
%{_sysconfdir}/cloud-network/cloud-network.toml
%{_sysusersdir}/%{name}.sysusers
%{_unitdir}/cloud-network.service

%changelog
* Fri Jul 12 2024 Mukul Sikka <mukul.sikka@broadcom.com> 0.2.2-10
- Bump version as a part of go upgrade
* Thu Jun 20 2024 Mukul Sikka <msikka@vmware.com> 0.2.2-9
- Bump version as a part of go upgrade
* Thu Feb 22 2024 Mukul Sikka <msikka@vmware.com> 0.2.2-8
- Bump version as a part of go upgrade
* Tue Nov 21 2023 Piyush Gupta <gpiyush@vmware.com> 0.2.2-7
- Bump up version to compile with new go
* Wed Oct 11 2023 Piyush Gupta <gpiyush@vmware.com> 0.2.2-6
- Bump up version to compile with new go
* Mon Sep 18 2023 Piyush Gupta <gpiyush@vmware.com> 0.2.2-5
- Bump up version to compile with new go
* Mon Jul 17 2023 Piyush Gupta <gpiyush@vmware.com> 0.2.2-4
- Bump up version to compile with new go
* Thu Jun 22 2023 Piyush Gupta <gpiyush@vmware.com> 0.2.2-3
- Bump up version to compile with new go
* Wed May 03 2023 Piyush Gupta <gpiyush@vmware.com> 0.2.2-2
- Bump up version to compile with new go
* Mon Mar 20 2023 Nitesh Kumar <kunitesh@vmware.com> 0.2.2-1
- Version upgrade to v0.2.2
* Sun Mar 12 2023 Piyush Gupta <gpiyush@vmware.com> 0.2.1-6
- Bump up version to compile with new go
* Fri Mar 10 2023 Mukul Sikka <msikka@vmware.com> 0.2.1-5
- Use systemd-rpm-macros for user creation
* Mon Nov 21 2022 Piyush Gupta <gpiyush@vmware.com> 0.2.1-4
- Bump up version to compile with new go
* Wed Oct 26 2022 Piyush Gupta <gpiyush@vmware.com> 0.2.1-3
- Bump up version to compile with new go
* Fri Jun 17 2022 Piyush Gupta <gpiyush@vmware.com> 0.2.1-2
- Bump up version to compile with new go
* Thu Mar 03 2022 Susant Sahani <ssahani@vmware.com> 0.2.1-1
- Version bump.
* Sun Feb 13 2022 Susant Sahani <ssahani@vmware.com> 0.2-1
- Version bump.
* Wed Jun 30 2021 Susant Sahani <ssahani@vmware.com> 0.1-1
- Initial rpm release.
