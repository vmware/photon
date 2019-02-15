Summary:	Logstash is a tool for managing events and logs.
Name:           logstash
Version:        6.4.3
Release:        1%{?dist}
License:        Apache License Version 2.0
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon
URL:		https://github.com/elastic/logstash/archive/%{name}-%{version}.tar.gz
Source0:        %{name}-%{version}.tar.gz
%define sha1 %{name}-%{version}.tar.gz=a55f9d8f5d13c46cf44bba743469b77130b7487b
Source1:        %{name}.service
Source2:        %{name}.conf
Patch0:         logstash-update-java-dependencies.patch
BuildRequires:	openjdk
BuildRequires:	ruby
Requires:	openjdk
Requires:	ruby
Requires:       systemd
Requires:       elasticsearch
Requires:       kibana

%description
Logstash is a tool to collect, process, and forward events and log messages. Collection is accomplished via configurable input plugins including raw socket/packet communication, file tailing, and several message bus clients. Once an input plugin has collected data it can be processed by any number of filters which modify and annotate the event data. Finally logstash routes events to output plugins which can forward the events to a variety of external programs including Elasticsearch, local files and several message bus implementations.

%define debug_package %{nil}

%prep
%setup -q
%patch0 -p1

%build
export OSS=true
export LC_ALL=en_US.UTF-8
export JAVA_HOME=/usr/lib/jvm/OpenJDK-%{JAVA_VERSION}
#Note: Only Building and Packaging Apache Licensed OSS part of Logstash. It doesn't include x-pack coponent of Elastic
./gradlew assembleOssTarDistribution

%install
export LC_ALL=en_US.UTF-8
export JAVA_HOME=/usr/lib/jvm/OpenJDK-%{JAVA_VERSION}
rm -rf %{buildroot}
install -vdm 755 %{buildroot}%{_sysconfdir}/%{name}/conf.d
install -vdm 755 %{buildroot}/var/lib/%{name}
install -vdm 755 %{buildroot}/var/log/%{name}
install -vdm 750 %{buildroot}%{_datadir}/%{name}/bin
install -vdm 775 %{buildroot}%{_datadir}/%{name}/data
install -vdm 750 %{buildroot}%{_datadir}/%{name}/lib
install -vdm 750 %{buildroot}%{_datadir}/%{name}/config
install -vdm 750 %{buildroot}%{_datadir}/%{name}/logstash-core
install -vdm 750 %{buildroot}%{_datadir}/%{name}/logstash-core-plugin-api
install -vdm 750 %{buildroot}%{_datadir}/%{name}/modules
install -vdm 750 %{buildroot}%{_datadir}/%{name}/tools
install -vdm 750 %{buildroot}%{_datadir}/%{name}/vendor

install -vdm 755 %{buildroot}/usr/lib/systemd/system
install -p -m 0644 %{SOURCE1} %{buildroot}/usr/lib/systemd/system/
install -p -m 0644 %{SOURCE2} %{buildroot}%{_sysconfdir}/%{name}/
cd build/
tar -xvf %{name}-oss-%{version}-SNAPSHOT.tar.gz
cp -r %{name}-%{version}-SNAPSHOT/config/* %{buildroot}%{_sysconfdir}/%{name}
cp -r %{name}-%{version}-SNAPSHOT/config/* %{buildroot}%{_datadir}/%{name}/config

cp -r %{name}-%{version}-SNAPSHOT/bin/* %{buildroot}%{_datadir}/%{name}/bin

cp -r %{name}-%{version}-SNAPSHOT/lib/* %{buildroot}%{_datadir}/%{name}/lib
cp -r %{name}-%{version}-SNAPSHOT/tools/* %{buildroot}%{_datadir}/%{name}/tools

cp -r %{name}-%{version}-SNAPSHOT/modules/* %{buildroot}%{_datadir}/%{name}/modules
cp -r %{name}-%{version}-SNAPSHOT/vendor/* %{buildroot}%{_datadir}/%{name}/vendor
cp -r %{name}-%{version}-SNAPSHOT/logstash-core-plugin-api/* %{buildroot}%{_datadir}/%{name}/logstash-core-plugin-api
cp -r %{name}-%{version}-SNAPSHOT/logstash-core/* %{buildroot}%{_datadir}/%{name}/logstash-core
install -p -m 0664 %{name}-%{version}-SNAPSHOT/CONTRIBUTORS %{buildroot}%{_datadir}/%{name}
install -p -m 0640 %{name}-%{version}-SNAPSHOT/Gemfile %{buildroot}%{_datadir}/%{name}
install -p -m 0640 %{name}-%{version}-SNAPSHOT/Gemfile.lock %{buildroot}%{_datadir}/%{name}
install -p -m 0664 %{name}-%{version}-SNAPSHOT/LICENSE.txt %{buildroot}%{_datadir}/%{name}
install -p -m 0640 %{name}-%{version}-SNAPSHOT/NOTICE.TXT %{buildroot}%{_datadir}/%{name}

%pre
if ! getent group %{name} >/dev/null; then
    groupadd %{name}
fi
if ! getent passwd %{name} >/dev/null; then
    useradd -c "Logstash" -d /var/lib/%{name} -g %{name} -s /bin/false %{name}
fi
exit 0

%post
%systemd_post %{name}.service

%postun
if [ $1 -eq 0 ]; then
  # this is delete operation
  if getent passwd %{name} >/dev/null; then
      userdel %{name}
  fi
  if getent group %{name} >/dev/null; then
      groupdel %{name}
  fi
fi
%systemd_postun_with_restart %{name}.service

%preun
%systemd_preun %{name}.service

%files
%defattr(-,root,root)
%dir %{_datadir}/%{name}
%attr(-,logstash,logstash) %{_datadir}/%{name}
%{_sysconfdir}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/%{name}.conf
/usr/lib/systemd/system/%{name}.service
%attr(-,logstash,logstash) /var/lib/%{name}
%attr(-,logstash,logstash) /var/log/%{name}

%changelog
*   Wed Feb 13 2019 Siju Maliakkal <smaliakkal@vmware.com> 6.4.3-1
-   Upgraded to 6.4.3 for kibana,elasticsearch compatibility
*   Fri Feb 08 2019 Ankit Jain <ankitja@vmware.com> 6.4.1-2
-   Updated the Java dependencies
*   Wed Jan 23 2019 Siju Maliakkal <smaliakkal@vmware.com> 6.4.1-1
-   Upgrade to 6.4.1
*   Fri Nov 09 2018 Tapas Kundu <tkundu@vmware.com> 6.4.0-2
-   Updated to build and package only oss distribution.
*   Thu Oct 25 2018 Ankit Jain <ankitja@vmware.com> 6.4.0-1
-   Updated to release 6.4.0
*   Mon Aug 06 2018 Ankit Jain <ankitja@vmware.com> 6.3.0-2
-   Added logstash.service and logstash.conf
*   Thu Jul 19 2018 Ankit Jain <ankitja@vmware.com> 6.3.0-1
-   Initial Version.
