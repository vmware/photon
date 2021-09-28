#%global debug_package %{nil}
%global __os_install_post %{nil}
Summary:        Cassandra is a highly scalable, eventually consistent, distributed, structured key-value store
Name:           cassandra
Version:        3.11.11
Release:        1%{?dist}
URL:            http://cassandra.apache.org/
License:        Apache License, Version 2.0
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://repo1.maven.org/maven2/org/apache/cassandra/apache-cassandra/%{version}/apache-%{name}-%{version}-src.tar.gz
%define sha1    apache-cassandra=34a6f6ef2de5607fd5130d8dcca20773ae6cbdfd
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
%autosetup -p1 -n apache-%{name}-%{version}-src

%build
export JAVA_HOME=`echo /usr/lib/jvm/OpenJDK*`

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

cp -pr conf/* %{buildroot}%{_sysconfdir}/cassandra/

rm -f bin/cqlsh bin/cqlsh.py
mv bin/%{name} %{buildroot}%{_sbindir}
mv bin/%{name}.in.sh %{buildroot}%{_datadir}/cassandra/
cp -p bin/* %{buildroot}%{_bindir}/
cp -p tools/bin/* %{buildroot}%{_bindir}/
cp -r lib build %{buildroot}/var/opt/cassandra/
cp -p build/tools/lib/stress.jar build/apache-cassandra-%{version}.jar %{buildroot}/var/opt/cassandra/lib

mkdir -p %{buildroot}%{_unitdir}
install -p -D -m 644 %{SOURCE1}  %{buildroot}%{_unitdir}/%{name}.service

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
%{_sysconfdir}/profile.d/cassandra.sh
%{_unitdir}/cassandra.service
%exclude /var/opt/cassandra/build/lib

%changelog
*   Tue Sep 28 2021 Ankit Jain <ankitja@vmware.com> 3.11.11-1
-   Update to 3.11.11 to fix several second level dep vuln.
*   Mon Feb 08 2021 Ankit Jain <ankitja@vmware.com> 3.11.10-1
-   Update to 3.11.10 to fix CVE-2020-17516
*   Thu Dec 17 2020 Gerrit Photon <photon-checkins@vmware.com> 3.11.9-1
-   Automatic Version Bump
*   Mon Sep 21 2020 Michelle Wang <michellew@vmware.com> 3.11.8-1
-   Fix CVE-2020-13946
*   Fri Apr 24 2020 Ankit Jain <ankitja@vmware.com> 3.11.5-4
-   Changed openjdk install directory name
*   Wed Feb 05 2020 Ankit Jain <ankitja@vmware.com> 3.11.5-3
-   Bump jackson version to >= 2.9.5
*   Wed Feb 05 2020 Shreyas B. <shreyasb@vmware.com> 3.11.5-2
-   Shadow require by Cassandra for the installation.
*   Fri Jan 17 2020 Ankit Jain <ankitja@vmware.com> 3.11.5-1
-   Central maven repository not responding, Updated to 3.11.5
*   Tue Dec 17 2019 Shreyas B. <shreyasb@vmware.com> 3.11.3-3
-   Bumping up the thrift version to 0.9.3.1 to fix vulnerability.
*   Mon Nov 05 2018 Alexey Makhalov <amakhalov@vmware.com> 3.11.3-2
-   Removed dependency on JAVA8_VERSION macro
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
