Summary:	Highly reliable distributed coordination
Name:		zookeeper
Version:	3.4.6
Release:	2%{?dist}
URL:		http://zookeeper.apache.org/
License:	Apache License, Version 2.0
Group:		Applications/System
Vendor:		VMware, Inc.
Distribution: 	Photon
Source:	http://www.carfab.com/apachesoftware/zookeeper/stable/%{name}-%{version}.tar.gz
%define sha1 zookeeper=2a9e53f5990dfe0965834a525fbcad226bf93474
Requires: shadow, openjdk
Provides: zookeeper
%description
ZooKeeper is a centralized service for maintaining configuration information, naming, providing distributed synchronization, and providing group services. All of these kinds of services are used in some form or another by distributed applications. Each time they are implemented there is a lot of work that goes into fixing the bugs and race conditions that are inevitable. Because of the difficulty of implementing these kinds of services, applications initially usually skimp on them ,which make them brittle in the presence of change and difficult to manage. Even when done correctly, different implementations of these services lead to management complexity when the applications are deployed.

%prep
%setup -q

%install
mkdir -p %{buildroot}%{_prefix}
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_libdir}
mkdir -p %{buildroot}%{_var}/log/zookeeper
mkdir -p %{buildroot}%{_sysconfdir}/zookeeper
mkdir -p %{buildroot}%{_var}/run
mkdir -p %{buildroot}/sbin
mkdir -p %{buildroot}%{_prefix}/share/zookeeper/templates/conf
mkdir -p %{buildroot}%{_var}/zookeeper
mkdir -p %{buildroot}/etc/init.d

cp zookeeper-%{version}.jar %{buildroot}%{_libdir}
cp src/packages/rpm/init.d/zookeeper %{buildroot}/etc/init.d/zookeeper
cp src/packages/update-zookeeper-env.sh %{buildroot}/sbin/update-zookeeper-env.sh
cp src/packages/templates/conf/zookeeper-env.sh %{buildroot}%{_prefix}/share/zookeeper/templates/conf
cp conf/zoo_sample.cfg %{buildroot}%{_prefix}/share/zookeeper/templates/conf/zoo.cfg
chmod 0755 %{buildroot}/sbin/*
chmod 0755 %{buildroot}/etc/init.d/zookeeper

mv bin/* %{buildroot}%{_bindir}
mv lib/* %{buildroot}%{_libdir}
mv conf/zoo_sample.cfg %{buildroot}%{_sysconfdir}/zookeeper/zoo.cfg
mv conf/* %{buildroot}%{_sysconfdir}/zookeeper
cd ..
rm -rf %{buildroot}/%{name}-%{version}

%pre
getent group hadoop 2>/dev/null >/dev/null || /usr/sbin/groupadd -r hadoop
/usr/sbin/useradd --comment "ZooKeeper" --shell /bin/bash -M -r --groups hadoop --home %{_share_dir} zookeeper 2> /dev/null || :

%post
bash %{_prefix}/sbin/update-zookeeper-env.sh \
       --prefix=%{_prefix} \
       --conf-dir=%{_sysconfdir}/zookeeper \
       --log-dir=%{_var}/log/zookeeper \
       --pid-dir=%{_var}/run \
       --var-dir=%{_var}/zookeeper
-p /sbin/ldconfig

%preun
bash %{_prefix}/sbin/update-zookeeper-env.sh \
       --prefix=%{_prefix} \
       --conf-dir=%{_sysconfdir}/zookeeper \
       --log-dir=%{_var}/log/zookeeper \
       --pid-dir=%{_var}/run \
       --var-dir=%{_var}/zookeeper \
       --uninstall

%postun	-p /sbin/ldconfig
%files
%defattr(-,root,root)
%attr(0755,root,hadoop) %{_var}/log/zookeeper
%attr(0775,root,hadoop) %{_var}/run
%attr(0775,root,hadoop) /etc/init.d/zookeeper
%attr(0775,root,hadoop) /sbin/update-zookeeper-env.sh
%config(noreplace) %{_sysconfdir}/zookeeper/*
%{_prefix}

%changelog

*	Wed Aug 05 2015 Kumar Kaushik <kaushikk@vmware.com> 3.4.6-2
        Adding ldconfig in post section.
*       Thu Jun 11 2015 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 3.4.6-1
        Initial build. First version	Initial build. First version
