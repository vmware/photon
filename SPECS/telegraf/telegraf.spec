%define debug_package   %{nil}
%define plugin_ver      1.4.0
%define golang_dep_ver  0.5.4

Summary:          agent for collecting, processing, aggregating, and writing metrics.
Name:             telegraf
Version:          1.28.1
Release:          6%{?dist}
License:          MIT
URL:              https://github.com/influxdata/telegraf
Group:            Development/Tools
Vendor:           VMware, Inc.
Distribution:     Photon

Source0: https://github.com/influxdata/telegraf/archive/%{name}-%{version}.tar.gz
%define sha512 %{name}=ab5d84ed665c16e90fa0a5c97cc4e34580f6f2079007328cba9c0b579245e0dbdae712e5d4079221d7b1bbaf674ae2994b68a37567ea5f9a6600787a31ab0082

Source1: https://github.com/wavefrontHQ/telegraf/archive/%{name}-plugin-%{plugin_ver}.zip
%define sha512 %{name}-plugin=3f49e403a92da5e45eaab7e9683c2f36e1143036db59e167568bec348499af6b7cc2b37135a37f6ebaf4be63bee25cf7859b6f164c6ed3064ad786a55111bfcc

Source2: %{name}.conf

Source3: golang-dep-%{golang_dep_ver}.tar.gz
%define sha512 golang-dep-%{golang_dep_ver}=b7657447c13a34d44bce47a0e0e4a3e7471efd7dffbbc18366d941302c561995ef1f2b58f92a46ed7e3d86322627964637772aab5216d334ad53fba94c1e241b

BuildRequires:    go
BuildRequires:    git
BuildRequires:    systemd-devel
BuildRequires:    unzip

Requires:         systemd
Requires:         logrotate
Requires(pre):    /usr/sbin/useradd /usr/sbin/groupadd

%description
Telegraf is an agent written in Go for collecting, processing, aggregating, and writing metrics.
Design goals are to have a minimal memory footprint with a plugin system so that developers in
the community can easily add support for collecting metrics from well known services (like Hadoop,
Postgres, or Redis) and third party APIs (like Mailchimp, AWS CloudWatch, or Google Analytics).

%prep
%autosetup -p1 -cn srcs -a0 -a3 -b1

mkdir -p ${GOPATH}/src/github.com/golang/ \
         ${GOPATH}/src/github.com/influxdata/ \
         ${GOPATH}/src/github.com/wavefronthq/%{name}/

