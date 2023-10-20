%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name fiber-local

Name:           rubygem-fiber-local
Version:        1.0.0
Release:        1%{?dist}
Summary:        Provides a class-level mixin to make fiber local state easy.
Group:          Development/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
License:        MIT
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}

Source0: https://rubygems.org/downloads/%{gem_name}-%{version}.gem
%define sha512 %{gem_name}=6784f91c8eb37c553e34e476cc85bf5b985b086913e045dcecc28e2b5ead093d158e10d51f6d7a0e1f16a3e466825ec1fe771071a4688301befd327b78013e81

BuildRequires:  ruby

Requires: ruby
Requires: rubygem-io-event

BuildArch: noarch

%description
%{summary}

%prep
%autosetup -p1 -n %{gem_name}-%{version}

%build

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{SOURCE0}

%files
%defattr(-,root,root,-)
%{gemdir}

%changelog
* Wed Oct 18 2023 Shreenidhi Shedi <sshedi@vmware.com> 1.0.0-1
- Initial version. Needed by rubygem-async packages.
