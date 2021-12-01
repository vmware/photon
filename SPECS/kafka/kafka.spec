%define debug_package %{nil}
%define _conf_dir    %{_sysconfdir}/%{name}
%define _log_dir     %{_var}/log/%{name}
%define _data_dir    %{_sharedstatedir}/%{name}
Summary:       Apache Kafka is publish-subscribe messaging rethought as a distributed commit log.
Name: 	       kafka
Version:       3.0.0
Release:       2%{?dist}
License:       Apache License, Version 2.0
Group:         Productivity/Networking/Other
URL:           http://kafka.apache.org/
Source0:       %{name}-%{version}-src.tgz
%define sha1   kafka=4eee044bba66f19be20a189b5d2db9348c0c10cc
Source1:       %{name}.service
Source2:       %{name}-build-jars-%{version}.tar.gz
%define sha1   %{name}-build-jars=86ba550a5718a601852131003a1b525265cbb596
Vendor:	       VMware, Inc.
Distribution:  Photon
Provides:      kafka kafka-server
BuildRequires: systemd
BuildRequires: openjdk8
BuildRequires: curl
BuildRequires: zookeeper
Requires:      zookeeper

%systemd_requires

%description
Kafka is designed to allow a single cluster to serve as the central data backbone for a large organization. It can be elastically and transparently expanded without downtime. Data streams are partitioned and spread over a cluster of machines to allow data streams larger than the capability of any single machine and to allow clusters of co-ordinated consumers. Messages are persisted on disk and replicated within the cluster to prevent data loss.

%prep
%autosetup -n %{name}-%{version}-src

%build
tar -xf %{SOURCE2}
#Keeping the below code for future reference.
#export JAVA_HOME=`echo /usr/lib/jvm/OpenJDK*`
#./gradlew jar
#./gradlew srcJar
#./gradlew javadoc
#./gradlew javadocJar
#./gradlew scaladoc
#./gradlew scaladocJar
#./gradlew docsJar

%install
export JAVA_HOME=`echo /usr/lib/jvm/OpenJDK*`
mkdir -p %{buildroot}/%{_prefix}/%{name}/{libs,bin,config}
mkdir -p %{buildroot}/%{_log_dir}
mkdir -p %{buildroot}/%{_data_dir}
mkdir -p %{buildroot}/%{_unitdir}
mkdir -p %{buildroot}/%{_conf_dir}/
cp -pr config/* %{buildroot}/%{_prefix}/%{name}/config
install -p -D -m 755 bin/*.sh %{buildroot}/%{_prefix}/%{name}/bin
install -p -D -m 644 config/server.properties %{buildroot}/%{_conf_dir}/
install -p -D -m 644 config/zookeeper.properties %{buildroot}/%{_conf_dir}/
install -p -D -m 755 %{S:1} %{buildroot}/%{_unitdir}/
install -p -D -m 644 config/log4j.properties %{buildroot}/%{_conf_dir}/
install -p -D -m 644 connect/mirror/build/dependant-libs/* %{buildroot}/%{_prefix}/%{name}/libs
install -p -D -m 644 connect/runtime/build/dependant-libs/* %{buildroot}/%{_prefix}/%{name}/libs
install -p -D -m 644 tools/build/dependant-libs-2.13.6/* %{buildroot}/%{_prefix}/%{name}/libs
install -p -D -m 644 core/build/dependant-libs-2.13.6/* %{buildroot}/%{_prefix}/%{name}/libs
install -p -D -m 644 core/build/libs/* %{buildroot}/%{_prefix}/%{name}/libs
install -p -D -m 644 clients/build/libs/* %{buildroot}/%{_prefix}/%{name}/libs
install -p -D -m 644 connect/api/build/libs/* %{buildroot}/%{_prefix}/%{name}/libs
install -p -D -m 644 connect/basic-auth-extension/build/libs/* %{buildroot}/%{_prefix}/%{name}/libs
install -p -D -m 644 connect/json/build/libs/* %{buildroot}/%{_prefix}/%{name}/libs
install -p -D -m 644 connect/transforms/build/libs/* %{buildroot}/%{_prefix}/%{name}/libs
install -p -D -m 644 connect/file/build/libs/* %{buildroot}/%{_prefix}/%{name}/libs
install -p -D -m 644 connect/mirror-client/build/libs/* %{buildroot}/%{_prefix}/%{name}/libs
install -p -D -m 644 streams/examples/build/dependant-libs-2.13.6/* %{buildroot}/%{_prefix}/%{name}/libs
install -p -D -m 644 streams/upgrade-system-tests-0110/build/libs/* %{buildroot}/%{_prefix}/%{name}/libs
install -p -D -m 644 streams/build/libs/* %{buildroot}/%{_prefix}/%{name}/libs

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
if [ $1 -eq 0 ]
then
    /usr/sbin/userdel %{name}
    /usr/sbin/groupdel %{name}
fi

%files
%defattr(-,root,root)
%{_unitdir}/%{name}.service
%config(noreplace) %{_conf_dir}/*
%{_prefix}/%{name}
%attr(0755,kafka,kafka) %dir %{_log_dir}
%attr(0700,kafka,kafka) %dir %{_data_dir}
%doc NOTICE
%doc LICENSE

%changelog
* Wed Dec 01 2021 Piyush Gupta <gpiyush@vmware.com> 3.0.0-2
- Bundled build time generated jars into a seperate source.
* Thu Oct 14 2021 Piyush Gupta <gpiyush@vmware.com> 3.0.0-1
- Update to 3.0.0.
* Fri Jul 31 2020 Anisha Kumari <kanisha@vmware.com> 2.5.0-1
- initial package