mv dep-%{golang_dep_ver} ${GOPATH}/src/github.com/golang/dep
mv %{name}-%{version} ${GOPATH}/src/github.com/influxdata/%{name}
mv ../%{name}-%{plugin_ver}/* ${GOPATH}/src/github.com/wavefronthq/%{name}/

%build
pushd ${GOPATH}/src/github.com/golang/dep
CGO_ENABLED=0 GOOS=linux GO111MODULE=auto \
    go build -v -ldflags "-s -w" -o ${GOPATH}/bin/dep ./cmd/dep/
popd

pushd ${GOPATH}/src/github.com/influxdata/%{name}
# make doesn't support _smp_mflags
make
popd

%install
install -m 755 -D ${GOPATH}/src/github.com/influxdata/%{name}/%{name} \
    %{buildroot}%{_bindir}/%{name}

install -m 755 -D ${GOPATH}/src/github.com/influxdata/%{name}/scripts/%{name}.service \
    %{buildroot}%{_unitdir}/%{name}.service

install -m 755 -D ${GOPATH}/src/github.com/influxdata/%{name}/etc/logrotate.d/%{name} \
    %{buildroot}%{_sysconfdir}/logrotate.d/%{name}

install -m 640 -D %{SOURCE2} %{buildroot}%{_sysconfdir}/%{name}/%{name}.conf

mkdir -p %{buildroot}%{_sharedstatedir}/%{name}

%clean
rm -rf %{buildroot}/*

%pre
getent group %{name} >/dev/null || groupadd -r %{name}

getent passwd %{name} >/dev/null || \
  useradd -c "Telegraf" -d %{_sharedstatedir}/%{name} -g %{name} -s /sbin/nologin -M -r %{name}

%post
chown -R root:%{name} %{_sharedstatedir}/%{name}
chmod 0770 %{_sharedstatedir}/%{name}
chown -R %{name}:%{name} %{_sysconfdir}/%{name}
%systemd_post %{name}.service
systemctl daemon-reload

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun_with_restart %{name}.service

%files
%defattr(-,root,root)
%{_bindir}/%{name}
%{_unitdir}/%{name}.service
%{_sysconfdir}/logrotate.d/%{name}
%{_sharedstatedir}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/%{name}.conf

%changelog
* Fri Jul 12 2024 Mukul Sikka <mukul.sikka@broadcom.com> 1.28.1-6
- Bump version as a part of go upgrade
* Thu Jun 20 2024 Mukul Sikka <msikka@vmware.com> 1.28.1-5
- Bump version as a part of go upgrade
* Thu Apr 18 2024 Mukul Sikka <msikka@vmware.com> 1.28.1-4
- Bump version as a part of go upgrade
* Tue Nov 21 2023 Piyush Gupta <gpiyush@vmware.com> 1.28.1-3
- Bump up version to compile with new go
* Wed Oct 11 2023 Piyush Gupta <gpiyush@vmware.com> 1.28.1-2
- Bump up version to compile with new go
* Wed Oct 11 2023 Shreenidhi Shedi <sshedi@vmware.com> 1.28.1-1
- Upgrade telegraf to v1.28.1, fixes some second level CVEs
- Home directory should be owned by telegraf user
* Fri Aug 18 2023 Piyush Gupta <gpiyush@vmware.com> 1.27.1-2
- Bump up version to compile with new go
* Tue Jun 27 2023 Prashant S Chauhan <psinghchauha@vmware.com> 1.27.1-1
- Update to 1.27.1, Fixes second level CVEs
* Tue Jun 20 2023 Piyush Gupta <gpiyush@vmware.com> 1.25.2-4
- Bump up version to compile with new go
* Wed May 03 2023 Piyush Gupta <gpiyush@vmware.com> 1.25.2-3
- Bump up version to compile with new go
* Thu Mar 16 2023 Piyush Gupta <gpiyush@vmware.com> 1.25.2-2
- Bump up version to compile with new go
* Tue Feb 21 2023 Prashant S Chauhan <psinghchauha@vmware.com> 1.25.2-1
- Update to 1.25.2
* Tue Dec 20 2022 Piyush Gupta <gpiyush@vmware.com> 1.15.3-16
- Bump up version to compile with new go
* Sun Nov 13 2022 Piyush Gupta <gpiyush@vmware.com> 1.15.3-15
- Bump up version to compile with new go
* Wed Oct 26 2022 Piyush Gupta <gpiyush@vmware.com> 1.15.3-14
- Bump up version to compile with new go
* Thu Sep 15 2022 Piyush Gupta <gpiyush@vmware.com> 1.15.3-13
- Bump up version to compile with new go
* Fri Aug 19 2022 Piyush Gupta <gpiyush@vmware.com> 1.15.3-12
- Bump up version to compile with new go
* Tue Jul 12 2022 Piyush Gupta <gpiyush@vmware.com> 1.15.3-11
- Bump up version to compile with new go
* Sat May 07 2022 Piyush Gupta <gpiyush@vmware.com> 1.15.3-10
- Bump up version to compile with new go
* Tue Feb 22 2022 Piyush Gupta <gpiyush@vmware.com> 1.15.3-9
- Bump up version to compile with new go
* Mon Jan 24 2022 Piyush Gupta <gpiyush@vmware.com> 1.15.3-8
- Bump up version to compile with new go
* Wed Oct 20 2021 Piyush Gupta <gpiyush@vmware.com> 1.15.3-7
- Bump up version to compile with new go
* Tue Oct 05 2021 Piyush Gupta <gpiyush@vmware.com> 1.15.3-6
- Bump up version to compile with new go
* Fri Jun 11 2021 Piyush Gupta <gpiyush@vmware.com> 1.15.3-5
- Bump up version to compile with new go
* Thu Mar 25 2021 Piyush Gupta<gpiyush@vmware.com> 1.15.3-4
- Bump up version to compile with new go
* Fri Feb 05 2021 Harinadh D <hdommaraju@vmware.com> 1.15.3-3
- Bump up version to compile with new go
* Fri Jan 15 2021 Piyush Gupta<gpiyush@vmware.com> 1.15.3-2
- Bump up version to compile with new go
* Mon Sep 21 2020 Gerrit Photon <photon-checkins@vmware.com> 1.15.3-1
- Automatic Version Bump
* Mon Jul 27 2020 Gerrit Photon <photon-checkins@vmware.com> 1.15.2-1
- Automatic Version Bump
* Thu Jul 09 2020 Gerrit Photon <photon-checkins@vmware.com> 1.14.5-1
- Automatic Version Bump
* Fri Sep 07 2018 Michelle Wang <michellew@vmware.com> 1.7.4-1
- Update version to 1.7.4 and its plugin version to 1.4.0.
* Mon Sep 18 2017 Alexey Makhalov <amakhalov@vmware.com> 1.3.4-2
- Remove shadow from requires and use explicit tools for post actions
* Tue Jul 18 2017 Dheeraj Shetty <dheerajs@vmware.com> 1.3.4-1
- first version
