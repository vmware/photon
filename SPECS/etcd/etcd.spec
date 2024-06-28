Summary:        Distributed reliable key-value store
Name:           etcd
Version:        3.5.9
Release:        6%{?dist}
License:        Apache License
URL:            https://github.com/etcd-io/etcd
Group:          System Environment/Security
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://github.com/etcd-io/etcd/archive/refs/tags/%{name}-%{version}.tar.gz
%define sha512 %{name}=c71c8bb532f0f7d7f2bb63f3eed0a2a0f05e3299a9dd7b7fd5a4ca7c0acb89ea0259797306053c7dc5ca3ad735711df6540bf134ce15975330a2fe1754bb27d5

Source1:        %{name}.service
%ifarch aarch64
Source2:        %{name}.sysconfig
%endif
Source3:        %{name}.sysusers

BuildRequires:  go
BuildRequires:  git
BuildRequires:  systemd-devel

Requires: systemd

Requires(pre): shadow
Requires(pre): systemd-rpm-macros
Requires(postun): /usr/sbin/userdel /usr/sbin/groupdel

%description
A highly-available key value store for shared configuration and service discovery.

%prep
%autosetup -p1

%build
go mod vendor
./build

%install
install -vdm755 %{buildroot}%{_bindir}
install -vdm755 %{buildroot}%{_docdir}/%{name}-%{version}
install -vdm755 %{buildroot}%{_unitdir}
%ifarch aarch64
install -vdm 0755 %{buildroot}%{_sysconfdir}/sysconfig
%endif
install -vdm 0755 %{buildroot}%{_sysconfdir}/%{name}
install -vpm 0755 -T %{name}.conf.yml.sample %{buildroot}%{_sysconfdir}/%{name}/%{name}-default-conf.yml
install -p -D -m 0644 %{SOURCE3} %{buildroot}%{_sysusersdir}/%{name}.sysusers

chown -R root:root %{buildroot}%{_bindir}
chown -R root:root %{buildroot}/%{_docdir}/%{name}-%{version}

mv %{_builddir}/%{name}-%{version}/bin/%{name} \
   %{_builddir}/%{name}-%{version}/bin/etcdctl \
   %{buildroot}%{_bindir}

mv %{_builddir}/%{name}-%{version}/README.md %{buildroot}/%{_docdir}/%{name}-%{version}/
mv %{_builddir}/%{name}-%{version}/etcdctl/README.md %{buildroot}/%{_docdir}/%{name}-%{version}/README-etcdctl.md
mv %{_builddir}/%{name}-%{version}/etcdctl/READMEv2.md %{buildroot}/%{_docdir}/%{name}-%{version}/READMEv2-etcdctl.md

install -vdm755 %{buildroot}%{_presetdir}
echo "disable %{name}.service" > %{buildroot}%{_presetdir}/50-%{name}.preset

cp %{SOURCE1} %{buildroot}%{_unitdir}
%ifarch aarch64
cp %{SOURCE2} %{buildroot}%{_sysconfdir}/sysconfig/%{name}
%endif
install -vdm755 %{buildroot}%{_sharedstatedir}/%{name}

