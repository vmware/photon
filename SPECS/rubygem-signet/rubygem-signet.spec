%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name signet

Summary:        Signet is an OAuth 1.0 / OAuth 2.0 implementation.
Name:           rubygem-signet
Version:        0.19.0
Release:        1%{?dist}
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
* Fri Feb 07 2025 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 0.19.0-1
- Initial version.
