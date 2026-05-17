%global build_if %{photon_subrelease} <= 90
%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name io-stream

Summary:        Simple IO stream utilities for Ruby
Name:           rubygem-io-stream
Version:        0.6.1
Release:        1.1.1%{?dist}
Group:          Development/Languages
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://rubygems.org/gems/%{gem_name}

Source0: https://rubygems.org/downloads/%{gem_name}-%{version}.gem

Source1: license.txt
%include %{SOURCE1}

BuildRequires: ruby-devel

Requires: ruby

BuildArch:      noarch

%description
A small Ruby gem providing IO stream utilities that abstract and unify
input/output stream handling in Ruby applications.

%prep
%gem_unpack %{SOURCE0}

%build
%gem_build

%install
%gem_install

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root,-)
%{gemdir}

%changelog
* Fri May 15 2026 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 0.6.1-1.1.1
- Adjusted to build for subrelease 90
* Fri Feb 13 2026 Shivani Agarwal <shivani.agarwal@broadcom.com> 0.6.1-1.1
- Bump after moving to SPECS/91
* Tue May 06 2025 Shivani Agarwal <shivani.agarwal@broadcom.com> 0.6.1-1
- Initial version.
