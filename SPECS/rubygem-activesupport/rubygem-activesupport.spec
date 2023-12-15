%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name activesupport

Name: rubygem-activesupport
Version:        7.0.4
Release:        2%{?dist}
Summary:        Support libaries for Rails framework.
Group:          Development/Languages
License:        MIT
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://rubygems.org/gems/activesupport/versions/%{version}
Source0:        https://rubygems.org/downloads/activesupport-%{version}.gem
%define sha512    activesupport=54859a1cccda0940a91be3be8a68087a4cb8ae6f5850dc3ae92bb79a722b04f34a5d9a61456146c2d7c994e95cd5f1b40c16766e0ef54828acc91edb5aba1d2b
BuildRequires:  ruby

Requires: ruby
Requires: rubygem-i18n
Requires: rubygem-concurrent-ruby
Requires: rubygem-tzinfo

%description
A toolkit of support libraries and Ruby core extensions extracted from the
Rails framework. Rich support for multibyte strings, internationalization,
time zones, and testing.

%prep
%autosetup -c -T

%build

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{SOURCE0}

%files
%defattr(-,root,root,-)
%{gemdir}

%changelog
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
