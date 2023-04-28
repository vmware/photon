Summary:          Highly reliable distributed coordination
Name:             zookeeper
Version:          3.8.0
Release:          3%{?dist}
URL:              http://zookeeper.apache.org/
License:          Apache License, Version 2.0
Group:            Applications/System
Vendor:           VMware, Inc.
Distribution:     Photon
Source:           %{name}-%{version}.tar.gz
%define sha512    zookeeper=d66e3a40451f840406901b2cd940992b001f92049a372ae48d8b420891605871cd1ae5f6cceb3b10665491e7abef36a4078dace158bd1e0938fcd3567b5234ca
Source1:          zookeeper.service
Source2:          zkEnv.sh
Source3:          %{name}.sysusers
Patch0:           zkSever_remove_cygwin_cypath.patch
BuildRequires:    systemd
BuildRequires:    systemd-devel
Requires:         systemd
Requires:         openjdk11
Requires(pre):    systemd-rpm-macros
Requires(pre):    /usr/sbin/useradd /usr/sbin/groupadd

%description
ZooKeeper is a centralized service for maintaining configuration information, naming,
providing distributed synchronization, and providing group services.
All of these kinds of services are used in some form or another by distributed applications.
Each time they are implemented there is a lot of work that goes into fixing the bugs and race conditions that are inevitable.
Because of the difficulty of implementing these kinds of services, applications initially usually skimp on them,
which make them brittle in the presence of change and difficult to manage.
Even when done correctly, different implementations of these services lead to management complexity when the applications are deployed.

%prep
%autosetup -p1 -n apache-zookeeper-%{version}-bin

%install
mkdir -p %{buildroot}%{_prefix}
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_libdir}/java/zookeeper
mkdir -p %{buildroot}%{_libdir}/zookeeper
mkdir -p %{buildroot}%{_var}/log/zookeeper
mkdir -p %{buildroot}%{_sysconfdir}/zookeeper
mkdir -p %{buildroot}%{_prefix}/share/zookeeper/templates/conf
mkdir -p %{buildroot}%{_var}/zookeeper

cp lib/zookeeper-%{version}.jar %{buildroot}%{_libdir}/java/zookeeper
cp conf/zoo_sample.cfg %{buildroot}%{_prefix}/share/zookeeper/templates/conf/zoo.cfg

