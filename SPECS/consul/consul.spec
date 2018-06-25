Summary:        Consul-1.1.0
Name:           consul
Version:        1.1.0
Release:        1%{?dist}
License:        Mozilla Public License, version 2.0
URL:            https://www.consul.io/
Group:          System Environment/Daemons
Vendor:         VMware, Inc.
Distribution:   Photon
Source0: https://releases.hashicorp.com/%{name}/%{version}/%{name}_%{version}_linux_amd64.zip
%define sha1 %{name}_%{version}_linux_amd64.zip=92241656f310f924ad20c0a7c93a3f2b9ec59b8a
Source1:        consul.service
BuildRequires:  unzip
BuildRequires:  systemd
Requires:       systemd

%description
Consul is a tool for service discovery and configuration. Consul is distributed, highly available, and extremely scalable.

Consul provides several key features:
 - Service Discovery - Consul makes it simple for services to register themselves and to discover other services via a DNS or HTTP interface. External services such as SaaS providers can be registered as well.
 - Health Checking - Health Checking enables Consul to quickly alert operators about any issues in a cluster. The integration with service discovery prevents routing traffic to unhealthy hosts and enables service level circuit breakers.
 - Key/Value Storage - A flexible key/value store enables storing dynamic configuration, feature flagging, coordination, leader election and more. The simple HTTP API makes it easy to use anywhere.
 - Multi-Datacenter - Consul is built to be datacenter aware, and can support any number of regions without complex configuration.


%prep -p exit
%setup -qcn %{name}-%{version}

%build
export LANG=en_US.UTF-8
export LC_ALL=en_US.UTF-8

%install
install -vdm755 %{buildroot}%{_bindir}
install -vdm755 %{buildroot}%{_sysconfdir}/%{name}.d
install -vdm755 %{buildroot}/usr/lib/systemd/system

chown -R root:root %{buildroot}%{_bindir}

mv %{_builddir}/%{name}-%{version}/%{name} %{buildroot}%{_bindir}/

cp %{SOURCE1} %{buildroot}/usr/lib/systemd/system

chmod +x %{buildroot}/usr/lib/systemd/system/%{name}.service

install -vdm755 %{buildroot}/var/lib/consul

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
*       Mon Jun 25 2018 Ankit Jain <ankitja@vmware.com> 1.1.0-1
-       Updated the package with latest version
*       Sat Nov 12 2016 Ivan Porto Carrero <icarrero@vmware.com> 0.7.1-1
-       Defaults to dev mode
-       Fix user and group creation
*       Sun Jul 24 2016 Ivan Porto Carrero <icarrero@vmware.com> 0.6.4-1
-       Initial build.  First version
