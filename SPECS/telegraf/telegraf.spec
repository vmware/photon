Summary:         agent for collecting, processing, aggregating, and writing metrics.
Name:            telegraf
Version:         1.27.1
Release:         1%{?dist}
License:         MIT
URL:             https://github.com/influxdata/telegraf
Source0:         https://github.com/influxdata/telegraf/archive/%{name}-%{version}.tar.gz
%define sha512   telegraf=0f28d5c6edb0b1d8ed6a3b223412bc5f7dc27fdb643c94bc0d8f03d03d05ec58d333c5e4a5fc269ea22f137f655ab9b1c8cadb1bc649d0856a48554f9185fb2c
Source1:         https://github.com/wavefrontHQ/telegraf/archive/telegraf-plugin-1.4.0.zip
%define sha512   telegraf-plugin=3f49e403a92da5e45eaab7e9683c2f36e1143036db59e167568bec348499af6b7cc2b37135a37f6ebaf4be63bee25cf7859b6f164c6ed3064ad786a55111bfcc
Source2:         https://raw.githubusercontent.com/wavefrontHQ/integrations/master/telegraf/telegraf.conf
Source3:         golang-dep-0.5.4.tar.gz
%define sha512   golang-dep-0.5.4=b7657447c13a34d44bce47a0e0e4a3e7471efd7dffbbc18366d941302c561995ef1f2b58f92a46ed7e3d86322627964637772aab5216d334ad53fba94c1e241b
Group:           Development/Tools
Vendor:          VMware, Inc.
Distribution:    Photon
BuildRequires:   go
BuildRequires:   git
BuildRequires:   systemd-devel
BuildRequires:   unzip
Requires:        systemd
Requires:        logrotate
Requires(pre):   /usr/sbin/useradd /usr/sbin/groupadd
Requires(postun):/usr/sbin/userdel /usr/sbin/groupdel

%description
Telegraf is an agent written in Go for collecting, processing, aggregating, and writing metrics.
Design goals are to have a minimal memory footprint with a plugin system so that developers in
the community can easily add support for collecting metrics from well known services (like Hadoop,
Postgres, or Redis) and third party APIs (like Mailchimp, AWS CloudWatch, or Google Analytics).

%prep
%autosetup
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
CGO_ENABLED=0 GOOS=linux GO111MODULE=auto go build -v -ldflags "-s -w" -o ${GOPATH}/bin/dep ./cmd/dep/
popd
mkdir -p ${GOPATH}/src/github.com/wavefronthq/telegraf/plugins/outputs/wavefront
pushd ../telegraf-1.4.0
cp -r *  ${GOPATH}/src/github.com/wavefronthq/telegraf/
popd
pushd ${GOPATH}/src/github.com/influxdata/telegraf
# make doesn't support _smp_mflags
make
popd

