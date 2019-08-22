%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name fluent-plugin-concat

Name: rubygem-fluent-plugin-concat
Version:        2.4.0
Release:        1%{?dist}
Summary:        Fluentd Filter plugin to concat multiple event messages.
Group:          Development/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
License:        MIT
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}
Source0:        https://rubygems.org/downloads/fluent-plugin-concat-%{version}.gem
%define sha1    fluent-plugin-concat=e2847b6fdbbe8f2eca10e5f9927874d7d4a2d528
BuildRequires:  ruby >= 2.1

Requires: rubygem-fluentd >= 0.14.0, rubygem-fluentd < 2.0.0
BuildArch: noarch

%description
Fluentd Filter plugin to concatenate multiline log separated in multiple events.

%prep
%setup -q -c -T

%build

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{SOURCE0}

%files
%defattr(-,root,root,-)
%{gemdir}

%changelog
*   Thu Aug 22 2019 Stanislav Hadjiiski <hadjiiskis@vmware.com> 2.4.0-1
-   Initial build
