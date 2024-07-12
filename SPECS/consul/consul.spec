%global debug_package %{nil}

Name:           consul
Version:        1.14.8
Release:        9%{?dist}
Summary:        Consul is a tool for service discovery and configuration.
License:        Mozilla Public License, version 2.0
Group:          System Environment/Daemons
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://github.com/hashicorp/consul

Source0: https://github.com/hashicorp/consul/archive/refs/tags/%{name}-%{version}.tar.gz
%define sha512 %{name}-%{version}=d13c7291774a9884d04ace7d731f64c3efe0970fba18debe8fc30792342c267104b0e4a6ddfb1636270213fa7ff8189cdbeb2e4f2655192b341ec281da0dc804
Source1: %{name}.service
Source2: %{name}.sysusers

BuildRequires: systemd-devel
BuildRequires: go
BuildRequires: ca-certificates

Requires(pre): systemd-rpm-macros
Requires:      systemd

%description
Consul is a tool for service discovery and configuration. Consul is distributed, highly available, and extremely scalable.

Consul provides several key features:
 * Service Discovery - Consul makes it simple for services to register themselves and to discover other services via a DNS or HTTP interface.
                     - External services such as SaaS providers can be registered as well.

 * Health Checking - Health Checking enables Consul to quickly alert operators about any issues in a cluster.
                   - The integration with service discovery prevents routing traffic to unhealthy hosts and enables service level circuit breakers.

 * Key/Value Storage - A flexible key/value store enables storing dynamic configuration, feature flagging, coordination, leader election and more.
                     - The simple HTTP API makes it easy to use anywhere.

 * Multi-Datacenter - Consul is built to be datacenter aware, and can support any number of regions without complex configuration.

%prep
%autosetup -p1

%build
go build -v -o %{name}

%install
install -vdm 755 %{buildroot}%{_bindir}
install %{name} %{buildroot}%{_bindir}
install -vdm 755 %{buildroot}%{_sysconfdir}/%{name}.d
install -vdm 755 %{buildroot}%{_unitdir}
install -p -m 0644 %{SOURCE1} %{buildroot}%{_unitdir}
install -vdm 755 %{buildroot}%{_sharedstatedir}/%{name}
install -p -D -m 0644 %{SOURCE2} %{buildroot}%{_sysusersdir}/%{name}.sysusers

%pre
%sysusers_create_compat %{SOURCE2}

%post
/sbin/ldconfig
%systemd_post %{name}.service
if [ $1 -ge 1 ]; then
  chown -PR %{name}:%{name} %{_sharedstatedir}/%{name}
fi

%postun
/sbin/ldconfig
%systemd_postun_with_restart %{name}.service

%preun
/sbin/ldconfig
%systemd_preun %{name}.service

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%{_bindir}/%{name}
%{_unitdir}/%{name}.service
%dir %{_sysconfdir}/%{name}.d
%dir %{_sharedstatedir}/%{name}
%{_sysusersdir}/%{name}.sysusers

