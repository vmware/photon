#%global debug_package %{nil}
%global __os_install_post %{nil}
Summary:        Cassandra is a highly scalable, eventually consistent, distributed, structured key-value store
Name:           cassandra
Version:        4.0.1
Release:        1%{?dist}
URL:            http://cassandra.apache.org/
License:        Apache License, Version 2.0
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        http://archive.apache.org/dist/cassandra/%{version}/apache-%{name}-%{version}-src.tar.gz
%define sha1    apache-cassandra=63c2e267f34e00b477fdd96b9279f3aae7716546
Source1:        cassandra.service
BuildRequires:  apache-ant
BuildRequires:  unzip zip
BuildRequires:  openjdk8
BuildRequires:  wget
BuildRequires:  git
BuildRequires:  systemd-rpm-macros
Requires:       openjre8
Requires:       gawk
Requires:       shadow
Requires(post): /bin/chown
%{?systemd_requires}

%description
Cassandra is a highly scalable, eventually consistent, distributed, structured key-value store.
Cassandra brings together the distributed systems technologies from Dynamo and the log-structured storage engine from Google's BigTable.

%prep
%autosetup -p1 -n apache-%{name}-%{version}-src

%build
export JAVA_HOME=`echo /usr/lib/jvm/OpenJDK-*`
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

rm -f bin/cqlsh
rm -f bin/cqlsh.py
mv bin/%{name} %{buildroot}%{_sbindir}
mv bin/%{name}.in.sh %{buildroot}%{_datadir}/cassandra/
cp -p bin/* %{buildroot}%{_bindir}/
cp -p tools/bin/* %{buildroot}%{_bindir}/
cp -r lib %{buildroot}/var/opt/cassandra/
cp -r build %{buildroot}/var/opt/cassandra/
cp -p build/tools/lib/stress.jar %{buildroot}/var/opt/cassandra/lib
cp -p build/apache-cassandra-%{version}.jar %{buildroot}/var/opt/cassandra/lib

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

%preun
%systemd_preun cassandra.service

%postun
%{_sbindir}/ldconfig
%systemd_postun_with_restart cassandra.service
if [ $1 -eq 0 ] ; then
    /usr/sbin/userdel cassandra
    /usr/sbin/groupdel cassandra
fi

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
*   Tue Sep 21 2021 Ankit Jain <ankitja@vmware.com> 4.0.1-1
-   Update to 4.0.1 to fix second level dependency vuln
*   Wed Jun 09 2021 Ankit Jain <ankitja@vmware.com> 3.11.10-2
-   Remove cqlsh and cqlsh.py, since it requires python2 to run
-   python3-cqlsh is introduced
-   fix post and postun script failure
*   Tue Mar 09 2021 Ankit Jain <ankitja@vmware.com> 3.11.10-1
-   Update to 3.11.10 to fix CVE-2020-17516
*   Thu Oct 29 2020 Ankit Jain <ankitja@vmware.com> 3.11.8-2
-   Added cqlsh and cqlsh.py.
-   Since, python-cqlsh is deprecated.
*   Tue Sep 01 2020 Gerrit Photon <photon-checkins@vmware.com> 3.11.8-1
-   Automatic Version Bump
*   Mon Aug 24 2020 Gerrit Photon <photon-checkins@vmware.com> 3.11.7-1
-   Automatic Version Bump
*   Mon Jun 22 2020 Gerrit Photon <photon-checkins@vmware.com> 3.11.6-1
-   Automatic Version Bump
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
