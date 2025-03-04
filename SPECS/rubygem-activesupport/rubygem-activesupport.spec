%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name activesupport

Name: rubygem-activesupport
Version:        7.1.3.4
Release:        1%{?dist}
Summary:        Support libaries for Rails framework.
Group:          Development/Languages
License:        MIT
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://rubygems.org/gems/activesupport/versions/%{version}

Source0:        https://rubygems.org/downloads/activesupport-%{version}.gem
%define sha512  activesupport=b9cc7cfede2014dcd871b4d2bbec1df14d134111a8b4f51661b9217300b27e6b97fe34db4a541f63b16a51b9b177f4754b83d7cc8bf3acc77106990525b9fc94

BuildRequires: ruby-devel
BuildRequires: rubygem-i18n
BuildRequires: rubygem-concurrent-ruby
BuildRequires: rubygem-tzinfo
BuildRequires: rubygem-base64
BuildRequires: rubygem-connection_pool
BuildRequires: rubygem-drb
BuildRequires: rubygem-ruby2-keywords

Requires: ruby
Requires: rubygem-i18n
Requires: rubygem-concurrent-ruby
Requires: rubygem-tzinfo
Requires: rubygem-base64
Requires: rubygem-connection_pool
Requires: rubygem-drb
Requires: rubygem-ruby2-keywords

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
*   Thu Feb 27 2025 Shivani Agarwal <shivani.agarwal@broadcom.com> 7.1.3.4-1
-   Fix CVE-2024-28103
*   Fri Dec 15 2023 Shivani Agarwal <shivania2@vmware.com> 7.1.0-1
-   Fix requires and upgraded version
*   Mon Sep 21 2020 Gerrit Photon <photon-checkins@vmware.com> 6.0.3.3-1
-   Automatic Version Bump
*   Mon Jun 22 2020 Gerrit Photon <photon-checkins@vmware.com> 6.0.3.2-1
-   Automatic Version Bump
*   Tue Sep 11 2018 srinidhira0 <srinidhir@vmware.com> 5.2.1-1
-   Update to version 5.2.1
*   Fri Aug 25 2017 Kumar Kaushik <kaushikk@vmware.com> 5.0.0.1-1
-   Initial build
