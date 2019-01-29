Name:           influxdb
Version:        1.6.0
Release:        5%{?dist}
Summary:        InfluxDB is an open source time series database
License:        MIT
URL:            https://influxdata.com
Source0:        https://github.com/influxdata/influxdb/archive/%{name}-%{version}.tar.gz
%define sha1    %{name}=364d2fb39fc3a983f96910133a6256932fffd0e3
Source1:       golang-dep-0.3.0.tar.gz
%define sha1 golang-dep-0.3.0=e5e9952227930fe1e8632edc03d690bffc3e1132
Vendor:         VMware, Inc.
Distribution:   Photon
Group:          Applications/Database
BuildRequires:  go = 1.9.7
BuildRequires:  git
BuildRequires:  systemd
Requires:       systemd
Requires:       shadow

%description
InfluxDB is an open source time series database with no external dependencies.
It's useful for recording metrics, events, and performing analytics.

%prep
%setup -q
mkdir -p ${GOPATH}/src/github.com/golang/dep
tar xf %{SOURCE1} --no-same-owner --strip-components 1 -C ${GOPATH}/src/github.com/golang/dep/

%build
pushd ${GOPATH}/src/github.com/golang/dep
CGO_ENABLED=0 GOOS=linux go build -v -ldflags "-s -w" -o ${GOPATH}/bin/dep ./cmd/dep/
popd
mkdir -p ${GOPATH}/src/github.com/influxdata/influxdb
cp -r * ${GOPATH}/src/github.com/influxdata/influxdb/.
pushd ${GOPATH}/src/github.com/influxdata/influxdb/
${GOPATH}/bin/dep ensure
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
if [ $1 -eq 1 ]; then
    # Initial installation.
    getent group %{name} >/dev/null || groupadd -r %{name}
    getent passwd %{name} >/dev/null || useradd -r -g %{name} -d /var/lib/%{name} -s /sbin/nologin \
            -c "InfluxDB" %{name}
fi

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
%{_bindir}/influx-tools
%{_bindir}/influx_tsm
%{_mandir}/man1/*
%exclude %{_bindir}/store
%exclude %{_bindir}/stress_test_server
%exclude %{_bindir}/test_client

%changelog
*   Tue Jan 29 2019 Keerthana K <keerthanak@vmware.com> 1.6.0-5
-   Using golang dep to resolve dependencies.
*   Fri Jan 25 2019 Keerthana K <keerthanak@vmware.com> 1.6.0-4
-   Added make check.
*   Mon Jan 21 2019 Bo Gan <ganb@vmware.com> 1.6.0-3
-   Build using go 1.9.7
*   Thu Oct 25 2018 Ajay Kaher <akaher@vmware.com> 1.6.0-2
-   Fix for aarch64
*   Wed Aug 1 2018 Keerthana K <keerthanak@vmware.com> 1.6.0-1
-   Initial influxdb package for Photon.
