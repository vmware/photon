%global build_if %{photon_subrelease} >= 92
%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name declarative

Summary:        DSL for nested generic schemas with inheritance and refining.
Name:           rubygem-declarative
Version:        0.0.20
Release:        3%{?dist}
Group:          Development/Languages
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://rubygems.org/gems/%{gem_name}

Source0: https://rubygems.org/downloads/%{gem_name}-%{version}.gem

Source1: license.txt
%include %{SOURCE1}

BuildRequires: ruby-devel

Requires: ruby
Requires: rubygem-uber

%description
DSL for nested generic schemas with inheritance and refining.

%prep
%gem_unpack %{SOURCE0}

%build
%gem_build

%install
%gem_install

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root,-)
%{gemdir}

%changelog
* Mon Jan 19 2026 Shivani Agarwal <shivani.agarwal@broadcom.com>  0.0.20-3
- bump version with ruby upgrade
* Tue May 06 2025 Shivani Agarwal <shivani.agarwal@broadcom.com> 0.0.20-2
- Spec bump with ruby upgrade
* Fri Feb 07 2025 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 0.0.20-1
- Initial version.
