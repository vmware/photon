%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name fluent-plugin-remote_syslog

Name:           rubygem-fluent-plugin-remote_syslog
Summary:        Fluentd output plugin for remote syslog
Version:        1.1.0
Release:        2%{?dist}
Group:          Development/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}
Source0:        https://rubygems.org/downloads/%{gem_name}-%{version}.gem

Source1: license.txt
%include %{SOURCE1}

BuildArch:      noarch

BuildRequires:  ruby >= 2.1

Requires: rubygem-fluentd >= 0
Requires: rubygem-remote_syslog_sender >= 1.1.1

%description
Fluentd plugin for remote syslog protocol

%prep
%autosetup -c -T

%build

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{SOURCE0}

%files
%defattr(-,root,root,-)
%{gemdir}

%changelog
*   Wed Dec 11 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 1.1.0-2
-   Release bump for SRP compliance
*   Mon Oct 31 2022 Gerrit Photon <photon-checkins@vmware.com> 1.1.0-1
-   Automatic Version Bump
*   Wed Sep 02 2020 Sujay G <gsujay@vmware.com> 1.0.0-2
-   Rebuilt using ruby-2.7.1
*   Mon Jan 27 2020 Nikolay Stanchev <nstanchev@vmware.com> 1.0.0-1
-   Initial build
