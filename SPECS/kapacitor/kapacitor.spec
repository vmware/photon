Name:           kapacitor
Version:        1.5.0
Release:        29%{?dist}
Summary:        Open source framework for processing, monitoring, and alerting on time series data
License:        MIT
URL:            https://www.influxdata.com/time-series-platform/kapacitor
Source0:        https://github.com/influxdata/kapacitor/archive/%{name}-%{version}.tar.gz
%define sha512  %{name}=b17e03735a01a5e2c454f70793bb55bb915fc604e8541e7fa8ec52f02c2977695e72a7c2c0391314576267c5fbe202f4e70fadb33c3ab043e1ada76f5c85d3c6
Vendor:         VMware, Inc.
Distribution:   Photon
Group:          System/Monitoring
BuildRequires:  go
BuildRequires:  systemd
Requires:       systemd
Requires(pre):      /usr/sbin/useradd /usr/sbin/groupadd
Requires(postun):   /usr/sbin/userdel /usr/sbin/groupdel

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
eu-elfcompress -q -p -t none %{buildroot}%{_bindir}/*

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
* Tue Nov 21 2023 Piyush Gupta <gpiyush@vmware.com> 1.5.0-29
- Bump up version to compile with new go
* Wed Oct 11 2023 Piyush Gupta <gpiyush@vmware.com> 1.5.0-28
- Bump up version to compile with new go
* Tue Sep 26 2023 Piyush Gupta <gpiyush@vmware.com> 1.5.0-27
- Bump up version to compile with new go
* Fri Aug 18 2023 Piyush Gupta <gpiyush@vmware.com> 1.5.0-26
- Bump up version to compile with new go
* Thu Jun 22 2023 Piyush Gupta <gpiyush@vmware.com> 1.5.0-25
- Bump up version to compile with new go
* Wed May 03 2023 Piyush Gupta <gpiyush@vmware.com> 1.5.0-24
- Bump up version to compile with new go
* Tue Apr 04 2023 Piyush Gupta <gpiyush@vmware.com> 1.5.0-23
- Bump up version to compile with new go
* Tue Dec 20 2022 Piyush Gupta <gpiyush@vmware.com> 1.5.0-22
- Bump up version to compile with new go
* Sun Nov 13 2022 Piyush Gupta <gpiyush@vmware.com> 1.5.0-21
- Bump up version to compile with new go
* Wed Oct 26 2022 Piyush Gupta <gpiyush@vmware.com> 1.5.0-20
- Bump up version to compile with new go
* Thu Sep 15 2022 Piyush Gupta <gpiyush@vmware.com> 1.5.0-19
- Bump up version to compile with new go
* Thu Aug 18 2022 Piyush Gupta <gpiyush@vmware.com> 1.5.0-18
- Bump up version to compile with new go
* Mon May 09 2022 Piyush Gupta <gpiyush@vmware.com> 1.5.0-17
- Bump up version to compile with new go
* Fri Apr 08 2022 Prashant S Chauhan <psinghchauha@vmware.com> 1.5.0-16
- Add useradd,groupadd etc in requires to fix installation failure
* Wed Mar 16 2022 Piyush Gupta <gpiyush@vmware.com> 1.5.0-15
- Bump up version to compile with new go
* Tue Feb 22 2022 Piyush Gupta <gpiyush@vmware.com> 1.5.0-14
- Bump up version to compile with new go
* Mon Jan 24 2022 Piyush Gupta <gpiyush@vmware.com> 1.5.0-13
- Bump up version to compile with new go
* Tue Nov 16 2021 Piyush Gupta <gpiyush@vmware.com> 1.5.0-12
- Bump up version to compile with new go
* Wed Oct 20 2021 Piyush Gupta <gpiyush@vmware.com> 1.5.0-11
- Bump up version to compile with new go
* Sat Aug 21 2021 Piyush Gupta<gpiyush@vmware.com> 1.5.0-10
- Bump up version to compile with new go
* Tue Jun 29 2021 Piyush Gupta <gpiyush@vmware.com> 1.5.0-9
- Bump up version to compile with new go
* Mon May 03 2021 Piyush Gupta<gpiyush@vmware.com> 1.5.0-8
- Bump up version to compile with new go
* Mon Feb 08 2021 Harinadh D <hdommaraju@vmware.com> 1.5.0-7
- Bump up version to compile with new go
* Fri Nov 27 2020 HarinadhD <hdommaraju@vmware.com> 1.5.0-6
- Bump up version to compile with new go
* Tue Aug 18 2020 Ashwin H <ashwinh@vmware.com> 1.5.0-5
- Bump up version to compile with new go
* Fri Apr 10 2020 Harinadh D <hdommaraju@vmware.com> 1.5.0-4
- Bump up version to compile with go 1.13.3-2
* Tue Oct 22 2019 Ashwin H <ashwinh@vmware.com> 1.5.0-3
- Bump up version to compile with go 1.13.3
* Fri Aug 30 2019 Ashwin H <ashwinh@vmware.com> 1.5.0-2
- Bump up version to compile with new go
* Fri Aug 03 2018 Keerthana K <keerthanak@vmware.com> 1.5.0-1
- Initial kapacitor package for Photon.
