Summary:       advanced key-value store
Name:          redis
Version:       7.2.4
Release:       1%{?dist}
License:       BSD
URL:           http://redis.io
Group:         Applications/Databases
Vendor:        VMware, Inc.
Distribution:  Photon

Source0: https://github.com/redis/redis/archive/refs/tags/%{name}-%{version}.tar.gz
%define sha512 %{name}=d15ec5ccb610eded6d0c54f4a29fefaa1906e4db8479c3fa291d0a4474d3ed4795373e7fcb3d55dbb1ae840eac5ec50b56c0127054e406bca04ca71650f9fecd

Source1: %{name}.sysusers

Patch0: %{name}-conf.patch

BuildRequires: build-essential
BuildRequires: systemd-devel
BuildRequires: systemd-rpm-macros
BuildRequires: tcl-devel
BuildRequires: which

Requires: systemd
Requires: openssl
Requires(pre): systemd-rpm-macros
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
install -p -D -m 0644 %{SOURCE1} %{buildroot}%{_sysusersdir}/%{name}.sysusers

%check
%if 0%{?with_check}
make check %{?_smp_mflags}
%endif

%pre
%sysusers_create_compat %{SOURCE1}

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
%{_libdir}/systemd/*
%config(noreplace) %attr(0640, %{name}, %{name}) %{_sysconfdir}/%{name}.conf
%{_sysusersdir}/%{name}.sysusers

%changelog
* Thu Jan 18 2024 Nitesh Kumar <nitesh-nk.kumar@broadcom.com> 7.2.4-1
- Version upgrade to v7.2.4 to fix CVE-2023-41056
* Tue Dec 19 2023 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 7.2.3-1
- Upgrade to v7.2.3
* Wed Oct 25 2023 Shreenidhi Shedi <sshedi@vmware.com> 7.2.2-1
- Upgrade to v7.2.2
* Mon Sep 11 2023 Nitesh Kumar <kunitesh@vmware.com> 7.0.13-1
- Upgrade to v7.0.13 to fix CVE-2023-41053
* Tue Aug 08 2023 Mukul Sikka <msikka@vmware.com> 7.0.12-2
- Resolving systemd-rpm-macros for group creation
* Thu Jul 13 2023 Nitesh Kumar <kunitesh@vmware.com> 7.0.12-1
- Upgrade to v7.0.12 to fix following CVE's:
- CVE-2022-24834, CVE-2023-36824
* Thu Apr 20 2023 Shreenidhi Shedi <sshedi@vmware.com> 7.0.9-3
- Fix CVE-2023-28856
* Fri Mar 10 2023 Mukul Sikka <msikka@vmware.com> 7.0.9-2
- Use systemd-rpm-macros for user creation
* Thu Mar 09 2023 Shreenidhi Shedi <sshedi@vmware.com> 7.0.9-1
- Upgrade to v7.0.9
* Mon Feb 06 2023 Shreenidhi Shedi <sshedi@vmware.com> 7.0.8-1
- Upgrade to v7.0.8
* Fri Oct 28 2022 Shreenidhi Shedi <sshedi@vmware.com> 7.0.5-2
- Fix CVE-2022-3647
* Wed Sep 28 2022 Shreenidhi Shedi <sshedi@vmware.com> 7.0.5-1
- Upgrade to v7.0.5
- Fixes CVE-2022-35951
* Wed Jul 27 2022 Shreenidhi Shedi <sshedi@vmware.com> 7.0.4-1
- Upgrade to v7.0.4, this also fixes CVE-2022-31144
* Sat Jul 02 2022 Shreenidhi Shedi <sshedi@vmware.com> 7.0.2-1
- Upgrade to v7.0.2, this also fixes CVE-2022-33105
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
* Thu Dec 28 2017 Divya Thaluru <dthaluru@vmware.com> 3.2.8-5
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
