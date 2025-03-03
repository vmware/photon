%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name activesupport

Name: rubygem-activesupport
Version:        7.0.8.5
Release:        1%{?dist}
Summary:        Support libaries for Rails framework.
Group:          Development/Languages
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://rubygems.org/gems/activesupport/versions/%{version}

Source0:        https://rubygems.org/downloads/activesupport-%{version}.gem
%define sha512  activesupport=d9a3bcb2b06c8015eb47047d63282929d212a34c23205159be7a7e328d3e2f1639635a6e268ff0dd43c9b9a310208eac0a66e7ed57eb97e58bf41bdb90e55859

Source1: license.txt
%include %{SOURCE1}

BuildRequires:  ruby-devel
BuildRequires:  rubygem-concurrent-ruby
BuildRequires:  rubygem-i18n
BuildRequires:  rubygem-tzinfo

Requires: ruby
Requires: rubygem-i18n
Requires: rubygem-concurrent-ruby
Requires: rubygem-tzinfo

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
*   Thu Feb 27 2025 Shivani Agarwal <shivani.agarwal@broadcom.com> 7.0.8.5-1
-   Fix CVE-2024-28103
*   Wed Dec 11 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 7.0.4-3
-   Release bump for SRP compliance
*   Fri Dec 15 2023 Shivani Agarwal <shivania2@vmware.com> 7.0.4-2
-   Fix requires
*   Wed Aug 17 2022 Gerrit Photon <photon-checkins@vmware.com> 7.0.4-1
-   Automatic Version Bump
*   Mon Sep 21 2020 Gerrit Photon <photon-checkins@vmware.com> 6.0.3.3-1
-   Automatic Version Bump
*   Mon Jun 22 2020 Gerrit Photon <photon-checkins@vmware.com> 6.0.3.2-1
-   Automatic Version Bump
*   Tue Sep 11 2018 srinidhira0 <srinidhir@vmware.com> 5.2.1-1
-   Update to version 5.2.1
*   Fri Aug 25 2017 Kumar Kaushik <kaushikk@vmware.com> 5.0.0.1-1
-   Initial build
