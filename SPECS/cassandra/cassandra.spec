%global debug_package %{nil}
%global __os_install_post %{nil}

Summary:        Cassandra is a highly scalable, eventually consistent, distributed, structured key-value store
Name:           cassandra
Version:        3.11.12
Release:        1%{?dist}
URL:            http://cassandra.apache.org/
License:        Apache License, Version 2.0
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        https://repo1.maven.org/maven2/org/apache/cassandra/apache-cassandra/%{version}/apache-%{name}-%{version}-src.tar.gz
%define sha1    apache-cassandra=08180d32795adb6986d57c390555c477509faa76
Source1:        cassandra.service
Patch0:         0001-build.xml-Upgraded-vuln-jar-version.patch
BuildRequires:  apache-ant
BuildRequires:  unzip zip
BuildRequires:  openjdk8
BuildRequires:  wget
BuildRequires:  git

Requires:       openjre8
Requires:       gawk
Requires:       shadow

%description
Cassandra is a highly scalable, eventually consistent, distributed, structured key-value store.
Cassandra brings together the distributed systems technologies from Dynamo and the log-structured storage engine from Google's BigTable.

%prep
# Using autosetup is not feasible
%setup -qn apache-%{name}-%{version}-src
%patch0 -p1

%build
export JAVA_HOME=$(echo /usr/lib/jvm/OpenJDK*)

ant jar javadoc -Drelease=true

%install
mkdir -p %{buildroot}/var/opt/%{name}/data \
         %{buildroot}/var/log/%{name} \
         %{buildroot}%{_bindir} \
         %{buildroot}%{_sbindir} \
         %{buildroot}%{_datadir}/cassandra \
         %{buildroot}%{_sysconfdir}/cassandra \
         %{buildroot}%{_sysconfdir}/sysconfig \
         %{buildroot}/etc/profile.d \
         %{buildroot}/var/opt/cassandra \
         %{buildroot}/lib/systemd/system

cp bin/%{name} %{buildroot}%{_sbindir}
cp bin/%{name}.in.sh %{buildroot}%{_datadir}/cassandra/

cp bin/nodetool \
   bin/sstableloader \
   bin/sstablescrub \
   bin/sstableupgrade \
   bin/sstableutil \
   bin/sstableverify \
   %{buildroot}%{_bindir}

cp conf/cassandra-env.sh \
   conf/cassandra.yaml \
   conf/cassandra-jaas.config \
   conf/cassandra-topology.properties \
   conf/jvm.options \
   conf/logback-tools.xml \
   conf/logback.xml \
   conf/metrics-reporter-config-sample.yaml \
   %{buildroot}%{_sysconfdir}/cassandra/

cp -r lib build %{buildroot}/var/opt/cassandra/

cp build/tools/lib/stress.jar \
   build/apache-cassandra-%{version}.jar \
   %{buildroot}/var/opt/cassandra/lib

cp tools/bin/cassandra-stress \
   tools/bin/cassandra-stressd \
   tools/bin/sstabledump \
   tools/bin/sstableexpiredblockers \
   tools/bin/sstablelevelreset \
   tools/bin/sstablemetadata \
   tools/bin/sstableofflinerelevel \
   tools/bin/sstablerepairedset \
   tools/bin/sstablesplit \
   tools/bin/cassandra-stress \
   tools/bin/cassandra-stressd \
   %{buildroot}%{_bindir}

install -p -D -m 644 %{SOURCE1}  %{buildroot}/lib/systemd/system/%{name}.service

cat >> %{buildroot}/etc/sysconfig/cassandra <<- "EOF"
CASSANDRA_HOME=/var/opt/cassandra/
CASSANDRA_CONF=%{_sysconfdir}/cassandra/
EOF

cat >> %{buildroot}/etc/profile.d/cassandra.sh <<- "EOF"
export CASSANDRA_HOME=/var/opt/cassandra/
export CASSANDRA_CONF=%{_sysconfdir}/cassandra/
EOF

%pre
getent group cassandra >/dev/null || /usr/sbin/groupadd -r cassandra
getent passwd cassandra >/dev/null || /usr/sbin/useradd --comment "Cassandra" --shell /bin/bash -M -r --groups cassandra --home /var/opt/%{name}/data cassandra

%post
%{_sbindir}/ldconfig
chown -R cassandra: /var/opt/cassandra
source /etc/profile.d/cassandra.sh
%systemd_post cassandra.service

%postun
%systemd_postun_with_restart cassandra.service
if [ $1 -eq 0 ] ; then
    /usr/sbin/userdel cassandra
    /usr/sbin/groupdel cassandra
fi
/sbin/ldconfig

%files
%defattr(-,root,root)
%doc README.asc CHANGES.txt NEWS.txt conf/cqlshrc.sample LICENSE.txt NOTICE.txt
%dir /var/opt/cassandra
%{_bindir}/*
%{_datadir}/cassandra
/var/opt/cassandra
%{_sbindir}
%{_sysconfdir}/cassandra
%{_sysconfdir}/sysconfig/cassandra
/etc/profile.d/cassandra.sh
/lib/systemd/system/cassandra.service
%exclude /var/opt/cassandra/build/lib

%changelog
* Mon Feb 21 2022 Ankit Jain <ankitja@vmware.com> 3.11.12-1
- Update to 3.11.12 and fixes CVE-2021-44521
* Mon Feb 08 2021 Ankit Jain <ankitja@vmware.com> 3.11.10-1
- Update to 3.11.10 to fix CVE-2020-17516
* Mon Sep 21 2020 Michelle Wang <michellew@vmware.com> 3.11.8-1
- Fix CVE-2020-13946
- Add patch cassandra-bump-jackson-version.patch
* Thu Feb 06 2020 Shreyas B. <shreyasb@vmware.com> 3.11.5-2
- Shadow require by Cassandra for installation.
* Tue Jan 21 2020 Michelle Wang <michellew@vmware.com> 3.11.5-1
- Central maven repository not responding, Updated to 3.11.5
* Tue Dec 17 2019 Shreyas B. <shreyasb@vmware.com> 3.11.2-3
- Bumping up the thrift version to 0.9.3.1 to fix vulnerability.
* Wed Jul 31 2019 Ankit Jain <ankitja@vmware.com> 3.11.2-2
- Modified the path of JAVA_HOME
* Wed Jul 25 2018 Tapas Kundu <tkundu@vmware,com> 3.11.2-1
- Upgraded cassandra to 3.11.2 version
* Tue Apr 24 2018 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 3.10-8
- Remove patch to build on openjdk-1.8.0.162, updated openjdk to 1.8.0.172
* Sat Jan 20 2018 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 3.10-7
- Add patch to build on openjdk-1.8.0.162
* Thu Aug 17 2017 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 3.10-6
- Add SuccessExitStatus to cassandra service file
* Thu Aug 10 2017 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 3.10-5
- Remove the build/libs directory from the cassandra package
* Tue Jul 25 2017 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 3.10-4
- Remove hadoop jars, upgrade logback jars and change service type to simple
* Mon Jul 10 2017 Xiaolin Li <xiaolinl@vmware.com> 3.10-3
- Remove cqlsh and cqlsh.py.
* Mon Jun 19 2017 Divya Thaluru <dthaluru@vmware.com> 3.10-2
- Removed dependency on ANT_HOME
* Mon May 08 2017 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 3.10-1
- Initial build. First version
