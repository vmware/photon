%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name fluent-plugin-remote_syslog

Name:           rubygem-fluent-plugin-remote_syslog
Summary:        Fluentd output plugin for remote syslog
Version:        1.0.0
Release:        2%{?dist}
License:        MIT
Group:          Development/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}
Source0:        https://rubygems.org/downloads/%{gem_name}-%{version}.gem
BuildArch:      noarch
%define sha1    fluent-plugin-remote_syslog=a25f03f8027d99b774ff96c59fac4c42c893aa8d
BuildRequires:  ruby >= 2.1
Requires: rubygem-fluentd >= 0
Requires: rubygem-remote_syslog_sender >= 1.1.1

%description
Fluentd plugin for remote syslog protocol

%prep
%setup -q -c -T

%build

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{SOURCE0}

%files
%defattr(-,root,root,-)
%{gemdir}

%changelog
*   Wed Sep 02 2020 Sujay G <gsujay@vmware.com> 1.0.0-2
-   Rebuilt using ruby-2.7.1
*   Mon Jan 27 2020 Nikolay Stanchev <nstanchev@vmware.com> 1.0.0-1
-   Initial build
