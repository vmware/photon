%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name fluent-plugin-vmware-loginsight

Name: rubygem-fluent-plugin-vmware-loginsight
Version:        0.1.10
Release:        1%{?dist}
Summary:        Fluent output plugin to forward logs to VMware Log Insight.
Group:          Development/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
License:        MIT
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}
Source0:        https://rubygems.org/downloads/%{gem_name}-%{version}.gem
%define sha1    fluent-plugin-vmware-loginsight=f1817478c8d57bd35d0d197ceeab8c09af7331b9
BuildRequires:  ruby >= 2.1

Requires: rubygem-fluentd >= 0.14.10, rubygem-fluentd < 2.0.0
BuildArch: noarch

%description
Fluent output plugin to forward logs to VMware Log Insight.

%prep
%setup -q -c -T

%build

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{SOURCE0}

%files
%defattr(-,root,root,-)
%{gemdir}

%changelog
*   Thu Jul 16 2020 Gerrit Photon <photon-checkins@vmware.com> 0.1.10-1
-   Automatic Version Bump
*   Fri Aug 23 2019 Stanislav Hadjiiski <hadjiiskis@vmware.com> 0.1.5-1
-   Initial build
