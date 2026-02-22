%global build_if %{photon_subrelease} <= 91
%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%define gem_name rubyzip

Name:           rubygem-rubyzip
Version:        2.4.1
Release:        1.1%{?dist}
Summary:        Ruby library for reading and writing Zip files
Group:          Applications/Programming
Vendor:         VMware, Inc.
Distribution:   Photon
URL: https://rubygems.org/gems/%{gem_name}
Source0: https://rubygems.org/downloads/%{gem_name}-%{version}.gem

Source1: license.txt
%include %{SOURCE1}

Provides:      rubygem-zip <= 2.0.2-9
Obsoletes:     rubygem-zip <= 2.0.2-9

BuildRequires: ruby-devel

Requires: ruby

%description
Ruby library for reading and writing Zip files

%prep
%gem_unpack %{SOURCE0}

%build
%gem_build

%install
%gem_install

%check
cd %{buildroot}%{gemdir}/gems/zip-%{version}
gem install jeweler
rake test

%files
%defattr(-,root,root,-)
%{gemdir}

%changelog
* Fri Feb 13 2026 Shivani Agarwal <shivani.agarwal@broadcom.com> 2.4.1-1.1
- Bump after moving to SPECS/91
* Tue May 06 2025 Shivani Agarwal <shivani.agarwal@broadcom.com> 2.4.1-1
- Initial version
