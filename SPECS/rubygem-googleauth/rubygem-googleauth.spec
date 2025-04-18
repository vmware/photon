%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name googleauth

Summary:        Google Auth Library for Ruby
Name:           rubygem-googleauth
Version:        1.13.1
Release:        2%{?dist}
Group:          Development/Languages
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://rubygems.org/gems/%{gem_name}

Source0: https://rubygems.org/downloads/%{gem_name}-%{version}.gem
%define sha512 %{gem_name}=70729a0238f3d54bf74d8ec52d9c20f2bd6c880ad3214d6e5da582a6b466007887e44f9810a94e10f2820e33f66117f1ebbe3654ebd32d5f342ab26c8342da72

Source1: license.txt
%include %{SOURCE1}

BuildRequires: ruby-devel
BuildRequires: rubygem-signet
BuildRequires: rubygem-os
BuildRequires: rubygem-google-logging-utils
BuildRequires: rubygem-google-cloud-env

Requires: ruby
Requires: rubygem-faraday
Requires: rubygem-jwt
Requires: rubygem-os
Requires: rubygem-google-cloud-env
Requires: rubygem-google-logging-utils
Requires: rubygem-signet

%description
Implements simple authorization for accessing Google APIs, and provides support
for Application Default Credentials.

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
* Thu Apr 17 2025 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 1.13.1-2
- Build gems properly
* Fri Feb 07 2025 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 1.13.1-1
- Initial version.
