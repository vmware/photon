#%global debug_package %{nil}
%global __os_install_post %{nil}
Summary:        Cassandra is a highly scalable, eventually consistent, distributed, structured key-value store
Name:           cassandra
Version:        3.11.3
Release:        1%{?dist}
URL:            http://cassandra.apache.org/
License:        Apache License, Version 2.0
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://repo1.maven.org/maven2/org/apache/cassandra/apache-cassandra/3.10/apache-%{name}-%{version}-src.tar.gz
%define sha1    apache-cassandra=6860ef5a085429e7bd5783551304c7922d4efbc1
Source1:        cassandra.service
BuildRequires:  apache-ant
BuildRequires:  unzip zip
BuildRequires:  openjdk8
BuildRequires:  wget
Requires:       openjre8
Requires:       gawk
%description
Cassandra is a highly scalable, eventually consistent, distributed, structured key-value store. Cassandra brings together the distributed systems technologies from Dynamo and the log-structured storage engine from Google's BigTable.

%prep
%setup -qn apache-%{name}-%{version}-src
sed -i 's#\"logback-core\" version=\"1.1.3\"#\"logback-core\" version=\"1.2.0\"#g' build.xml
sed -i 's#\"logback-classic\" version=\"1.1.3\"#\"logback-classic\" version=\"1.2.0\"#g' build.xml
rm lib/logback-*
mv lib/licenses/logback-core-1.1.3.txt lib/licenses/logback-core-1.2.0.txt
mv lib/licenses/logback-classic-1.1.3.txt lib/licenses/logback-classic-1.2.0.txt

wget http://central.maven.org/maven2/ch/qos/logback/logback-classic/1.2.0/logback-classic-1.2.0.jar -P lib
wget http://central.maven.org/maven2/ch/qos/logback/logback-core/1.2.0/logback-core-1.2.0.jar -P lib

%build
export JAVA_HOME=/usr/lib/jvm/OpenJDK-%{JAVA8_VERSION}

ant jar javadoc -Drelease=true

%install
mkdir -p %{buildroot}/var/opt/%{name}/data
mkdir -p %{buildroot}/var/log/%{name}
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_sbindir}
mkdir -p %{buildroot}%{_datadir}/cassandra
mkdir -p %{buildroot}%{_sysconfdir}/cassandra
mkdir -p %{buildroot}%{_sysconfdir}/sysconfig
mkdir -p %{buildroot}/etc/profile.d
mkdir -p %{buildroot}/var/opt/cassandra

cp bin/%{name} %{buildroot}%{_sbindir}
cp bin/%{name}.in.sh %{buildroot}%{_datadir}/cassandra/
cp bin/nodetool %{buildroot}%{_bindir}/
cp bin/sstableloader %{buildroot}%{_bindir}/
cp bin/sstablescrub %{buildroot}%{_bindir}/
cp bin/sstableupgrade %{buildroot}%{_bindir}/
cp bin/sstableutil %{buildroot}%{_bindir}/
cp bin/sstableverify %{buildroot}%{_bindir}/
cp conf/cassandra-env.sh %{buildroot}%{_sysconfdir}/cassandra/
cp conf/cassandra.yaml %{buildroot}%{_sysconfdir}/cassandra/
cp conf/cassandra-jaas.config %{buildroot}%{_sysconfdir}/cassandra/
cp conf/cassandra-topology.properties %{buildroot}%{_sysconfdir}/cassandra/
cp conf/jvm.options %{buildroot}%{_sysconfdir}/cassandra/
cp conf/logback-tools.xml %{buildroot}%{_sysconfdir}/cassandra/
cp conf/logback.xml %{buildroot}%{_sysconfdir}/cassandra/
cp conf/metrics-reporter-config-sample.yaml %{buildroot}%{_sysconfdir}/cassandra/
cp -r lib %{buildroot}/var/opt/cassandra/
cp -r build %{buildroot}/var/opt/cassandra/
cp build/tools/lib/stress.jar %{buildroot}/var/opt/cassandra/lib
cp build/apache-cassandra-%{version}.jar %{buildroot}/var/opt/cassandra/lib
cp tools/bin/cassandra-stress %{buildroot}%{_bindir}
cp tools/bin/cassandra-stressd %{buildroot}%{_bindir}
cp tools/bin/sstabledump %{buildroot}%{_bindir}/
cp tools/bin/sstableexpiredblockers %{buildroot}%{_bindir}/sstableexpiredblockers
cp tools/bin/sstablelevelreset %{buildroot}%{_bindir}/sstablelevelreset
cp tools/bin/sstablemetadata %{buildroot}%{_bindir}/sstablemetadata
cp tools/bin/sstableofflinerelevel %{buildroot}%{_bindir}/sstableofflinerelevel
cp tools/bin/sstablerepairedset %{buildroot}%{_bindir}/sstablerepairedset
cp tools/bin/sstablesplit %{buildroot}%{_bindir}/sstablesplit
cp tools/bin/cassandra-stress %{buildroot}%{_bindir}/
cp tools/bin/cassandra-stressd %{buildroot}%{_bindir}/

mkdir -p %{buildroot}/lib/systemd/system
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
*   Mon Sep 03 2018 Keerthana K <keerthanak@vmware.com> 3.11.3-1
-   Updated to version 3.11.3.
*   Tue Apr 24 2018 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 3.10-8
-   Remove patch to build on openjdk-1.8.0.162, updated openjdk to 1.8.0.172
*   Sat Jan 20 2018 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 3.10-7
-   Add patch to build on openjdk-1.8.0.162
*   Thu Aug 17 2017 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 3.10-6
-   Add SuccessExitStatus to cassandra service file
*   Thu Aug 10 2017 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 3.10-5
-   Remove the build/libs directory from the cassandra package
*   Tue Jul 25 2017 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 3.10-4
-   Remove hadoop jars, upgrade logback jars and change service type to simple
*   Mon Jul 10 2017 Xiaolin Li <xiaolinl@vmware.com> 3.10-3
-   Remove cqlsh and cqlsh.py.
*   Mon Jun 19 2017 Divya Thaluru <dthaluru@vmware.com> 3.10-2
-   Removed dependency on ANT_HOME
*   Mon May 08 2017 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 3.10-1
-   Initial build. First version
