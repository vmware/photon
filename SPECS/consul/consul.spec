Name:           consul
Version:        1.9.15
Release:        9%{?dist}
Summary:        Consul is a tool for service discovery and configuration.
License:        Mozilla Public License, version 2.0
Group:          System Environment/Daemons
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://github.com/hashicorp/consul/archive/v%{version}.tar.gz
Source0:        %{name}-%{version}.tar.gz
%define sha512  %{name}-%{version}.tar.gz=e8050bbc9d819ef26952a66adfd78efad2db4e1776bf02db041481cd74365d180da4ab07d63f4465ea7bf6dfcc5ea25770f2d12f68c010f810b7c2f1ae408c6b
Source1:        %{name}.service
BuildRequires:  unzip
BuildRequires:  systemd
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

%global debug_package %{nil}

%prep
%autosetup -p1

%build
go build -v -o %{name}

%install
install -vdm 755 %{buildroot}%{_bindir}
install %{name} %{buildroot}%{_bindir}
chown -R root:root %{buildroot}%{_bindir}
install -vdm 755 %{buildroot}%{_sysconfdir}/%{name}.d
install -vdm 755 %{buildroot}/usr/lib/systemd/system
install -vdm 755 %{buildroot}/usr/lib/systemd/system
install -p -m 0644 %{SOURCE1} %{buildroot}/usr/lib/systemd/system/
install -vdm 755 %{buildroot}/var/lib/%{name}

%pre
if ! getent group %{name} >/dev/null; then
    groupadd %{name}
fi
if ! getent passwd %{name} >/dev/null; then
    useradd -c "Consul Agent" -d /var/lib/%{name} -g %{name} -s /bin/false %{name}
fi
exit 0

%post
/sbin/ldconfig
%systemd_post %{name}.service

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
%defattr(-,%{name},%{name})
%{_bindir}/%{name}
/usr/lib/systemd/system/%{name}.service
%dir /var/lib/%{name}
%dir %{_sysconfdir}/%{name}.d

%changelog
* Tue Apr 04 2023 Piyush Gupta <gpiyush@vmware.com> 1.9.15-9
- Bump up version to compile with new go
* Tue Dec 20 2022 Piyush Gupta <gpiyush@vmware.com> 1.9.15-8
- Bump up version to compile with new go
* Sun Nov 13 2022 Piyush Gupta <gpiyush@vmware.com> 1.9.15-7
- Bump up version to compile with new go
* Wed Oct 26 2022 Piyush Gupta <gpiyush@vmware.com> 1.9.15-6
- Bump up version to compile with new go
* Thu Sep 15 2022 Piyush Gupta <gpiyush@vmware.com> 1.9.15-5
- Bump up version to compile with new go
* Thu Aug 18 2022 Piyush Gupta <gpiyush@vmware.com> 1.9.15-4
- Bump up version to compile with new go
* Mon May 09 2022 Piyush Gupta <gpiyush@vmware.com> 1.9.15-3
- Bump up version to compile with new go
* Fri Mar 18 2022 Piyush Gupta <gpiyush@vmware.com> 1.9.15-2
- Bump up version to compile with new go.
* Thu Mar 17 2022 Nitesh Kumar <kunitesh@vmware.com> 1.9.15-1
- Version upgrade 1.9.15 to fix CVE-2022-24687
* Tue Feb 22 2022 Piyush Gupta <gpiyush@vmware.com> 1.8.17-3
- Bump up version to compile with new go
* Mon Jan 24 2022 Piyush Gupta <gpiyush@vmware.com> 1.8.17-2
- Bump up version to compile with new go
* Tue Dec 21 2021 Nitesh Kumar <kunitesh@vmware.com> 1.8.17-1
- Version upgrade 1.8.17 to fix CVE-2021-41805
* Tue Nov 16 2021 Piyush Gupta <gpiyush@vmware.com> 1.8.14-5
- Bump up version to compile with new go
* Wed Oct 20 2021 Piyush Gupta <gpiyush@vmware.com> 1.8.14-4
- Bump up version to compile with new go
* Mon Sep 20 2021 Piyush Gupta <gpiyush@vmware.com> 1.8.14-3
- Fix for CVE-2021-37219, CVE-2021-3121, CVE-2021-38698
* Sat Aug 21 2021 Piyush Gupta<gpiyush@vmware.com> 1.8.14-2
- Bump up version to compile with new go
* Tue Aug 03 2021 Nitesh Kumar <kunitesh@vmware.com> 1.8.14-1
- Version upgrade to 1.8.14, fixes CVE-2021-32574
* Tue Jun 29 2021 Piyush Gupta <gpiyush@vmware.com> 1.7.14-3
- Bump up version to compile with new go
* Mon May 03 2021 Piyush Gupta<gpiyush@vmware.com> 1.7.14-2
- Bump up version to compile with new go
* Thu Apr 29 2021 Piyush Gupta <gpiyush@vmware.com> 1.7.14-1
- Upgrade to 1.7.14
* Mon Feb 08 2021 Harinadh D <hdommaraju@vmware.com> 1.7.11-2
- Bump up version to compile with new go
* Wed Dec 16 2020 Shreenidhi Shedi <sshedi@vmware.com> 1.7.11-1
- Bump version to fix CVE-2020-28053
* Fri Nov 27 2020 HarinadhD <hdommaraju@vmware.com> 1.7.9-2
- Bump up version to compile with new go
* Tue Nov 17 2020 Shreenidhi Shedi <sshedi@vmware.com> 1.7.9-1
- Upgrade to v1.7.9, fixes CVE-2020-25201
* Thu Oct 08 2020 Shreenidhi Shedi <sshedi@vmware.com> 1.7.8-1
- Upgrade to v1.7.8, fixes bunch of CVEs
* Tue Aug 18 2020 Ashwin H <ashwinh@vmware.com> 1.7.1-3
- Bump up version to compile with new go
* Fri Apr 10 2020 Harinadh D <hdommaraju@vmware.com> 1.7.1-2
- Bump up version to compile with go 1.13.3-2
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
