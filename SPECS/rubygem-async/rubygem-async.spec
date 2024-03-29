%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name async

Name:           rubygem-async
Version:        2.2.1
Release:        2%{?dist}
Summary:        Async provides a modern asynchronous I/O framework for Ruby, based on nio4r.
Group:          Development/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
License:        MIT
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}
Source0:        https://rubygems.org/downloads/%{gem_name}-%{version}.gem

%define sha512 %{gem_name}=5a4654eeec8dbb092b4d3e6b425fe48ef818110710cd442f36e0e939d185d06aa7bf0d82e0eae690e26fa608ce853dab71d28c8f21a8a7dc80b9ebe9b60d26f3

BuildRequires:  ruby

Requires: rubygem-console >= 1.0.0, rubygem-console < 2.0.0
Requires: rubygem-nio4r >= 2.3.0, rubygem-nio4r < 3.0.0
Requires: rubygem-timers >= 4.1.0, rubygem-timers < 5.0.0
Requires: rubygem-fiber-local
Requires: ruby

BuildArch: noarch

%description
Async provides a modern asynchronous I/O framework for Ruby, based on nio4r.
It implements the reactor pattern, providing both IO and timer based events.

%prep
%autosetup -c -T

%build

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{SOURCE0}

%files
%defattr(-,root,root,-)
%{gemdir}

%changelog
* Wed Oct 18 2023 Shreenidhi Shedi <sshedi@vmware.com> 2.2.1-2
- Fix requires
* Wed Aug 17 2022 Gerrit Photon <photon-checkins@vmware.com> 2.2.1-1
- Automatic Version Bump
* Thu Jul 16 2020 Gerrit Photon <photon-checkins@vmware.com> 1.26.2-1
- Automatic Version Bump
* Wed Aug 21 2019 Stanislav Hadjiiski <hadjiiskis@vmware.com> 1.20.1-1
- Initial build
