%global build_if %{photon_subrelease} <= 90

%define network_required    1
%define debug_package       %{nil}
%define branch              %{version}-%{release}
%define tag                 %{version}
%define commit              467473bdb7

Summary:          agent for collecting, processing, aggregating, and writing metrics.
Name:             telegraf
Version:          1.36.4
Release:          2.3.1%{?dist}
URL:              https://github.com/influxdata/telegraf
Group:            Development/Tools
Vendor:           VMware, Inc.
Distribution:     Photon

Source0: https://github.com/influxdata/telegraf/archive/%{name}-%{version}.tar.gz

Source1: %{name}.sysusers
Source2: post.inc
Source3: %{name}.preset

Source4: license.txt
%include %{SOURCE4}

Patch0: CVE-2026-33186.patch
Patch1: 0001-Upgrade-nats-server-for-multiple-CVEs.patch

BuildRequires:    go
BuildRequires:    systemd-devel

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

%build
make %{?_smp_mflags} \
    config \
    %{name} \
    commit=%{commit} tag=%{tag} branch=%{branch}

%install
%make_install %{?_smp_mflags} \
  commit=%{commit} tag=%{tag} branch=%{branch} \
  prefix=%{_prefix} \
  localstatedir=%{_var} \
  sysconfdir=%{_sysconfdir} \
  buildbin=%{name}

install -pDm 0644 %{SOURCE1} %{buildroot}%{_sysusersdir}/%{name}.conf

mkdir -p %{buildroot}%{_sharedstatedir}/%{name} \
         %{buildroot}%{_var}/log/%{name} \
         %{buildroot}%{_unitdir} \
         %{buildroot}%{_sysconfdir}/%{name}/%{name}.d \
         %{buildroot}%{_sysconfdir}/default

mv %{buildroot}%{_libdir}/%{name}/scripts/%{name}.service \
   %{buildroot}%{_unitdir}

install -pDm 0644 %{SOURCE3} %{buildroot}%{_presetdir}/99-%{name}.preset

touch %{buildroot}%{_sysconfdir}/default/%{name}

%clean
rm -rf %{buildroot}/*

%pre
%sysusers_create_compat %{SOURCE1}

%post
%include %{SOURCE2}
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun_with_restart %{name}.service

%files
%defattr(-,root,root)
%{_bindir}/%{name}
%{_unitdir}/%{name}.service
%{_presetdir}/99-%{name}.preset
%attr(0644,root,root) %{_sysconfdir}/logrotate.d/%{name}
%attr(0644,root,root) %{_sysconfdir}/default/%{name}
%attr(0644,%{name},%{name}) %{_sysusersdir}/%{name}.conf
%attr(0755,-,-) %{_libdir}/%{name}/scripts/init.sh
%dir %{_sharedstatedir}/%{name}
%dir %{_var}/log/%{name}
%dir %{_libdir}/%{name}
%dir %{_sysconfdir}/%{name}/%{name}.d
%config(noreplace) %{_sysconfdir}/%{name}/%{name}.conf

%changelog
* Fri May 15 2026 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 1.36.4-2.3.1
- Adjusted to build for subrelease 90
* Fri Apr 24 2026 Mukul Sikka <mukul.sikka@broadcom.com> 1.36.4-2.3
- Upgrade bundled nats-server module for multiple CVEs
* Wed Apr 22 2026 Mukul Sikka <mukul.sikka@broadcom.com> 1.36.4-2.2
- Fix CVE-2026-33186
* Mon Apr 06 2026 Harinadh Dommaraju <Harinadh.Dommaraju@broadcom.com> 1.36.4-2.1
- Bump after moving to SPECS/91
* Wed Feb 04 2026 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 1.36.4-2
- Bump version as a part of go upgrade
* Fri Dec 05 2025 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 1.36.4-1
- Update to 1.36.4
- Update jose2go from 1.6.0 to 1.7.0 to address CVE-2025-63811
* Thu Nov 27 2025 Guruswamy Basavaiah <guruswamy.basavaiah@broadcom.com> 1.34.4-4
- Fix permission issue on /etc/default/telegraf
* Wed Nov 26 2025 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 1.34.4-3
- Fix permission issue on logrotate file
* Thu Oct 09 2025 Mukul Sikka <mukul.sikka@broadcom.com> 1.34.4-2
- Bump version as a part of go upgrade
* Wed Jun 04 2025 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 1.34.4-1
- Upgrade to v1.34.4
* Thu May 08 2025 Mukul Sikka <mukul.sikka@broadcom.com> 1.28.1-10
- Renaming sysusers to conf to fix auto user creation
* Fri Jan 10 2025 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 1.28.1-9
- Fix go input dependencies which have Capital letters in name.
* Wed Jan 08 2025 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 1.28.1-8
- Release bump for network_required packages
* Thu Dec 12 2024 Dweep Advani <dweep.advani@broadcom.com> 1.28.1-7
- Release bump for SRP compliance
* Thu Sep 19 2024 Mukul Sikka <mukul.sikka@broadcom.com> 1.28.1-6
- Bump version as a part of go upgrade
* Fri Jul 12 2024 Mukul Sikka <mukul.sikka@broadcom.com> 1.28.1-5
- Bump version as a part of go upgrade
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
