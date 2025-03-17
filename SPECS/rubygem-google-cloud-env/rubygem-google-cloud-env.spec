%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name google-cloud-env

Summary:        google-cloud-env provides information on the Google Cloud Platform hosting environment.
Name:           rubygem-google-cloud-env
Version:        2.2.1
Release:        1%{?dist}
Group:          Development/Languages
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://rubygems.org/gems/%{gem_name}

Source0: https://rubygems.org/downloads/%{gem_name}-%{version}.gem

Source1: license.txt
%include %{SOURCE1}

BuildRequires: ruby-devel
BuildRequires: rubygem-faraday

Requires: ruby
Requires: rubygem-faraday

%description
This library provides information on the application hosting environment for apps
running on Google Cloud Platform. This includes information on the Google compute
product being used, the current project and credentials, and other information
surfaced via environment variables, the file system, and the Metadata Server.

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
* Fri Feb 07 2025 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 2.2.1-1
- Initial version.
