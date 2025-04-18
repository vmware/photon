%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name fiber-local

Name:           rubygem-fiber-local
Version:        1.0.0
Release:        3%{?dist}
Summary:        Provides a class-level mixin to make fiber local state easy.
Group:          Development/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}

Source0: https://rubygems.org/downloads/%{gem_name}-%{version}.gem
%define sha512 %{gem_name}=6784f91c8eb37c553e34e476cc85bf5b985b086913e045dcecc28e2b5ead093d158e10d51f6d7a0e1f16a3e466825ec1fe771071a4688301befd327b78013e81

Source1: license.txt
%include %{SOURCE1}

BuildRequires: ruby-devel
BuildRequires: rubygem-io-event

Requires: ruby
Requires: rubygem-io-event

BuildArch: noarch

%description
%{summary}

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
* Thu Apr 17 2025 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 1.0.0-3
- Build gems properly
* Mon Feb 26 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 1.0.0-2
- Bump Version to build with new ruby
* Wed Oct 18 2023 Shreenidhi Shedi <sshedi@vmware.com> 1.0.0-1
- Initial version. Needed by rubygem-async packages.