%pre
%sysusers_create_compat %{SOURCE3}

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%clean
rm -rf %{buildroot}/*

%files
%{_bindir}/%{name}*
%{_docdir}/%{name}-%{version}/*
%{_unitdir}/%{name}.service
%{_presetdir}/50-%{name}.preset
%attr(0700,%{name},%{name}) %dir %{_sharedstatedir}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/%{name}-default-conf.yml
%{_sysusersdir}/%{name}.sysusers
%ifarch aarch64
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%endif

%changelog
* Sun Nov 05 2023 Shreenidhi Shedi <sshedi@vmware.com> 3.5.9-6
- Fix requires
* Wed Oct 11 2023 Piyush Gupta <gpiyush@vmware.com> 3.5.9-5
- Bump up version to compile with new go
* Mon Sep 18 2023 Piyush Gupta <gpiyush@vmware.com> 3.5.9-4
- Bump up version to compile with new go
* Tue Aug 08 2023 Mukul Sikka <msikka@vmware.com> 3.5.9-3
- Resolving systemd-rpm-macros for group creation
* Mon Jul 17 2023 Piyush Gupta <gpiyush@vmware.com> 3.5.9-2
- Bump up version to compile with new go
* Thu Jul 06 2023 Prashant S Chauhan <psinghchauha@vmware.com> 3.5.9-1
- Update to 3.5.9
* Mon Jul 03 2023 Piyush Gupta <gpiyush@vmware.com> 3.5.7-3
- Bump up version to compile with new go
* Wed May 03 2023 Piyush Gupta <gpiyush@vmware.com> 3.5.7-2
- Bump up version to compile with new go
* Sun Mar 12 2023 Prashant S Chauhan <psinghchauha@vmware.com> 3.5.7-1
- Update to 3.5.7
* Sun Mar 12 2023 Piyush Gupta <gpiyush@vmware.com> 3.5.6-3
- Bump up version to compile with new go
* Fri Mar 10 2023 Mukul Sikka <msikka@vmware.com> 3.5.6-2
- Use systemd-rpm-macros for user creation
* Tue Dec 13 2022 Gerrit Photon <photon-checkins@vmware.com> 3.5.6-1
- Automatic Version Bump
* Mon Nov 21 2022 Piyush Gupta <gpiyush@vmware.com> 3.5.1-3
- Bump up version to compile with new go
* Wed Oct 26 2022 Piyush Gupta <gpiyush@vmware.com> 3.5.1-2
- Bump up version to compile with new go
* Fri Jun 17 2022 Prashant S Chauhan <psinghchauha@vmware.com> 3.5.1-1
- Update to 3.5.1
* Sun May 29 2022 Shreenidhi Shedi <sshedi@vmware.com> 3.4.18-2
- Fix binary path
* Mon Apr 18 2022 Gerrit Photon <photon-checkins@vmware.com> 3.4.18-1
- Automatic Version Bump
* Wed Jun 23 2021 Prashant S Chauhan <psinghchauha@vmware.com> 3.4.15-3
- Change etcd data directory ownership to etcd:etcd as per CIS benchmark
* Fri Jun 11 2021 Piyush Gupta<gpiyush@vmware.com> 3.4.15-2
- Bump up version to compile with new go
* Mon Apr 12 2021 Gerrit Photon <photon-checkins@vmware.com> 3.4.15-1
- Automatic Version Bump
* Fri Feb 05 2021 Harinadh D <hdommaraju@vmware.com> 3.4.13-3
- Bump up version to compile with new go
* Fri Jan 15 2021 Piyush Gupta<gpiyush@vmware.com> 3.4.13-2
- Bump up version to compile with new go
* Wed Aug 26 2020 Gerrit Photon <photon-checkins@vmware.com> 3.4.13-1
- Automatic Version Bump
* Wed Aug 19 2020 Gerrit Photon <photon-checkins@vmware.com> 3.4.12-1
- Automatic Version Bump
* Mon Jul 27 2020 Gerrit Photon <photon-checkins@vmware.com> 3.4.10-1
- Automatic Version Bump
* Mon Jun 22 2020 Gerrit Photon <photon-checkins@vmware.com> 3.4.9-1
- Automatic Version Bump
* Wed Apr 08 2020 Shreyas B <shreyasb@vmware.com> 3.4.3-2
- Remove vendor dependencies, which is occurs due to Go v1.14.
* Mon Mar 16 2020 Ankit Jain <ankitja@vmware.com> 3.4.3-1
- Update to 3.4.3
* Mon Feb 25 2019 Keerthana K <keerthanak@vmware.com> 3.3.9-2
- Add env variable ETCD_UNSUPPORTED_ARCH=arm64 for arm to start etcd service.
* Fri Sep 21 2018 Sujay G <gsujay@vmware.com> 3.3.9-1
- Bump etcd version to 3.3.9
* Mon Sep 18 2017 Alexey Makhalov <amakhalov@vmware.com> 3.1.5-4
- Remove shadow requires
* Sun Aug 27 2017 Vinay Kulkarni <kulkarniv@vmware.com> 3.1.5-3
- File based configuration for etcd service.
* Wed May 31 2017 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 3.1.5-2
- Provide preset file to deactivate service by default
* Thu Apr 06 2017 Anish Swaminathan <anishs@vmware.com> 3.1.5-1
- Upgraded to version 3.1.5, build from sources
* Fri Sep 2 2016 Xiaolin Li <xiaolinl@vmware.com> 3.0.9-1
- Upgraded to version 3.0.9
* Fri Jun 24 2016 Xiaolin Li <xiaolinl@vmware.com> 2.3.7-1
- Upgraded to version 2.3.7
* Wed May 25 2016 Nick Shi <nshi@vmware.com> 2.2.5-3
- Changing etcd service type from simple to notify
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.2.5-2
- GA - Bump release of all rpms
* Tue Feb 23 2016 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 2.2.5-1
- Upgraded to version 2.2.5
* Tue Jul 28 2015 Divya Thaluru <dthaluru@vmware.com> 2.1.1-2
- Adding etcd service file
* Tue Jul 21 2015 Vinay Kulkarni <kulkarniv@vmware.com> 2.1.1-1
- Update to version etcd v2.1.1
* Tue Mar 10 2015 Divya Thaluru <dthaluru@vmware.com> 2.0.4-1
- Initial build.  First version
