%global security_hardening nopie
%define debug_package %{nil}
%define __os_install_post %{nil}

Summary:        EdgeX Foundry Go Services
Name:           edgex
Version:        2.2.0
Release:        13%{?dist}
License:        Apache-2.0
URL:            https://github.com/edgexfoundry/edgex-go
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://github.com/edgexfoundry/edgex-go/archive/refs/tags/%{name}-%{version}.tar.gz
%define sha512 %{name}=446f34753fe095049095f3525d77b0b1b1cc3b04f22c9955c6a5262908526547e84ba48581dc3ca67c47a65d029291a204c9ca88cc791a136245915e5623fece

Source1: %{name}-template.service

BuildRequires: go
BuildRequires: make
BuildRequires: systemd-devel
BuildRequires: zeromq-devel

Requires: systemd
Requires: zeromq
Requires: redis

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
%autosetup -p1 -c -T -a 0 -n src/github.com/edgexfoundry
mv %{_builddir}/src/github.com/edgexfoundry/%{name}-go-%{version} %{_builddir}/src/github.com/edgexfoundry/%{name}-go

%build
cd %{_builddir}/src/github.com/edgexfoundry/%{name}-go

go mod tidy
export GO111MODULE=auto

# Disable consul [Registry] section for all services
find cmd -name configuration.toml | xargs sed -i "/^\[Registry\]/,+3 s/^/#/"

%make_build build

%install
# edgex-go
cd %{_builddir}/src/github.com/edgexfoundry/%{name}-go

install -d -m755 %{buildroot}%{_bindir}
install -d -m755 %{buildroot}%{_datadir}/%{name}
install -d -m755 %{buildroot}%{_var}/log/%{name}
install -d -m755 %{buildroot}%{_unitdir}

# install binary
for srv in core-command core-data core-metadata \
           security-proxy-setup security-secretstore-setup \
           support-notifications support-scheduler \
           sys-mgmt-agent; do

  install -p -m755 cmd/${srv}/${srv} %{buildroot}%{_bindir}/%{name}-${srv}

  install -d -m755 %{buildroot}%{_datadir}/%{name}/${srv}/res

  install -p -m644 cmd/${srv}/res/configuration.toml \
      %{buildroot}%{_datadir}/%{name}/${srv}/res/configuration.toml

  sed "s/SERVICE_NAME/${srv}/" %{SOURCE1} > %{buildroot}%{_unitdir}/%{name}-${srv}.service
done

install -p -m755 cmd/security-file-token-provider/security-file-token-provider \
        %{buildroot}%{_bindir}/%{name}-security-file-token-provider

sed "s/SERVICE_NAME/security-file-token-provider/" %{SOURCE1} > \
        %{buildroot}%{_unitdir}/%{name}-security-file-token-provider.service

install -p -m755 cmd/sys-mgmt-executor/sys-mgmt-executor \
        %{buildroot}%{_bindir}/%{name}-sys-mgmt-executor

sed "s/SERVICE_NAME/sys-mgmt-executor/" %{SOURCE1} > \
        %{buildroot}%{_unitdir}/%{name}-sys-mgmt-executor.service

# core data does not stop on SIGINT, so use SIGKILL instead.
# It allows `systemctl stop edgex-core-data` to work properly.
sed -i "s/SIGINT/SIGKILL/" %{buildroot}%{_unitdir}/%{name}-core-data.service

