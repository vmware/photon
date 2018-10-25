Name:           influxdb
Version:        1.6.0
Release:        2%{?dist}
Summary:        InfluxDB is an open source time series database
License:        MIT
URL:            https://influxdata.com
Source0:        https://github.com/influxdata/influxdb/archive/%{name}-%{version}.tar.gz
%define sha1    %{name}=364d2fb39fc3a983f96910133a6256932fffd0e3
Source1:        influxdata.tar.gz
%define sha1    influxdata=eceaa0c1bb8712cd1f10407b3a6e5e09d5a1945e
Source2:        liner.tar.gz
%define sha1    liner=8bbbccb2c5878f9ce31aaed4aa7fb400996ef13d
Source3:        toml.tar.gz
%define sha1    toml=22c1d1d230be805248ac9d19439ae4a2bd2070d7
Source4:        roaring.tar.gz
%define sha1    roaring=3126a09d46b08d562857e9f07eb1f213b32b63fb
Source5:        pat.tar.gz
%define sha1    pat=6b6dfbefa7289d0b18836156250beece71617dba
Source6:        xxhash.tar.gz
%define sha1    xxhash=f5882005086a932ad7b915049aaf94d1deb1aa06
Source7:        jwt-go.tar.gz
%define sha1    jwt-go=7b5f1ed04032b54c4eb2a5d5c535281b71a70114
Source8:        go-bitstream.tar.gz
%define sha1    go-bitstream=e53f387f69d571f538114321311f79162729d500
Source9:        snappy.tar.gz
%define sha1    snappy=bc13a6be54bd26bb203f74f5b50b900fadc5d63b
Source10:       zap-logfmt.tar.gz
%define sha1    zap-logfmt=09c051661fc0f77c3c14680117ac2c14a18b299a
Source11:       encoding.tar.gz
%define sha1    encoding=19eceae2608686fd561b1c5c7341014a810a4f0c
Source12:       go-isatty.tar.gz
%define sha1    go-isatty=fe4a9ce5a81501ad46831590d9dbb4b47825a583
Source13:       opentracing-go.tar.gz
%define sha1    opentracing-go=cb0b37e9a6cfdb5f641f132340081e705ed5691f
Source14:       client_golang.tar.gz
%define sha1    client_golang=aa559fd695323b980b3eec464b23fc27550c72ee
Source15:       msgp.tar.gz
%define sha1    msgp=31a49f9b34bc7f6b8aca8f66eec2eb9e007582a7
Source16:       treeprint.tar.gz
%define sha1    treeprint=54d4c5adea21a6dd9388af68b678d0607f21be44
Source17:       hllpp.tar.gz
%define sha1    hllpp=35a079df8b578d453cdd3b9cafbb48e87a705326
Source18:       bolt.tar.gz
%define sha1    bolt=9dfece85c773d20bf57c55759765c46d8bf00b84
Source19:       pgzip.tar.gz
%define sha1    pgzip=14c338202812c7a036cd2f651525db59a4eaac0b
Source20:       ratecounter.tar.gz
%define sha1    ratecounter=80ed07ec366a8f9e525d3d5452cdc96381c7bb64
Source21:       x-golang.tar.gz
%define sha1    x-golang=815014d8c3654f894903b27fa0e426bbd06f7a9e
Source22:       collectd.org.tar.gz
%define sha1    collectd.org=c4b785a64b789fb01a1c7c03211101893f62ee7c
Source23:       protobuf-gogo.tar.gz
%define sha1    protobuf-gogo=1dd504f012f2e4134d92075bdf2434c25d9cc92f
Source24:       go-runewidth.tar.gz
%define sha1    go-runewidth=b285c56da43ad7a7c1a7dff1996af00738908466
Source25:       perks.tar.gz
%define sha1    perks=9238e0f9f9756192ae821fa8d4389e1b4adb50cd
Source26:       go-unsnap-stream.tar.gz
%define sha1    go-unsnap-stream=5f524be03e8ddc20f01c5e13a250cf52fdb870e4
Source27:       protobuf-golang.tar.gz
%define sha1    protobuf-golang=5af8d015243c934befb699404b78374d9fdde4d9
Source28:       fwd.tar.gz
%define sha1    fwd=babaa98dc9ba8f75e90b5f3cd00cb05ef212fe5a
Source29:       client_model.tar.gz
%define sha1    client_model=dbf38a3217a4ac943fa17502424edf4363bb226a
Source30:       common-prometheus.tar.gz
%define sha1    common-prometheus=8c2b0ca3f398844fc2f35c15f40cc4596bc0f749
Source31:       procfs-prometheus.tar.gz
%define sha1    procfs-prometheus=4b34db5de4a849601cacd759e71d9d637d0b7bde
Source32:       zap-gouber.tar.gz
%define sha1    zap-gouber=7dc49e1d132300b1d282cc5b3d2f06d4c068cdbf
Source33:       compress.tar.gz
%define sha1    compress=6e24a9b94a6e9e8a14d13fa21b10df98e2d84641
Source34:       crc32.tar.gz
%define sha1    crc32=f2a5e0f7b94c913a87c0f8bee56d5d43fe31b0a8
Source35:       golang_protobuf_extensions.tar.gz
%define sha1    golang_protobuf_extensions=a28c3060440942f4439b656c00a9b62fbae74950
Source36:       atomic.tar.gz
%define sha1    atomic=ca0810ba1b97bf35e953daa07157596cbbad33ae
Source37:       multierr.tar.gz
%define sha1    multierr=ac35063c9f23fd2eb5cb0c7b5ded4b47a861877f
Source38:       cpuid.tar.gz
%define sha1    cpuid=e3fafb37e0d46282784c26bed14cde2f4979be86
Source39:       yamux.tar.gz
%define sha1    yamux=306f059060067e4c093e5ebf1e2dbd47bbc573d0
Vendor:         VMware, Inc.
Distribution:   Photon
Group:          Applications/Database
BuildRequires:  go = 1.9.4
BuildRequires:  git
BuildRequires:  systemd
Requires:       systemd
Requires:       shadow

