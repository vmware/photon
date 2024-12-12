%define network_required 1
%global security_hardening nopie
%define debug_package       %{nil}
%define __os_install_post   %{nil}

Summary:        EdgeX Foundry Go Services
Name:           edgex
Version:        2.2.0
Release:        17%{?dist}
URL:            https://github.com/edgexfoundry/edgex-go
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://github.com/edgexfoundry/edgex-go/archive/refs/tags/%{name}-%{version}.tar.gz
%define sha512 %{name}=446f34753fe095049095f3525d77b0b1b1cc3b04f22c9955c6a5262908526547e84ba48581dc3ca67c47a65d029291a204c9ca88cc791a136245915e5623fece

Source1: %{name}-template.service

Source2: license.txt
%include %{SOURCE2}

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
%autosetup -p1 -c -T -a0 -n src/github.com/edgexfoundry
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
* Thu Dec 12 2024 Guruswamy Basavaiah <guruswamy.basavaiah@broadcom.com> 2.2.0-17
- Release bump for SRP compliance
* Thu Sep 19 2024 Mukul Sikka <mukul.sikka@broadcom.com> 2.2.0-16
- Bump version as a part of go upgrade
* Thu Jun 20 2024 Mukul Sikka <msikka@vmware.com> 2.2.0-15
- Bump version as a part of go upgrade
* Thu Feb 22 2024 Mukul Sikka <msikka@vmware.com> 2.2.0-14
- Bump version as a part of go upgrade
* Thu Jan 18 2024 Nitesh Kumar <nitesh-nk.kumar@broadcom.com> 2.2.0-13
- Version bump up to consume redis v7.2.4
* Tue Nov 21 2023 Piyush Gupta <gpiyush@vmware.com> 2.2.0-12
- Bump up version to compile with new go
* Wed Oct 11 2023 Piyush Gupta <gpiyush@vmware.com> 2.2.0-11
- Bump up version to compile with new go
* Mon Sep 18 2023 Piyush Gupta <gpiyush@vmware.com> 2.2.0-10
- Bump up version to compile with new go
* Mon Sep 11 2023 Nitesh Kumar <kunitesh@vmware.com> 2.2.0-9
- Bump up version to consume redis v7.0.13
* Mon Jul 17 2023 Piyush Gupta <gpiyush@vmware.com> 2.2.0-8
- Bump up version to compile with new go
* Thu Jul 13 2023 Nitesh Kumar <kunitesh@vmware.com> 2.2.0-7
- Bump up version to consume redis v7.0.12
* Thu Jun 22 2023 Piyush Gupta <gpiyush@vmware.com> 2.2.0-6
- Bump up version to compile with new go
* Wed May 03 2023 Piyush Gupta <gpiyush@vmware.com> 2.2.0-5
- Bump up version to compile with new go
* Thu Mar 09 2023 Piyush Gupta <gpiyush@vmware.com> 2.2.0-4
- Bump up version to compile with new go
* Mon Nov 21 2022 Piyush Gupta <gpiyush@vmware.com> 2.2.0-3
- Bump up version to compile with new go
* Wed Oct 26 2022 Piyush Gupta <gpiyush@vmware.com> 2.2.0-2
- Bump up version to compile with new go
* Sun Aug 14 2022 Shreenidhi Shedi <sshedi@vmware.com> 2.2.0-1
- Upgrade to v2.2.0
* Wed Jul 27 2022 Shreenidhi Shedi <sshedi@vmware.com> 1.3.1-3
- Bump version as a part of redis upgrade
* Tue Jul 19 2022 Piyush Gupta <gpiyush@vmware.com> 1.3.1-2
- Bump up version to compile with new go
* Sat Jul 02 2022 Shreenidhi Shedi <sshedi@vmware.com> 1.3.1-1
- Upgrade to v1.3.1
- security-secretstore-read has been removed from upstream
* Tue Oct 26 2021 Nitesh Kumar <kunitesh@vmware.com> 1.2.1-7
- Bump up to consume redis v6.2.6.
* Wed Aug 18 2021 Shreyas B<shreyasb@vmware.com> 1.2.1-6
- Bump up to consume redis v6.2.5
* Fri Jun 11 2021 Piyush Gupta<gpiyush@vmware.com> 1.2.1-5
- Bump up version to compile with new go
* Tue May 25 2021 Shreyas B<shreyasb@vmware.com> 1.2.1-4
- Bump up version to consume redis v6.2.3
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
