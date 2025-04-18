%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name google-cloud-core

Summary:        google-cloud-core is the internal shared library for google-cloud-ruby.
Name:           rubygem-google-cloud-core
Version:        1.7.1
Release:        2%{?dist}
Group:          Development/Languages
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://rubygems.org/gems/%{gem_name}

Source0: https://rubygems.org/downloads/%{gem_name}-%{version}.gem
%define sha512 %{gem_name}=308545210f816438d6d7abdbf61bac72084bb6c9f2c7b870fd3dde748c742f6da7011ec18a9425a092b89c917d7f2468a2c326b9e66ec55176676878ed4c2385

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
* Thu Apr 17 2025 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 1.7.1-2
- Build gems properly
* Fri Feb 07 2025 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 1.7.1-1
- Initial version.
