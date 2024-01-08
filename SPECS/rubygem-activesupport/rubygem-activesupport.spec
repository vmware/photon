%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name activesupport

Name: rubygem-activesupport
Version:        7.1.0
Release:        1%{?dist}
Summary:        Support libaries for Rails framework.
Group:          Development/Languages
License:        MIT
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://rubygems.org/gems/activesupport/versions/%{version}
Source0:        https://rubygems.org/downloads/activesupport-%{version}.gem
%define sha512  activesupport=f27dc7a76741bd5a000b2f141e5d8eae9d46406dce95c44acb9f9b2d8bbbbcaedde9889944163cbe0c3f5342c6c48c3b4383c7f7c28bbe189665ea345109d3df

BuildRequires:  ruby

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
%autosetup -c -T

%build

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{SOURCE0}

%files
%defattr(-,root,root,-)
%{gemdir}

%changelog
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
