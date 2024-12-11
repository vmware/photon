%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name fluent-plugin-vmware-loginsight

Name: rubygem-fluent-plugin-vmware-loginsight
Version:        1.3.0
Release:        2%{?dist}
Summary:        Fluent output plugin to forward logs to VMware Log Insight.
Group:          Development/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}
Source0:        https://rubygems.org/downloads/%{gem_name}-%{version}.gem
%define sha512    fluent-plugin-vmware-loginsight=e076332f0905e73614186e218f86e8df592d9b0aad2c4f09cf825c3c1383ad402b64580642e89ed86a95d76cbfabe8cec6236ed57a2823bbae986ee51e050fa3

Source1: license.txt
%include %{SOURCE1}
BuildRequires:  ruby >= 2.1

Requires: rubygem-fluentd >= 0.14.10, rubygem-fluentd < 2.0.0
BuildArch: noarch

%description
Fluent output plugin to forward logs to VMware Log Insight.

%prep
%autosetup -c -T

%build

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{SOURCE0}

%files
%defattr(-,root,root,-)
%{gemdir}

%changelog
*   Wed Dec 11 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 1.3.0-2
-   Release bump for SRP compliance
*   Wed Aug 17 2022 Gerrit Photon <photon-checkins@vmware.com> 1.3.0-1
-   Automatic Version Bump
*   Thu Jul 16 2020 Gerrit Photon <photon-checkins@vmware.com> 0.1.10-1
-   Automatic Version Bump
*   Fri Aug 23 2019 Stanislav Hadjiiski <hadjiiskis@vmware.com> 0.1.5-1
-   Initial build
