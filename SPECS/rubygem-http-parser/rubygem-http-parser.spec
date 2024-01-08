%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name http-parser

Name:           rubygem-http-parser
Version:        1.2.3
Release:        1%{?dist}
Summary:        An easy-to-use client library for making requests from Ruby.
Group:          Development/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
License:        MIT
URL:            https://rubygems.org/gems/%{gem_name}

Source0: https://rubygems.org/downloads/%{gem_name}-%{version}.gem
%define sha512 %{gem_name}=03c34c3e8174d9010440483af34800b74a7bbddd5daa63607e6aa2254d9c91cf36d90854ea65827b32680432de278aeeb7b8878f788f124c150f163409fa5107

BuildRequires: ruby
BuildRequires: rubygem-ffi-compiler

Requires: rubygem-ffi-compiler
Requires: ruby

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
* Mon Jan 08 2024 Shivani Agarwal <shivania2@vmware.com> 1.2.3-1
- Initial version.
- Needed by rubygem-http
