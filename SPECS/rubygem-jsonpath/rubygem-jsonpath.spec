%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name jsonpath

Name:           rubygem-jsonpath
Version:        1.1.5
Release:        2%{?dist}
Summary:        Ruby Gem for JSONPath implementation
Group:          Development/Languages
Vendor:         VMware, Inc.
URL:            https://rubygems.org/gems/%{gem_name}
Distribution:   Photon

Source0: https://rubygems.org/downloads/%{gem_name}-%{version}.gem

Source1: license.txt
%include %{SOURCE1}

BuildRequires: ruby

Requires: ruby
Requires: rubygem-multi_json

%description
JSONPath is a lightweight library to search and extract data from JSON documents.

%prep
%autosetup -p1 -n %{gem_name}-%{version}

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{SOURCE0}

%files
%defattr(-,root,root,-)
%{gemdir}

%changelog
* Wed Dec 11 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 1.1.5-2
- Release bump for SRP compliance
* Fri Dec 15 2023 Shivani Agarwal <shivania2@vmware.com> 1.1.5-1
- Initial version.
- Needed by rubygem-fluent-plugin-kubernetes_metadata_filter.
