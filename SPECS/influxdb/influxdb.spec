%define network_required 1
%define gopath_comp_influxdb github.com/influxdata/influxdb

Name:           influxdb
Version:        1.8.10
Release:        11%{?dist}
Summary:        InfluxDB is an open source time series database
License:        MIT
URL:            https://influxdata.com
Source0:        https://github.com/influxdata/influxdb/archive/%{name}-%{version}.tar.gz
%define sha512  %{name}=4f5d20c190288d6397f0e87abd9b9136340b17f091c361cbc111ba661a3e63626edf5c74ddeeda164d82102dd06026e0037f50da546cda25e6c8647f4c739fae

Source2:        %{name}.sysusers
Vendor:         VMware, Inc.
Distribution:   Photon
Group:          Applications/Database
BuildRequires:  go >= 1.13
BuildRequires:  git
BuildRequires:  systemd
BuildRequires:  systemd-devel
Requires:       systemd-rpm-macros
Requires:       systemd
Requires:       shadow

%description
InfluxDB is an open source time series database with no external dependencies.
It's useful for recording metrics, events, and performing analytics.

%prep
# Using autosetup is not feasible
%setup -q -c -n %{name}-%{version}

mkdir -p "$(dirname src/%{gopath_comp_influxdb})"
mv %{name}-%{version} src/%{gopath_comp_influxdb}

%build
export GO111MODULE=auto
export GOPATH="${PWD}"
pushd src/%{gopath_comp_influxdb}
go clean ./...
go install ./...
popd

%check
export GO111MODULE=auto
export GOPATH="${PWD}"
pushd src/%{gopath_comp_influxdb}
go test -run=TestDatabase . -v
popd

%install
export GOPATH="${PWD}"
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_sysconfdir}/influxdb
mkdir -p %{buildroot}%{_sysconfdir}/logrotate.d
mkdir -p %{buildroot}%{_prefix}/lib/systemd/system
mkdir -p %{buildroot}%{_mandir}/man1/
mkdir -p %{buildroot}%{_sharedstatedir}/influxdb
mkdir -p %{buildroot}%{_localstatedir}/log/influxdb
mkdir -m 755 -p %{buildroot}%{_libdir}/influxdb/scripts
cp -r bin/influx* %{buildroot}%{_bindir}
pushd src/%{gopath_comp_influxdb}
install -p -D -m 0644 %{SOURCE2} %{buildroot}%{_sysusersdir}/%{name}.sysusers
install -p -m 0755 scripts/influxd-systemd-start.sh %{buildroot}%{_libdir}/influxdb/scripts/influxd-systemd-start.sh
cp etc/config.sample.toml %{buildroot}%{_sysconfdir}/influxdb/influxdb.conf
cp scripts/logrotate %{buildroot}%{_sysconfdir}/logrotate.d/influxdb
cp scripts/influxdb.service %{buildroot}%{_prefix}/lib/systemd/system
cp man/influx.txt %{buildroot}%{_mandir}/man1/influx.1
cp man/influx_inspect.txt %{buildroot}%{_mandir}/man1/influx_inspect.1
cp man/influx_stress.txt %{buildroot}%{_mandir}/man1/influx_stress.1
cp man/influxd-backup.txt %{buildroot}%{_mandir}/man1/influxd-backup.1
cp man/influxd-config.txt %{buildroot}%{_mandir}/man1/influxd-config.1
cp man/influxd-restore.txt %{buildroot}%{_mandir}/man1/influxd-restore.1
cp man/influxd-run.txt %{buildroot}%{_mandir}/man1/influxd-run.1
cp man/influxd-version.txt %{buildroot}%{_mandir}/man1/influxd-version.1
cp man/influxd.txt %{buildroot}%{_mandir}/man1/influxd.1
popd

