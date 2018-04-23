Summary:        agent for collecting, processing, aggregating, and writing metrics.
Name:           telegraf
Version:        1.5.3
Release:        1%{?dist}
License:        MIT
URL:            https://github.com/influxdata/telegraf
Source0:        https://github.com/influxdata/telegraf/archive/%{name}-%{version}.tar.gz
%define sha1    telegraf=ff9860f1491cedb965283e1ffd5bd6870c473f77
Source1:        https://raw.githubusercontent.com/wavefrontHQ/integrations/master/telegraf/telegraf.conf
Group:          Development/Tools
Vendor:         VMware, Inc.
Distribution:   Photon
BuildRequires:  go
BuildRequires:  git
BuildRequires:  systemd-devel
BuildRequires:  unzip
BuildRequires:  elfutils
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

%build
mkdir -p ${GOPATH}/src/github.com/influxdata/telegraf
cp -r * ${GOPATH}/src/github.com/influxdata/telegraf
pushd ${GOPATH}/src/github.com/influxdata/telegraf
make
popd

%install
install -m 755 -D ${GOPATH}/src/github.com/influxdata/telegraf/telegraf %{buildroot}%{_bindir}/telegraf
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
*   Fri Apr 20 2018 Dheeraj Shetty <dheerajs@vmware.com> 1.5.3-1
-   upgrade to 1.5.3
*   Mon Sep 18 2017 Alexey Makhalov <amakhalov@vmware.com> 1.3.4-2
-   Remove shadow from requires and use explicit tools for post actions
*   Tue Jul 18 2017 Dheeraj Shetty <dheerajs@vmware.com> 1.3.4-1
-   first version
