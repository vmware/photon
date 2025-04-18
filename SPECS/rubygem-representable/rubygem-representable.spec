%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name representable

Summary:        Renders and parses JSON/XML/YAML documents from and to Ruby objects.
Name:           rubygem-representable
Version:        3.2.0
Release:        2%{?dist}
Group:          Development/Languages
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://rubygems.org/gems/%{gem_name}

Source0: https://rubygems.org/downloads/%{gem_name}-%{version}.gem
%define sha512 %{gem_name}=a28fa81501e54dc3fc432133126c8ef7868f2ca8038d992c01a0516ed2329721dcab035b6533cf7453c14576299f0266f4603ee62a6ebb935f496be21b6f67ef

Source1: license.txt
%include %{SOURCE1}

BuildRequires: ruby-devel
BuildRequires: rubygem-trailblazer-option
BuildRequires: rubygem-declarative

Requires: ruby
Requires: rubygem-uber
Requires: rubygem-declarative
Requires: rubygem-trailblazer-option
Requires: rubygem-multi_json

%description
Renders and parses JSON/XML/YAML documents from and to Ruby objects.
Includes plain properties, collections, nesting, coercion and more.

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
* Thu Apr 17 2025 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 3.2.0-2
- Build gems properly
* Fri Feb 07 2025 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 3.2.0-1
- Initial version.
