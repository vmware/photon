Summary:	Nomad Scheduler 0.4.1
Name:		nomad
Version:	0.4.1
Release:	1%{?dist}
License:	Mozilla Public License, version 2.0
URL:		https://www.nomadproject.io/
Group:		System Environment/Security
Vendor:		VMware, Inc.
Distribution:	Photon
Source0: https://releases.hashicorp.com/%{name}/%{version}/%{name}_%{version}_linux_amd64.zip
%define sha1 %{name}_%{version}_linux_amd64.zip=33ebb18daf38621e1c5e1d5e98b5eb9dbc3446c9
Source1:	%{name}-client.conf
Source2:	%{name}-client.service
Source3:	%{name}-server.conf
Source4:	%{name}-server.service
Requires:	shadow
BuildRequires:  unzip

%description
Easily deploy applications at any scale. A Distributed, Highly Available, Datacenter-Aware Scheduler

%prep -p exit
%setup -qcn %{name}-%{version}

%build

%install
install -vdm755 %{buildroot}%{_bindir}
install -vdm755 %{buildroot}%{_sysconfdir}/nomad.d
install -vdm755 %{buildroot}/usr/lib/systemd/system

chown -R root:root %{buildroot}%{_bindir}

mv %{_builddir}/%{name}-%{version}/%{name} %{buildroot}%{_bindir}/

cp %{SOURCE2} %{buildroot}/usr/lib/systemd/system
cp %{SOURCE4} %{buildroot}/usr/lib/systemd/system
install -vdm755 %{buildroot}/var/lib/%{name}

%post
%systemd_post %{name}-client.service
%systemd_post %{name}-server.service

%postun
%systemd_postun_with_restart %{name}-client.service
%systemd_postun_with_restart %{name}-server.service

%preun
%systemd_preun %{name}-client.service
%systemd_preun %{name}-server.service

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%{_bindir}/%{name}
/usr/lib/systemd/system/%{name}-client.service
/usr/lib/systemd/system/%{name}-server.service
%dir /var/lib/%{name}
%dir %{_sysconfdir}/%{name}

%changelog
*	Sat Nov 12 2016 Ivan Porto Carrero <icarrero@vmware.com> 0.4.1-1
-	Defaults to dev mode
*	Sun Jul 24 2016 Ivan Porto Carrero <icarrero@vmware.com> 0.4.0-1
-	Initial build.	First version
