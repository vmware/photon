Summary:	Vault secrets management
Name:		vault
Version:	0.6.0
Release:	1%{?dist}
License:	Mozilla Public License, version 2.0
URL:		https://www.vaultproject.io/
Group:		System Environment/Security
Vendor:		VMware, Inc.
Distribution:	Photon
Source0: https://releases.hashicorp.com/%{name}/%{version}/%{name}_%{version}_linux_amd64.zip
%define sha1 vault=ec1115ba639870a63460884a59b44c77b0c71221
Source1:	vault.service
Source2:        vault.hcl
Requires:	shadow
Requires:       consul >= 0.6.4
BuildRequires:  unzip

%description
Vault secures, stores, and tightly controls access to tokens, passwords, certificates, API keys, and other secrets in modern computing. Vault handles leasing, key revocation, key rolling, and auditing. Vault presents a unified API to access multiple backends: HSMs, AWS IAM, SQL databases, raw key/value, and more.

%prep -p exit
%setup -qcn %{name}-%{version}

%build

%install
install -vdm755 %{buildroot}%{_bindir}
install -vdm755 %{buildroot}/usr/lib/systemd/system
install -vdm755 %{buildroot}/%{_sysconfdir}/vault.d

chown -R root:root %{buildroot}%{_bindir}

mv %{_builddir}/%{name}-%{version}/%{name} %{buildroot}%{_bindir}/

cp %{SOURCE1} %{buildroot}/usr/lib/systemd/system
cp %{SOURCE2} %{buildroot}%{_sysconfdir}/vault.d/
install -vdm755 %{buildroot}/var/lib/vault

%post	-p /sbin/ldconfig
setcap cap_ipc_lock=+ep /usr/bin/%{name}
%systemd_post vault.service

%postun	-p /sbin/ldconfig
%systemd_postun_with_restart vault.service

%preun
%systemd_preun vault.service

%clean
rm -rf %{buildroot}/*

%files
%{_bindir}/%{name}
%{_sysconfdir}/%{name}.d/vault.hcl
/usr/lib/systemd/system/%{name}.service
%dir %{_sysconfdir}/%{name}.d
%dir /var/lib/%{name}

%changelog
*	Sun Jul 24 2016 Ivan Porto Carrero <icarrero@vmware.com> 0.6.0-1
-	Initial build.	First version
