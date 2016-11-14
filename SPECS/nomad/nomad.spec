Summary:	Nomad Scheduler 0.4.0
Name:		nomad
Version:	0.4.0
Release:	1%{?dist}
License:	Mozilla Public License, version 2.0
URL:		https://www.nomadproject.io/
Group:		System Environment/Security
Vendor:		VMware, Inc.
Distribution:	Photon
Source0: https://releases.hashicorp.com/%{name}/%{version}/%{name}_%{version}_linux_amd64.zip
%define sha1 nomad=62685976dc86b3d2c89b529ade8e4d83be4d80fa
Source1:	%{name}.service
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

cp %{SOURCE1} %{buildroot}/usr/lib/systemd/system
install -vdm755 %{buildroot}/var/lib/%{name}

%post	-p /sbin/ldconfig
%systemd_post %{name}.service

%postun	-p /sbin/ldconfig
%systemd_postun_with_restart %{name}.service

%preun
%systemd_preun %{name}.service

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,%{name},%{name})
%{_bindir}/%{name}
/usr/lib/systemd/system/%{name}.service
%dir /var/lib/%{name}
%dir %{_sysconfdir}/%{name}

%changelog
*	Sun Jul 24 2016 Ivan Porto Carrero <icarrero@vmware.com> 0.4.0-1
-	Initial build.	First version
