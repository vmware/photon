%global build_if %{photon_subrelease} >= 91
%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name signet

Summary:        Signet is an OAuth 1.0 / OAuth 2.0 implementation.
Name:           rubygem-signet
Version:        0.21.0
Release:        2%{?dist}
Group:          Development/Languages
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://rubygems.org/gems/%{gem_name}

Source0: https://rubygems.org/downloads/%{gem_name}-%{version}.gem

Source1: license.txt
%include %{SOURCE1}

BuildRequires: ruby-devel
BuildRequires: rubygem-multi_json
BuildRequires: rubygem-jwt
BuildRequires: rubygem-faraday
BuildRequires: rubygem-addressable

Requires: ruby
Requires: rubygem-addressable
Requires: rubygem-faraday
Requires: rubygem-jwt
Requires: rubygem-multi_json

%description
Signet is an OAuth 1.0 / OAuth 2.0 implementation.

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
* Fri May 15 2026 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 0.21.0-2
- Extended to build for subrelease 91 and above
* Fri Feb 13 2026 Shivani Agarwal <shivani.agarwal@broadcom.com> 0.21.0-1
- Update to version 0.21.0
* Thu Feb 12 2026 Shivani Agarwal <shivani.agarwal@broadcom.com> 0.20.0-2
- Spec bump with rubygem-faraday upgrade
* Tue May 06 2025 Shivani Agarwal <shivani.agarwal@broadcom.com> 0.20.0-1
- Upgrade to 0.20.0
* Fri Feb 07 2025 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 0.19.0-1
- Initial version.
