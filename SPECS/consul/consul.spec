Summary:        Consul is a tool for service discovery and configuration.
Name:           consul
Version:        1.2.3
Release:        1%{?dist}
License:        Mozilla Public License, version 2.0
Group:          System Environment/Daemons
Vendor:         VMware, Inc.
Distribution:   Photon
URL:		https://github.com/hashicorp/consul/archive/v%{version}.tar.gz
Source0:	%{name}-%{version}.tar.gz
%define sha1 %{name}-%{version}.tar.gz=c507e1c0b31fa02dd5ba3f8a3a981e6f7b0c464d
Source1:        %{name}.service
BuildRequires:  unzip
BuildRequires:  systemd
BuildRequires:  go
Requires:       systemd

%description
Consul is a tool for service discovery and configuration. Consul is distributed, highly available, and extremely scalable.

Consul provides several key features:
 - Service Discovery - Consul makes it simple for services to register themselves and to discover other services via a DNS or HTTP interface. External services such as SaaS providers can be registered as well.
 - Health Checking - Health Checking enables Consul to quickly alert operators about any issues in a cluster. The integration with service discovery prevents routing traffic to unhealthy hosts and enables service level circuit breakers.
 - Key/Value Storage - A flexible key/value store enables storing dynamic configuration, feature flagging, coordination, leader election and more. The simple HTTP API makes it easy to use anywhere.
 - Multi-Datacenter - Consul is built to be datacenter aware, and can support any number of regions without complex configuration.

%global debug_package %{nil}

%prep
%setup -q

%build
export LANG=en_US.UTF-8
export LC_ALL=en_US.UTF-8
export PKG=github.com/hashicorp/%{name}
export GOPATH=/usr/share/gocode
export GOROOT=/usr/lib/golang
export GOHOSTOS=linux
export CGO_ENABLED=0
export GOOS=linux
export VERSION=%{version}
mkdir -p ${GOPATH}/src/${PKG}
cp -r * ${GOPATH}/src/${PKG}/.
pushd ${GOPATH}/src/${PKG}
mkdir -p %{name}_bin
CGO_ENABLED=0 GOOS=linux go build -v -o %{name}_bin/%{name} -ldflags "-X main.VERSION=%{version} -s -w" *.go

%install
export PKG=github.com/hashicorp/%{name}
pushd ${GOPATH}/src/${PKG}
install -vdm 755 %{buildroot}%{_bindir}
install ${GOPATH}/src/${PKG}/%{name}_bin/%{name} %{buildroot}%{_bindir}
install -vdm 755 %{buildroot}%{_sysconfdir}/%{name}.d
install -vdm 755 %{buildroot}/usr/lib/systemd/system

chown -R root:root %{buildroot}%{_bindir}

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
*  Mon Oct 22 2018 Ajay Kaher <akaher@vmware.com> 1.2.3-1
-  Upgraded to version 1.2.3
*  Mon Jul 09 2018 Alexey Makhalov <amakhalov@vmware.com> 1.1.0-2
-  Modify command line parameters in .service file.
*  Thu Jun 28 2018 Ankit Jain <ankitja@vmware.com> 1.1.0-1
-  Initial build.  First version
