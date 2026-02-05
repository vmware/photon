%global zk_root %{_libdir}/java/%{name}
%global zk_conf_dir %{_sysconfdir}/%{name}

Summary:        High-performance coordination service for distributed applications
Name:           zookeeper
Version:        3.9.4
Release:        1%{?dist}
URL:            https://zookeeper.apache.org
License:        Apache License, Version 2.0
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://github.com/apache/zookeeper/archive/refs/tags/%{name}-%{version}-source.tar.gz
%define sha512 %{name}=3cee277cb97279eb1597dd4dfa3ceef73b9c9eb24efaa6d9cf8ead13adda748b25486ad15001c8abd1685d054e9005fdcdc30d89386823901df9d0b8daa90957

Source1: %{name}.service
Source2: %{name}.preset
Source3: zkEnv.sh

Patch0: zkSever_remove_cygwin_cypath.patch

BuildRequires: openjdk8
BuildRequires: apache-maven
BuildRequires: systemd-devel
BuildRequires: net-tools

Requires: systemd
Requires: (openjre8 or openjdk11-jre or openjdk17-jre or openjdk21-jre)
Requires(pre):  shadow
Requires(pre):  systemd-rpm-macros
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd

%description
ZooKeeper is a centralized service for maintaining configuration information,
naming, providing distributed synchronization, and providing group services.
This package provides the Java server, client scripts, libraries, and systemd unit.

%prep
%autosetup -p1 -n %{name}-release-%{version}

%build
JAVA_BIN=$(readlink -f $(command -v java))
export JAVA_HOME=$(dirname $(dirname $JAVA_BIN))

mvn clean install \
  -Dmaven.javadoc.skip=true \
  -DskipTests \
  -DskipDocs

%install
install -d -m 0755 \
  %{buildroot}%{_bindir} \
  %{buildroot}%{zk_root} \
  %{buildroot}%{zk_conf_dir} \
  %{buildroot}%{_sharedstatedir}/%{name}/data \
  %{buildroot}%{_var}/log/%{name} \
  %{buildroot}%{_unitdir} \
  %{buildroot}%{_presetdir} \
  %{buildroot}%{_sysconfdir}/sysconfig \
  %{buildroot}%{_libdir}/%{name}

tar xf %{name}-assembly/target/apache-%{name}-%{version}-bin.tar.gz

pushd apache-%{name}-%{version}-bin
mv bin/* %{buildroot}%{_bindir}
mv lib/*.jar %{buildroot}%{zk_root}/
mv lib/* %{buildroot}%{_libdir}/%{name}
mv conf/zoo_sample.cfg %{buildroot}%{zk_conf_dir}/zoo.cfg
mv conf/* %{buildroot}%{zk_conf_dir}/
popd

install -D -m 0644 %{SOURCE1} %{buildroot}%{_unitdir}/%{name}.service
install -D -m 0644 %{SOURCE2} %{buildroot}%{_presetdir}/50-%{name}.preset
install -D -m 0755 %{SOURCE3} %{buildroot}%{_bindir}/zkEnv.sh

%clean
rm -rf %{buildroot}

%pre
getent group hadoop >/dev/null || %{_sbindir}/groupadd -r hadoop
getent passwd %{name} >/dev/null || \
    %{_sbindir}/useradd --comment "ZooKeeper" \
        --shell /bin/bash -M -r \
        --groups hadoop \
        --home %{_datadir}/%{name} %{name}

%post
/sbin/ldconfig
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun_with_restart %{name}.service
/sbin/ldconfig

%files
%defattr(-,root,root,-)
%config(noreplace) %{zk_conf_dir}/*
%dir %attr(0755,%{name},hadoop) %{_var}/log/%{name}
%dir %{zk_root}
%{zk_root}/*
%{_bindir}/*
%dir %{_libdir}/%{name}
%{_libdir}/%{name}/*
%{_unitdir}/%{name}.service
%{_presetdir}/50-%{name}.preset

%changelog
* Thu Feb 05 2026 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 3.9.4-1
- Upgrade to v3.9.4
- Build deliverables from source
* Sat Aug 23 2025 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 3.9.3-2
- Add jdk21 to requires list
* Wed Jul 16 2025 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 3.9.3-1
- Update to 3.9.3, fixes many second level CVEs
* Fri Sep 08 2023 Shreenidhi Shedi <sshedi@vmware.com> 3.8.0-2
- Require jre8 or jdk11-jre or jdk17-jre
* Tue Sep 5 2023 Michelle Wang <michellew@vmware.com> 3.8.0-1
- Update zookeeper to 3.8.0
* Wed Sep 08 2021 Nitesh Kumar <kunitesh@vmware.com> 3.6.3-2
- Replacement of ITS suggested words.
* Thu May 20 2021 Piyush Gupta <gpiyush@vmware.com> 3.6.3-1
- Update to 3.6.3.
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
- Initial build. First version.
