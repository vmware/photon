%define debug_package %{nil}
%define _conf_dir    %{_sysconfdir}/%{name}
%define _log_dir     %{_var}/log/%{name}
%define _data_dir    %{_sharedstatedir}/%{name}
%define dep_libs_ver 2.13.15

Summary:       Apache Kafka is publish-subscribe messaging rethought as a distributed commit log.
Name:          kafka
Version:       3.9.1
Release:       2%{?dist}
License:       Apache License, Version 2.0
Group:         Productivity/Networking/Other
URL:           http://kafka.apache.org/
Vendor:        VMware, Inc.
Distribution:  Photon

Source0: %{name}-%{version}-src.tgz
%define sha512 %{name}=28b3066cb554e573428ef69d366cd344b0e7114a560eb57b2d3dda0507d266e6e804389457e8788f27b9c8f1dab027698a448bd82ca1d38b788e2874683e8019

Source1: %{name}.service

Source2: %{name}-build-jars-%{version}.tar.gz
%define sha512 %{name}-build-jars=09032ff06f9486fab237047b31ed6b7290a63d9398548cd71c757192dd06ddba50dcae574fcfdf0903c3c6368d442794afbe579fb4a80160d5121717bfd0f698

Provides: %{name}-server = %{version}-%{release}

BuildRequires: systemd-devel
BuildRequires: openjdk11
BuildRequires: curl
BuildRequires: zookeeper

Requires: zookeeper
Requires: (openjre8 or openjdk11-jre or openjdk17-jre or openjdk21-jre)
Requires(post): (coreutils or coreutils-selinux)

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

cat << EOF >> %{buildroot}/%{_conf_dir}/%{name}.env
LOG_DIR=/var/log/kafka
EOF

%clean
rm -rf %{buildroot}

%pre
/usr/bin/getent group %{name} >/dev/null || /usr/sbin/groupadd -r %{name}
/usr/bin/getent passwd %{name} >/dev/null || /usr/sbin/useradd -r \
  -g %{name} -d %{_prefix}/%{name} -s /bin/bash -c "Kafka" %{name}

%post
if [ -d %{_prefix}/%{name}/logs ] && [ ! -L %{_prefix}/%{name}/logs ]; then
    shopt -s dotglob
    mv %{_prefix}/%{name}/logs/* %{_log_dir}/
    shopt -u dotglob
    rmdir %{_prefix}/%{name}/logs/
    ln -s %{_log_dir} %{_prefix}/%{name}/logs
fi
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
%attr(0755,kafka,kafka) %{_prefix}/%{name}
%attr(0755,kafka,kafka) %dir %{_log_dir}
%attr(0700,kafka,kafka) %dir %{_data_dir}

%changelog
* Sat Aug 23 2025 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 3.9.1-2
- Add jdk21 to requires list
* Thu May 15 2025 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 3.9.1-1
- Update to 3.9.1, fixes multiple CVEs
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
