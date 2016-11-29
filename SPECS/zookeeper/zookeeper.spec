Summary:        Highly reliable distributed coordination
Name:           zookeeper
Version:        3.4.9
Release:        1%{?dist}
URL:            http://zookeeper.apache.org/
License:        Apache License, Version 2.0
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon
Source:         http://mirrors.ocf.berkeley.edu/apache/zookeeper/zookeeper-3.4.9/%{name}-%{version}.tar.gz
%define sha1 zookeeper=0285717bf5ea87a7a36936bf37851d214a32bb99
Source1:        zookeeper.service
Source2:        zkEnv.sh
Patch0:	        zookeeper-3.4.8-server.patch
BuildRequires:  systemd
Requires:       systemd
Requires:       shadow
Requires:       openjre
Provides:       zookeeper
%description
ZooKeeper is a centralized service for maintaining configuration information, naming, providing distributed synchronization, and providing group services. All of these kinds of services are used in some form or another by distributed applications. Each time they are implemented there is a lot of work that goes into fixing the bugs and race conditions that are inevitable. Because of the difficulty of implementing these kinds of services, applications initially usually skimp on them ,which make them brittle in the presence of change and difficult to manage. Even when done correctly, different implementations of these services lead to management complexity when the applications are deployed.

%prep
%setup -q
%patch0 -p1

%install
mkdir -p %{buildroot}%{_prefix}
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_libdir}/java/zookeeper
mkdir -p %{buildroot}%{_libdir}/zookeeper
mkdir -p %{buildroot}%{_var}/log/zookeeper
mkdir -p %{buildroot}%{_sysconfdir}/zookeeper
mkdir -p %{buildroot}%{_var}/run/zookeeper
mkdir -p %{buildroot}/sbin
mkdir -p %{buildroot}%{_prefix}/share/zookeeper/templates/conf
mkdir -p %{buildroot}%{_var}/zookeeper

cp zookeeper-%{version}.jar %{buildroot}%{_libdir}/java/zookeeper
cp src/packages/update-zookeeper-env.sh %{buildroot}/sbin/update-zookeeper-env.sh
cp src/packages/templates/conf/zookeeper-env.sh %{buildroot}%{_prefix}/share/zookeeper/templates/conf
cp conf/zoo_sample.cfg %{buildroot}%{_prefix}/share/zookeeper/templates/conf/zoo.cfg
chmod 0755 %{buildroot}/sbin/*

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
%pre
getent group hadoop >/dev/null || /usr/sbin/groupadd -r hadoop
getent passwd zookeeper >/dev/null || /usr/sbin/useradd --comment "ZooKeeper" --shell /bin/bash -M -r --groups hadoop --home %{_prefix}/share/zookeeper zookeeper

%post
if [ $1 -eq 1 ] ; then
    # Initial installation
    # Enabled by default per "runs once then goes away" exception
    source %{_sysconfdir}/profile.d/java-exports.sh
    bash %{_prefix}/sbin/update-zookeeper-env.sh \
       --prefix=%{_prefix} \
       --conf-dir=%{_sysconfdir}/zookeeper \
       --log-dir=%{_var}/log/zookeeper \
       --pid-dir=%{_var}/run/zookeeper \
       --var-dir=%{_var}/zookeeper
fi
%{_sbindir}/ldconfig
%systemd_post zookeeper.service
 
%preun
if [ $1 -eq 0 ] ; then
source %{_sysconfdir}/profile.d/java-exports.sh
bash %{_prefix}/sbin/update-zookeeper-env.sh \
       --prefix=%{_prefix} \
       --conf-dir=%{_sysconfdir}/zookeeper \
       --log-dir=%{_var}/log/zookeeper \
       --pid-dir=%{_var}/run/zookeeper \
       --var-dir=%{_var}/zookeeper \
       --uninstall
fi
%systemd_preun zookeeper.service

%postun
%systemd_postun_with_restart zookeeper.service
if [ $1 -eq 0 ] ; then
    /usr/sbin/userdel zookeeper
    /usr/sbin/groupdel hadoop
fi
/sbin/ldconfig

%files
%defattr(-,root,root)
%attr(0755,zookeeper,hadoop) %{_var}/log/zookeeper
%attr(0775,zookeeper,hadoop) %{_var}/run/zookeeper
%attr(0775,zookeeper,hadoop) /sbin/update-zookeeper-env.sh
%config(noreplace) %{_sysconfdir}/zookeeper/*
/lib/systemd/system/zookeeper.service
%{_prefix}

%changelog
*   Mon Nov 28 2016 Vinay Kulkarni <kulkarniv@vmware.com> 3.4.9-1
-   Upgrade to 3.4.9 to address CVE-2016-5017
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 3.4.8-4
-   GA - Bump release of all rpms
*   Mon May 2 2016 Divya Thaluru <dthaluru@vmware.com>  3.4.8-3
-   Fixing spec file to handle rpm upgrade scenario correctly
*   Thu Apr 28 2016 Divya Thaluru <dthaluru@vmware.com>  3.4.8-2
-   Added logic to set classpath
*   Wed Feb 24 2016 Kumar Kaushik <kaushikk@vmware.com>  3.4.8-1
-   Updating version.
*   Fri Feb 05 2016 Anish Swaminathan <anishs@vmware.com>  3.4.6-8
-   Edit pre install script.
*   Tue Jan 12 2016 Anish Swaminathan <anishs@vmware.com>  3.4.6-7
-   Remove init.d file.
*   Thu Dec 10 2015 Xiaolin Li <xiaolinl@vmware.com>  3.4.6-6
-   Add systemd to Requires and BuildRequires.
*   Wed Nov 18 2015 Xiaolin Li <xiaolinl@vmware.com> 3.4.6-5
-   Add zookeeper to systemd service.
*   Tue Nov 10 2015 Mahmoud Bassiouny<mbassiouny@vmware.com> 3.4.6-4
-   Fix conflicts between zookeeper and chkconfig
*   Wed Sep 16 2015 Harish Udaiya Kumar<hudaiyakumar@vmware.com> 3.4.6-3
-   Udating the dependency after repackaging the openjdk, fixed post scripts
*   Wed Aug 05 2015 Kumar Kaushik <kaushikk@vmware.com> 3.4.6-2
-   Adding ldconfig in post section.
*   Thu Jun 11 2015 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 3.4.6-1
-   Initial build. First version	Initial build. First version
