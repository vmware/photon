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
%define sha256 %{name}_%{version}_linux_amd64.zip=b7561158d2074c3c68ff62ae6fc1eafe8db250894043382fb31f0c78150c513a
Source1:	consul-template.service
Requires:	shadow
Requires: consul >= 0.6.4
BuildRequires: unzip

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
