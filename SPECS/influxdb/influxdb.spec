Name:           influxdb
Version:        1.8.2
Release:        9%{?dist}
Summary:        InfluxDB is an open source time series database
License:        MIT
URL:            https://influxdata.com
Source0:        https://github.com/influxdata/influxdb/archive/%{name}-%{version}.tar.gz
%define sha512  %{name}=d45d96a1efa39f4896724c21be7992a4cd47b5e5eac97fe8b8fde87f4d9c6ed4d89e4a92e5c6957728f73fb58fbf01dbaf28a33b1f179535976aad83239c1f1c
Source1:        golang-dep-0.3.0.tar.gz
%define sha512  golang-dep-0.3.0=377869d69838a826499b9bc063eacc4b9db0d130d785901ae7fcbf28645276ba6bead33d251837646ded5f0a078e56b4a378c5227054b738cd6d581224977dc2
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
%autosetup -p1
mkdir -p ${GOPATH}/src/github.com/golang/dep
tar xf %{SOURCE1} --no-same-owner --strip-components 1 -C ${GOPATH}/src/github.com/golang/dep/

%build
export GO111MODULE=auto
pushd ${GOPATH}/src/github.com/golang/dep
CGO_ENABLED=0 GOOS=linux go build -ldflags=-linkmode=external -v -ldflags "-s -w" -o ${GOPATH}/bin/dep ./cmd/dep/
popd
mkdir -p ${GOPATH}/src/github.com/influxdata/influxdb
cp -r * ${GOPATH}/src/github.com/influxdata/influxdb/.
pushd ${GOPATH}/src/github.com/influxdata/influxdb/
go clean ./...
go install ./...

%check
go test -run=TestDatabase . -v

%install
pushd ${GOPATH}/src/github.com/influxdata
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_sysconfdir}/influxdb
mkdir -p %{buildroot}%{_sysconfdir}/logrotate.d
mkdir -p %{buildroot}%{_prefix}/lib/systemd/system
mkdir -p %{buildroot}%{_mandir}/man1/
mkdir -p %{buildroot}%{_sharedstatedir}/influxdb
mkdir -p %{buildroot}%{_localstatedir}/log/influxdb
install -p -D -m 0644 %{SOURCE2} %{buildroot}%{_sysusersdir}/%{name}.sysusers
cp -r ${GOPATH}/bin/influx* %{buildroot}%{_bindir}
cp %{name}/etc/config.sample.toml %{buildroot}%{_sysconfdir}/influxdb/influxdb.conf
cp %{name}/scripts/logrotate %{buildroot}%{_sysconfdir}/logrotate.d/influxdb
cp %{name}/scripts/influxdb.service %{buildroot}%{_prefix}/lib/systemd/system
cp %{name}/man/influx.txt %{buildroot}%{_mandir}/man1/influx.1
cp %{name}/man/influx_inspect.txt %{buildroot}%{_mandir}/man1/influx_inspect.1
cp %{name}/man/influx_stress.txt %{buildroot}%{_mandir}/man1/influx_stress.1
cp %{name}/man/influx_tsm.txt %{buildroot}%{_mandir}/man1/influx_tsm.1
cp %{name}/man/influxd-backup.txt %{buildroot}%{_mandir}/man1/influxd-backup.1
cp %{name}/man/influxd-config.txt %{buildroot}%{_mandir}/man1/influxd-config.1
cp %{name}/man/influxd-restore.txt %{buildroot}%{_mandir}/man1/influxd-restore.1
cp %{name}/man/influxd-run.txt %{buildroot}%{_mandir}/man1/influxd-run.1
cp %{name}/man/influxd-version.txt %{buildroot}%{_mandir}/man1/influxd-version.1
cp %{name}/man/influxd.txt %{buildroot}%{_mandir}/man1/influxd.1

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
if [ $1 -eq 0 ]; then
    # Package deletion
    userdel %{name}
    groupdel %{name}
fi

%files
%defattr(-,root,root,755)
%dir %config(noreplace) %{_sysconfdir}/influxdb
%dir %{_sharedstatedir}/influxdb
%dir %{_localstatedir}/log/influxdb
%config(noreplace) %{_sysconfdir}/influxdb/influxdb.conf
%config(noreplace) %{_sysconfdir}/logrotate.d/influxdb
%{_prefix}/lib/systemd/system/influxdb.service
%{_bindir}/influxd
%{_bindir}/influx
%{_bindir}/influx_inspect
%{_bindir}/influx_stress
%{_bindir}/influx_tools
%{_bindir}/influx_tsm
%{_mandir}/man1/*
%{_sysusersdir}/%{name}.sysusers

%changelog
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
