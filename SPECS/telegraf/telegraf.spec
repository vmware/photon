Summary:        agent for collecting, processing, aggregating, and writing metrics.
Name:           telegraf
Version:        1.3.4
Release:        1%{?dist}
License:        MIT
URL:            https://github.com/influxdata/telegraf
Source0:        https://github.com/influxdata/telegraf/archive/%{name}-%{version}.tar.gz
%define sha1    telegraf=b9613ff3960ab791ec992426067b99c02b8797c7
#wget https://raw.githubusercontent.com/wavefrontHQ/integrations/master/telegraf/telegraf.conf
Source1:        telegraf.conf
Group:          Development/Tools
Vendor:         VMware, Inc.
Distribution:   Photon
BuildRequires:  go
BuildRequires:  git
BuildRequires:  systemd-devel
Requires:       systemd
Requires:       logrotate

%description
Telegraf is an agent written in Go for collecting, processing, aggregating, and writing metrics.

Design goals are to have a minimal memory footprint with a plugin system so that developers in
the community can easily add support for collecting metrics from well known services (like Hadoop,
Postgres, or Redis) and third party APIs (like Mailchimp, AWS CloudWatch, or Google Analytics).

%prep
%setup
cat << EOF >>%{SOURCE1}
[[outputs.wavefront]]
host = "localhost"
port = 2878
metric_separator = "."
source_override = ["hostname", "snmp_host", "node_host"]
convert_paths = true
use_regex = false
EOF

%build
mkdir -p ${GOPATH}/src/github.com/influxdata/telegraf
cp -r * ${GOPATH}/src/github.com/influxdata/telegraf
pushd ${GOPATH}/src/github.com/influxdata/telegraf
#Get the wavefront plugin for telegraf
go get github.com/wavefronthq/telegraf/plugins/outputs/wavefront
sed -i '/import (/ a \\t_ "github.com/wavefronthq/telegraf/plugins/outputs/wavefront"' ${GOPATH}/src/github.com/influxdata/telegraf/plugins/outputs/all/all.go
make
popd

%install
install -m 755 -D ${GOPATH}/bin/telegraf %{buildroot}%{_bindir}/telegraf
install -m 755 -D ${GOPATH}/src/github.com/influxdata/telegraf/scripts/telegraf.service %{buildroot}%{_unitdir}/telegraf.service
install -m 755 -D ${GOPATH}/src/github.com/influxdata/telegraf/etc/logrotate.d/%{name} %{buildroot}%{_sysconfdir}/logrotate.d/%{name}
install -m 755 -D %{SOURCE1} %{buildroot}%{_sysconfdir}/%{name}/telegraf.conf

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
*   Tue Jul 18 2017 Dheeraj Shetty <dheerajs@vmware.com> 1.3.4-1
-   first version
