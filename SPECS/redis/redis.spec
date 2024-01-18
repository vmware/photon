Summary:       advanced key-value store
Name:          redis
Version:       7.0.15
Release:       1%{?dist}
License:       BSD
URL:           http://redis.io
Group:         Applications/Databases
Vendor:        VMware, Inc.
Distribution:  Photon

Source0: https://github.com/redis/redis/archive/refs/tags/%{name}-%{version}.tar.gz
%define sha512 %{name}=572c6b604bed18000168cbfdc516550d78ff37dcc51c9139e73981dfe71386681555a2c853b6ad8f3e1d2ad8d8116c0ba338e772f87fe087bc986363a4828e9d

Patch0: %{name}-conf.patch

BuildRequires: build-essential
BuildRequires: systemd-devel
BuildRequires: systemd-rpm-macros
BuildRequires: tcl-devel
BuildRequires: which

Requires: systemd
Requires(pre): /usr/sbin/useradd /usr/sbin/groupadd

%description
Redis is an in-memory data structure store, used as database, cache and message broker.

%prep
%autosetup -p1

%build
# %%make_build gets stuck for some unknown reason
make %{?_smp_mflags} BUILD_TLS=yes

%install
%make_install PREFIX=%{buildroot}%{_usr} %{?_smp_mflags}
install -D -m 0640 %{name}.conf %{buildroot}%{_sysconfdir}/%{name}.conf

mkdir -p %{buildroot}%{_sharedstatedir}/%{name} \
         %{buildroot}%{_var}/log \
         %{buildroot}%{_var}/opt/%{name}/log \
         %{buildroot}%{_unitdir}

ln -sfv %{_var}/opt/%{name}/log %{buildroot}%{_var}/log/%{name}

cat << EOF >> %{buildroot}%{_unitdir}/%{name}.service
[Unit]
Description=Redis in-memory key-value database
After=network.target

[Service]
ExecStart=%{_bindir}/%{name}-server %{_sysconfdir}/%{name}.conf --daemonize no
ExecStop=%{_bindir}/%{name}-cli shutdown
User=%{name}
Group=%{name}

[Install]
WantedBy=multi-user.target
EOF

%if 0%{?with_check}
%check
make check %{?_smp_mflags}
%endif

%pre
getent group %{name} &> /dev/null || groupadd -r %{name} &> /dev/null

getent passwd %{name} &> /dev/null || \
useradd -r -g %{name} -d %{_sharedstatedir}/%{name} -s /sbin/nologin \
    -c 'Redis Database Server' %{name} &> /dev/null

%post
/sbin/ldconfig
%systemd_post %{name}.service

%postun
/sbin/ldconfig
%systemd_postun_with_restart %{name}.service

%files
%defattr(-,root,root)
%dir %attr(0750, %{name}, %{name}) %{_sharedstatedir}/%{name}
%dir %attr(0750, %{name}, %{name}) %{_var}/opt/%{name}/log
%attr(0750, %{name}, %{name}) %{_var}/log/%{name}
%{_bindir}/*
%{_unitdir}/*
%config(noreplace) %attr(0640, %{name}, %{name}) %{_sysconfdir}/%{name}.conf

%changelog
* Thu Jan 18 2024 Nitesh Kumar <nitesh-nk.kumar@broadcom.com> 7.0.15-1
- Version upgrade to v7.0.15 to fix CVE-2023-41056
* Wed Oct 25 2023 Shreenidhi Shedi <sshedi@vmware.com> 7.0.14-1
- Upgrade to v7.0.14
* Mon Sep 11 2023 Nitesh Kumar <kunitesh@vmware.com> 7.0.12-2
- Patched for CVE-2023-41053
* Thu Jul 13 2023 Nitesh Kumar <kunitesh@vmware.com> 7.0.12-1
- Upgrade to v7.0.12 to fix following CVE's:
- CVE-2022-24834, CVE-2023-36824
* Thu Apr 20 2023 Shreenidhi Shedi <sshedi@vmware.com> 7.0.0-8
- Fix CVE-2023-28856
* Thu Mar 09 2023 Shreenidhi Shedi <sshedi@vmware.com> 7.0.0-7
- Fix CVE-2023-25155, CVE-2022-36021
* Mon Feb 06 2023 Shreenidhi Shedi <sshedi@vmware.com> 7.0.0-6
- Fix CVE-2023-22458, CVE-2022-35977
* Fri Oct 28 2022 Shreenidhi Shedi <sshedi@vmware.com> 7.0.0-5
- Fix CVE-2022-3647
* Wed Sep 28 2022 Shreenidhi Shedi <sshedi@vmware.com> 7.0.0-4
- Fix CVE-2022-35951
* Wed Jul 27 2022 Shreenidhi Shedi <sshedi@vmware.com> 7.0.0-3
- Fix CVE-2022-31144
* Sat Jul 02 2022 Shreenidhi Shedi <sshedi@vmware.com> 7.0.0-2
- Fix CVE-2022-33105
* Wed May 11 2022 Shreenidhi Shedi <sshedi@vmware.com> 7.0.0-1
- Upgrade to v7.0.0
- This fixes CVE-2022-24735, CVE-2022-24736
* Wed Dec 01 2021 Satya Naga Vasamsetty <svasamsetty@vmware.com> 6.0.16-2
- Bump up to fix downgrading issue
* Thu Oct 21 2021 Nitesh Kumar <kunitesh@vmware.com> 6.0.16-1
- Upgrade to v6.0.16 to fix following CVE's:
- 2021-32672, 2021-41099, 2021-32762, 2021-32687
- 2021-32675, 2021-32628, 2021-32627 and 2021-32626
* Wed Oct 13 2021 Nitesh Kumar <kunitesh@vmware.com> 6.0.15-3
- Fix for CVE-2021-32672
* Thu Sep 23 2021 Shreyas B. <shreyasb@vmware.com> 6.0.15-2
- Build with TLS
* Sat Aug 07 2021 Shreyas B <shreyasb@vmware.com> 6.0.15-1
- Upgrade to v6.0.15 to address CVE-2021-32761
* Mon Jun 21 2021 Shreyas B <shreyasb@vmware.com> 6.0.14-1
- Upgrade to v6.0.14 to address CVE-2021-32625
* Mon May 24 2021 Shreyas B <shreyasb@vmware.com> 6.0.13-1
- Upgrade to v6.0.13 to address CVE-2021-29477
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
* Thu Dec 28 2017 Divya Thaluru <dthaluru@vmware.com> 3.2.8-5
- Fixed the log file directory structure
* Mon Sep 18 2017 Alexey Makhalov <amakhalov@vmware.com> 3.2.8-4
- Remove shadow from requires and use explicit tools for post actions
* Wed May 31 2017 Siju Maliakkal <smaliakkal@vmware.com> 3.2.8-3
- Fix DB persistence,log file,grace-ful shutdown issues
* Tue May 16 2017 Siju Maliakkal <smaliakkal@vmware.com> 3.2.8-2
- Added systemd service unit
* Wed Apr 5 2017 Siju Maliakkal <smaliakkal@vmware.com> 3.2.8-1
- Updating to latest version
* Mon Oct 3 2016 Dheeraj Shetty <dheerajs@vmware.com> 3.2.4-1
- initial version
