%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name llhttp-ffi

Name:           rubygem-llhttp-ffi
Version:        0.4.0
Release:        1%{?dist}
Summary:        An easy-to-use client library for making requests from Ruby.
Group:          Development/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
License:        MIT
URL:            https://rubygems.org/gems/%{gem_name}

Source0: https://rubygems.org/downloads/%{gem_name}-%{version}.gem
%define sha512 %{gem_name}=66ed073e435853f74fc936d8f90bf913fb5ec36e1db85ac5797248f8c4632a490f3bb3ca4efea7fb90941295bd732bb51c31e717281ce737f192b3a45d8778d5

BuildRequires: ruby
BuildRequires: rubygem-ffi-compiler

Requires: rubygem-addressable >= 2.3.0, rubygem-addressable < 3.0.0
Requires: rubygem-http-cookie >= 1.0.0, rubygem-http-cookie < 2.0.0
Requires: rubygem-http-form_data >= 2.2.0
Requires: rubygem-http_parser.rb >= 0.6.0, rubygem-http_parser.rb < 0.8.1
Requires: rubygem-http-parser
Requires: rubygem-ffi-compiler
Requires: ruby

BuildArch: noarch

%description
An easy-to-use client library for making requests from Ruby. It uses a simple
method chaining system for building requests, similar to Python's Requests.

%prep
%autosetup -p1 -n %{gem_name}-%{version}

%build

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{SOURCE0}

%files
%defattr(-,root,root,-)
%{gemdir}

%changelog
* Fri Oct 20 2023 Shreenidhi Shedi <sshedi@vmware.com> 0.4.0-1
- Initial version.
- Needed by rubygem-fluent-plugin-kubernetes_metadata_filter.
