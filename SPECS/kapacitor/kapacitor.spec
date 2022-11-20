Name:           kapacitor
Version:        1.5.9
Release:        5%{?dist}
Summary:        Open source framework for processing, monitoring, and alerting on time series data
License:        MIT
URL:            https://www.influxdata.com/time-series-platform/kapacitor
Source0:        https://github.com/influxdata/kapacitor/archive/%{name}-%{version}.tar.gz
%define sha512  %{name}=948d5a2a495ff05c10ca3a2a57dcdddba633579b096dc520e8575e0da46f0d5c0e6f961c9f97e6d1bce7dc695c178e4b9e04b201cec70db913943f601445bbcd
Vendor:         VMware, Inc.
Distribution:   Photon
Group:          System/Monitoring
BuildRequires:  go
BuildRequires:  systemd
Requires:       systemd

%description
Kapacitor is an Open source framework for processing, monitoring, and alerting on time series data.

%prep
%autosetup -n %{name}-%{version}

%build
go env -w GO111MODULE=auto
cd ..
mkdir -p build/src/github.com/influxdata/kapacitor
mv %{name}-%{version}/* build/src/github.com/influxdata/%{name}
cd build
export GOPATH=$PWD
cd src/github.com/influxdata/kapacitor
go build ./cmd/kapacitor
go build ./cmd/kapacitord
go build ./tick/cmd/tickfmt

%install
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_libdir}/systemd/system
mkdir -p %{buildroot}%{_sharedstatedir}/kapacitor
mkdir -p %{buildroot}%{_localstatedir}/log/kapacitor
mkdir -p %{buildroot}%{_datadir}/bash-completion/completions
mkdir -p %{buildroot}%{_sysconfdir}/logrotate.d
mkdir -p %{buildroot}%{_sysconfdir}/kapacitor
cd ../build/src/github.com/influxdata/kapacitor
cp -r kapacitor %{buildroot}%{_bindir}
cp -r kapacitord %{buildroot}%{_bindir}
cp -r tickfmt %{buildroot}%{_bindir}
cp -r usr/share/bash-completion/completions/kapacitor %{buildroot}%{_datadir}/bash-completion/completions/
cp -r scripts/kapacitor.service %{buildroot}%{_libdir}/systemd/system/
cp -r etc/logrotate.d/kapacitor %{buildroot}%{_sysconfdir}/logrotate.d/
cp -r etc/kapacitor/kapacitor.conf %{buildroot}%{_sysconfdir}/kapacitor

%clean
rm -rf %{buildroot}/*

%pre
if [ $1 -eq 1 ]; then
    # Initial installation.
    getent group %{name} >/dev/null || groupadd -r %{name}
    getent passwd %{name} >/dev/null || useradd -r -g %{name} -d /var/lib/%{name} -s /sbin/nologin \
            -c "Kapacitor" %{name}
fi

%post
chown -R %{name}:%{name} /var/lib/%{name}
chown -R %{name}:%{name} /var/log/%{name}
%systemd_post kapacitor.service

%preun
%systemd_preun kapacitor.service

%postun
%systemd_postun_with_restart kapacitor.service
if [ $1 -eq 0 ]; then
    # Package deletion
    userdel %{name}
    groupdel %{name}
fi

%files
%defattr(-,root,root,755)
%dir %config(noreplace) %{_sysconfdir}/kapacitor
%dir %{_sharedstatedir}/kapacitor
%dir %{_localstatedir}/log/kapacitor
%{_bindir}/kapacitor
%{_bindir}/kapacitord
%{_bindir}/tickfmt
%{_datadir}/bash-completion/completions/kapacitor
%{_libdir}/systemd/system/kapacitor.service
%config(noreplace) %{_sysconfdir}/logrotate.d/kapacitor
%config(noreplace) %{_sysconfdir}/kapacitor/kapacitor.conf

%changelog
* Mon Nov 21 2022 Piyush Gupta <gpiyush@vmware.com> 1.5.9-5
- Bump up version to compile with new go
* Wed Oct 26 2022 Piyush Gupta <gpiyush@vmware.com> 1.5.9-4
- Bump up version to compile with new go
*   Fri Jun 17 2022 Piyush Gupta <gpiyush@vmware.com> 1.5.9-3
-   Bump up version to compile with new go
*   Fri Jun 11 2021 Piyush Gupta <gpiyush@vmware.com> 1.5.9-2
-   Bump up version to compile with new go
*   Thu Apr 29 2021 Gerrit Photon <photon-checkins@vmware.com> 1.5.9-1
-   Automatic Version Bump
*   Fri Feb 05 2021 Harinadh D <hdommaraju@vmware.com> 1.5.6-3
-   Bump up version to compile with new go
*   Fri Jan 15 2021 Piyush Gupta<gpiyush@vmware.com> 1.5.6-2
-   Bump up version to compile with new go
*   Wed Jul 22 2020 Gerrit Photon <photon-checkins@vmware.com> 1.5.6-1
-   Automatic Version Bump
*   Fri Aug 03 2018 Keerthana K <keerthanak@vmware.com> 1.5.0-1
-   Initial kapacitor package for Photon.
