%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name fluent-plugin-concat

Name: rubygem-fluent-plugin-concat
Version:        2.5.0
Release:        2%{?dist}
Summary:        Fluentd Filter plugin to concat multiple event messages.
Group:          Development/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}
Source0:        https://rubygems.org/downloads/fluent-plugin-concat-%{version}.gem

Source1: license.txt
%include %{SOURCE1}
BuildRequires:  ruby >= 2.1

Requires: rubygem-fluentd >= 0.14.0, rubygem-fluentd < 2.0.0
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
*   Wed Dec 11 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 2.5.0-2
-   Release bump for SRP compliance
*   Wed Aug 17 2022 Gerrit Photon <photon-checkins@vmware.com> 2.5.0-1
-   Automatic Version Bump
*   Wed Sep 02 2020 Sujay G <gsujay@vmware.com> 2.4.0-2
-   Rebuilt using ruby-2.7.1
*   Thu Aug 22 2019 Stanislav Hadjiiski <hadjiiskis@vmware.com> 2.4.0-1
-   Initial build
