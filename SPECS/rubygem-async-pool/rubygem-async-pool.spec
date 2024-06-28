%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name async-pool

Name:           rubygem-async-pool
Version:        0.4.0
Release:        1%{?dist}
Summary:        A singleplex and multiplex resource pool for implementing robust clients.
Group:          Development/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
License:        MIT
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}

Source0: https://rubygems.org/downloads/%{gem_name}-%{version}.gem
%define sha512 %{gem_name}=6eb66c940a42364a0d2b57aea9131697e18b982de63bbd87955bf12c0dd778508a6e836cc77ebacf36c644b429e630fc66f76710208370c5a0923697a659855c

BuildRequires:  ruby

Requires: ruby
Requires: rubygem-async

BuildArch: noarch

%description
A singleplex and multiplex resource pool for implementing robust clients.

%prep
%autosetup -p1 -n %{gem_name}-%{version}

%build

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{SOURCE0}

%files
%defattr(-,root,root,-)
%{gemdir}

%changelog
* Wed Oct 18 2023 Shreenidhi Shedi <sshedi@vmware.com> 0.4.0-1
- Initial version. Needed by rubygem-async-http.
