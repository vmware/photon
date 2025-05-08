%define gopath_comp_neb github.com/vmware/network-event-broker

Summary:        Manages network configuration
Name:           network-event-broker
Version:        0.3
Release:        16%{?dist}
URL:            https://github.com/vmware/%{name}
Source0:        https://github.com/vmware/%{name}/archive/refs/tags/%{name}-%{version}.tar.gz
Source1:        %{name}.sysusers

Source2: license.txt
%include %{SOURCE2}
Group:          Networking
Vendor:         VMware, Inc.
Distribution:   Photon

BuildRequires:  go
BuildRequires:  systemd-devel

Requires:         systemd
Requires(pre):    systemd-rpm-macros
Requires(pre):    /usr/sbin/useradd /usr/sbin/groupadd

%global debug_package %{nil}

%description
A daemon that configures the network and executes scripts on network events such as
systemd-networkd's DBus events or dhclient gaining a lease. It also watches
when an address gets added/removed/modified or links get added/removed.

%prep
# Using autosetup is not feasible
%setup -q -c -n %{name}-%{version}

mkdir -p "$(dirname src/%{gopath_comp_neb})"
mv %{name}-%{version} src/%{gopath_comp_neb}

%build
export GO111MODULE=auto
export GOPATH="${PWD}"
export GOFLAGS=-mod=vendor
pushd src/%{gopath_comp_neb}
go build -o bin/network-broker ./cmd/network-broker
popd

%install
pushd src/%{gopath_comp_neb}
install -m 755 -d %{buildroot}%{_bindir}
install -m 755 -d %{buildroot}%{_sysconfdir}/network-broker
install -m 755 -d %{buildroot}%{_unitdir}
install -p -D -m 0644 %{SOURCE1} %{buildroot}%{_sysusersdir}/%{name}.conf
install -pm 755 -t %{buildroot}%{_bindir} bin/network-broker

install -pm 755 -t %{buildroot}%{_sysconfdir}/network-broker distribution/network-broker.toml
install -pm 755 -t %{buildroot}%{_unitdir}/ distribution/network-broker.service
popd

%clean
rm -rf %{buildroot}/*

%pre
%sysusers_create_compat %{SOURCE1}

%post
%systemd_post network-broker.service

%preun
%systemd_preun network-broker.service

%postun
%systemd_postun_with_restart network-broker.service

%files
%defattr(-,root,root)
%{_bindir}/network-broker
%{_sysusersdir}/%{name}.conf
%{_sysconfdir}/network-broker/network-broker.toml
%{_unitdir}/network-broker.service

%changelog
* Thu May 08 2025 Mukul Sikka <mukul.sikka@broadcom.com> 0.3-16
- Renaming sysusers to conf to fix auto user creation
* Thu Dec 12 2024 Ajay Kaher <ajay.kaher@broadcom.com> 0.3-15
- Release bump for SRP compliance
* Thu Sep 19 2024 Mukul Sikka <mukul.sikka@broadcom.com> 0.3-14
- Bump version as a part of go upgrade
* Fri Aug 23 2024 Bo Gan <bo.gan@broadcom.com> 0.3-13
- Simplify build scripts
* Fri Jul 12 2024 Mukul Sikka <mukul.sikka@broadcom.com> 0.3-12
- Bump version as a part of go upgrade
* Thu Jun 20 2024 Mukul Sikka <msikka@vmware.com> 0.3-11
- Bump version as a part of go upgrade
* Thu Feb 22 2024 Mukul Sikka <msikka@vmware.com> 0.3-10
- Bump version as a part of go upgrade
* Tue Nov 21 2023 Piyush Gupta <gpiyush@vmware.com> 0.3-9
- Bump up version to compile with new go
* Wed Oct 11 2023 Piyush Gupta <gpiyush@vmware.com> 0.3-8
- Bump up version to compile with new go
* Mon Sep 18 2023 Piyush Gupta <gpiyush@vmware.com> 0.3-7
- Bump up version to compile with new go
* Mon Jul 17 2023 Piyush Gupta <gpiyush@vmware.com> 0.3-6
- Bump up version to compile with new go
* Thu Jun 22 2023 Piyush Gupta <gpiyush@vmware.com> 0.3-5
- Bump up version to compile with new go
* Wed May 03 2023 Piyush Gupta <gpiyush@vmware.com> 0.3-4
- Bump up version to compile with new go
* Fri Mar 10 2023 Mukul Sikka <msikka@vmware.com> 0.3-3
- Use systemd-rpm-macros for user creation
* Thu Mar 09 2023 Piyush Gupta <gpiyush@vmware.com> 0.3-2
- Bump up version to compile with new go
* Wed Jan 11 2023 Nitesh Kumar <kunitesh@vmware.com> 0.3-1
- Version upgrade to v0.3
* Mon Nov 21 2022 Piyush Gupta <gpiyush@vmware.com> 0.2.1-4
- Bump up version to compile with new go
* Wed Oct 26 2022 Piyush Gupta <gpiyush@vmware.com> 0.2.1-3
- Bump up version to compile with new go
* Fri Jun 17 2022 Piyush Gupta <gpiyush@vmware.com> 0.2.1-2
- Bump up version to compile with new go
* Wed Dec 22 2021 Susant Sahani <ssahani@vmware.com> 0.2.1-1
- Version bump and add groupadd and useradd to requires.
* Tue Dec 14 2021 Susant Sahani <ssahani@vmware.com> 0.2-1
- Version bump.
* Wed Jun 30 2021 Susant Sahani <ssahani@vmware.com> 0.1-1
- Initial rpm release.
