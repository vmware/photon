%global build_if %{photon_subrelease} <= 91
%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name google-cloud-core

Summary:        google-cloud-core is the internal shared library for google-cloud-ruby.
Name:           rubygem-google-cloud-core
Version:        1.8.0
Release:        1.1%{?dist}
Group:          Development/Languages
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://rubygems.org/gems/%{gem_name}

Source0: https://rubygems.org/downloads/%{gem_name}-%{version}.gem

Source1: license.txt
%include %{SOURCE1}

BuildRequires: ruby-devel
BuildRequires: rubygem-retriable
BuildRequires: rubygem-httpclient
BuildRequires: rubygem-addressable
BuildRequires: rubygem-googleauth
BuildRequires: rubygem-google-cloud-env
BuildRequires: rubygem-google-cloud-errors

Requires: ruby
Requires: rubygem-retriable
Requires: rubygem-httpclient
Requires: rubygem-addressable
Requires: rubygem-googleauth
Requires: rubygem-google-cloud-env
Requires: rubygem-google-cloud-errors

%description
google-cloud-core is the internal shared library for google-cloud-ruby.

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
* Fri Feb 13 2026 Shivani Agarwal <shivani.agarwal@broadcom.com> 1.8.0-1.1
- Bump after moving to SPECS/91
* Tue May 06 2025 Shivani Agarwal <shivani.agarwal@broadcom.com> 1.8.0-1
- Upgrade to 1.8.0
* Fri Feb 07 2025 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 1.7.1-1
- Initial version.
