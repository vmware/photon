%define debug_package %{nil}

Summary:          Elastic Search
Name:             elasticsearch
Version:          6.8.10
Release:          1%{?dist}
License:          Apache License Version 2.0
URL:              https://github.com/elastic/elasticsearch/archive/v%{version}.tar.gz
Source0:          %{name}-%{version}.tar.gz
%define sha1      %{name}-%{version}.tar.gz=063835b80b35d1c97bcbc0f0adc4fa566926c6c2
Source1:          cacerts
%define sha1      cacerts=f584c7c1f48c552f39acfb5560a300a657d9f3bb
Source2:          distribution-for-elasticsearch-%{version}.tar.gz
%define sha1      distribution-for-elasticsearch=0035e7622d2ab5df36bc91f6302c282718e4294b
Group:            Development/Daemons
Vendor:           VMware, Inc.
Distribution:     Photon
BuildRequires:    unzip
BuildRequires:    curl
BuildRequires:    which
BuildRequires:    git
BuildRequires:    make
BuildRequires:    automake
BuildRequires:    autoconf
BuildRequires:    libtool
BuildRequires:    tar
BuildRequires:    wget
BuildRequires:    patch
BuildRequires:    texinfo
BuildRequires:    systemd
Requires:         systemd
Requires(pre):    /usr/sbin/useradd /usr/sbin/groupadd
Requires(postun): /usr/sbin/userdel /usr/sbin/groupdel

%description
Elasticsearch is a highly distributed RESTful search engine built for the cloud.

%prep
%setup -qn %{name}-%{version}

%build
export LANG="en_US.UTF-8"
export JAVA_TOOL_OPTIONS="-Dfile.encoding=UTF8"
export JAVA_HOME=`echo /usr/lib/jvm/OpenJDK-*`
export PATH=$JAVA_HOME/bin:$PATH
export _JAVA_OPTIONS="-Xmx10g"
cp %{SOURCE1} $JAVA_HOME/lib/security/
#For building elasticsearch, we need to execute the below command

#./gradlew assemble

rm -rf distribution
tar xf %{SOURCE2} --no-same-owner

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_datadir}/%{name}
mkdir -p %{buildroot}/etc/%{name}
mkdir -p %{buildroot}/usr/lib/sysctl.d/
mkdir -p %{buildroot}/usr/lib/systemd/system/
mkdir -p %{buildroot}/usr/lib/tmpfiles.d/
mkdir -p %{buildroot}/var/lib/elasticsearch
mkdir -p %{buildroot}/var/log/elasticsearch
mkdir -p %{buildroot}/var/run/elasticsearch
mkdir -p %{buildroot}%{_datadir}/%{name}/data

tar -xvf distribution/archives/oss-tar/build/distributions/%{name}-oss-%{version}-SNAPSHOT.tar.gz
cp %{name}-%{version}-SNAPSHOT/LICENSE.txt %{buildroot}%{_datadir}/%{name}/
cp %{name}-%{version}-SNAPSHOT/NOTICE.txt %{buildroot}%{_datadir}/%{name}/
cp %{name}-%{version}-SNAPSHOT/README.textile %{buildroot}%{_datadir}/%{name}/
cp -r %{name}-%{version}-SNAPSHOT/* %{buildroot}%{_datadir}/%{name}/
cp distribution/packages/build/packaging/oss-rpm/systemd/sysctl/elasticsearch.conf %{buildroot}/usr/lib/sysctl.d/
cp distribution/packages/build/packaging/oss-rpm/systemd/elasticsearch.service %{buildroot}/usr/lib/systemd/system/
cp distribution/packages/build/packaging/oss-rpm/systemd/elasticsearch.conf %{buildroot}/usr/lib/tmpfiles.d/
cp %{name}-%{version}-SNAPSHOT/config/log4j2.properties %{buildroot}/etc/%{name}/
cp %{name}-%{version}-SNAPSHOT/config/jvm.options %{buildroot}/etc/%{name}/

chmod 755 %{buildroot}%{_datadir}/%{name}/
chmod 755 %{buildroot}/etc/%{name}/
chmod 755 %{buildroot}/var/log/%{name}/
chmod 755 %{buildroot}/var/lib/%{name}/
chmod 755 %{buildroot}/var/run/%{name}/
chmod 755 %{buildroot}%{_datadir}/%{name}/data

%pre
if [ $1 -eq 1 ] ; then
    getent group elasticsearch >/dev/null || /usr/sbin/groupadd -r elasticsearch
    getent passwd elasticsearch >/dev/null || /usr/sbin/useradd --comment "ElasticSearch" --shell /bin/bash -M -r --groups elasticsearch --home /usr/share/elasticsearch elasticsearch
fi

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
%attr(755,elasticsearch,elasticsearch) /usr/share/elasticsearch/data
%attr(755,elasticsearch,elasticsearch) /var/lib/elasticsearch
%attr(755,elasticsearch,elasticsearch) /var/run/elasticsearch
%attr(755,elasticsearch,elasticsearch) /usr/share/elasticsearch
%attr(755,elasticsearch,elasticsearch) /usr/share/elasticsearch/logs
%dir %{_datadir}/%{name}
%{_datadir}/%{name}
%attr(755,elasticsearch,elasticsearch) /etc/%{name}
%attr(755,elasticsearch,elasticsearch) /usr/lib/systemd/system/elasticsearch.service
%attr(755,elasticsearch,elasticsearch) /usr/lib/sysctl.d/elasticsearch.conf
%attr(755,elasticsearch,elasticsearch) /usr/lib/tmpfiles.d/elasticsearch.conf

%changelog
*    Thu Jun 18 2020 Tapas Kundu <tkundu@vmware.com> 6.8.10-1
-    Update to release 6.8.10
*    Tue Jun 09 2020 Tapas Kundu <tkundu@vmware.com> 6.8.9-1
-    update to release 6.8.9
*    Wed Oct 9 2019 Michelle Wang <michellew@vmware.com> 6.7.0-4
-    Add gradle-tarball-for-elasticsearch-6.7.0.tar.gz to avoid download failures
*    Mon Sep 16 2019 Tapas Kundu <tkundu@vmware.com> 6.7.0-3
-    Update jackson databind to 2.9.9.3
*    Fri Aug 09 2019 Tapas Kundu <tkundu@vmware.com> 6.7.0-2
-    Update jackson
*    Tue Apr 02 2019 Ankit Jain <ankitja@vmware.com> 6.7.0-1
-    Updated to 6.7.0
*    Wed Mar 27 2019 Siju Maliakkal <smaliakkal@vmware.com> 6.4.3-2
-    Patch to upgrade bouncycastle version
*    Wed Feb 13 2019 Siju Maliakkal <smaliakkal@vmware.com> 6.4.3-1
-    Upgrade to 6.4.3 for CVE-2018-17244
*    Wed Dec 19 2018 Siju Maliakkal <smaliakkal@vmware.com> 6.4.1-1
-    Upgraded elasticsearch to 6.4.1 to mitigate CVE-2018-3831
*    Thu Oct 25 2018 Tapas Kundu <tkundu@vmware.com> 6.4.0-1
-    Updated to 6.4.0 and corrected typo.
*    Mon Aug 06 2018 Tapas Kundu <tkundu@vmware.com> 6.3.0-2
-    Added permissions for elasticsearch service and removed hardcoded value for JDK10.
*    Mon Jul 09 2018 Tapas Kundu <tkundu@vmware.com> 6.3.0-1
-    Initial build added for Photon.