%files
%defattr(-,root,root)
%{_bindir}/*
%{_datadir}/*
%{_libdir}/*
%{_var}/log/*

%changelog
* Tue Nov 21 2023 Piyush Gupta <gpiyush@vmware.com> 2.2.0-13
- Bump up version to compile with new go
* Wed Oct 11 2023 Piyush Gupta <gpiyush@vmware.com> 2.2.0-12
- Bump up version to compile with new go
* Fri Aug 18 2023 Piyush Gupta <gpiyush@vmware.com> 2.2.0-11
- Bump up version to compile with new go
* Thu Jul 13 2023 Nitesh Kumar <kunitesh@vmware.com> 2.2.0-10
- Bump up version to consume redis v7.0.12
* Tue Jun 20 2023 Piyush Gupta <gpiyush@vmware.com> 2.2.0-9
- Bump up version to compile with new go
* Wed May 03 2023 Piyush Gupta <gpiyush@vmware.com> 2.2.0-8
- Bump up version to compile with new go
* Thu Mar 16 2023 Piyush Gupta <gpiyush@vmware.com> 2.2.0-7
- Bump up version to compile with new go
* Tue Dec 20 2022 Piyush Gupta <gpiyush@vmware.com> 2.2.0-6
- Bump up version to compile with new go
* Sun Nov 13 2022 Piyush Gupta <gpiyush@vmware.com> 2.2.0-5
- Bump up version to compile with new go
* Wed Oct 26 2022 Piyush Gupta <gpiyush@vmware.com> 2.2.0-4
- Bump up version to compile with new go
* Thu Sep 15 2022 Piyush Gupta <gpiyush@vmware.com> 2.2.0-3
- Bump up version to compile with new go
* Fri Aug 19 2022 Piyush Gupta <gpiyush@vmware.com> 2.2.0-2
- Bump up version to compile with new go
* Mon Jul 25 2022 Shreenidhi Shedi <sshedi@vmware.com> 2.2.0-1
- Upgrade to v2.2.0
- security-secrets-setup security-secretstore-read
  have been removed from upstream
* Tue Jul 12 2022 Piyush Gupta <gpiyush@vmware.com> 1.2.1-15
- Bump up version to compile with new go
* Sat May 07 2022 Piyush Gupta <gpiyush@vmware.com> 1.2.1-14
- Bump up version to compile with new go
* Tue Feb 22 2022 Piyush Gupta <gpiyush@vmware.com> 1.2.1-13
- Bump up version to compile with new go
* Mon Jan 24 2022 Piyush Gupta <gpiyush@vmware.com> 1.2.1-12
- Bump up version to compile with new go
* Thu Oct 28 2021 Piyush Gupta <gpiyush@vmware.com> 1.2.1-11
- Bump up version to compile with new go
* Tue Oct 26 2021 Nitesh Kumar <kunitesh@vmware.com> 1.2.1-10
- Bump up to consume redis v6.0.16.
* Tue Oct 05 2021 Piyush Gupta <gpiyush@vmware.com> 1.2.1-9
- Bump up version to compile with new go
* Wed Aug 18 2021 Shreyas B<shreyasb@vmware.com> 1.2.1-8
- Bump up to consume redis v6.0.15
* Mon Jun 21 2021 Shreyas B<shreyasb@vmware.com> 1.2.1-7
- Bump up version to consume redis v6.0.14
* Fri Jun 11 2021 Piyush Gupta <gpiyush@vmware.com> 1.2.1-6
- Bump up version to compile with new go
* Tue May 25 2021 Shreyas B<shreyasb@vmware.com> 1.2.1-5
- Bump up version to consume redis v6.0.13
* Thu Mar 25 2021 Piyush Gupta<gpiyush@vmware.com> 1.2.1-4
- Bump up version to compile with new go
* Fri Feb 05 2021 Harinadh D <hdommaraju@vmware.com> 1.2.1-3
- Bump up version to compile with new go
* Fri Jan 15 2021 Piyush Gupta<gpiyush@vmware.com> 1.2.1-2
- Bump up version to compile with new go
* Mon Jun 22 2020 Gerrit Photon <photon-checkins@vmware.com> 1.2.1-1
- Automatic Version Bump
* Mon Feb 04 2019 Alexey Makhalov <amakhalov@vmware.com> 0.7.1-2
- Remove consul dependency.
- Use SIGKILL for core-data to terminate the service.
* Wed Jan 16 2019 Alexey Makhalov <amakhalov@vmware.com> 0.7.1-1
- Version update. Use redis db.
* Wed Dec 05 2018 Alexey Makhalov <amakhalov@vmware.com> 0.6.0-2
- Remove 'Requires: mongodb'. But edgex still depends on mongo.
* Fri Jul 06 2018 Alexey Makhalov <amakhalov@vmware.com> 0.6.0-1
- Initial version
