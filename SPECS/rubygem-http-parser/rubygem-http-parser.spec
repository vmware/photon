%global debug_package %{nil}
%global gem_name http-parser

Name:           rubygem-http-parser
Version:        1.2.3
Release:        5%{?dist}
Summary:        An easy-to-use client library for making requests from Ruby.
Group:          Development/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://rubygems.org/gems/%{gem_name}

Source0: https://rubygems.org/downloads/%{gem_name}-%{version}.gem

Source1: license.txt
%include %{SOURCE1}

BuildRequires: ruby-devel
BuildRequires: rubygem-ffi-compiler

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
* Wed Dec 11 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 1.2.3-5
- Release bump for SRP compliance
* Wed Sep 11 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 1.2.3-4
- Remove noarch
* Tue Apr 30 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 1.2.3-3
- Add gem macros
* Mon Apr 22 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 1.2.3-2
- Update build command, to build with source code
* Fri Dec 15 2023 Shivani Agarwal <shivania2@vmware.com> 1.2.3-1
- Initial version.
- Needed by rubygem-http-4.4.1.
