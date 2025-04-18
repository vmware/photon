%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name http

Name:           rubygem-http
Version:        4.4.1
Release:        3%{?dist}
Summary:        An easy-to-use client library for making requests from Ruby.
Group:          Development/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://rubygems.org/gems/%{gem_name}

Source0: https://rubygems.org/downloads/%{gem_name}-%{version}.gem
%define sha512 %{gem_name}=6e43a8ae379d7c8a807a9a03c87bfb5ad1719f9838e26ac7a695220ee2bc50344accc2db268d30da175328fd5468b87ec8532d17ce42a5b74d6c2c4c281d1bc9

Source1: license.txt
%include %{SOURCE1}

BuildRequires: ruby-devel
BuildRequires: rubygem-addressable
BuildRequires: rubygem-http-cookie
BuildRequires: rubygem-http-form_data
BuildRequires: rubygem-http_parser.rb
BuildRequires: rubygem-llhttp-ffi

Requires: rubygem-addressable >= 2.3.0, rubygem-addressable < 3.0.0
Requires: rubygem-http-cookie >= 1.0.0, rubygem-http-cookie < 2.0.0
Requires: rubygem-http-form_data >= 2.2.0
Requires: rubygem-http_parser.rb >= 0.6.0, rubygem-http_parser.rb < 0.8.1
Requires: rubygem-http-parser
Requires: rubygem-llhttp-ffi
Requires: ruby

BuildArch: noarch

%description
An easy-to-use client library for making requests from Ruby. It uses a simple
method chaining system for building requests, similar to Python's Requests.

%prep
%gem_unpack %{SOURCE0}

%build
%gem_build

%install
%gem_install

%files
%defattr(-,root,root,-)
%{gemdir}

%changelog
* Thu Apr 17 2025 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 4.4.1-3
- Build gems properly
* Mon Feb 26 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 4.4.1-2
- Bump Version to build with new ruby
* Fri Oct 20 2023 Shreenidhi Shedi <sshedi@vmware.com> 4.4.1-1
- Initial version.
- Needed by rubygem-http.
