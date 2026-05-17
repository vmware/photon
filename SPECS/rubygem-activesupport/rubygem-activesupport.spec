%global build_if %{photon_subrelease} >= 91
%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name activesupport

Name: rubygem-activesupport
Version:        8.1.3
Release:        2%{?dist}
Summary:        Support libaries for Rails framework.
Group:          Development/Languages
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://rubygems.org/gems/activesupport/versions/%{version}

Source0:        https://rubygems.org/downloads/activesupport-%{version}.gem

Source1: license.txt
%include %{SOURCE1}

BuildRequires:  ruby-devel
BuildRequires:  ruby
BuildRequires:  rubygem-concurrent-ruby
BuildRequires:  rubygem-connection_pool
BuildRequires:  rubygem-i18n
BuildRequires:  rubygem-tzinfo

Requires: ruby
Requires: rubygem-concurrent-ruby >= 1.3.1
Requires: rubygem-connection_pool >= 2.2.5
Requires: rubygem-i18n >= 1.6
Requires: rubygem-tzinfo >= 2.0.5

%description
A toolkit of support libraries and Ruby core extensions extracted from the
Rails framework. Rich support for multibyte strings, internationalization,
time zones, and testing.

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
* Fri May 15 2026 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 8.1.3-2
- Extended to build for subrelease 91 and above
* Thu Apr 02 2026 Shivani Agarwal <shivani.agarwal@broadcom.com> 8.1.3-1
- Update to version 8.1.3
* Wed Apr 01 2026 Shivani Agarwal <shivani.agarwal@broadcom.com> 7.0.8.7-2
- Fix CVE-2026-33176, CVE-2026-33170 and CVE-2026-33169
* Tue May 06 2025 Shivani Agarwal <shivani.agarwal@broadcom.com> 7.0.8.7-1
- Upgrade to 7.0.8.7
* Thu Feb 27 2025 Shivani Agarwal <shivani.agarwal@broadcom.com> 7.0.8.5-1
- Fix CVE-2024-28103
* Wed Dec 11 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 7.0.4-3
- Release bump for SRP compliance
* Fri Dec 15 2023 Shivani Agarwal <shivania2@vmware.com> 7.0.4-2
- Fix requires
* Wed Aug 17 2022 Gerrit Photon <photon-checkins@vmware.com> 7.0.4-1
- Automatic Version Bump
* Mon Sep 21 2020 Gerrit Photon <photon-checkins@vmware.com> 6.0.3.3-1
- Automatic Version Bump
* Mon Jun 22 2020 Gerrit Photon <photon-checkins@vmware.com> 6.0.3.2-1
- Automatic Version Bump
* Tue Sep 11 2018 srinidhira0 <srinidhir@vmware.com> 5.2.1-1
- Update to version 5.2.1
* Fri Aug 25 2017 Kumar Kaushik <kaushikk@vmware.com> 5.0.0.1-1
- Initial build
