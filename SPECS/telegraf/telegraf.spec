

Summary:        agent for collecting, processing, aggregating, and writing metrics.
Name:           telegraf
Version:        1.10.0
Release:        1%{?dist}
License:        MIT
URL:            https://github.com/influxdata/telegraf
Source0:        https://github.com/influxdata/telegraf/archive/%{name}-%{version}.tar.gz
%define sha1    telegraf=e02d4c1319099f4111ab06a4fa6c4e47b8e70742
Source1:        https://github.com/wavefrontHQ/telegraf/archive/telegraf-plugin-1.4.0.zip
%define sha1    telegraf-plugin=51d2bedf6b7892dbe079e7dd948d60c31a2fc436
Source2:        https://raw.githubusercontent.com/wavefrontHQ/integrations/master/telegraf/telegraf.conf
Source3:       golang-dep-0.5.0.tar.gz
%define sha1 golang-dep-0.5.0=b8bb441fe3a4445e6cd4fa263dd2112e8566a734
Group:          Development/Tools
Vendor:         VMware, Inc.
Distribution:   Photon
BuildRequires:  go
BuildRequires:  git
BuildRequires:  systemd
BuildRequires:  unzip
Requires:       systemd
Requires:       logrotate
Requires(pre):  /usr/sbin/useradd /usr/sbin/groupadd
Requires(postun):/usr/sbin/userdel /usr/sbin/groupdel

%description
Telegraf is an agent written in Go for collecting, processing, aggregating, and writing metrics.

Design goals are to have a minimal memory footprint with a plugin system so that developers in
the community can easily add support for collecting metrics from well known services (like Hadoop,
Postgres, or Redis) and third party APIs (like Mailchimp, AWS CloudWatch, or Google Analytics).

%prep
%setup
mkdir -p ${GOPATH}/src/github.com/golang/dep
tar xf %{SOURCE3} --no-same-owner --strip-components 1 -C ${GOPATH}/src/github.com/golang/dep/
mkdir -p ${GOPATH}/src/github.com/influxdata/telegraf
tar xf %{SOURCE0} --no-same-owner --strip-components 1 -C ${GOPATH}/src/github.com/influxdata/telegraf
cat << EOF >>%{SOURCE2}
[[outputs.wavefront]]
host = "localhost"
port = 2878
metric_separator = "."
source_override = ["hostname", "snmp_host", "node_host"]
convert_paths = true
use_regex = false
EOF

pushd ..
unzip %{SOURCE1}
popd

%build
pushd ${GOPATH}/src/github.com/golang/dep
CGO_ENABLED=0 GOOS=linux go build -v -ldflags "-s -w" -o ${GOPATH}/bin/dep ./cmd/dep/
popd
mkdir -p ${GOPATH}/src/github.com/wavefronthq/telegraf/plugins/outputs/wavefront
pushd ../telegraf-1.4.0
cp -r *  ${GOPATH}/src/github.com/wavefronthq/telegraf/
popd
pushd ${GOPATH}/src/github.com/influxdata/telegraf
sed -i '/import (/ a \\t_ "github.com/wavefronthq/telegraf/plugins/outputs/wavefront"' ${GOPATH}/src/github.com/influxdata/telegraf/plugins/outputs/all/all.go
sed -i 's/m.UnixNano()/m.Time().UnixNano()/g' ${GOPATH}/src/github.com/wavefronthq/telegraf/plugins/outputs/wavefront/wavefront.go
sed -i 's/github.com\/golang\/lint\/golint/golang.org\/x\/lint\/golint/g' ${GOPATH}/src/github.com/influxdata/telegraf/Makefile
make
popd

%install
install -m 755 -D ${GOPATH}/src/github.com/influxdata/%{name}/%{name} %{buildroot}%{_bindir}/%{name}
install -m 755 -D ${GOPATH}/src/github.com/influxdata/%{name}/scripts/%{name}.service %{buildroot}%{_unitdir}/%{name}.service
install -m 755 -D ${GOPATH}/src/github.com/influxdata/%{name}/etc/logrotate.d/%{name} %{buildroot}%{_sysconfdir}/logrotate.d/%{name}
install -m 755 -D %{SOURCE2} %{buildroot}%{_sysconfdir}/%{name}/%{name}.conf

%clean
rm -rf %{buildroot}/*

%pre
getent group telegraf >/dev/null || groupadd -r telegraf
getent passwd telegraf >/dev/null || useradd -c "Telegraf" -d %{_localstatedir}/lib/%{name} -g %{name} \
        -s /sbin/nologin -M -r %{name}

%post
chown -R telegraf:telegraf /etc/telegraf
%systemd_post %{name}.service
systemctl daemon-reload

%preun
%systemd_preun %{name}.service

%postun
if [ $1 -eq 0 ] ; then
    getent passwd telegraf >/dev/null && userdel telegraf
    getent group telegraf >/dev/null && groupdel telegraf
fi
%systemd_postun_with_restart %{name}.service

%files
%defattr(-,root,root)
%{_bindir}/telegraf
%{_unitdir}/telegraf.service
%{_sysconfdir}/logrotate.d/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/telegraf.conf

%changelog
*   Thu Mar 14 2019 Keerthana K <keerthanak@vmware.com> 1.10.0-1
-   Update to version 1.10.0
*   Fri Sep 07 2018 Michelle Wang <michellew@vmware.com> 1.7.4-1
-   Update version to 1.7.4 and its plugin version to 1.4.0.
*   Mon Sep 18 2017 Alexey Makhalov <amakhalov@vmware.com> 1.3.4-2
-   Remove shadow from requires and use explicit tools for post actions
*   Tue Jul 18 2017 Dheeraj Shetty <dheerajs@vmware.com> 1.3.4-1
-   first version
