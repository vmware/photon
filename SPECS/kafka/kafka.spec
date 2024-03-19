%define debug_package %{nil}
%define _conf_dir    %{_sysconfdir}/%{name}
%define _log_dir     %{_var}/log/%{name}
%define _data_dir    %{_sharedstatedir}/%{name}
%define dep_libs_ver 2.13.10

Summary:       Apache Kafka is publish-subscribe messaging rethought as a distributed commit log.
Name:          kafka
Version:       3.4.0
Release:       4%{?dist}
License:       Apache License, Version 2.0
Group:         Productivity/Networking/Other
URL:           http://kafka.apache.org/
Vendor:        VMware, Inc.
Distribution:  Photon

Source0: %{name}-%{version}-src.tgz
%define sha512 %{name}=84e368c6d5e6487ab7a9892a4f7859fa1f7a4c90880706d0b6a855affdf165fd1aa1ae25e098d5ef11f452a71f76e5edab083db98d6eec5ff5e61c69cb65d302

Source1: %{name}.service

Source2: %{name}-build-jars-%{version}.tar.gz
%define sha512 %{name}-build-jars=2a932bcccac8c1fe1dfa6b18e397bdb728275b06a397b0e484d735c96f53854db7f94ae18989cbc6fad0643b1d087486128c08479429c6a9f3dee9e2fe87b0c3

Provides: %{name}-server = %{version}-%{release}

BuildRequires: systemd-devel
BuildRequires: openjdk8
BuildRequires: curl
BuildRequires: zookeeper

Requires: zookeeper
Requires: (openjre8 or openjdk11-jre or openjdk17-jre)

%{?systemd_requires}

%description
Kafka is designed to allow a single cluster to serve as the central data backbone for a large organization. It can be elastically and transparently expanded without downtime. Data streams are partitioned and spread over a cluster of machines to allow data streams larger than the capability of any single machine and to allow clusters of co-ordinated consumers. Messages are persisted on disk and replicated within the cluster to prevent data loss.

%prep
%autosetup -p1 -n %{name}-%{version}-src -a2

%build
#Keeping the below code for future reference.
#export JAVA_HOME=`echo /usr/lib/jvm/OpenJDK-1.11.0`
#./gradlew jar
#./gradlew srcJar
#./gradlew javadoc
#./gradlew javadocJar
#./gradlew scaladoc
#./gradlew scaladocJar
#./gradlew docsJar

%install
export JAVA_HOME=$(echo /usr/lib/jvm/OpenJDK*)

mkdir -p %{buildroot}%{_prefix}/%{name}/{libs,bin,config} \
         %{buildroot}%{_log_dir} \
         %{buildroot}%{_data_dir} \
         %{buildroot}%{_unitdir} \
         %{buildroot}%{_conf_dir}

cp -pr config/* %{buildroot}%{_prefix}/%{name}/config

install -p -D -m 755 bin/*.sh %{buildroot}%{_prefix}/%{name}/bin
install -p -D -m 644 config/server.properties %{buildroot}%{_conf_dir}/
install -p -D -m 644 config/zookeeper.properties %{buildroot}%{_conf_dir}/
install -p -D -m 755 %{S:1} %{buildroot}%{_unitdir}/
install -p -D -m 644 config/log4j.properties %{buildroot}%{_conf_dir}/
install -p -D -m 644 connect/mirror/build/dependant-libs/* %{buildroot}%{_prefix}/%{name}/libs
install -p -D -m 644 connect/runtime/build/dependant-libs/* %{buildroot}%{_prefix}/%{name}/libs
install -p -D -m 644 tools/build/dependant-libs-%{dep_libs_ver}/* %{buildroot}%{_prefix}/%{name}/libs
install -p -D -m 644 core/build/dependant-libs-%{dep_libs_ver}/* %{buildroot}%{_prefix}/%{name}/libs
install -p -D -m 644 core/build/libs/* %{buildroot}%{_prefix}/%{name}/libs
install -p -D -m 644 clients/build/libs/* %{buildroot}%{_prefix}/%{name}/libs
install -p -D -m 644 connect/api/build/libs/* %{buildroot}%{_prefix}/%{name}/libs
install -p -D -m 644 connect/basic-auth-extension/build/libs/* %{buildroot}%{_prefix}/%{name}/libs
install -p -D -m 644 connect/json/build/libs/* %{buildroot}%{_prefix}/%{name}/libs
install -p -D -m 644 connect/transforms/build/libs/* %{buildroot}%{_prefix}/%{name}/libs
install -p -D -m 644 connect/file/build/libs/* %{buildroot}%{_prefix}/%{name}/libs
install -p -D -m 644 connect/mirror-client/build/libs/* %{buildroot}%{_prefix}/%{name}/libs
install -p -D -m 644 streams/examples/build/dependant-libs-%{dep_libs_ver}/* %{buildroot}%{_prefix}/%{name}/libs
install -p -D -m 644 streams/upgrade-system-tests-0110/build/libs/* %{buildroot}%{_prefix}/%{name}/libs
install -p -D -m 644 streams/build/libs/* %{buildroot}%{_prefix}/%{name}/libs

%clean
rm -rf %{buildroot}

%pre
/usr/bin/getent group %{name} >/dev/null || /usr/sbin/groupadd -r %{name}
/usr/bin/getent passwd %{name} >/dev/null || /usr/sbin/useradd -r \
  -g %{name} -d %{_prefix}/%{name} -s /bin/bash -c "Kafka" %{name}

%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun %{name}.service

%files
%defattr(-,root,root)
%doc NOTICE
%doc LICENSE
%{_unitdir}/%{name}.service
%config(noreplace) %{_conf_dir}/*
%{_prefix}/%{name}
%attr(0755,kafka,kafka) %dir %{_log_dir}
%attr(0700,kafka,kafka) %dir %{_data_dir}

%changelog
* Tue Mar 19 2024 Mukul Sikka <mukul.sikka@broadcom.com> 3.4.0-4
- Bump version as a part of openjdk8 upgrade
* Fri Sep 08 2023 Shreenidhi Shedi <sshedi@vmware.com> 3.4.0-3
- Require jre8 or jdk11-jre or jdk17-jre
* Sat Jun 17 2023 Shreenidhi Shedi <sshedi@vmware.com> 3.4.0-2
- Bump version as a part of openjdk11 upgrade
* Mon Feb 13 2023 Prashant S Chauhan <psinghchauha@vmware.com> 3.4.0-1
- Update to 3.4.0, use Java11. Fixes CVE-2023-25194.
* Mon Oct 17 2022 Prashant S Chauhan <psinghchauha@vmware.com> 3.0.2-1
- Update to 3.0.2, Fixes CVE-2022-34917
* Wed Dec 01 2021 Piyush Gupta <gpiyush@vmware.com> 3.0.0-2
- Bundled build time generated jars into a seperate source.
* Thu Oct 14 2021 Piyush Gupta <gpiyush@vmware.com> 3.0.0-1
- Update to 3.0.0.
* Fri Jul 31 2020 Anisha Kumari <kanisha@vmware.com> 2.5.0-1
- initial package
