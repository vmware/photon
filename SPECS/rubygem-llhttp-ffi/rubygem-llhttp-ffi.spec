%global debug_package %{nil}
%global gem_name llhttp-ffi

Name:           rubygem-llhttp-ffi
Version:        0.5.0
Release:        3%{?dist}
Summary:        An easy-to-use client library for making requests from Ruby.
Group:          Development/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
License:        MIT
URL:            https://rubygems.org/gems/%{gem_name}

Source0: https://rubygems.org/downloads/%{gem_name}-%{version}.gem
%define sha512 %{gem_name}=9e10b360d605ce3ffc15c8c9f63e8ff65dba7d6664859e8fd38c5a3a6411cbd1dff38a52f30b9d2fb95f61a70fcabf680ce973da4d0cef7f48b59215845c1beb

BuildRequires: ruby-devel
BuildRequires: rubygem-ffi-compiler

Requires: rubygem-addressable >= 2.3.0, rubygem-addressable < 3.0.0
Requires: rubygem-http-cookie >= 1.0.0, rubygem-http-cookie < 2.0.0
Requires: rubygem-http-form_data >= 2.2.0
Requires: rubygem-http_parser.rb >= 0.6.0, rubygem-http_parser.rb < 0.8.1
Requires: rubygem-http-parser
Requires: rubygem-ffi-compiler
Requires: ruby

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
%{gem_base}

%changelog
* Mon Oct 14 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 0.5.0-3
- Remove noarch
* Tue Apr 30 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 0.5.0-2
- Add gem macros
* Mon Feb 26 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 0.5.0-1
- Update to version 0.5.0
* Fri Oct 20 2023 Shreenidhi Shedi <sshedi@vmware.com> 0.4.0-1
- Initial version.
- Needed by rubygem-fluent-plugin-kubernetes_metadata_filter.
