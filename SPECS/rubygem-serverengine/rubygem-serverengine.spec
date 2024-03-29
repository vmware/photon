%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name serverengine

Name:           rubygem-serverengine
Version:        2.3.0
Release:        2%{?dist}
Summary:        A framework to implement robust multiprocess servers like Unicorn
Group:          Development/Languages
License:        Apache 2
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://rubygems.org/gems/%{gem_name}

Source0: https://rubygems.org/downloads/serverengine-%{version}.gem
%define sha512 %{gem_name}=0887ac556f9f4faa7d8e25743b2f79694153c0e7e39666c8ea02d0313c17835e0e5697da498ad1b23612ec938d8d9f430cfb9699711479ae088011c5a7fee4c4

BuildRequires: ruby

Requires: ruby
Requires: rubygem-sigdump

%description
A framework to implement robust multiprocess servers like Unicorn.

%prep
%autosetup -c -T

%build

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{SOURCE0}

%files
%defattr(-,root,root,-)
%{gemdir}

%changelog
* Mon Oct 23 2023 Shreenidhi Shedi <sshedi@vmware.com> 2.3.0-2
- Fix requires
* Wed Aug 17 2022 Gerrit Photon <photon-checkins@vmware.com> 2.3.0-1
- Automatic Version Bump
* Thu Jul 16 2020 Gerrit Photon <photon-checkins@vmware.com> 2.2.1-1
- Automatic Version Bump
* Tue Jul 24 2018 Srinidhi Rao <srinidhir@vmware.com> 2.0.7-1
- Initial build
