%define gopath_comp_cns github.com/vmware/cloud-network-setup

%global debug_package %{nil}

Summary:        Configures network interfaces in cloud enviroment
Name:           cloud-network-setup
Version:        0.2.2
Release:        14%{?dist}
Group:          Networking
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://github.com/vmware/%{name}/archive/refs/tags/v%{version}.tar.gz

Source0:        https://github.com/vmware/%{name}/archive/refs/tags/%{name}-%{version}.tar.gz
Source1:        %{name}.sysusers

Source2: license.txt
%include %{SOURCE2}

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

%prep
# Using autosetup is not feasible
%setup -q -c -n %{name}-%{version}

mkdir -p "$(dirname src/%{gopath_comp_cns})"
mv %{name}-%{version} src/%{gopath_comp_cns}

%build
export GO111MODULE=auto
export GOPATH="${PWD}"
export GOFLAGS=-mod=vendor
pushd src/%{gopath_comp_cns}
go build -o bin/cloud-network ./cmd/cloud-network
go build -o bin/cnctl ./cmd/cnctl
popd

%install
pushd src/%{gopath_comp_cns}
install -m 755 -d %{buildroot}%{_bindir}
install -m 755 -d %{buildroot}%{_sysconfdir}/cloud-network
install -m 755 -d %{buildroot}%{_unitdir}

install -pm 755 -t %{buildroot}%{_bindir} bin/cloud-network
install -pm 755 -t %{buildroot}%{_bindir} bin/cnctl

install -pm 755 -t %{buildroot}%{_sysconfdir}/cloud-network distribution/cloud-network.toml
install -pm 755 -t %{buildroot}%{_unitdir}/ distribution/cloud-network.service
install -p -D -m 0644 %{SOURCE1} %{buildroot}%{_sysusersdir}/%{name}.conf
popd

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
%{_sysusersdir}/%{name}.conf
%{_unitdir}/cloud-network.service

%changelog
* Thu May 08 2025 Mukul Sikka <mukul.sikka@broadcom.com> 0.2.2-14
- Renaming sysusers to conf to fix auto user creation
* Thu Dec 12 2024 HarinadhD <harinadh.dommaraju@broadcom.com> 0.2.2-13
- Release bump for SRP compliance
* Thu Sep 19 2024 Mukul Sikka <mukul.sikka@broadcom.com> 0.2.2-12
- Bump version as a part of go upgrade
* Fri Aug 23 2024 Bo Gan <bo.gan@broadcom.com> 0.2.2-11
- Simplify build scripts
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
