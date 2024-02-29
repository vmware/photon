%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name activesupport

Name:           rubygem-activesupport
Version:        7.1.3.2
Release:        1%{?dist}
Summary:        Support libaries for Rails framework.
Group:          Development/Languages
License:        MIT
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://rubygems.org/gems/activesupport/versions/%{version}

Source0: https://rubygems.org/downloads/activesupport-%{version}.gem
%define sha512 %{gem_name}=50b587e9f6d715bc3c0616e3fa8087b24c4dc837246babf39e4b1d42ed98f85877481b3be1f75d669c4da19df8f645ef644fb8afa16578f921a67576122c792d

BuildRequires:  ruby

Requires: ruby
Requires: rubygem-i18n
Requires: rubygem-concurrent-ruby
Requires: rubygem-connection_pool
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
*   Mon Feb 26 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 7.1.3.2-1
-   Update to version 7.1.3.2
* Wed Oct 18 2023 Shreenidhi Shedi <sshedi@vmware.com> 7.0.4-2
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
