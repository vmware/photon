%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name i18n

Name:           rubygem-i18n
Version:        1.12.0
Release:        2%{?dist}
Summary:        Support for ruby.
Group:          Development/Languages
License:        MIT
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://rubygems.org/gems/i18n/versions/%{version}

Source0: https://rubygems.org/downloads/i18n-%{version}.gem
%define sha512 %{gem_name}=7b8af5bb6146c0d2333c7d319276ca45e1c360354636f02f3c64bc113c8877388fbca77a0f49e5d5f6b6eb97e79f74ddba0fff0d689a940dc2879a2741cd9e16

BuildRequires: ruby

Requires: ruby
Requires: rubygem-concurrent-ruby

%description
New wave Internationalization support for Ruby.

%prep
%autosetup -c -T

%build

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{SOURCE0}

%files
%defattr(-,root,root,-)
%{gemdir}

%changelog
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
