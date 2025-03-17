%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name googleauth

Summary:        Google Auth Library for Ruby
Name:           rubygem-googleauth
Version:        1.13.1
Release:        1%{?dist}
Group:          Development/Languages
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://rubygems.org/gems/%{gem_name}

Source0: https://rubygems.org/downloads/%{gem_name}-%{version}.gem

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
* Fri Feb 07 2025 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 1.13.1-1
- Initial version.
