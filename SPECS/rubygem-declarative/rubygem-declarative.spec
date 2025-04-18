%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name declarative

Summary:        DSL for nested generic schemas with inheritance and refining.
Name:           rubygem-declarative
Version:        0.0.20
Release:        2%{?dist}
Group:          Development/Languages
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://rubygems.org/gems/%{gem_name}

Source0: https://rubygems.org/downloads/%{gem_name}-%{version}.gem
%define sha512 %{gem_name}=de162d347ae327725c45779424d8a9f4e25109eb45e5f4bc4f8e8b86ddd347623aa93630f371b766f070f6236e2d03008d481e1e9332073869468abbe3eca822

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
* Thu Apr 17 2025 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 0.0.20-2
- Build gems properly
* Fri Feb 07 2025 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 0.0.20-1
- Initial version.
