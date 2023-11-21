Name:           influxdb
Version:        1.8.2
Release:        11%{?dist}
Summary:        InfluxDB is an open source time series database
License:        MIT
URL:            https://influxdata.com
Vendor:         VMware, Inc.
Distribution:   Photon
Group:          Applications/Database

Source0: https://github.com/influxdata/influxdb/archive/%{name}-%{version}.tar.gz
%define sha512 %{name}=d45d96a1efa39f4896724c21be7992a4cd47b5e5eac97fe8b8fde87f4d9c6ed4d89e4a92e5c6957728f73fb58fbf01dbaf28a33b1f179535976aad83239c1f1c

Source1: golang-dep-0.3.0.tar.gz
%define sha512 golang-dep-0.3.0=377869d69838a826499b9bc063eacc4b9db0d130d785901ae7fcbf28645276ba6bead33d251837646ded5f0a078e56b4a378c5227054b738cd6d581224977dc2

BuildRequires:  go >= 1.13
BuildRequires:  git
BuildRequires:  systemd-devel

Requires:       systemd
Requires:       shadow

%description
InfluxDB is an open source time series database with no external dependencies.
It's useful for recording metrics, events, and performing analytics.

%prep
%autosetup
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

%install
pushd ${GOPATH}/src/github.com/influxdata
mkdir -p %{buildroot}%{_bindir} \
         %{buildroot}%{_sysconfdir}/influxdb \
         %{buildroot}%{_sysconfdir}/logrotate.d \
         %{buildroot}%{_prefix}%{_unitdir} \
         %{buildroot}%{_mandir}/man1/ \
         %{buildroot}%{_sharedstatedir}/influxdb \
         %{buildroot}%{_localstatedir}/log/influxdb

cp -r ${GOPATH}/bin/influx* %{buildroot}%{_bindir}
cp %{name}/etc/config.sample.toml %{buildroot}%{_sysconfdir}/influxdb/influxdb.conf
cp %{name}/scripts/logrotate %{buildroot}%{_sysconfdir}/logrotate.d/influxdb
cp %{name}/scripts/influxdb.service %{buildroot}%{_prefix}%{_unitdir}
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
eu-elfcompress -q -p -t none %{buildroot}%{_bindir}/*

%check
go test -run=TestDatabase . -v

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

%files
%defattr(-,root,root,755)
%dir %config(noreplace) %{_sysconfdir}/influxdb
%dir %{_sharedstatedir}/influxdb
%dir %{_localstatedir}/log/influxdb
%config(noreplace) %{_sysconfdir}/influxdb/influxdb.conf
%config(noreplace) %{_sysconfdir}/logrotate.d/influxdb
%{_prefix}%{_unitdir}/influxdb.service
%{_bindir}/influxd
%{_bindir}/influx
%{_bindir}/influx_inspect
%{_bindir}/influx_stress
%{_bindir}/influx_tools
%{_bindir}/influx_tsm
%{_mandir}/man1/*

%changelog
* Tue Nov 21 2023 Piyush Gupta <gpiyush@vmware.com> 1.8.2-11
- Bump up version to compile with new go
* Wed Oct 11 2023 Piyush Gupta <gpiyush@vmware.com> 1.8.2-10
- Bump up version to compile with new go
* Tue Sep 26 2023 Piyush Gupta <gpiyush@vmware.com> 1.8.2-9
- Bump up version to compile with new go
* Fri Aug 18 2023 Piyush Gupta <gpiyush@vmware.com> 1.8.2-8
- Bump up version to compile with new go
* Thu Jun 22 2023 Piyush Gupta <gpiyush@vmware.com> 1.8.2-7
- Bump up version to compile with new go
* Wed May 03 2023 Piyush Gupta <gpiyush@vmware.com> 1.8.2-6
- Bump up version to compile with new go
* Tue Apr 04 2023 Piyush Gupta <gpiyush@vmware.com> 1.8.2-5
- Bump up version to compile with new go
* Tue Dec 20 2022 Piyush Gupta <gpiyush@vmware.com> 1.8.2-4
- Bump up version to compile with new go
* Sun Nov 13 2022 Piyush Gupta <gpiyush@vmware.com> 1.8.2-3
- Bump up version to compile with new go
* Wed Oct 26 2022 Piyush Gupta <gpiyush@vmware.com> 1.8.2-2
- Bump up version to compile with new go
* Wed Oct 12 2022 Shreenidhi Shedi <sshedi@vmware.com> 1.8.2-1
- Upgrade to v1.8.2
* Thu Sep 15 2022 Piyush Gupta <gpiyush@vmware.com> 1.6.0-23
- Bump up version to compile with new go
* Thu Aug 18 2022 Piyush Gupta <gpiyush@vmware.com> 1.6.0-22
- Bump up version to compile with new go
* Mon May 09 2022 Piyush Gupta <gpiyush@vmware.com> 1.6.0-21
- Bump up version to compile with new go
* Wed Mar 16 2022 Piyush Gupta <gpiyush@vmware.com> 1.6.0-20
- Bump up version to compile with new go
* Tue Feb 22 2022 Piyush Gupta <gpiyush@vmware.com> 1.6.0-19
- Bump up version to compile with new go
* Mon Jan 24 2022 Piyush Gupta <gpiyush@vmware.com> 1.6.0-18
- Bump up version to compile with new go
* Tue Nov 16 2021 Piyush Gupta <gpiyush@vmware.com> 1.6.0-17
- Bump up version to compile with new go
* Wed Oct 20 2021 Piyush Gupta <gpiyush@vmware.com> 1.6.0-16
- Bump up version to compile with new go
* Sat Aug 21 2021 Piyush Gupta<gpiyush@vmware.com> 1.6.0-15
- Bump up version to compile with new go
* Tue Jun 29 2021 Piyush Gupta <gpiyush@vmware.com> 1.6.0-14
- Bump up version to compile with new go
* Mon May 03 2021 Piyush Gupta<gpiyush@vmware.com> 1.6.0-13
- Bump up version to compile with new go
* Mon Feb 08 2021 Harinadh D <hdommaraju@vmware.com> 1.6.0-12
- Bump up version to compile with new go
* Fri Dec 04 2020 HarinadhD <hdommaraju@vmware.com> 1.6.0-11
- Bump up version to compile with new go
* Thu Dec 03 2020 Shreenidhi Shedi <sshedi@vmware.com> 1.6.0-10
- Fix for CVE-2019-20933
* Tue Aug 18 2020 Ashwin H <ashwinh@vmware.com> 1.6.0-9
- Bump up version to compile with new go
* Fri Apr 10 2020 Harinadh D <hdommaraju@vmware.com> 1.6.0-8
- Bump up version to compile with go 1.13.3-2
* Tue Oct 22 2019 Ashwin H <ashwinh@vmware.com> 1.6.0-7
- Bump up version to compile with go 1.13.3
* Fri Oct 11 2019 Ashwin H <ashwinh@vmware.com> 1.6.0-6
- Build with go 1.13
* Fri Aug 30 2019 Ashwin H <ashwinh@vmware.com> 1.6.0-5
- Bump up version to compile with new go
* Fri Jan 25 2019 Keerthana K <keerthanak@vmware.com> 1.6.0-4
- Added make check.
* Mon Jan 21 2019 Bo Gan <ganb@vmware.com> 1.6.0-3
- Build using go 1.9.7
* Thu Oct 25 2018 Ajay Kaher <akaher@vmware.com> 1.6.0-2
- Fix for aarch64
* Wed Aug 1 2018 Keerthana K <keerthanak@vmware.com> 1.6.0-1
- Initial influxdb package for Photon.
