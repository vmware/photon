Summary:	Consul Template-0.15.0
Name:		consul-template
Version:	0.15.0
Release:	1%{?dist}
License:	Mozilla Public License, version 2.0
URL:		https://www.consul.io/
Group:		System Environment/Security
Vendor:		VMware, Inc.
Distribution:	Photon
Source0: https://releases.hashicorp.com/%{name}/%{version}/%{name}_%{version}_linux_amd64.zip
%define sha1 consul-template=6cb37c40ea9a3885f12121d74f1b50a814fd0bb1
Source1:	consul-template.service
Requires:	shadow
Requires:       consul >= 0.6.4
BuildRequires:  unzip

%description
Generic template rendering and notifications with Consul

%prep -p exit
%setup -qcn %{name}-%{version}

%build

%install
install -vdm755 %{buildroot}%{_bindir}
install -vdm755 %{buildroot}%{_sysconfdir}/consul-template.d
install -vdm755 %{buildroot}/usr/lib/systemd/system

chown -R root:root %{buildroot}%{_bindir}

mv %{_builddir}/%{name}-%{version}/%{name} %{buildroot}%{_bindir}/

cp %{SOURCE1} %{buildroot}/usr/lib/systemd/system

%check
make -k check |& tee %{_specdir}/%{name}-check-log || %{nocheck}

%post	-p /sbin/ldconfig
%systemd_post %{name}.service

%postun	-p /sbin/ldconfig
%systemd_postun_with_restart %{name}.service

%preun
%systemd_preun %{name}.service

%clean
rm -rf %{buildroot}/*

%files
%{_bindir}/%{name}
%dir %{_sysconfdir}/%{name}.d
/usr/lib/systemd/system/%{name}.service

%changelog
*	Sun Jul 24 2016 Ivan Porto Carrero <icarrero@vmware.com> 0.15.0-1
-	Initial build.	First version
