%global debug_package %{nil}

Name:           consul
Version:        1.11.9
Release:        8%{?dist}
Summary:        Consul is a tool for service discovery and configuration.
License:        Mozilla Public License, version 2.0
Group:          System Environment/Daemons
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://github.com/hashicorp/consul/archive/v%{version}.tar.gz

Source0:        %{name}-%{version}.tar.gz
%define sha512  %{name}-%{version}=dc2b16a31e93dc6bef9a97c37f58c09ffdedb00b2209a847e045fa8aebb322c1578dc20ce6b29c47f9da5983c78d30458c2e258822ec2061945a6d3cbfd4fd28
Source1:        %{name}.service

BuildRequires:  systemd-devel
BuildRequires:  go
BuildRequires:  ca-certificates

Requires:       systemd

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

%pre
if ! getent group %{name} >/dev/null; then
    groupadd %{name}
fi
if ! getent passwd %{name} >/dev/null; then
    useradd -c "Consul Agent" -d %{_sharedstatedir}/%{name} -g %{name} -s /bin/false %{name}
fi
exit 0

%post
/sbin/ldconfig
%systemd_post %{name}.service
if [ $1 -ge 1 ]; then
  chown -PR %{name}:%{name} %{_sharedstatedir}/%{name}
fi

%postun
if [ $1 -eq 0 ]; then
  # this is delete operation
  if getent passwd %{name} >/dev/null; then
    userdel %{name}
  fi
  if getent group %{name} >/dev/null; then
    groupdel %{name}
  fi
fi
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
%dir %{_sharedstatedir}/%{name}
%dir %{_sysconfdir}/%{name}.d

%changelog
* Thu Jun 20 2024 Mukul Sikka <msikka@vmware.com> 1.11.9-8
- Bump version as a part of go upgrade
* Thu Apr 18 2024 Mukul Sikka <msikka@vmware.com> 1.11.9-7
- Bump version as a part of go upgrade
* Tue Nov 21 2023 Piyush Gupta <gpiyush@vmware.com> 1.11.9-6
- Bump up version to compile with new go
* Wed Oct 11 2023 Piyush Gupta <gpiyush@vmware.com> 1.11.9-5
- Bump up version to compile with new go
* Fri Aug 18 2023 Piyush Gupta <gpiyush@vmware.com> 1.11.9-4
- Bump up version to compile with new go
* Tue Jun 20 2023 Piyush Gupta <gpiyush@vmware.com> 1.11.9-3
- Bump up version to compile with new go
* Wed May 03 2023 Piyush Gupta <gpiyush@vmware.com> 1.11.9-2
- Bump up version to compile with new go
* Thu Apr 06 2023 Harinadh D <hdommaraju@vmware.com> 1.11.9-1
- Version upgrade
- Fix CVE-CVE-2021-41803, CVE-2022-29153
* Thu Mar 16 2023 Piyush Gupta <gpiyush@vmware.com> 1.9.16-9
- Bump up version to compile with new go
* Tue Dec 20 2022 Piyush Gupta <gpiyush@vmware.com> 1.9.16-8
- Bump up version to compile with new go
* Sun Nov 13 2022 Piyush Gupta <gpiyush@vmware.com> 1.9.16-7
- Bump up version to compile with new go
* Wed Oct 26 2022 Piyush Gupta <gpiyush@vmware.com> 1.9.16-6
- Bump up version to compile with new go
* Thu Sep 15 2022 Piyush Gupta <gpiyush@vmware.com> 1.9.16-5
- Bump up version to compile with new go
* Fri Aug 19 2022 Piyush Gupta <gpiyush@vmware.com> 1.9.16-4
- Bump up version to compile with new go
* Tue Jul 12 2022 Piyush Gupta <gpiyush@vmware.com> 1.9.16-3
- Bump up version to compile with new go
* Mon Apr 11 2022 Piyush Gupta <gpiyush@vmware.com> 1.9.16-2
- Bump up version to compile with new go.
* Tue Apr 05 2022 Shreenidhi Shedi <sshedi@vmware.com> 1.9.16-1
- Upgradeto v1.9.16 & fix spec issues
* Thu Mar 17 2022 Nitesh Kumar <kunitesh@vmware.com> 1.9.15-1
- Version upgrade 1.9.15 to fix CVE-2022-24687
* Tue Feb 22 2022 Piyush Gupta <gpiyush@vmware.com> 1.9.11-3
- Bump up version to compile with new go
* Mon Jan 24 2022 Piyush Gupta <gpiyush@vmware.com> 1.9.11-2
- Bump up version to compile with new go
* Tue Dec 21 2021 Nitesh Kumar <kunitesh@vmware.com> 1.9.11-1
- Version upgrade 1.9.11 to fix CVE-2021-41805
* Wed Oct 20 2021 Piyush Gupta <gpiyush@vmware.com> 1.9.8-4
- Bump up version to compile with new go
* Thu Sep 23 2021 Piyush Gupta <gpiyush@vmware.com> 1.9.8-3
- Bump up version to compile with new go
* Tue Sep 21 2021 Piyush Gupta <gpiyush@vmware.com> 1.9.8-2
- Fix for CVE-2021-37219, CVE-2021-3121, CVE-2021-38698.
* Tue Aug 03 2021 Nitesh Kumar <kunitesh@vmware.com> 1.9.8-1
- Version upgrade to 1.9.8, fixes CVE-2021-32574
* Fri Jun 11 2021 Piyush Gupta <gpiyush@vmware.com> 1.9.5-2
- Bump up version to compile with new go
* Wed Apr 28 2021 Piyush Gupta <gpiyush@vmware.com> 1.9.5-1
- Upgrade to 1.9.5
* Thu Mar 25 2021 Piyush Gupta<gpiyush@vmware.com> 1.9.1-4
- Bump up version to compile with new go
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