%description
InfluxDB is an open source time series database with no external dependencies.
It's useful for recording metrics, events, and performing analytics.

%prep
%setup -c -T -a 0 -n build/src/github.com/influxdata
%setup -D -c -T -a 1 -n build/src/github.com/influxdata
%setup -D -c -T -a 2 -n build/src/github.com/peterh
%setup -D -c -T -a 3 -n build/src/github.com/BurntSushi
%setup -D -c -T -a 4 -n build/src/github.com/RoaringBitmap
%setup -D -c -T -a 5 -n build/src/github.com/bmizerany
%setup -D -c -T -a 6 -n build/src/github.com/cespare
%setup -D -c -T -a 7 -n build/src/github.com/dgrijalva
%setup -D -c -T -a 8 -n build/src/github.com/dgryski
%setup -D -c -T -a 9 -n build/src/github.com/golang
%setup -D -c -T -a 10 -n build/src/github.com/jsternberg
%setup -D -c -T -a 11 -n build/src/github.com/jwilder
%setup -D -c -T -a 12 -n build/src/github.com/mattn
%setup -D -c -T -a 13 -n build/src/github.com/opentracing
%setup -D -c -T -a 14 -n build/src/github.com/prometheus
%setup -D -c -T -a 15 -n build/src/github.com/tinylib
%setup -D -c -T -a 16 -n build/src/github.com/xlab
%setup -D -c -T -a 17 -n build/src/github.com/retailnext
%setup -D -c -T -a 18 -n build/src/github.com/boltdb
%setup -D -c -T -a 19 -n build/src/github.com/klauspost
%setup -D -c -T -a 20 -n build/src/github.com/paulbellamy
%setup -D -c -T -a 21 -n build/src/golang.org/
%setup -D -c -T -a 22 -n build/src/
%setup -D -c -T -a 23 -n build/src/github.com/gogo
%setup -D -c -T -a 24 -n build/src/github.com/mattn
%setup -D -c -T -a 25 -n build/src/github.com/beorn7
%setup -D -c -T -a 26 -n build/src/github.com/glycerine
%setup -D -c -T -a 27 -n build/src/github.com/golang
%setup -D -c -T -a 28 -n build/src/github.com/philhofer
%setup -D -c -T -a 29 -n build/src/github.com/prometheus
%setup -D -c -T -a 30 -n build/src/github.com/prometheus
%setup -D -c -T -a 31 -n build/src/github.com/prometheus
%setup -D -c -T -a 32 -n build/src/go.uber.org
%setup -D -c -T -a 33 -n build/src/github.com/klauspost
%setup -D -c -T -a 34 -n build/src/github.com/klauspost
%setup -D -c -T -a 35 -n build/src/github.com/matttproud
%setup -D -c -T -a 36 -n build/src/go.uber.org/
%setup -D -c -T -a 37 -n build/src/go.uber.org/
%setup -D -c -T -a 38 -n build/src/github.com/klauspost
%setup -D -c -T -a 39 -n build/src/github.com/influxdata

%build
cd ../../../
export GOPATH=`pwd`
mkdir -p bin
cd bin
export GOBIN=`pwd`
export PATH=$PATH:$GOBIN
cd ../src/github.com/influxdata/
mv -f %{name}-%{version} %{name}
cd %{name}

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
cp -r ../../../bin/* %{buildroot}%{_bindir}
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
*   Thu Oct 25 2018 Ajay Kaher <akaher@vmware.com> 1.6.0-2
-   Fix for aarch64
*   Wed Aug 1 2018 Keerthana K <keerthanak@vmware.com> 1.6.0-1
-   Initial influxdb package for Photon.
