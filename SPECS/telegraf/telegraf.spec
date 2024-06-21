%define debug_package   %{nil}
%define plugin_ver      1.4.0

Summary:          agent for collecting, processing, aggregating, and writing metrics.
Name:             telegraf
Version:          1.28.1
Release:          4%{?dist}
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
Source3: %{name}.sysusers

Patch0: fix-compile-error.patch

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
%autosetup -p1 -b1

%build
mkdir -p ${GOPATH}/src/github.com/influxdata/%{name} \
         ${GOPATH}/src/github.com/wavefronthq/%{name}/plugins/outputs/wavefront

cp -r * ${GOPATH}/src/github.com/influxdata/%{name}
rm -rf ./*

pushd ../%{name}-%{plugin_ver}
cp -r * ${GOPATH}/src/github.com/wavefronthq/%{name}/
popd
rm -rf ../%{name}-%{plugin_ver}

pushd ${GOPATH}/src/github.com/influxdata/%{name}
%make_build
popd

%install
install -m 755 -D ${GOPATH}/src/github.com/influxdata/%{name}/%{name} \
    %{buildroot}%{_bindir}/%{name}

install -m 755 -D ${GOPATH}/src/github.com/influxdata/%{name}/scripts/%{name}.service \
    %{buildroot}%{_unitdir}/%{name}.service

install -m 755 -D ${GOPATH}/src/github.com/influxdata/%{name}/etc/logrotate.d/%{name} \
    %{buildroot}%{_sysconfdir}/logrotate.d/%{name}

install -m 640 -D %{SOURCE2} %{buildroot}%{_sysconfdir}/%{name}/%{name}.conf

install -p -D -m 0644 %{SOURCE3} %{buildroot}%{_sysusersdir}/%{name}.sysusers

mkdir -p %{buildroot}%{_sharedstatedir}/%{name}

%clean
rm -rf %{buildroot}/*

%pre
%sysusers_create_compat %{SOURCE3}

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
%{_sysusersdir}/%{name}.sysusers
%config(noreplace) %{_sysconfdir}/%{name}/%{name}.conf

%changelog
* Thu Jun 20 2024 Mukul Sikka <msikka@vmware.com> 1.28.1-4
- Bump version as a part of go upgrade
* Thu Feb 22 2024 Mukul Sikka <msikka@vmware.com> 1.28.1-3
- Bump version as a part of go upgrade
* Tue Nov 21 2023 Piyush Gupta <gpiyush@vmware.com> 1.28.1-2
- Bump up version to compile with new go
* Tue Oct 17 2023 Shreenidhi Shedi <sshedi@vmware.com> 1.28.1-1
- Upgrade to v1.28.1
- Change homedir ownership
* Wed Oct 11 2023 Piyush Gupta <gpiyush@vmware.com> 1.27.1-5
- Bump up version to compile with new go
* Mon Sep 18 2023 Piyush Gupta <gpiyush@vmware.com> 1.27.1-4
- Bump up version to compile with new go
* Tue Aug 08 2023 Mukul Sikka <msikka@vmware.com> 1.27.1-3
- Resolving systemd-rpm-macros for group creation
* Mon Jul 17 2023 Piyush Gupta <gpiyush@vmware.com> 1.27.1-2
- Bump up version to compile with new go
* Tue Jun 27 2023 Prashant S Chauhan <psinghchauha@vmware.com> 1.27.1-1
- Update to 1.27.1, Fixes second level CVEs
* Thu Jun 22 2023 Piyush Gupta <gpiyush@vmware.com> 1.18.2-9
- Bump up version to compile with new go
* Wed May 03 2023 Piyush Gupta <gpiyush@vmware.com> 1.18.2-8
- Bump up version to compile with new go
* Fri Mar 10 2023 Mukul Sikka <msikka@vmware.com> 1.18.2-7
- Use systemd-rpm-macros for user creation
* Thu Mar 09 2023 Piyush Gupta <gpiyush@vmware.com> 1.18.2-6
- Bump up version to compile with new go
* Mon Nov 21 2022 Piyush Gupta <gpiyush@vmware.com> 1.18.2-5
- Bump up version to compile with new go
* Wed Oct 26 2022 Piyush Gupta <gpiyush@vmware.com> 1.18.2-4
- Bump up version to compile with new go
* Fri Jun 17 2022 Piyush Gupta <gpiyush@vmware.com> 1.18.2-3
- Bump up version to compile with new go
* Fri Jun 11 2021 Piyush Gupta <gpiyush@vmware.com> 1.18.2-2
- Bump up version to compile with new go
* Tue Apr 13 2021 Gerrit Photon <photon-checkins@vmware.com> 1.18.2-1
- Automatic Version Bump
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
