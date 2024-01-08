%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name fluent-plugin-concat

Name: rubygem-fluent-plugin-concat
Version:        2.4.0
Release:        3%{?dist}
Summary:        Fluentd Filter plugin to concat multiple event messages.
Group:          Development/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
License:        MIT
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}
Source0:        https://rubygems.org/downloads/fluent-plugin-concat-%{version}.gem
%define sha512  fluent-plugin-concat=4866cfac85f61319ec889519f1b514dd34f51b02415b9ce6b9b2d32ccbacd630932f4acc66a07204a764d37762a7597c9102d56ff83bcb30f6c31543b70a34e1

BuildRequires:  ruby >= 2.1

Requires:       rubygem-fluentd >= 0.14.0
Requires:       rubygem-fluentd < 2.0.0
Requires:       rubygem-tzinfo-data
Requires:       ruby

BuildArch: noarch

%description
Fluentd Filter plugin to concatenate multiline log separated in multiple events.

%prep
%autosetup -c -T

%build

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{SOURCE0}

%files
%defattr(-,root,root,-)
%{gemdir}

%changelog
*   Fri Jan 5 2024 Shivani Agarwal <shivania2@vmware.com> 2.4.0-3
-   Fix Requires. Needed by rubygem-fluent-plugin-concat
*   Wed Sep 02 2020 Sujay G <gsujay@vmware.com> 2.4.0-2
-   Rebuilt using ruby-2.7.1
*   Thu Aug 22 2019 Stanislav Hadjiiski <hadjiiskis@vmware.com> 2.4.0-1
-   Initial build
