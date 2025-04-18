%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name fluent-plugin-vmware-loginsight

Name: rubygem-fluent-plugin-vmware-loginsight
Version:        1.4.2
Release:        2%{?dist}
Summary:        Fluent output plugin to forward logs to VMware Log Insight.
Group:          Development/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}

Source0:        https://rubygems.org/downloads/%{gem_name}-%{version}.gem
%define sha512 %{gem_name}=7b8799439f319bc6049f0c81a12ec0c57c6e535db26310915aeec15b6ca14c967cb66752a203e7eff85a8b1891a716f603b34a12f57518753abffad230a5a8c8

Source1: license.txt
%include %{SOURCE1}

BuildArch: noarch

BuildRequires: ruby-devel
BuildRequires: rubygem-fluentd

Requires: ruby
Requires: rubygem-fluentd >= 0.14.10, rubygem-fluentd < 2.0.0

%description
Fluent output plugin to forward logs to VMware Log Insight.

%prep
%gem_unpack %{SOURCE0}

%build
%gem_build

%install
%gem_install

%files
%defattr(-,root,root,-)
%{gemdir}

%changelog
* Thu Apr 17 2025 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 1.4.2-2
- Build gems properly
* Mon Feb 26 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 1.4.2-1
- Update to version 1.4.2
* Wed Aug 17 2022 Gerrit Photon <photon-checkins@vmware.com> 1.3.0-1
- Automatic Version Bump
* Thu Jul 16 2020 Gerrit Photon <photon-checkins@vmware.com> 0.1.10-1
- Automatic Version Bump
* Fri Aug 23 2019 Stanislav Hadjiiski <hadjiiskis@vmware.com> 0.1.5-1
- Initial build
