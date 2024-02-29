%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name llhttp-ffi
%global ruby_ver 3.3.0

Name:           rubygem-llhttp-ffi
Version:        0.5.0
Release:        1%{?dist}
Summary:        An easy-to-use client library for making requests from Ruby.
Group:          Development/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
License:        MIT
URL:            https://rubygems.org/gems/%{gem_name}

Source0: https://rubygems.org/downloads/%{gem_name}-%{version}.gem
%define sha512 %{gem_name}=9e10b360d605ce3ffc15c8c9f63e8ff65dba7d6664859e8fd38c5a3a6411cbd1dff38a52f30b9d2fb95f61a70fcabf680ce973da4d0cef7f48b59215845c1beb

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
gem unpack %{SOURCE0}
%autosetup -p1 -D -T -n  %{gem_name}-%{version}
gem spec %{SOURCE0} -l --ruby > %{gem_name}.gemspec

%build
gem build %{gem_name}.gemspec
gem install %{gem_name}-%{version}.gem

%install
mkdir -p %{buildroot}%{gemdir}
mkdir -p %{buildroot}%{gemdir}/cache
mkdir -p %{buildroot}%{gemdir}/doc
mkdir -p %{buildroot}%{gemdir}/plugins
mkdir -p %{buildroot}%{gemdir}/specifications
mkdir -p %{buildroot}%{gemdir}/gems
mkdir -p %{buildroot}%{gemdir}/extensions/%{_arch}-linux/%{ruby_ver}
cp -pa %{gemdir}/build_info %{buildroot}%{gemdir}/
cp -pa %{gemdir}/cache/%{gem_name}-%{version}.gem %{buildroot}%{gemdir}/cache/
cp -pa %{gemdir}/doc/%{gem_name}-%{version} %{buildroot}%{gemdir}/doc/
cp -pa %{gemdir}/plugins %{buildroot}%{gemdir}/
cp -pa %{gemdir}/specifications/%{gem_name}-%{version}.gemspec %{buildroot}%{gemdir}/specifications
cp -pa %{gemdir}/extensions %{buildroot}%{gemdir}/extensions
cp -pa %{gemdir}/gems/%{gem_name}-%{version} %{buildroot}%{gemdir}/gems
cp -pa %{gemdir}/extensions/%{_arch}-linux/%{ruby_ver}/%{gem_name}-%{version} %{buildroot}%{gemdir}/extensions/%{_arch}-linux/%{ruby_ver}

%files
%defattr(-,root,root,-)
%{gemdir}

%changelog
* Mon Feb 26 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 0.5.0-1
- Update to version 0.5.0
* Fri Oct 20 2023 Shreenidhi Shedi <sshedi@vmware.com> 0.4.0-1
- Initial version.
- Needed by rubygem-fluent-plugin-kubernetes_metadata_filter.
