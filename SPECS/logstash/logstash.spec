Summary:	Logstash is a tool for managing events and logs.
Name:           logstash
Version:        6.8.15
Release:        2%{?dist}
License:        Apache License Version 2.0
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon
URL:		https://github.com/elastic/logstash/archive/v%{version}.tar.gz
Source0:        %{name}-%{version}.tar.gz
%define sha1 %{name}-%{version}.tar.gz=97af85061109be81f41b023579f80550ff44b73c
Source1:        %{name}.service
Source2:        %{name}.conf
Patch0:         CVE-2021-44228.patch
Patch1:         CVE-2021-45046.patch
BuildArch:      x86_64
BuildRequires:	openjdk8
BuildRequires:	ruby
BuildRequires:  git
Requires:	openjdk8
Requires:	ruby
Requires:       systemd
Requires:       elasticsearch = %{version}
Requires:       kibana = %{version}

%description
Logstash is a tool to collect, process, and forward events and log messages. Collection is accomplished via configurable input plugins including raw socket/packet communication, file tailing, and several message bus clients. Once an input plugin has collected data it can be processed by any number of filters which modify and annotate the event data. Finally logstash routes events to output plugins which can forward the events to a variety of external programs including Elasticsearch, local files and several message bus implementations.

%define debug_package %{nil}

%prep
%autosetup -p1
#Build only Apache License oss part of logstash
rm -rf x-pack

%build
export OSS=true
export JAVA_HOME=`echo /usr/lib/jvm/OpenJDK*`
#Note: Only Building and Packaging Apache Licensed OSS part of Logstash. It doesn't include x-pack coponent of Elastic
./gradlew assembleOssTarDistribution

%install
rm -rf %{buildroot}
export JAVA_HOME=`echo /usr/lib/jvm/OpenJDK*`
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
*   Wed Dec 15 2021 Ankit Jain <ankitja@vmware.com> 6.8.15-2
-   Fix for CVE-2021-44228 and CVE-2021-45046
*   Wed Apr 07 2021 Piyush Gupta <gpiyush@vmware.com> 6.8.15-1
-   Update to 6.8.15
*   Wed Nov 18 2020 Piyush Gupta <gpiyush@vmware.com> 6.8.13-1
-   Update to 6.8.13, Fix for CVE-2020-7020
*   Mon Aug 31 2020 Piyush Gupta <gpiyush@vmware.com> 6.8.12-1
-   Update to 6.8.12
*   Thu Jun 18 2020 Tapas Kundu <tkundu@vmware.com> 6.8.10-1
-   Update to 6.8.10
*   Mon Jun 08 2020 Tapas Kundu <tkundu@vmware.com> 6.8.9-1
-   Update to 6.8.9
*   Mon Apr 27 2020 Tapas Kundu <tkundu@vmware.com> 6.8.8-1
-   Update to 6.8.8
*   Fri Apr 24 2020 Ankit Jain <ankitja@vmware.com> 6.7.0-6
-   Changed openjdk install directory name
*   Thu Nov 28 2019 Ankit Jain <ankitja@vmware.com> 6.7.0-5
-   Updated the logstash-input-beat version to fix CVE-2019-7620
*   Mon Sep 16 2019 Tapas Kundu <tkundu@vmware.com> 6.7.0-4
-   Updated jackson to 2.9.9.3
*   Thu Sep 05 2019 Ankit Jain <ankitja@vmware.com> 6.7.0-3
-   Bump up to consume the latest release of openjdk8
*   Fri Aug 09 2019 Tapas Kundu <tkundu@vmware.com> 6.7.0-2
-   Updated jackson
*   Thu Apr 25 2019 Ankit Jain <ankitja@vmware.com> 6.7.0-1
-   Upgrade to 6.7.0
*   Wed Mar 20 2019 Ankit Jain <ankitja@vmware.com> 6.4.3-2
-   Updated the Java dependencies
*   Wed Feb 13 2019 Siju Maliakkal <smaliakkal@vmware.com> 6.4.3-1
-   Upgrade to 6.4.3 for kibana,elasticsearch compatibility
*   Wed Jan 23 2019 Siju Maliakkal <smaliakkal@vmware.com> 6.4.1-1
-   Upgrade to 6.4.1
*   Wed Dec 12 2018 Ajay Kaher <akaher@vmware.com> 6.4.0-2
-   Adding BuildArch.
*   Tue Dec 04 2018 Ankit Jain <ankitja@vmware.com> 6.4.0-1
-   Initial Version.