%clean
rm -rf %{buildroot}/*

%pre
%sysusers_create_compat %{SOURCE2}

%post
chown -R %{name}:%{name} /var/lib/%{name}
chown -R %{name}:%{name} /var/log/%{name}
%systemd_post influxdb.service

%preun
%systemd_preun influxdb.service

%postun
%systemd_postun_with_restart influxdb.service

%files
%defattr(-,root,root,755)
%dir %config(noreplace) %{_sysconfdir}/influxdb
%dir %{_sharedstatedir}/influxdb
%dir %{_localstatedir}/log/influxdb
%config(noreplace) %{_sysconfdir}/influxdb/influxdb.conf
%config(noreplace) %{_sysconfdir}/logrotate.d/influxdb
%{_libdir}/influxdb/scripts/influxd-systemd-start.sh
%{_prefix}/lib/systemd/system/influxdb.service
%{_bindir}/influxd
%{_bindir}/influx
%{_bindir}/influx_inspect
%{_bindir}/influx_stress
%{_bindir}/influx_tools
%{_mandir}/man1/*
%{_sysusersdir}/%{name}.sysusers

%changelog
* Fri Aug 23 2024 Bo Gan <bo.gan@broadcom.com> 1.8.10-11
- Simplify build scripts. Godep is removed in favor of gomod.
* Fri Jul 12 2024 Mukul Sikka <mukul.sikka@broadcom.com> 1.8.10-10
- Bump version as a part of go upgrade
* Thu Jun 20 2024 Mukul Sikka <msikka@vmware.com> 1.8.10-9
- Bump version as a part of go upgrade
* Thu Feb 22 2024 Mukul Sikka <msikka@vmware.com> 1.8.10-8
- Bump version as a part of go upgrade
* Tue Nov 21 2023 Piyush Gupta <gpiyush@vmware.com> 1.8.10-7
- Bump up version to compile with new go
* Wed Oct 11 2023 Piyush Gupta <gpiyush@vmware.com> 1.8.10-6
- Bump up version to compile with new go
* Mon Sep 18 2023 Piyush Gupta <gpiyush@vmware.com> 1.8.10-5
- Bump up version to compile with new go
* Tue Aug 08 2023 Mukul Sikka <msikka@vmware.com> 1.8.10-4
- Resolving systemd-rpm-macros for group creation
* Mon Jul 17 2023 Piyush Gupta <gpiyush@vmware.com> 1.8.10-3
- Bump up version to compile with new go
* Thu Jun 22 2023 Piyush Gupta <gpiyush@vmware.com> 1.8.10-2
- Bump up version to compile with new go
* Thu May 18 2023 Anmol Jain <anmolja@vmware.com> 1.8.10-1
- Version Bump
* Wed May 03 2023 Piyush Gupta <gpiyush@vmware.com> 1.8.2-10
- Bump up version to compile with new go
* Sun Mar 12 2023 Piyush Gupta <gpiyush@vmware.com> 1.8.2-9
- Bump up version to compile with new go
* Fri Mar 10 2023 Mukul Sikka <msikka@vmware.com> 1.8.2-8
- Use systemd-rpm-macros for user creation
* Mon Nov 21 2022 Piyush Gupta <gpiyush@vmware.com> 1.8.2-7
- Bump up version to compile with new go
* Wed Oct 26 2022 Piyush Gupta <gpiyush@vmware.com> 1.8.2-6
- Bump up version to compile with new go
* Fri Jun 17 2022 Piyush Gupta <gpiyush@vmware.com> 1.8.2-5
- Bump up version to compile with new go
* Fri Jun 11 2021 Piyush Gupta<gpiyush@vmware.com> 1.8.2-4
- Bump up version to compile with new go
* Fri Feb 05 2021 Harinadh D <hdommaraju@vmware.com> 1.8.2-3
- Bump up version to compile with new go
* Fri Jan 15 2021 Piyush Gupta<gpiyush@vmware.com> 1.8.2-2
- Bump up version to compile with new go
* Wed Aug 19 2020 Gerrit Photon <photon-checkins@vmware.com> 1.8.2-1
- Automatic Version Bump
* Wed Jul 22 2020 Gerrit Photon <photon-checkins@vmware.com> 1.8.1-1
- Automatic Version Bump
* Tue Jan 29 2019 Keerthana K <keerthanak@vmware.com> 1.6.0-5
- Using golang dep to resolve dependencies.
* Fri Jan 25 2019 Keerthana K <keerthanak@vmware.com> 1.6.0-4
- Added make check.
* Mon Jan 21 2019 Bo Gan <ganb@vmware.com> 1.6.0-3
- Build using go 1.9.7
* Thu Oct 25 2018 Ajay Kaher <akaher@vmware.com> 1.6.0-2
- Fix for aarch64
* Wed Aug 1 2018 Keerthana K <keerthanak@vmware.com> 1.6.0-1
- Initial influxdb package for Photon.
