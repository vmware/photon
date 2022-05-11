Summary:    advanced key-value store
Name:       redis
Version:    7.0.0
Release:    1%{?dist}
License:    BSD
URL:        http://redis.io
Group:      Applications/Databases
Vendor:     VMware, Inc.
Distribution:   Photon

Source0:    http://download.redis.io/releases/%{name}-%{version}.tar.gz
%define sha512 %{name}=9209dd95511a27802f83197b037c006c5f40c50fe5315eb6a5ac2af1619a7b1c890160106157086420c1aca8a058f573681bfad1897052308ca6e64407404757

Patch0:         redis-conf.patch

BuildRequires:  gcc
BuildRequires:  systemd-devel
BuildRequires:  systemd-rpm-macros
BuildRequires:  make
BuildRequires:  which
BuildRequires:  tcl
BuildRequires:  tcl-devel

Requires:   systemd
Requires(pre):  /usr/sbin/useradd /usr/sbin/groupadd

%description
Redis is an in-memory data structure store, used as database, cache and message broker.

%prep
%autosetup -p1

%build
make BUILD_TLS=yes %{?_smp_mflags}

%install
install -vdm 755 %{buildroot}
make PREFIX=%{buildroot}%{_usr} install %{?_smp_mflags}
install -D -m 0640 %{name}.conf %{buildroot}%{_sysconfdir}/%{name}.conf

mkdir -p %{buildroot}%{_sharedstatedir}/%{name} \
          %{buildroot}/var/log \
          %{buildroot}/var/opt/%{name}/log \
          %{buildroot}%{_unitdir}

ln -sfv /var/opt/%{name}/log %{buildroot}/var/log/%{name}

cat << EOF >>  %{buildroot}%{_unitdir}/redis.service
[Unit]
Description=Redis in-memory key-value database
After=network.target

[Service]
ExecStart=%{_bindir}/redis-server %{_sysconfdir}/redis.conf --daemonize no
ExecStop=%{_bindir}/redis-cli shutdown
User=redis
Group=redis

[Install]
WantedBy=multi-user.target
EOF

%check
%if 0%{?with_check}
make check %{?_smp_mflags}
%endif

%pre
getent group %{name} &> /dev/null || groupadd -r %{name} &> /dev/null

getent passwd %{name} &> /dev/null || \
useradd -r -g %{name} -d %{_sharedstatedir}/%{name} -s /sbin/nologin \
-c 'Redis Database Server' %{name} &> /dev/null

%post
/sbin/ldconfig
%systemd_post  redis.service

%postun
/sbin/ldconfig
%systemd_postun_with_restart redis.service

%files
%defattr(-,root,root)
%dir %attr(0750, redis, redis) /var/lib/redis
%dir %attr(0750, redis, redis) /var/opt/%{name}/log
%attr(0750, redis, redis) %{_var}/log/%{name}
%{_bindir}/*
%{_libdir}/systemd/*
%config(noreplace) %attr(0640, %{name}, %{name}) %{_sysconfdir}/redis.conf

%changelog
* Wed May 11 2022 Shreenidhi Shedi <sshedi@vmware.com> 7.0.0-1
- Upgrade to v7.0.0
- This fixes CVE-2022-24735, CVE-2022-24736
* Thu Oct 21 2021 Nitesh Kumar <kunitesh@vmware.com> 6.2.6-1
- Upgrade to v6.2.6 to fix following CVE's:
- 2021-32672, 2021-41099, 2021-32762, 2021-32687
- 2021-32675, 2021-32628, 2021-32627 and 2021-32626.
* Wed Oct 13 2021 Nitesh Kumar <kunitesh@vmware.com> 6.2.5-3
- Fix for CVE-2021-32672
* Thu Sep 23 2021 Shreyas B. <shreyasb@vmware.com> 6.2.5-2
- Build with TLS
* Wed Aug 11 2021 Shreyas B <shreyasb@vmware.com> 6.2.5-1
- Upgrade to v6.2.5 to address CVE-2021-32761
* Mon May 24 2021 Shreyas B <shreyasb@vmware.com> 6.2.3-1
- Upgrade to v6.2.3 to address CVE-2021-29477
* Tue Apr 13 2021 Gerrit Photon <photon-checkins@vmware.com> 6.2.2-1
- Automatic Version Bump
* Thu Apr 08 2021 Shreyas B <shreyasb@vmware.com> 6.0.9-1
- Upgrade to v6.0.9 to address CVE-2021-3470
* Thu Sep 10 2020 Gerrit Photon <photon-checkins@vmware.com> 6.0.8-1
- Automatic Version Bump
* Tue Sep 01 2020 Gerrit Photon <photon-checkins@vmware.com> 6.0.7-1
- Automatic Version Bump
* Mon Jul 27 2020 Gerrit Photon <photon-checkins@vmware.com> 6.0.6-1
- Automatic Version Bump
* Wed Jul 08 2020 Gerrit Photon <photon-checkins@vmware.com> 6.0.5-1
- Automatic Version Bump
* Wed Jun 24 2020 Shreyas B <shreyasb@vmware.com> 5.0.5-2
- Fix for CVE-2020-14147
* Mon Jul 22 2019 Shreyas B. <shreyasb@vmware.com> 5.0.5-1
- Updated to version 5.0.5.
* Tue Sep 11 2018 Keerthana K <keerthanak@vmware.com> 4.0.11-1
- Updated to version 4.0.11.
* Thu Dec 28 2017 Divya Thaluru <dthaluru@vmware.com>  3.2.8-5
- Fixed the log file directory structure
* Mon Sep 18 2017 Alexey Makhalov <amakhalov@vmware.com> 3.2.8-4
- Remove shadow from requires and use explicit tools for post actions
* Wed May 31 2017 Siju Maliakkal <smaliakkal@vmware.com> 3.2.8-3
- Fix DB persistence,log file,grace-ful shutdown issues
* Tue May 02 2017 Siju Maliakkal <smaliakkal@vmware.com> 3.2.8-2
- Added systemd service unit
* Wed Apr 5 2017 Siju Maliakkal <smaliakkal@vmware.com> 3.2.8-1
- Updating to latest version
* Mon Oct 3 2016 Dheeraj Shetty <dheerajs@vmware.com> 3.2.4-1
- initial version
