%global debug_package %{nil}
Summary:        The Apache Portable Runtime
Name:           logstash
Version:        6.2.4
Release:        1%{?dist}
License:        Apache License 2.0/ELASTIC LICENSE
URL:            https://www.elastic.co/downloads/logstash
Group:          System Environment/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://artifacts.elastic.co/downloads/logstash/%{name}-%{version}.tar.gz
%define sha1    logstash=a9e47590689d6d3eb01738afe1d7ca43604f3f61
%description
Logstash is an open source, server-side data processing pipeline that ingests data from a multitude of sources simultaneously, transforms it, and then sends it to your favorite “stash.” (Ours is Elasticsearch, naturally.)

%prep
%setup -q
%build

%install
mkdir -p \
    %{buildroot}/%{_sysconfdir}/logstash \
    %{buildroot}/%{_sysconfdir}/logstash/conf.d \
    %{buildroot}/%{_datadir}/logstash \
    %{buildroot}/%{_datadir}/logstash/data \
    %{buildroot}/%{_var}/run/logstash \
    %{buildroot}/%{_var}/log/logstash \

install -m644 -p config/jvm.options %{buildroot}/%{_sysconfdir}/logstash/jvm.options
install -m644 -p config/log4j2.properties %{buildroot}/%{_sysconfdir}/logstash/log4j2.properties
install -m644 -p config/logstash.yml %{buildroot}/%{_sysconfdir}/logstash/logstash.yml 
install -m644 -p config/pipelines.yml %{buildroot}/%{_sysconfdir}/logstash/pipelines.yml
install -m644 -p config/startup.options %{buildroot}/%{_sysconfdir}/logstash/startup.options
cp -r bin lib modules tools vendor %{buildroot}/%{_datadir}/logstash
cp -r logstash-core logstash-core-plugin-api %{buildroot}/%{_datadir}/logstash
cp  CONTRIBUTORS Gemfile Gemfile.lock LICENSE NOTICE.TXT %{buildroot}/%{_datadir}/logstash

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/logstash/jvm.options
%config(noreplace) %{_sysconfdir}/logstash/logstash.yml
%config(noreplace) %{_sysconfdir}/logstash/pipelines.yml
%config(noreplace) %{_sysconfdir}/logstash/startup.options
%{_sysconfdir}/logstash/log4j2.properties
%{_datadir}/logstash/bin/*
%{_datadir}/logstash/lib/*
%{_datadir}/logstash/modules/*
%{_datadir}/logstash/tools/*
%{_datadir}/logstash/vendor/*
%{_datadir}/logstash/logstash-core/*
%{_datadir}/logstash/logstash-core-plugin-api/*
%{_datadir}/logstash/CONTRIBUTORS
%{_datadir}/logstash/Gemfile
%{_datadir}/logstash/Gemfile.lock
%{_datadir}/logstash/LICENSE
%{_datadir}/logstash/NOTICE.TXT
%dir %{_datadir}/logstash/data

%changelog
*   Wed May 09 2018 Xiaolin Li <xiaolinl@vmware.com> 6.2.4-1
-   Initial build. First version
