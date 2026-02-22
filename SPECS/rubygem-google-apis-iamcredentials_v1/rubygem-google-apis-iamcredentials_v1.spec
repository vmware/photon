%global build_if %{photon_subrelease} >= 92
%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name google-apis-iamcredentials_v1

Summary:        This is a simple REST client for IAM Service Account Credentials API V1.
Name:           rubygem-google-apis-iamcredentials_v1
Version:        0.26.0
Release:        1%{?dist}
Group:          Development/Languages
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://rubygems.org/gems/%{gem_name}

Source0: https://rubygems.org/downloads/%{gem_name}-%{version}.gem

Source1: license.txt
%include %{SOURCE1}

BuildRequires: ruby-devel
BuildRequires: rubygem-google-apis-core

Requires: ruby
Requires: rubygem-google-apis-core

%description
This is a simple REST client for IAM Service Account Credentials API V1.

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
* Mon Jan 19 2026 Shivani Agarwal <shivani.agarwal@broadcom.com> 0.26.0-1
- Update to version 0.26.0
* Tue May 06 2025 Shivani Agarwal <shivani.agarwal@broadcom.com> 0.22.0-2
- Spec bump with ruby upgrade
* Fri Feb 07 2025 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 0.22.0-1
- Initial version.
