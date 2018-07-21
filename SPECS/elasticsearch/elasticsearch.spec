Summary:        Elastic Serch
Name:           elasticsearch
Version:        6.3.0
Release:        1%{?dist}
License:        Apache License Version 2.0
URL:            https://artifacts.elastic.co/downloads/elasticsearch/%{name}-%{version}.tar.gz
Source0:        %{name}-%{version}.tar.gz
%define sha1    %{name}-%{version}.tar.gz=3f356bf80bd31c0107622cf7213d0ee9f43536d8
Source1:        cacerts
%define sha1    cacerts=f584c7c1f48c552f39acfb5560a300a657d9f3bb
Group:          Development/Daemons
Vendor:         VMware, Inc.
Distribution:   Photon
BuildRequires:  openjdk10 
BuildRequires:  unzip 
BuildRequires:  curl
BuildRequires:  which
BuildRequires:  git
BuildRequires:  make
BuildRequires:  automake
BuildRequires:  autoconf
BuildRequires:  libtool
BuildRequires:  tar
BuildRequires:  wget
BuildRequires:  patch
BuildRequires:  texinfo
Requires(pre):  /usr/sbin/useradd /usr/sbin/groupadd
Requires(postun):/usr/sbin/userdel /usr/sbin/groupdel

%description
Elasticsearch is a highly distributed RESTful search engine built for the cloud.

%define debug_package %{nil}

%prep
%setup -qn %{name}-%{version}

%build
export LANG="en_US.UTF-8"
export JAVA_TOOL_OPTIONS="-Dfile.encoding=UTF8"
export JAVA_HOME=/usr/lib/jvm/OpenJDK-1.10.0.23
export PATH=$JAVA_HOME/bin:$PATH
export _JAVA_OPTIONS="-Xmx10g"
cp %{SOURCE1} /usr/lib/jvm/OpenJDK-1.10.0.23/lib/security/
./gradlew assemble

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_datadir}/%{name}
mkdir -p %{buildroot}/etc/%{name}
mkdir -p %{buildroot}/usr/lib/sysctl.d/
mkdir -p %{buildroot}/usr/lib/systemd/system/
mkdir -p %{buildroot}/usr/lib/tmpfiles.d/
mkdir -p %{buildroot}/etc/init.d/elasticsearch
mkdir -p %{buildroot}/etc/sysconfig/elasticsearch
mkdir -p %{buildroot}/var/lib/elasticsearch
mkdir -p %{buildroot}/var/log/elasticsearch
mkdir -p %{buildroot}/var/run/elasticsearch


tar -xvf distribution/archives/oss-tar/build/distributions/elasticsearch-oss-6.3.0-SNAPSHOT.tar.gz
cp elasticsearch-6.3.0-SNAPSHOT/LICENSE.txt %{buildroot}%{_datadir}/%{name}/
cp elasticsearch-6.3.0-SNAPSHOT/NOTICE.txt %{buildroot}%{_datadir}/%{name}/
cp elasticsearch-6.3.0-SNAPSHOT/README.textile %{buildroot}%{_datadir}/%{name}/
cp -r elasticsearch-6.3.0-SNAPSHOT/* %{buildroot}%{_datadir}/%{name}/
cp distribution/packages/build/packaging/oss-rpm/systemd/sysctl/elasticsearch.conf %{buildroot}/usr/lib/sysctl.d/
cp distribution/packages/build/packaging/oss-rpm/systemd/elasticsearch.service %{buildroot}/usr/lib/systemd/system/
cp distribution/packages/build/packaging/oss-rpm/systemd/elasticsearch.conf %{buildroot}/usr/lib/tmpfiles.d/
cp elasticsearch-6.3.0-SNAPSHOT/config/log4j2.properties %{buildroot}/etc/%{name}/
cp elasticsearch-6.3.0-SNAPSHOT/config/jvm.options %{buildroot}/etc/%{name}/

chmod 755 %{buildroot}%{_datadir}/%{name}/
chmod 755 %{buildroot}/etc/%{name}/
chmod 755 %{buildroot}/var/log/%{name}/

%pre

getent group elasticsearch >/dev/null || /usr/sbin/groupadd -r elasticsearch
getent passwd elasticsearch >/dev/null || /usr/sbin/useradd --comment "ElasticSearch" --shell /bin/bash -M -r --groups elasticsearch --home /usr/share/elasticsearch elasticsearch


%post
%{_sbindir}/ldconfig
%systemd_post elasticsearch.service

%preun
%systemd_preun elasticsearch.service

%postun
%systemd_postun_with_restart elasticsearch.service
if [ $1 -eq 0 ] ; then
    /usr/sbin/userdel elasticsearch
    /usr/sbin/groupdel elasticsearch
fi
/sbin/ldconfig


%check

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%attr(755,elasticsearch,elasticsearch) /var/log/elasticsearch
%attr(755,elasticsearch,elasticsearch) /usr/share/elasticsearch
%attr(755,elasticsearch,elasticsearch) /usr/share/elasticsearch/logs
%dir %{_datadir}/%{name}
%{_datadir}/%{name}
%attr(755,elasticsearch,elasticsearch) /etc/%{name}
%attr(755,elasticsearch,elasticsearch) /usr/lib/systemd/system/elasticsearch.service
%attr(755,elasticsearch,elasticsearch) /usr/lib/sysctl.d/elasticsearch.conf
%attr(755,elasticsearch,elasticsearch) /usr/lib/tmpfiles.d/elasticsearch.conf

%changelog
*    Mon Jul 09 2018 Tapas Kundu <tkundu@vmware.com> 6.3.0-1
-    Initial build added for Photon.
