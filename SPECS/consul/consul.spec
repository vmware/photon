Summary:	Consul-0.6.4
Name:		consul
Version:	0.6.4
Release:	1%{?dist}
License:	Mozilla Public License, version 2.0
URL:		https://www.consul.io/
Group:		System Environment/Security
Vendor:		VMware, Inc.
Distribution:	Photon
Source0: https://releases.hashicorp.com/%{name}/%{version}/%{name}_%{version}_linux_amd64.zip
%define sha1 consul=85de555de27cae126f0f89e762f6136e1c7104b6
Source1:	consul.service
Requires:	shadow
BuildRequires:  unzip

%description
Service discovery and configuration made easy. Distributed, highly available, and datacenter-aware.

%prep -p exit
%setup -qcn %{name}-%{version}

%build

%install
install -vdm755 %{buildroot}%{_bindir}
install -vdm755 %{buildroot}%{_sysconfdir}/%{name}.d
install -vdm755 %{buildroot}/usr/lib/systemd/system

chown -R root:root %{buildroot}%{_bindir}

mv %{_builddir}/%{name}-%{version}/%{name} %{buildroot}%{_bindir}/

cp %{SOURCE1} %{buildroot}/usr/lib/systemd/system
install -vdm755 %{buildroot}/var/lib/consul

%check
make -k check |& tee %{_specdir}/%{name}-check-log || %{nocheck}

%post	-p /sbin/ldconfig
if [ $1 -eq 1 ]; then
  # this is initial installation
  if ! getent group %{name} >/dev/null; then
      groupadd -g 850 %{name}
  fi
  if ! getent passwd %{name} >/dev/null; then
      useradd -c "Consul Agent" -d /var/lib/%{name} -g %{name} \
          -s /bin/false -u 850 %{name}
  fi
fi
%systemd_post consul.service

%postun	-p /sbin/ldconfig
if [ $1 -eq 0 ]; then
  # this is delete operation
  if getent passwd %{name} >/dev/null; then
      userdel %{name}
  fi
  if getent group %{name} >/dev/null; then
      groupdel %{name}
  fi
fi
%systemd_postun_with_restart consul.service

%preun
%systemd_preun consul.service

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,consul,consul)
%{_bindir}/%{name}
/usr/lib/systemd/system/%{name}.service
%dir /var/lib/%{name}
%dir %{_sysconfdir}/%{name}.d

%changelog
*	Sun Jul 24 2016 Ivan Porto Carrero <icarrero@vmware.com> 0.6.4-1
-	Initial build.	First version
