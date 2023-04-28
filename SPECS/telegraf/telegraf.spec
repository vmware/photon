Summary:          agent for collecting, processing, aggregating, and writing metrics.
Name:             telegraf
Version:          1.18.2
Release:          7%{?dist}
License:          MIT
URL:              https://github.com/influxdata/telegraf
Source0:          https://github.com/influxdata/telegraf/archive/%{name}-%{version}.tar.gz
%define sha512    telegraf=48231f6c57c7d4294479aaaeedc9abfc86c3c1b35d294056050436d24ab884a027695c8228f9218b1cb5f9f6811f843ccd907a30d6959750109aec9a52da5df8
Source1:          https://github.com/wavefrontHQ/telegraf/archive/telegraf-plugin-1.4.0.zip
%define sha512    telegraf-plugin=3f49e403a92da5e45eaab7e9683c2f36e1143036db59e167568bec348499af6b7cc2b37135a37f6ebaf4be63bee25cf7859b6f164c6ed3064ad786a55111bfcc
Source2:          https://raw.githubusercontent.com/wavefrontHQ/integrations/master/telegraf/telegraf.conf
Source3:          %{name}.sysusers
Group:            Development/Tools
Vendor:           VMware, Inc.
Distribution:     Photon
BuildRequires:    go
BuildRequires:    git
BuildRequires:    systemd-devel
BuildRequires:    unzip
Requires:         systemd
Requires:         logrotate
Requires(pre):    systemd-rpm-macros
Requires(pre):    /usr/sbin/useradd /usr/sbin/groupadd

%description
Telegraf is an agent written in Go for collecting, processing, aggregating, and writing metrics.
Design goals are to have a minimal memory footprint with a plugin system so that developers in
the community can easily add support for collecting metrics from well known services (like Hadoop,
Postgres, or Redis) and third party APIs (like Mailchimp, AWS CloudWatch, or Google Analytics).

%prep
%autosetup -p1
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
mkdir -p ${GOPATH}/src/github.com/influxdata/telegraf
cp -r * ${GOPATH}/src/github.com/influxdata/telegraf
mkdir -p ${GOPATH}/src/github.com/wavefronthq/telegraf/plugins/outputs/wavefront
pushd ../telegraf-1.4.0
cp -r *  ${GOPATH}/src/github.com/wavefronthq/telegraf/
popd
pushd ${GOPATH}/src/github.com/influxdata/telegraf
make %{_smp_mflags}
popd

%install
install -m 755 -D ${GOPATH}/src/github.com/influxdata/%{name}/%{name} %{buildroot}%{_bindir}/%{name}
install -m 755 -D ${GOPATH}/src/github.com/influxdata/%{name}/scripts/%{name}.service %{buildroot}%{_unitdir}/%{name}.service
install -m 755 -D ${GOPATH}/src/github.com/influxdata/%{name}/etc/logrotate.d/%{name} %{buildroot}%{_sysconfdir}/logrotate.d/%{name}
install -m 755 -D %{SOURCE2} %{buildroot}%{_sysconfdir}/%{name}/%{name}.conf
install -p -D -m 0644 %{SOURCE3} %{buildroot}%{_sysusersdir}/%{name}.sysusers

%clean
rm -rf %{buildroot}/*

%pre
%sysusers_create_compat %{SOURCE3}

%post
chown -R telegraf:telegraf /etc/telegraf
%systemd_post %{name}.service
systemctl daemon-reload

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun_with_restart %{name}.service

%files
%defattr(-,root,root)
%{_bindir}/telegraf
%{_unitdir}/telegraf.service
%{_sysconfdir}/logrotate.d/%{name}
%{_sysusersdir}/%{name}.sysusers
%config(noreplace) %{_sysconfdir}/%{name}/telegraf.conf

%changelog
* Fri Mar 10 2023 Mukul Sikka <msikka@vmware.com> 1.18.2-7
- Use systemd-rpm-macros for user creation
* Thu Mar 09 2023 Piyush Gupta <gpiyush@vmware.com> 1.18.2-6
- Bump up version to compile with new go
* Mon Nov 21 2022 Piyush Gupta <gpiyush@vmware.com> 1.18.2-5
- Bump up version to compile with new go
* Wed Oct 26 2022 Piyush Gupta <gpiyush@vmware.com> 1.18.2-4
- Bump up version to compile with new go
*   Fri Jun 17 2022 Piyush Gupta <gpiyush@vmware.com> 1.18.2-3
-   Bump up version to compile with new go
*   Fri Jun 11 2021 Piyush Gupta <gpiyush@vmware.com> 1.18.2-2
-   Bump up version to compile with new go
*   Tue Apr 13 2021 Gerrit Photon <photon-checkins@vmware.com> 1.18.2-1
-   Automatic Version Bump
*   Fri Feb 05 2021 Harinadh D <hdommaraju@vmware.com> 1.15.3-3
-   Bump up version to compile with new go
*   Fri Jan 15 2021 Piyush Gupta<gpiyush@vmware.com> 1.15.3-2
-   Bump up version to compile with new go
*   Mon Sep 21 2020 Gerrit Photon <photon-checkins@vmware.com> 1.15.3-1
-   Automatic Version Bump
*   Mon Jul 27 2020 Gerrit Photon <photon-checkins@vmware.com> 1.15.2-1
-   Automatic Version Bump
*   Thu Jul 09 2020 Gerrit Photon <photon-checkins@vmware.com> 1.14.5-1
-   Automatic Version Bump
*   Fri Sep 07 2018 Michelle Wang <michellew@vmware.com> 1.7.4-1
-   Update version to 1.7.4 and its plugin version to 1.4.0.
*   Mon Sep 18 2017 Alexey Makhalov <amakhalov@vmware.com> 1.3.4-2
-   Remove shadow from requires and use explicit tools for post actions
*   Tue Jul 18 2017 Dheeraj Shetty <dheerajs@vmware.com> 1.3.4-1
-   first version
