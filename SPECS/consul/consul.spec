Name:           consul
Version:        1.8.4
Release:        1%{?dist}
Summary:        Consul is a tool for service discovery and configuration.
License:        Mozilla Public License, version 2.0
Group:          System Environment/Daemons
Vendor:         VMware, Inc.
Distribution:   Photon
URL:		    https://github.com/hashicorp/consul/archive/v%{version}.tar.gz

Source0:	    %{name}-%{version}.tar.gz
%define sha1 %{name}-%{version}.tar.gz=ce9c49752146d78275e18d91f8c0cf74424208f8
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
%setup -q

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
*  Mon Sep 21 2020 Gerrit Photon <photon-checkins@vmware.com> 1.8.4-1
-  Automatic Version Bump
*  Wed Aug 12 2020 Gerrit Photon <photon-checkins@vmware.com> 1.8.3-1
-  Automatic Version Bump
*  Thu Jul 09 2020 Shreenidhi Shedi <sshedi@vmware.com> 1.8.0-1
-  Upgrade to version 1.8.0
*  Tue Mar 10 2020 Shreenidhi Shedi <sshedi@vmware.com> 1.7.1-1
-  Version upgrade to 1.7.1; fixes CVE-2020-7219 & CVE-2020-7955
*  Tue Oct 22 2019 Ashwin H <ashwinh@vmware.com> 1.2.3-4
-  Bump up version to compile with go 1.13.3
*  Fri Aug 30 2019 Ashwin H <ashwinh@vmware.com> 1.2.3-3
-  Bump up version to compile with new go
*  Mon Jun 03 2019 Siju Maliakkal <smaliakkal@vmware.com> 1.2.3-2
-  Applied patch for CVE-2018-19653
*  Mon Oct 22 2018 Ajay Kaher <akaher@vmware.com> 1.2.3-1
-  Upgraded to version 1.2.3
*  Mon Jul 09 2018 Alexey Makhalov <amakhalov@vmware.com> 1.1.0-2
-  Modify command line parameters in .service file.
*  Thu Jun 28 2018 Ankit Jain <ankitja@vmware.com> 1.1.0-1
-  Initial build. First version
