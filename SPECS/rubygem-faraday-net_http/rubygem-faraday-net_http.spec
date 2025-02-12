%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name faraday-net_http

Summary:        Faraday adapter for Net::HTTP
Name:           rubygem-faraday-net_http
Version:        3.4.0
Release:        1%{?dist}
Group:          Development/Languages
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://rubygems.org/gems/%{gem_name}

Source0: https://rubygems.org/downloads/%{gem_name}-%{version}.gem
%define sha512 %{gem_name}=4fe2bcc70b07249b8852e700ba8f8ac8060bcf36229c5d74a3f061450d39cb055db0785950d72cd7ca0c0fd636de168d4c5e2a1928940939e082feb5f6223e89

Source1: license.txt
%include %{SOURCE1}

BuildRequires: ruby-devel
BuildRequires: rubygem-net-http

Requires: ruby
Requires: rubygem-net-http
# this also requires rubygem-faraday at runtime
# not adding it to avoid circular dependency during build

%description
Faraday adapter for Net::HTTP

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
* Fri Feb 07 2025 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 3.4.0-1
- Initial version.
