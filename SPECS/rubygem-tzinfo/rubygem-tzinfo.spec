%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name tzinfo

Name:           rubygem-tzinfo
Version:        2.0.6
Release:        2%{?dist}
Summary:        Timezone related support for Ruby.
Group:          Development/Languages
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://rubygems.org/gems/tzinfo/versions/%{version}

Source0: https://rubygems.org/downloads/tzinfo-%{version}.gem
%define sha512 %{gem_name}=4c1b84060c1ec2aa1e7570330fecf1ee753ef45e3921282216dc27d20454a396f2f02906d0f2409c813f2919b23c2a9a28519d99a2f76dca72d8f94b4b95d3ff

Source1: license.txt
%include %{SOURCE1}

BuildRequires: ruby-devel
BuildRequires: rubygem-concurrent-ruby

Requires: ruby
Requires: rubygem-concurrent-ruby

%description
TZInfo provides daylight savings aware transformations between times in different time zones.

%prep
%gem_unpack %{SOURCE0}

%build
%gem_build

%install
%gem_install

%check
cd %{buildroot}%{gemdir}/gems/tzinfo-%{version}
gem install thread_safe
rake test

%files
%defattr(-,root,root,-)
%{gemdir}

%changelog
* Thu Apr 17 2025 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 2.0.6-2
- Build gems properly
* Mon Feb 26 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 2.0.6-1
- Update to version 2.0.6
* Tue Oct 24 2023 Shreenidhi Shedi <sshedi@vmware.com> 2.0.5-2
- Fix requires
* Wed Aug 17 2022 Gerrit Photon <photon-checkins@vmware.com> 2.0.5-1
- Automatic Version Bump
* Mon Jun 22 2020 Gerrit Photon <photon-checkins@vmware.com> 2.0.2-1
- Automatic Version Bump
* Tue Nov 27 2018 Sujay G <gsujay@vmware.com> 1.2.5-2
- Added %check section
* Tue Aug 14 2018 Srinidhi Rao <srinidhir@vmware.com> 1.2.5-1
- Upgraded to 1.2.5
* Fri Aug 25 2017 Kumar Kaushik <kaushikk@vmware.com> 1.2.3-1
- Initial build
