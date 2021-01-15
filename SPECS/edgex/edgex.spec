%global security_hardening nopie
%define debug_package %{nil}
%define __os_install_post %{nil}
Summary:        EdgeX Foundry Go Services
Name:           edgex
Version:        1.2.1
Release:        2%{?dist}
License:        Apache-2.0
URL:            https://github.com/edgexfoundry/edgex-go
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:	edgex-%{version}.tar.gz
%define sha1 edgex=7e530e3665a44b284fdd6b90fa409291e26cd451
Source1:	edgex-template.service

BuildRequires:  go
BuildRequires:  make
BuildRequires:  systemd-devel
BuildRequires:  zeromq-devel
Requires:       systemd
Requires:       zeromq
Requires:       redis

%description
EdgeX Foundry Go Services:
- core-command
- core-data
- core-metadata
- export-client
- export-distro
- support-logging
- support-notifications
- support-scheduler
- sys-mgmt-agent

%prep
%setup -c -T -a 0 -n src/github.com/edgexfoundry
mv %{_builddir}/src/github.com/edgexfoundry/edgex-go-%{version} %{_builddir}/src/github.com/edgexfoundry/edgex-go

%build
cd %{_builddir}/src/github.com/edgexfoundry/edgex-go

# Disable consul [Registry] section for all services
find cmd -name configuration.toml | xargs sed -i "/^\[Registry\]/,+3 s/^/#/"

make build %{?_smp_mflags}

%install
# edgex-go
cd %{_builddir}/src/github.com/edgexfoundry/edgex-go

install -d -m755 %{buildroot}%{_bindir}
install -d -m755 %{buildroot}%{_datadir}/%{name}
install -d -m755 %{buildroot}%{_var}/log/%{name}
install -d -m755 %{buildroot}%{_libdir}/systemd/system

# install binary
for srv in core-command core-data core-metadata security-proxy-setup security-secrets-setup security-secretstore-read security-secretstore-setup support-logging support-notifications support-scheduler sys-mgmt-agent ; do
install -p -m755 cmd/${srv}/${srv} %{buildroot}%{_bindir}/edgex-${srv}
install -d -m755 %{buildroot}%{_datadir}/%{name}/${srv}/res
install -p -m644 cmd/${srv}/res/configuration.toml %{buildroot}%{_datadir}/%{name}/${srv}/res/configuration.toml
sed "s/SERVICE_NAME/${srv}/" %{SOURCE1} > %{buildroot}%{_libdir}/systemd/system/edgex-${srv}.service
done
install -p -m755 cmd/security-file-token-provider/security-file-token-provider %{buildroot}%{_bindir}/edgex-security-file-token-provider
sed "s/SERVICE_NAME/security-file-token-provider/" %{SOURCE1} > %{buildroot}%{_libdir}/systemd/system/edgex-security-file-token-provider.service
install -p -m755 cmd/sys-mgmt-executor/sys-mgmt-executor %{buildroot}%{_bindir}/edgex-sys-mgmt-executor
sed "s/SERVICE_NAME/sys-mgmt-executor/" %{SOURCE1} > %{buildroot}%{_libdir}/systemd/system/edgex-sys-mgmt-executor.service

# core data does not stop on SIGINT, so use SIGKILL instead.
# It allows `systemctl stop edgex-core-data` to work properly.
sed -i "s/SIGINT/SIGKILL/" %{buildroot}%{_libdir}/systemd/system/edgex-core-data.service

%files
%defattr(-,root,root)
%{_bindir}/*
%{_datadir}/*
%{_libdir}/*
%{_var}/log/*

%changelog
*   Fri Jan 15 2021 Piyush Gupta<gpiyush@vmware.com> 1.2.1-2
-   Bump up version to compile with new go
*   Mon Jun 22 2020 Gerrit Photon <photon-checkins@vmware.com> 1.2.1-1
-   Automatic Version Bump
*   Mon Feb 04 2019 Alexey Makhalov <amakhalov@vmware.com> 0.7.1-2
-   Remove consul dependency.
-   Use SIGKILL for core-data to terminate the service.
*   Wed Jan 16 2019 Alexey Makhalov <amakhalov@vmware.com> 0.7.1-1
-   Version update. Use redis db.
*   Wed Dec 05 2018 Alexey Makhalov <amakhalov@vmware.com> 0.6.0-2
-   Remove 'Requires: mongodb'. But edgex still depends on mongo.
*   Fri Jul 06 2018 Alexey Makhalov <amakhalov@vmware.com> 0.6.0-1
-   Initial version
