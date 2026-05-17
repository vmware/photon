%global build_if %{photon_subrelease} >= 91
%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name googleauth

Summary:        Google Auth Library for Ruby
Name:           rubygem-googleauth
Version:        1.16.1
Release:        2%{?dist}
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
* Fri May 15 2026 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 1.16.1-2
- Extended to build for subrelease 91 and above
* Fri Feb 13 2026 Shivani Agarwal <shivani.agarwal@broadcom.com> 1.16.1-1
- Update to version 1.16.1
* Thu Feb 12 2026 Shivani Agarwal <shivani.agarwal@broadcom.com> 1.13.1-3
- Spec bump with rubygem-faraday upgrade
* Tue May 06 2025 Shivani Agarwal <shivani.agarwal@broadcom.com> 1.13.1-2
- Spec bump with ruby upgrade
* Fri Feb 07 2025 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 1.13.1-1
- Initial version.
