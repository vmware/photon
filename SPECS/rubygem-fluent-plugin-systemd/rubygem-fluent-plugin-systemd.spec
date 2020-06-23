%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name fluent-plugin-systemd

Name: rubygem-fluent-plugin-systemd
Version:        1.0.2
Release:        1%{?dist}
Summary:        This is a fluentd input plugin. It reads logs from the systemd journal.
Group:          Development/Languages
License:        Apache 2
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}
Source0:        https://rubygems.org/downloads/fluent-plugin-systemd-%{version}.gem
%define sha1    fluent-plugin-systemd=7e927b3bc361ba1af7581281f3f09dfb7c64841a
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
*   Thu Jul 16 2020 Gerrit Photon <photon-checkins@vmware.com> 1.0.2-1
-   Automatic Version Bump
*   Thu Aug 16 2018 Srinidhi Rao <srinidhir@vmware.com> 1.0.1-2
-   Added the dependency on rubygem-systemd-journal
*   Tue Jul 24 2018 Srinidhi Rao <srinidhir@vmware.com> 1.0.1-1
-   Initial build
