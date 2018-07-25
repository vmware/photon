Summary:	Logstash is a tool for managing events and logs.
Name:           logstash
Version:        6.3.0
Release:        1%{?dist}
License:        Apache License Version 2.0
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon
URL:		https://github.com/elastic/logstash/archive/v%{version}.tar.gz
Source0:        %{name}-%{version}.tar.gz
%define sha1 %{name}-%{version}.tar.gz=4140da67b1609b8664122e331cb8820ae786b3a6
BuildRequires:	openjdk
BuildRequires:	ruby
Requires:	openjdk
Requires:	ruby

%description
Logstash is a tool to collect, process, and forward events and log messages. Collection is accomplished via configurable input plugins including raw socket/packet communication, file tailing, and several message bus clients. Once an input plugin has collected data it can be processed by any number of filters which modify and annotate the event data. Finally logstash routes events to output plugins which can forward the events to a variety of external programs including Elasticsearch, local files and several message bus implementations.

%define debug_package %{nil}

%prep
%setup -q

%build
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
install -vdm 750 %{buildroot}%{_datadir}/%{name}/logstash-core
install -vdm 750 %{buildroot}%{_datadir}/%{name}/logstash-core-plugin-api
install -vdm 750 %{buildroot}%{_datadir}/%{name}/modules
install -vdm 750 %{buildroot}%{_datadir}/%{name}/tools
install -vdm 755 %{buildroot}%{_datadir}/%{name}/tools/ingest-converter
install -vdm 750 %{buildroot}%{_datadir}/%{name}/vendor

cp -r config/* %{buildroot}%{_sysconfdir}/%{name}/conf.d

cp -r bin/* %{buildroot}%{_datadir}/%{name}/bin
rm -rf %{buildroot}%{_datadir}/%{name}/bin/bundle
rm -rf %{buildroot}%{_datadir}/%{name}/bin/rspec
rm -rf %{buildroot}%{_datadir}/%{name}/bin/rspec.spec
rm -rf %{buildroot}%{_datadir}/%{name}/bin/rspec.bat

cp -r lib/* %{buildroot}%{_datadir}/%{name}/lib
cp -r tools/ingest-converter/* %{buildroot}%{_datadir}/%{name}/tools/ingest-converter
rm -rf %{buildroot}%{_datadir}/%{name}/tools/ingest-converter/build.gradle
rm -rf %{buildroot}%{_datadir}/%{name}/tools/ingest-converter/src

cp -r modules/* %{buildroot}%{_datadir}/%{name}/modules
cp -r vendor/* %{buildroot}%{_datadir}/%{name}/vendor
rm -rf %{buildroot}%{_datadir}/%{name}/vendor/_
cp -r logstash-core-plugin-api/* %{buildroot}%{_datadir}/%{name}/logstash-core-plugin-api
rm -rf %{buildroot}%{_datadir}/%{name}/logstash-core-plugin-api/versions-gem-copy.yml
cp -r logstash-core/lib %{buildroot}%{_datadir}/%{name}/logstash-core
cp -r logstash-core/locales %{buildroot}%{_datadir}/%{name}/logstash-core
cp -r logstash-core/logstash-core.gemspec %{buildroot}%{_datadir}/%{name}/logstash-core
cp -r logstash-core/versions-gem-copy.yml %{buildroot}%{_datadir}/%{name}/logstash-core
install -p -m 0664 CONTRIBUTORS %{buildroot}%{_datadir}/%{name}
install -p -m 0640 Gemfile %{buildroot}%{_datadir}/%{name}
install -p -m 0640 Gemfile.lock %{buildroot}%{_datadir}/%{name}
install -p -m 0664 LICENSE.txt %{buildroot}%{_datadir}/%{name}
install -p -m 0640 NOTICE.TXT %{buildroot}%{_datadir}/%{name}

%files
%defattr(-,root,root)
%dir %{_datadir}/%{name}
%{_datadir}/%{name}
%{_sysconfdir}/%{name}
/var/lib/%{name}
/var/log/%{name}

%changelog
*   Thu Jul 19 2018 Ankit Jain <ankitja@vmware.com> 6.3.0-1
-   Initial Version.
