%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name fluent-plugin-systemd

Name: rubygem-fluent-plugin-systemd
Version:        1.0.1
Release:        2%{?dist}
Summary:        This is a fluentd input plugin. It reads logs from the systemd journal.
Group:          Development/Languages
License:        Apache 2
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}
Source0:        https://rubygems.org/downloads/fluent-plugin-systemd-%{version}.gem
%define sha1    fluent-plugin-systemd=dd9c1e6ae7fa451822b5f244b0b92438a925670a
BuildRequires:  ruby

Requires: rubygem-fluentd >= 0.14.11
Requires: rubygem-fluentd < 2.0.0
Requires: systemd
Requires: rubygem-systemd-journal > 1.3.2

%description
This is a fluentd input plugin. It reads logs from the systemd journal.

%prep
%setup -q -c -T

%build

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{SOURCE0}

%files
%defattr(-,root,root,-)
%{gemdir}

%changelog
*   Thu Aug 16 2018 Srinidhi Rao <srinidhir@vmware.com> 1.0.1-2
-   Added the dependency on rubygem-systemd-journal
*   Tue Jul 24 2018 Srinidhi Rao <srinidhir@vmware.com> 1.0.1-1
-   Initial build
