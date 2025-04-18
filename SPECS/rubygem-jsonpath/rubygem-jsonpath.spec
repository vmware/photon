%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name jsonpath

Name:           rubygem-jsonpath
Version:        1.1.5
Release:        3%{?dist}
Summary:        Ruby Gem for JSONPath implementation
Group:          Development/Languages
Vendor:         VMware, Inc.
URL:            https://rubygems.org/gems/%{gem_name}
Distribution:   Photon

Source0: https://rubygems.org/downloads/%{gem_name}-%{version}.gem
%define sha512 %{gem_name}=c5f70c24c47cb703af25ac3302b3e4312f174c754d24965fd67c6b1ab0986c43a684a542e6fe520f14cf3765b3dec48306bd7321ed6a7b57dc6a5de4c78fdc42

Source1: license.txt
%include %{SOURCE1}

BuildRequires: ruby-devel
BuildRequires: rubygem-multi_json

Requires: ruby
Requires: rubygem-multi_json

%description
JSONPath is a lightweight library to search and extract data from JSON documents.

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
* Thu Apr 17 2025 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 1.1.5-3
- Build gems properly
* Mon Feb 26 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 1.1.5-2
- Bump Version to build with new ruby
* Fri Oct 20 2023 Shreenidhi Shedi <sshedi@vmware.com> 1.1.5-1
- Initial version.
- Needed by rubygem-fluent-plugin-kubernetes_metadata_filter.
