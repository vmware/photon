Name:           influxdb
Version:        1.6.0
Release:        1%{?dist}
Summary:        InfluxDB is an open source time series database
License:        MIT
URL:            https://influxdata.com
Source0:        https://github.com/influxdata/influxdb/archive/%{name}-%{version}.tar.gz
%define sha1    %{name}=364d2fb39fc3a983f96910133a6256932fffd0e3
Vendor:         VMware, Inc.
Distribution:   Photon
Group:          Applications/Database
BuildRequires:  go
BuildRequires:  git
Requires:       shadow

%description
InfluxDB is an open source time series database with no external dependencies.
It's useful for recording metrics, events, and performing analytics.

%prep
%setup -q -n %{name}-%{version}

%build
cd ..
mkdir -p build/src/github.com/influxdata/influxdb
mkdir -p build/bin
cp -r %{name}-%{version}/* build/src/github.com/influxdata/influxdb
cd build
export GOPATH=`pwd`
cd bin
export GOBIN=`pwd`
export PATH=$PATH:$GOBIN
cd ../src/github.com/influxdata/influxdb
go get github.com/influxdata/influxql
go get github.com/peterh/liner
go get golang.org/x/crypto/ssh/terminal
go get collectd.org/api
go get collectd.org/network
go get github.com/BurntSushi/toml
go get github.com/RoaringBitmap/roaring
go get github.com/bmizerany/pat
go get github.com/cespare/xxhash
go get github.com/dgrijalva/jwt-go
go get github.com/dgryski/go-bitstream
go get github.com/golang/snappy
go get github.com/influxdata/usage-client/v1
go get github.com/influxdata/yarpc
go get github.com/influxdata/yarpc/yarpcproto
go get github.com/jsternberg/zap-logfmt
go get github.com/jwilder/encoding/simple8b
go get github.com/mattn/go-isatty
go get github.com/opentracing/opentracing-go
go get github.com/opentracing/opentracing-go/ext
go get github.com/prometheus/client_golang/prometheus/promhttp
go get github.com/tinylib/msgp/msgp
go get github.com/xlab/treeprint
go get golang.org/x/sync/errgroup
go get golang.org/x/text/encoding/unicode
go get golang.org/x/text/transform
go get golang.org/x/time/rate
go get github.com/retailnext/hllpp
go get github.com/boltdb/bolt
go get github.com/klauspost/pgzip
go get github.com/paulbellamy/ratecounter

go clean ./...
go install ./...

%install
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_sysconfdir}/influxdb
mkdir -p %{buildroot}%{_sysconfdir}/logrotate.d
mkdir -p %{buildroot}%{_prefix}/lib/systemd/system
mkdir -p %{buildroot}%{_mandir}/man1/
mkdir -p %{buildroot}%{_sharedstatedir}/influxdb
mkdir -p %{buildroot}%{_localstatedir}/log/influxdb
cp -r ../build/bin/* %{buildroot}%{_bindir}
cp etc/config.sample.toml %{buildroot}%{_sysconfdir}/influxdb/influxdb.conf
cp scripts/logrotate %{buildroot}%{_sysconfdir}/logrotate.d/influxdb
cp scripts/influxdb.service %{buildroot}%{_prefix}/lib/systemd/system
cp man/influx.txt %{buildroot}%{_mandir}/man1/influx.1
cp man/influx_inspect.txt %{buildroot}%{_mandir}/man1/influx_inspect.1
cp man/influx_stress.txt %{buildroot}%{_mandir}/man1/influx_stress.1
cp man/influx_tsm.txt %{buildroot}%{_mandir}/man1/influx_tsm.1
cp man/influxd-backup.txt %{buildroot}%{_mandir}/man1/influxd-backup.1
cp man/influxd-config.txt %{buildroot}%{_mandir}/man1/influxd-config.1
cp man/influxd-restore.txt %{buildroot}%{_mandir}/man1/influxd-restore.1
cp man/influxd-run.txt %{buildroot}%{_mandir}/man1/influxd-run.1
cp man/influxd-version.txt %{buildroot}%{_mandir}/man1/influxd-version.1
cp man/influxd.txt %{buildroot}%{_mandir}/man1/influxd.1

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
systemctl daemon-reload
systemctl stop %{name}
systemctl enable %{name}

%preun
if [ $1 -eq 0 ]; then
    systemctl stop %{name}
fi

%postun
if [ $1 -eq 0 ]; then
    # Package deletion
    userdel %{name}
    groupdel %{name}
    systemctl daemon-reload
fi

%files
%defattr(-,root,root,755)
%dir %{_sysconfdir}/influxdb
%dir %{_sysconfdir}/logrotate.d
%dir %{_sharedstatedir}/influxdb
%dir %{_localstatedir}/log/influxdb
%{_sysconfdir}/influxdb/influxdb.conf
%{_sysconfdir}/logrotate.d/influxdb
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
*   Wed Aug 1 2018 Keerthana K <keerthanak@vmware.com> 1.6.0-1
-   Initial influxdb package for Photon.
