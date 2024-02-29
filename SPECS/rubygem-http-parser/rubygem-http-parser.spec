%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name http-parser
%global ruby_ver 3.3.0

Name:           rubygem-http-parser
Version:        1.2.3
Release:        2%{?dist}
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
* Wed Feb 28 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 1.2.3-2
- Update build command, to build with source code
* Fri Oct 20 2023 Shreenidhi Shedi <sshedi@vmware.com> 1.2.3-1
- Initial version.
- Needed by rubygem-http-4.4.1.
