Name:           kapacitor
Version:        1.5.6
Release:        23%{?dist}
Summary:        Open source framework for processing, monitoring, and alerting on time series data
License:        MIT
URL:            https://www.influxdata.com/time-series-platform/kapacitor
Source0:        https://github.com/influxdata/kapacitor/archive/%{name}-%{version}.tar.gz
%define sha512  %{name}=542e5f03422b5491f16b47394aa15762bcd4a8c5357ce1a009f7c9d10761245b1f77b3ebeeb562a88a39d72a30ba58dee2a9cb6378e9193b676a3b4fa3ea6e25
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
export GOPATH=`pwd`
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
* Thu Apr 18 2024 Mukul Sikka <msikka@vmware.com> 1.5.6-23
- Bump version as a part of go upgrade
* Tue Nov 21 2023 Piyush Gupta <gpiyush@vmware.com> 1.5.6-22
- Bump up version to compile with new go
* Wed Oct 11 2023 Piyush Gupta <gpiyush@vmware.com> 1.5.6-21
- Bump up version to compile with new go
* Fri Aug 18 2023 Piyush Gupta <gpiyush@vmware.com> 1.5.6-20
- Bump up version to compile with new go
* Tue Jun 20 2023 Piyush Gupta <gpiyush@vmware.com> 1.5.6-19
- Bump up version to compile with new go
* Wed May 03 2023 Piyush Gupta <gpiyush@vmware.com> 1.5.6-18
- Bump up version to compile with new go
* Thu Mar 16 2023 Piyush Gupta <gpiyush@vmware.com> 1.5.6-17
- Bump up version to compile with new go
* Tue Dec 20 2022 Piyush Gupta <gpiyush@vmware.com> 1.5.6-16
- Bump up version to compile with new go
* Sun Nov 13 2022 Piyush Gupta <gpiyush@vmware.com> 1.5.6-15
- Bump up version to compile with new go
* Wed Oct 26 2022 Piyush Gupta <gpiyush@vmware.com> 1.5.6-14
- Bump up version to compile with new go
* Thu Sep 15 2022 Piyush Gupta <gpiyush@vmware.com> 1.5.6-13
- Bump up version to compile with new go
* Fri Aug 19 2022 Piyush Gupta <gpiyush@vmware.com> 1.5.6-12
- Bump up version to compile with new go
* Tue Jul 12 2022 Piyush Gupta <gpiyush@vmware.com> 1.5.6-11
- Bump up version to compile with new go
*   Sat May 07 2022 Piyush Gupta <gpiyush@vmware.com> 1.5.6-10
-   Bump up version to compile with new go
*   Tue Feb 22 2022 Piyush Gupta <gpiyush@vmware.com> 1.5.6-9
-   Bump up version to compile with new go
*   Mon Jan 24 2022 Piyush Gupta <gpiyush@vmware.com> 1.5.6-8
-   Bump up version to compile with new go
*   Wed Oct 20 2021 Piyush Gupta <gpiyush@vmware.com> 1.5.6-7
-   Bump up version to compile with new go
*   Tue Oct 05 2021 Piyush Gupta <gpiyush@vmware.com> 1.5.6-6
-   Bump up version to compile with new go
*   Fri Jun 11 2021 Piyush Gupta <gpiyush@vmware.com> 1.5.6-5
-   Bump up version to compile with new go
*   Thu Mar 25 2021 Piyush Gupta<gpiyush@vmware.com> 1.5.6-4
-   Bump up version to compile with new go
*   Fri Feb 05 2021 Harinadh D <hdommaraju@vmware.com> 1.5.6-3
-   Bump up version to compile with new go
*   Fri Jan 15 2021 Piyush Gupta<gpiyush@vmware.com> 1.5.6-2
-   Bump up version to compile with new go
*   Wed Jul 22 2020 Gerrit Photon <photon-checkins@vmware.com> 1.5.6-1
-   Automatic Version Bump
*   Fri Aug 03 2018 Keerthana K <keerthanak@vmware.com> 1.5.0-1
-   Initial kapacitor package for Photon.