%changelog
* Fri Jul 12 2024 Mukul Sikka <mukul.sikka@broadcom.com> 1.14.8-9
- Bump version as a part of go upgrade
* Thu Jun 20 2024 Mukul Sikka <msikka@vmware.com> 1.14.8-8
- Bump version as a part of go upgrade
* Thu Feb 22 2024 Mukul Sikka <msikka@vmware.com> 1.14.8-7
- Bump version as a part of go upgrade
* Tue Nov 21 2023 Piyush Gupta <gpiyush@vmware.com> 1.14.8-6
- Bump up version to compile with new go
* Wed Oct 11 2023 Piyush Gupta <gpiyush@vmware.com> 1.14.8-5
- Bump up version to compile with new go
* Mon Sep 18 2023 Piyush Gupta <gpiyush@vmware.com> 1.14.8-4
- Bump up version to compile with new go
* Tue Aug 08 2023 Mukul Sikka <msikka@vmware.com> 1.14.8-3
- Resolving systemd-rpm-macros for group creation
* Wed Jul 19 2023 Piyush Gupta <gpiyush@vmware.com> 1.14.8-2
- Bump up version to compile with new go
* Mon Jul 17 2023 Nitesh Kumar <kunitesh@vmware.com> 1.14.8-1
- Version upgrade to v1.14.8 to fix following CVE's:
- CVE-2023-1297, CVE-2023-0845
* Thu Jun 22 2023 Piyush Gupta <gpiyush@vmware.com> 1.14.2-5
- Bump up version to compile with new go
* Wed May 03 2023 Piyush Gupta <gpiyush@vmware.com> 1.14.2-4
- Bump up version to compile with new go
* Sun Mar 12 2023 Piyush Gupta <gpiyush@vmware.com> 1.14.2-3
- Bump up version to compile with new go
* Fri Mar 10 2023 Mukul Sikka <msikka@vmware.com> 1.14.2-2
- Use systemd-rpm-macros for user creation
* Tue Dec 13 2022 Gerrit Photon <photon-checkins@vmware.com> 1.14.2-1
- Automatic Version Bump
* Mon Nov 21 2022 Piyush Gupta <gpiyush@vmware.com> 1.11.4-4
- Bump up version to compile with new go
* Wed Oct 26 2022 Piyush Gupta <gpiyush@vmware.com> 1.11.4-3
- Bump up version to compile with new go
* Fri Jun 17 2022 Piyush Gupta <gpiyush@vmware.com> 1.11.4-2
- Bump up version to compile with new go
* Tue Apr 05 2022 Shreenidhi Shedi <sshedi@vmware.com> 1.11.4-1
- Upgradeto v1.11.4 & fix spec issues
* Thu Mar 17 2022 Nitesh Kumar <kunitesh@vmware.com> 1.10.8-1
- Version upgrade to 1.10.8, fixes CVE-2022-24687
* Tue Dec 21 2021 Nitesh Kumar <kunitesh@vmware.com> 1.10.4-1
- Version upgrade to 1.10.4, fixes CVE-2021-41805
* Tue Aug 03 2021 Nitesh Kumar <kunitesh@vmware.com> 1.10.1-1
- Version upgrade to 1.10.1, fixes CVE-2021-32574
* Fri Jun 11 2021 Piyush Gupta <gpiyush@vmware.com> 1.9.5-2
- Bump up version to compile with new go
* Mon Apr 12 2021 Gerrit Photon <photon-checkins@vmware.com> 1.9.5-1
- Automatic Version Bump
* Fri Feb 05 2021 Harinadh D <hdommaraju@vmware.com> 1.9.1-3
- Bump up version to compile with new go
* Fri Jan 15 2021 Piyush Gupta<gpiyush@vmware.com> 1.9.1-2
- Bump up version to compile with new go
* Wed Dec 16 2020 Shreenidhi Shedi <sshedi@vmware.com> 1.9.1-1
- Bump version to fix CVE-2020-28053
* Tue Nov 17 2020 Shreenidhi Shedi <sshedi@vmware.com> 1.8.5-1
- Upgrade to v1.8.5, fixes CVE-2020-25201
* Mon Sep 21 2020 Gerrit Photon <photon-checkins@vmware.com> 1.8.4-1
- Automatic Version Bump
* Wed Aug 12 2020 Gerrit Photon <photon-checkins@vmware.com> 1.8.3-1
- Automatic Version Bump
* Thu Jul 09 2020 Shreenidhi Shedi <sshedi@vmware.com> 1.8.0-1
- Upgrade to version 1.8.0
* Tue Mar 10 2020 Shreenidhi Shedi <sshedi@vmware.com> 1.7.1-1
- Version upgrade to 1.7.1; fixes CVE-2020-7219 & CVE-2020-7955
* Tue Oct 22 2019 Ashwin H <ashwinh@vmware.com> 1.2.3-4
- Bump up version to compile with go 1.13.3
* Fri Aug 30 2019 Ashwin H <ashwinh@vmware.com> 1.2.3-3
- Bump up version to compile with new go
* Mon Jun 03 2019 Siju Maliakkal <smaliakkal@vmware.com> 1.2.3-2
- Applied patch for CVE-2018-19653
* Mon Oct 22 2018 Ajay Kaher <akaher@vmware.com> 1.2.3-1
- Upgraded to version 1.2.3
* Mon Jul 09 2018 Alexey Makhalov <amakhalov@vmware.com> 1.1.0-2
- Modify command line parameters in .service file.
* Thu Jun 28 2018 Ankit Jain <ankitja@vmware.com> 1.1.0-1
- Initial build. First version
