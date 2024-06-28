%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name tzinfo-data

Name:           rubygem-tzinfo-data
Version:        1.2022.6
Release:        2%{?dist}
Summary:        data from the IANA Time Zone database packaged as Ruby modules
Group:          Development/Languages
License:        MIT
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}

Source0: https://rubygems.org/downloads/tzinfo-data-%{version}.gem
%define sha512 %{gem_name}=fd3929465df1c6ee88133743c932f559995d6c6ac9317b5d044d1f24ab5b618f936ba4d6c9689198adffb8b8fea8f38faf85f644d4617d38665b95b6cc3129ed

BuildRequires: ruby

Requires: ruby
Requires: rubygem-tzinfo

%description
TZInfo::Data contains data from the IANA Time Zone database packaged as
Ruby modules for use with TZInfo.

%prep
%autosetup -c -T

%build

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{SOURCE0}

%files
%defattr(-,root,root,-)
%{gemdir}

%changelog
* Tue Oct 24 2023 Shreenidhi Shedi <sshedi@vmware.com> 1.2022.6-2
- Fix requires
* Wed Aug 17 2022 Gerrit Photon <photon-checkins@vmware.com> 1.2022.6-1
- Automatic Version Bump
* Thu Jul 16 2020 Gerrit Photon <photon-checkins@vmware.com> 1.2020.1-1
- Automatic Version Bump
* Tue Jul 24 2018 Srinidhi Rao <srinidhir@vmware.com> 1.2018.5-1
- Initial build
