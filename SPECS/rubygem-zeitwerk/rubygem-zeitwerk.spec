%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name zeitwerk

Name: rubygem-zeitwerk
Version:        2.3.0
Release:        1%{?dist}
Vendor:         VMware, Inc.
Distribution:   Photon
Summary:        Support libaries for Rails framework.
Group:          Development/Languages
License:        MIT
URL:            https://rubygems.org/gems/zeitwerk/versions/%{version}
Source0:        https://rubygems.org/downloads/zeitwerk-%{version}.gem
%define sha1    zeitwerk=b4a665e0adc3cd862264eb3e19578c0a470c2e30
BuildRequires:  ruby >= 2.4.4

%description
Zeitwerk implements constant autoloading with Ruby semantics.
Each gem and application may have their own independent autoloader, with its own configuration,
inflector, and logger. Supports autoloading, reloading, and eager loading.

%prep
%autosetup -c -T

%build

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{SOURCE0}

%files
%defattr(-,root,root,-)
%{gemdir}

%changelog
* Thu Feb 10 2022 Harinadh D <hdommaraju@vmware.com> 2.3.0-1
- Initial release