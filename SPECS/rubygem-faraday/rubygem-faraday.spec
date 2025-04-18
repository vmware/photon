%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name faraday

Summary:        HTTP/REST API client library.
Name:           rubygem-faraday
Version:        2.12.2
Release:        2%{?dist}
Group:          Development/Languages
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://rubygems.org/gems/%{gem_name}

Source0: https://rubygems.org/downloads/%{gem_name}-%{version}.gem
%define sha512 %{gem_name}=1cae919a782b17e62abbbf6f41a6ce16f48dc0500d354694cdae4e7b5fd0b8cac3b6fd4a6a8f1284c50fc4de1db65283a7185d757135fea76f65404175ef8efd

Source1: license.txt
%include %{SOURCE1}

BuildRequires: ruby-devel
BuildRequires: rubygem-faraday-net_http

Requires: ruby
Requires: rubygem-faraday-net_http

%description
HTTP/REST API client library.

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
* Thu Apr 17 2025 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 2.12.2-2
- Build gems properly
* Fri Feb 07 2025 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 2.12.2-1
- Initial version.
