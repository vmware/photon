%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name ffi-compiler

Name:           rubygem-ffi-compiler
Version:        1.0.1
Release:        2%{?dist}
Summary:        An easy-to-use client library for making requests from Ruby.
Group:          Development/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://rubygems.org/gems/%{gem_name}

Source0: https://rubygems.org/downloads/%{gem_name}-%{version}.gem

Source1: license.txt
%include %{SOURCE1}

BuildRequires: ruby

Requires: rubygem-ffi
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
* Wed Dec 11 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 1.0.1-2
- Release bump for SRP compliance
* Fri Dec 15 2023 Shivani Agarwal <shivania2@vmware.com> 1.0.1-1
- Initial version.
- Needed by rubygem-http-parser.
