%global build_if %{photon_subrelease} >= 92
%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name google-apis-core

Summary:        Common utility and base classes for legacy Google REST clients
Name:           rubygem-google-apis-core
Version:        1.0.2
Release:        1%{?dist}
Group:          Development/Languages
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://rubygems.org/gems/%{gem_name}

Source0: https://rubygems.org/downloads/%{gem_name}-%{version}.gem

Source1: license.txt
%include %{SOURCE1}

BuildRequires: ruby-devel
BuildRequires: rubygem-addressable
BuildRequires: rubygem-faraday-follow_redirects
BuildRequires: rubygem-googleauth
BuildRequires: rubygem-httpclient
BuildRequires: rubygem-mini_mime
BuildRequires: rubygem-representable
BuildRequires: rubygem-retriable
BuildRequires: rubygem-webrick

Requires: ruby
Requires: rubygem-addressable
Requires: rubygem-faraday-follow_redirects >= 0.3
Requires: rubygem-googleauth
Requires: rubygem-httpclient
Requires: rubygem-mini_mime
Requires: rubygem-representable
Requires: rubygem-retriable
Requires: rubygem-webrick

%description
Common utility and base classes for legacy Google REST clients

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
* Mon Jan 19 2026 Shivani Agarwal <shivani.agarwal@broadcom.com> 1.0.2-1
- Update to version 1.0.2
* Tue May 06 2025 Shivani Agarwal <shivani.agarwal@broadcom.com> 0.16.0-2
- Spec bump with ruby upgrade
* Fri Feb 07 2025 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 0.16.0-1
- Initial version.
