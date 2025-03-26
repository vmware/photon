%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name fluent-plugin-systemd

Name: rubygem-fluent-plugin-systemd
Version:        1.0.5
Release:        2%{?dist}
Summary:        This is a fluentd input plugin. It reads logs from the systemd journal.
Group:          Development/Languages
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}
Source0:        https://rubygems.org/downloads/fluent-plugin-systemd-%{version}.gem

Source1: license.txt
%include %{SOURCE1}
BuildRequires:  ruby

Requires: rubygem-fluentd >= 0.14.11
Requires: rubygem-fluentd < 2.0.0
Requires: systemd
Requires: rubygem-systemd-journal > 1.3.2

%description
This is a fluentd input plugin. It reads logs from the systemd journal.

%prep
%autosetup -c -T

%build

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{SOURCE0}

%files
%defattr(-,root,root,-)
%{gemdir}

%changelog
*   Wed Dec 11 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 1.0.5-2
-   Release bump for SRP compliance
*   Wed Aug 17 2022 Gerrit Photon <photon-checkins@vmware.com> 1.0.5-1
-   Automatic Version Bump
*   Thu Jul 16 2020 Gerrit Photon <photon-checkins@vmware.com> 1.0.2-1
-   Automatic Version Bump
*   Thu Aug 16 2018 Srinidhi Rao <srinidhir@vmware.com> 1.0.1-2
-   Added the dependency on rubygem-systemd-journal
*   Tue Jul 24 2018 Srinidhi Rao <srinidhir@vmware.com> 1.0.1-1
-   Initial build
