%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%define gem_name rubyzip

Name:           rubygem-rubyzip
Version:        2.3.2
Release:        2%{?dist}
Summary:        Ruby library for reading and writing Zip files
Group:          Applications/Programming
Vendor:         VMware, Inc.
Distribution:   Photon
URL: https://rubygems.org/gems/%{gem_name}

Source0: https://rubygems.org/downloads/%{gem_name}-%{version}.gem
%define sha512   %{gem_name}=ded141768b205cca10da6eed62cb744111008703f0cd1377b2edba59f0fa66e3a209e43c10a86749088c9517238b4dcac6173b56ebca4e4b8340632d1794bcd2

Source1: license.txt
%include %{SOURCE1}

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

%if 0%{?with_check}
%check
cd %{buildroot}%{gemdir}/gems/zip-%{version}
gem install jeweler
rake test
%endif

%files
%defattr(-,root,root,-)
%{gemdir}

%changelog
* Thu Apr 17 2025 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 2.3.2-2
- Build gems properly
* Mon Feb 26 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 2.3.2-1
- Initial Version