mv bin/* %{buildroot}%{_bindir}
mv lib/*.jar %{buildroot}%{_libdir}/java/zookeeper
mv lib/* %{buildroot}%{_libdir}/zookeeper
mv conf/zoo_sample.cfg %{buildroot}%{_sysconfdir}/zookeeper/zoo.cfg
mv conf/* %{buildroot}%{_sysconfdir}/zookeeper
pushd ..
rm -rf %{buildroot}/%{name}-%{version}
popd

mkdir -p %{buildroot}/lib/systemd/system
cp %{SOURCE1} %{buildroot}/lib/systemd/system/zookeeper.service
cp %{SOURCE2} %{buildroot}%{_bindir}/zkEnv.sh

install -vdm755 %{buildroot}/lib/systemd/system-preset
echo "disable zookeeper.service" > %{buildroot}/lib/systemd/system-preset/50-zookeeper.preset
install -p -D -m 0644 %{SOURCE3} %{buildroot}%{_sysusersdir}/%{name}.sysusers

%pre
%sysusers_create_compat %{SOURCE3}

%post
%{_sbindir}/ldconfig
%systemd_post zookeeper.service

%preun
%systemd_preun zookeeper.service

%postun
%systemd_postun_with_restart zookeeper.service
/sbin/ldconfig

%files
%defattr(-,root,root)
%attr(0755,zookeeper,hadoop) %{_var}/log/zookeeper
%config(noreplace) %{_sysconfdir}/zookeeper/*
/lib/systemd/system/zookeeper.service
/lib/systemd/system-preset/50-zookeeper.preset
%{_sysusersdir}/%{name}.sysusers
%{_prefix}

%changelog
* Fri Mar 10 2023 Mukul Sikka <msikka@vmware.com> 3.8.0-3
- Use systemd-rpm-macros for user creation
* Wed Sep 21 2022 Vamsi Krishna Brahmajosuyula <vbrahmajosyula@vmware.com> 3.8.0-2
- Use openjdk11
* Fri Apr 22 2022 Gerrit Photon <photon-checkins@vmware.com> 3.8.0-1
- Automatic Version Bump
* Thu Apr 29 2021 Gerrit Photon <photon-checkins@vmware.com> 3.7.0-1
- Automatic Version Bump
* Wed Jun 10 2020 Gerrit Photon <photon-checkins@vmware.com> 3.5.8-1
- Automatic Version Bump
* Fri May 31 2019 Tapas Kundu <tkundu@vmware.com> 3.4.14-1
- Updated to release 3.4.14
- Fix for CVE-2019-0201
* Wed Sep 19 2018 Siju Maliakkal <smaliakkal@vmware.com> 3.4.13-1
- Update to latest version
* Wed Sep 27 2017 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 3.4.10-7
- Remove the update script for zookeeper.
* Mon Sep 25 2017 Alexey Makhalov <amakhalov@vmware.com> 3.4.10-6
- Remove shadow from requires and use explicit tools for post actions
* Mon Sep 25 2017 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 3.4.10-5
- Removed the java-export.sh script reference.
* Thu Jun 01 2017 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 3.4.10-4
- Renamed openjdk to openjdk8.
* Wed May 31 2017 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 3.4.10-3
- Provide preset to deactivate service by default
* Wed May 24 2017 Xiaolin Li <xiaolinl@vmware.com> 3.4.10-2
- Used RuntimeDirectory to create folder /var/run/zookeeper.
* Wed Apr 05 2017 Xiaolin Li <xiaolinl@vmware.com> 3.4.10-1
- Updated to version 3.4.10.
* Mon Nov 28 2016 Vinay Kulkarni <kulkarniv@vmware.com> 3.4.9-1
- Upgrade to 3.4.9 to address CVE-2016-5017
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 3.4.8-4
- GA - Bump release of all rpms
* Mon May 2 2016 Divya Thaluru <dthaluru@vmware.com>  3.4.8-3
- Fixing spec file to handle rpm upgrade scenario correctly
* Thu Apr 28 2016 Divya Thaluru <dthaluru@vmware.com>  3.4.8-2
- Added logic to set classpath
* Wed Feb 24 2016 Kumar Kaushik <kaushikk@vmware.com>  3.4.8-1
- Updating version.
* Fri Feb 05 2016 Anish Swaminathan <anishs@vmware.com>  3.4.6-8
- Edit pre install script.
* Tue Jan 12 2016 Anish Swaminathan <anishs@vmware.com>  3.4.6-7
- Remove init.d file.
* Thu Dec 10 2015 Xiaolin Li <xiaolinl@vmware.com>  3.4.6-6
- Add systemd to Requires and BuildRequires.
* Wed Nov 18 2015 Xiaolin Li <xiaolinl@vmware.com> 3.4.6-5
- Add zookeeper to systemd service.
* Tue Nov 10 2015 Mahmoud Bassiouny<mbassiouny@vmware.com> 3.4.6-4
- Fix conflicts between zookeeper and chkconfig
* Wed Sep 16 2015 Harish Udaiya Kumar<hudaiyakumar@vmware.com> 3.4.6-3
- Udating the dependency after repackaging the openjdk, fixed post scripts
* Wed Aug 05 2015 Kumar Kaushik <kaushikk@vmware.com> 3.4.6-2
- Adding ldconfig in post section.
* Thu Jun 11 2015 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 3.4.6-1
- Initial build. First version. Initial build. First version