%install
install -m 755 -D ${GOPATH}/src/github.com/influxdata/%{name}/%{name} %{buildroot}%{_bindir}/%{name}
install -m 755 -D ${GOPATH}/src/github.com/influxdata/%{name}/scripts/%{name}.service %{buildroot}%{_unitdir}/%{name}.service
install -m 755 -D ${GOPATH}/src/github.com/influxdata/%{name}/etc/logrotate.d/%{name} %{buildroot}%{_sysconfdir}/logrotate.d/%{name}
install -m 755 -D %{SOURCE2} %{buildroot}%{_sysconfdir}/%{name}/%{name}.conf
eu-elfcompress -q -p -t none %{buildroot}%{_bindir}/*

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
* Tue Jun 27 2023 Prashant S Chauhan <psinghchauha@vmware.com> 1.27.1-1
- Update to 1.27.1, Fixes second level CVEs
* Thu Jun 22 2023 Piyush Gupta <gpiyush@vmware.com> 1.26.1-3
- Bump up version to compile with new go
* Wed May 03 2023 Piyush Gupta <gpiyush@vmware.com> 1.26.1-2
- Bump up version to compile with new go
* Tue Apr 04 2023 Piyush Gupta <gpiyush@vmware.com> 1.26.1-1
- Upgrade to 1.26.1.
* Tue Feb 21 2023 Prashant S Chauhan <psinghchauha@vmware.com> 1.25.2-1
- Update to 1.25.2
* Tue Dec 20 2022 Piyush Gupta <gpiyush@vmware.com> 1.23.3-6
- Bump up version to compile with new go
* Sun Nov 13 2022 Piyush Gupta <gpiyush@vmware.com> 1.23.3-5
- Bump up version to compile with new go
* Wed Oct 26 2022 Piyush Gupta <gpiyush@vmware.com> 1.23.3-4
- Bump up version to compile with new go
* Thu Sep 15 2022 Piyush Gupta <gpiyush@vmware.com> 1.23.3-3
- Bump up version to compile with new go
* Thu Aug 18 2022 Piyush Gupta <gpiyush@vmware.com> 1.23.3-2
- Bump up version to compile with new go
* Tue Aug 02 2022 Prashant S Chauhan <psinghchauha@vmware.com> 1.23.3-1
- Update to version 1.23.3
* Tue May 31 2022 Piyush Gupta <gpiyush@vmware.com> 1.22.3-2
- Bump up version to compile with new go
* Tue May 17 2022 Prashant S Chauhan <psinghchauha@vmware.com> 1.22.3-1
- Update to version 1.22.3
* Tue Apr 19 2022 Prashant S Chauhan <psinghchauha@vmware.com> 1.22.1-1
- Update to version 1.22.1
* Wed Mar 16 2022 Piyush Gupta <gpiyush@vmware.com> 1.20.3-5
- Bump up version to compile with new go
* Tue Feb 22 2022 Piyush Gupta <gpiyush@vmware.com> 1.20.3-4
- Bump up version to compile with new go
* Mon Jan 24 2022 Piyush Gupta <gpiyush@vmware.com> 1.20.3-3
- Bump up version to compile with new go
* Tue Nov 16 2021 Piyush Gupta <gpiyush@vmware.com> 1.20.3-2
- Bump up version to compile with new go
* Tue Nov 09 2021 Prashant S Chauhan <psinghchauha@vmware.com> 1.20.3-1
- Update to version 1.20.3
* Wed Oct 20 2021 Piyush Gupta <gpiyush@vmware.com> 1.16.1-7
- Bump up version to compile with new go
* Sat Aug 21 2021 Piyush Gupta<gpiyush@vmware.com> 1.16.1-6
- Bump up version to compile with new go
* Tue Jun 29 2021 Piyush Gupta <gpiyush@vmware.com> 1.16.1-5
- Bump up version to compile with new go
* Mon May 03 2021 Piyush Gupta<gpiyush@vmware.com> 1.16.1-4
- Bump up version to compile with new go
* Mon Feb 08 2021 Harinadh D <hdommaraju@vmware.com> 1.16.1-3
- Bump up version to compile with new go
* Fri Nov 27 2020 HarinadhD <hdommaraju@vmware.com> 1.16.1-2
- Bump up version to compile with new go
* Tue Nov 10 2020 Anisha Kumari <kanisha@vmware.com> 1.16.1-1
- Bump up version to 1.16.1
* Fri Apr 10 2020 Harinadh D <hdommaraju@vmware.com> 1.13.4-2
- Bump up version to compile with go 1.13.3-2
* Tue Feb 25 2020 Michelle Wang <michellew@vmware.com> 1.13.4-1
- Bump up version to 1.13.4
* Tue Oct 22 2019 Ashwin H <ashwinh@vmware.com> 1.10.0-3
- Bump up version to compile with go 1.13.3
* Fri Aug 30 2019 Ashwin H <ashwinh@vmware.com> 1.10.0-2
- Bump up version to compile with new go
* Thu Mar 14 2019 Keerthana K <keerthanak@vmware.com> 1.10.0-1
- Update to version 1.10.0
* Fri Sep 07 2018 Michelle Wang <michellew@vmware.com> 1.7.4-1
- Update version to 1.7.4 and its plugin version to 1.4.0.
* Mon Sep 18 2017 Alexey Makhalov <amakhalov@vmware.com> 1.3.4-2
- Remove shadow from requires and use explicit tools for post actions
* Tue Jul 18 2017 Dheeraj Shetty <dheerajs@vmware.com> 1.3.4-1
- first version
