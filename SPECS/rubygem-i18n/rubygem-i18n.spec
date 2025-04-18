%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name i18n

Name:           rubygem-i18n
Version:        1.14.1
Release:        2%{?dist}
Summary:        Support for ruby.
Group:          Development/Languages
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://rubygems.org/gems/i18n/versions/%{version}

Source0: https://rubygems.org/downloads/i18n-%{version}.gem
%define sha512 %{gem_name}=7b94b63c8cc318166e18596689c5b81222834c874d89dd4e076dde2a2aac902d0192d4b4efd84dbe7738420bd40a9b00665da058e7873bbcead307447ce82f41

Source1: license.txt
%include %{SOURCE1}

BuildRequires: ruby-devel
BuildRequires: rubygem-concurrent-ruby

Requires: ruby
Requires: rubygem-concurrent-ruby

%description
New wave Internationalization support for Ruby.

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
*   Thu Apr 17 2025 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 1.14.1-2
-   Build gems properly
*   Mon Feb 26 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 1.14.1-1
-   Update to version 1.14.1
* Sat Oct 21 2023 Shreenidhi Shedi <sshedi@vmware.com> 1.12.0-2
- Fix requires
* Wed Aug 17 2022 Gerrit Photon <photon-checkins@vmware.com> 1.12.0-1
- Automatic Version Bump
* Mon Jun 22 2020 Gerrit Photon <photon-checkins@vmware.com> 1.8.5-1
- Automatic Version Bump
* Tue Sep 11 2018 srinidhira0 <srinidhir@vmware.com> 1.1.0-1
- Update to version 1.1.0
* Fri Aug 25 2017 Kumar Kaushik <kaushikk@vmware.com> 0.8.6-1
- Initial build
